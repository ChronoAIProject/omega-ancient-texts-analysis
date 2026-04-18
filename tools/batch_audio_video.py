#!/usr/bin/env python3
"""Batch generate videos from audio + slides when NotebookLM video is unavailable.

Workflow per item:
  1. Generate audio via NotebookLM (if not already present)
  2. Render slides PDF to images via PyMuPDF
  3. Combine images + audio → video via ffmpeg (libx264 + aac)

Usage:
    # Generate for all items missing videos
    python tools/batch_audio_video.py

    # Generate for a specific book
    python tools/batch_audio_video.py --book 易经

    # Specific item
    python tools/batch_audio_video.py --item hexagram-09-xiaoxu

    # Skip NotebookLM audio generation (use existing audio only)
    python tools/batch_audio_video.py --skip-audio
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import fitz
except ModuleNotFoundError:
    # Try project .venv
    venv_fitz = Path(__file__).parent.parent / ".venv" / "lib"
    for sp in venv_fitz.rglob("site-packages"):
        sys.path.insert(0, str(sp))
    import fitz

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = REPO_ROOT / "workspace"
ARTIFACTS = WORKSPACE / "artifacts"
REGISTRY_PATH = WORKSPACE / "publish_registry.json"

# NotebookLM venv
NOTEBOOKLM_PYTHON = Path.home() / "venvs" / "notebooklm" / "bin" / "python3"
BATCH_SCRIPT = REPO_ROOT / "tools" / "notebooklm_batch.py"


def load_registry() -> list[dict]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def find_artifact_dir(item_id: str) -> Path | None:
    """Find the artifact directory anywhere under artifacts/."""
    for candidate in ARTIFACTS.rglob(item_id):
        if candidate.is_dir():
            return candidate
    return None


def find_source_md(entry: dict) -> Path | None:
    """Find the source markdown for NotebookLM audio generation."""
    article = entry.get("article")
    if article:
        p = WORKSPACE / article
        if p.is_file():
            return p
    # Try notebooklm_sources
    item_id = entry["id"]
    for src in WORKSPACE.rglob(f"*{item_id}*source*.md"):
        return src
    for src in WORKSPACE.rglob(f"*{item_id}*.md"):
        if "generated" in str(src) or "hexagrams" in str(src) or "chapters" in str(src):
            return src
    return None


def find_slides(artifact_dir: Path, item_id: str) -> Path | None:
    candidates = [
        artifact_dir / f"{item_id}_slides.pdf",
        *artifact_dir.glob("*_slides.pdf"),
        *artifact_dir.glob("*.pdf"),
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def find_audio(artifact_dir: Path, item_id: str) -> Path | None:
    candidates = [
        artifact_dir / f"{item_id}_audio.wav",
        *artifact_dir.glob("*_audio.wav"),
        *artifact_dir.glob("*.wav"),
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def generate_audio_via_notebooklm(source_md: Path, language: str = "zh") -> bool:
    """Call notebooklm_batch.py to generate audio."""
    if not NOTEBOOKLM_PYTHON.exists():
        print(f"    SKIP audio gen: {NOTEBOOKLM_PYTHON} not found")
        return False

    lang_profile = "zh_primary_bilingual" if language == "zh" else "en"
    result = subprocess.run(
        [str(NOTEBOOKLM_PYTHON), str(BATCH_SCRIPT),
         "--input", str(source_md),
         "--type", "audio",
         "--language-profile", lang_profile],
        capture_output=True, text=True, timeout=1200,
    )
    return result.returncode == 0


def render_slides(pdf_path: Path, output_dir: Path) -> int:
    """Render PDF pages to PNG images. Returns page count."""
    doc = fitz.open(str(pdf_path))
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        pix.save(str(output_dir / f"slide_{i:04d}.png"))
    count = doc.page_count
    doc.close()
    return count


def combine_audio_video(
    slides_dir: Path,
    page_count: int,
    audio_path: Path,
    output_path: Path,
) -> bool:
    """Combine rendered slide images + audio WAV → MP4."""
    duration_result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(audio_path)],
        capture_output=True, text=True,
    )
    if duration_result.returncode != 0:
        return False

    duration = float(duration_result.stdout.strip())
    sec_per_slide = duration / max(page_count, 1)

    concat_file = slides_dir / "concat.txt"
    with open(concat_file, "w") as f:
        for i in range(page_count):
            f.write(f"file 'slide_{i:04d}.png'\n")
            f.write(f"duration {sec_per_slide:.4f}\n")
        f.write(f"file 'slide_{page_count - 1:04d}.png'\n")

    result = subprocess.run(
        ["ffmpeg", "-y",
         "-f", "concat", "-safe", "0", "-i", str(concat_file),
         "-i", str(audio_path),
         "-c:v", "libx264", "-preset", "medium", "-crf", "23",
         "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "128k",
         "-shortest", "-movflags", "+faststart",
         str(output_path)],
        capture_output=True, text=True, timeout=300,
    )
    return result.returncode == 0


def process_item(entry: dict, skip_audio: bool = False) -> str:
    """Process one registry entry. Returns status string."""
    item_id = entry["id"]
    language = entry.get("language", "zh")

    artifact_dir = find_artifact_dir(item_id)
    if artifact_dir is None:
        return "SKIP: no artifact dir"

    # Check if video already exists
    video_path = artifact_dir / f"{item_id}_video.mp4"
    if video_path.is_file() and video_path.stat().st_size > 0:
        return "SKIP: video exists"

    # Find slides
    slides = find_slides(artifact_dir, item_id)
    if slides is None:
        return "SKIP: no slides PDF"

    # Find or generate audio
    audio = find_audio(artifact_dir, item_id)

    # Also check the flat artifacts dir (NotebookLM may write there)
    if audio is None:
        flat_dir = ARTIFACTS / item_id
        if flat_dir.is_dir():
            audio = find_audio(flat_dir, item_id)

    if audio is None and not skip_audio:
        source_md = find_source_md(entry)
        if source_md is None:
            return "SKIP: no source markdown for audio generation"
        print(f"    Generating audio via NotebookLM...")
        ok = generate_audio_via_notebooklm(source_md, language)
        if not ok:
            return "FAIL: NotebookLM audio generation failed"
        # Check both locations for audio
        audio = find_audio(artifact_dir, item_id)
        if audio is None:
            flat_dir = ARTIFACTS / item_id
            if flat_dir.is_dir():
                audio = find_audio(flat_dir, item_id)
        if audio is None:
            return "FAIL: audio generated but file not found"

    if audio is None:
        return "SKIP: no audio available (use --skip-audio=false to generate)"

    # Render slides + combine
    tmpdir = Path(tempfile.mkdtemp(prefix="batch_av_"))
    try:
        page_count = render_slides(slides, tmpdir)
        if page_count == 0:
            return "FAIL: empty PDF"

        print(f"    Combining {page_count} slides + audio → video...")
        ok = combine_audio_video(tmpdir, page_count, audio, video_path)
        if not ok:
            return "FAIL: ffmpeg encoding failed"

        size_mb = video_path.stat().st_size / (1024 * 1024)
        return f"OK: {size_mb:.1f}MB, {page_count} slides"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Batch audio+slides → video")
    parser.add_argument("--book", help="Filter by book name (e.g. 易经)")
    parser.add_argument("--item", help="Process single item by ID")
    parser.add_argument("--skip-audio", action="store_true",
                        help="Skip NotebookLM audio generation, only use existing audio")
    parser.add_argument("--max", type=int, default=0,
                        help="Max items to process (0 = all)")
    args = parser.parse_args()

    registry = load_registry()

    # Filter to not-ready items
    items = [e for e in registry if not e.get("ready")]

    if args.book:
        items = [e for e in items if e.get("book") == args.book]
    if args.item:
        items = [e for e in items if e["id"] == args.item]
    if args.max > 0:
        items = items[:args.max]

    print(f"Processing {len(items)} items (skip_audio={args.skip_audio})")
    print()

    results = {"OK": 0, "SKIP": 0, "FAIL": 0}
    for i, entry in enumerate(items, 1):
        print(f"[{i}/{len(items)}] {entry['id']} ({entry.get('book', '?')})...")
        status = process_item(entry, skip_audio=args.skip_audio)
        category = status.split(":")[0]
        results[category] = results.get(category, 0) + 1
        print(f"    → {status}")
        print()

    print(f"Done: {results.get('OK', 0)} generated, "
          f"{results.get('SKIP', 0)} skipped, "
          f"{results.get('FAIL', 0)} failed")


if __name__ == "__main__":
    main()
