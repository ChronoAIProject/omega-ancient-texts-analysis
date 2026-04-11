#!/usr/bin/env python3
"""Build infographic/video fallback assets from existing slide PDFs.

This is used when NotebookLM artifact generation is unstable but slide decks
already exist. It converts bilingual slide PDFs into:
  - a compact infographic PNG (contact sheet)
  - a slideshow MP4 built from the slide pages
"""

from __future__ import annotations

import argparse
import json
import math
import site
import sys
import time
from pathlib import Path

try:
    import fitz
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image, ImageColor
except ModuleNotFoundError:
    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    candidate = Path(__file__).resolve().parent.parent / ".venv" / "lib" / version / "site-packages"
    if candidate.exists():
        site.addsitedir(str(candidate))
    import fitz
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image, ImageColor


ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = ROOT / "workspace" / "artifacts"
DEFAULT_BG = ImageColor.getrgb("#f4f1ea")
DEFAULT_CARD = ImageColor.getrgb("#ffffff")
DEFAULT_GUTTER = 28


def load_manifest(artifact_dir: Path) -> dict:
    path = artifact_dir / "manifest.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_manifest(artifact_dir: Path, manifest: dict) -> None:
    path = artifact_dir / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def render_page(doc: fitz.Document, page_index: int, max_width: int) -> Image.Image:
    page = doc.load_page(page_index)
    pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    if image.width > max_width:
        scale = max_width / image.width
        image = image.resize((max_width, int(image.height * scale)), Image.Resampling.LANCZOS)
    return image


def select_infographic_pages(page_count: int) -> list[int]:
    if page_count <= 4:
        return list(range(page_count))
    positions = [0, 1, page_count // 2, page_count - 1]
    seen = []
    for pos in positions:
        pos = max(0, min(page_count - 1, pos))
        if pos not in seen:
            seen.append(pos)
    while len(seen) < min(4, page_count):
        for i in range(page_count):
            if i not in seen:
                seen.append(i)
            if len(seen) == min(4, page_count):
                break
    return seen[:4]


def build_infographic(slides_pdf: Path, output_path: Path, max_cell_width: int = 900) -> Path:
    doc = fitz.open(slides_pdf)
    selected = select_infographic_pages(doc.page_count)
    images = [render_page(doc, idx, max_cell_width) for idx in selected]
    doc.close()

    cols = 2 if len(images) > 1 else 1
    rows = math.ceil(len(images) / cols)
    col_width = max(img.width for img in images)
    row_heights = []
    for row in range(rows):
        start = row * cols
        row_heights.append(max(img.height for img in images[start : start + cols]))

    width = col_width * cols + DEFAULT_GUTTER * (cols + 1)
    height = sum(row_heights) + DEFAULT_GUTTER * (rows + 1)
    canvas = Image.new("RGB", (width, height), DEFAULT_BG)

    for idx, img in enumerate(images):
        row = idx // cols
        col = idx % cols
        x = DEFAULT_GUTTER + col * (col_width + DEFAULT_GUTTER)
        y = DEFAULT_GUTTER + sum(row_heights[:row]) + row * DEFAULT_GUTTER
        card = Image.new("RGB", (col_width, row_heights[row]), DEFAULT_CARD)
        card.paste(img, ((col_width - img.width) // 2, (row_heights[row] - img.height) // 2))
        canvas.paste(card, (x, y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG", optimize=True)
    return output_path


def resize_for_video(image: Image.Image, target_width: int = 1280, target_height: int = 720) -> Image.Image:
    background = Image.new("RGB", (target_width, target_height), DEFAULT_BG)
    image = image.copy()
    image.thumbnail((target_width - 80, target_height - 80), Image.Resampling.LANCZOS)
    x = (target_width - image.width) // 2
    y = (target_height - image.height) // 2
    background.paste(image, (x, y))
    return background


def build_video(
    slides_pdf: Path,
    output_path: Path,
    target_width: int = 1280,
    target_height: int = 720,
    fps: int = 12,
    seconds_per_slide: float = 3.0,
) -> Path:
    doc = fitz.open(slides_pdf)
    frames_per_slide = max(1, int(fps * seconds_per_slide))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = imageio.get_writer(output_path, fps=fps, codec="libx264", quality=8, macro_block_size=None)
    try:
        for page_index in range(doc.page_count):
            frame = resize_for_video(
                render_page(doc, page_index, max_width=target_width),
                target_width=target_width,
                target_height=target_height,
            )
            arr = np.asarray(frame)
            for _ in range(frames_per_slide):
                writer.append_data(arr)
    finally:
        writer.close()
        doc.close()
    return output_path


def process_artifact_dir(artifact_dir: Path, build_infographic_flag: bool, build_video_flag: bool) -> dict[str, str]:
    manifest = load_manifest(artifact_dir)
    slides_path = manifest.get("slides")
    if not slides_path:
        raise FileNotFoundError(f"No slides entry found in {artifact_dir / 'manifest.json'}")

    slides_pdf = Path(slides_path)
    if not slides_pdf.exists():
        raise FileNotFoundError(f"Slides PDF not found: {slides_pdf}")

    slug = artifact_dir.name
    results: dict[str, str] = {}
    if build_infographic_flag:
        infographic_path = artifact_dir / f"{slug}_infographic.png"
        build_infographic(slides_pdf, infographic_path)
        results["infographic"] = str(infographic_path)

    if build_video_flag:
        video_path = artifact_dir / f"{slug}_video.mp4"
        build_video(slides_pdf, video_path)
        results["video"] = str(video_path)

    manifest.update(results)
    manifest["media_builder"] = "fallback_from_slides"
    manifest["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    save_manifest(artifact_dir, manifest)
    return results


def resolve_dirs(args) -> list[Path]:
    def is_supported_dir(path: Path) -> bool:
        if not path.is_dir() or path.name.endswith("_source"):
            return False
        manifest = load_manifest(path)
        return bool(manifest.get("slides"))

    if args.slug:
        target = ARTIFACTS_DIR / args.slug
        return [target]
    if args.track:
        return sorted(
            p for p in ARTIFACTS_DIR.iterdir() if p.name.startswith(args.track) and is_supported_dir(p)
        )
    raise ValueError("Provide --slug or --track")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build fallback infographic/video from slide PDFs")
    parser.add_argument("--slug", help="Artifact slug directory name, e.g. synthesis_01_no11_golden_mean_shift")
    parser.add_argument("--track", help="Artifact slug prefix, e.g. synthesis_")
    parser.add_argument("--infographic", action="store_true", help="Build infographic PNG")
    parser.add_argument("--video", action="store_true", help="Build MP4 slideshow")
    args = parser.parse_args()

    if not args.infographic and not args.video:
        parser.error("Specify at least one of --infographic or --video")

    for artifact_dir in resolve_dirs(args):
        print(f"Processing {artifact_dir.name}")
        results = process_artifact_dir(artifact_dir, args.infographic, args.video)
        for key, value in results.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
