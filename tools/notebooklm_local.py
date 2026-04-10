#!/usr/bin/env python3
"""NotebookLM 本地脚本 — 从文章生成 infographic / slides / podcast / video.

Mac 本地使用，通过 notebooklm-py 库连接 Google NotebookLM。

Setup:
    pip install notebooklm-py
    notebooklm login          # 浏览器 Google 登录（一次性）

Usage:
    # 生成所有类型（slides + audio + video）
    python tools/notebooklm_local.py --input workspace/道德经/generated/category_01_generative_ground.md

    # 只生成 slides
    python tools/notebooklm_local.py --input workspace/道德经/generated/category_01_generative_ground.md --type slides

    # 批量处理某个作品的所有已生成文章
    python tools/notebooklm_local.py --batch workspace/道德经/generated/

    # 列出已有 notebooks
    python tools/notebooklm_local.py --list
"""

import argparse
import site
import sys
import time
from pathlib import Path

try:
    from notebooklm import NotebookLM
except ImportError:
    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    candidates = [
        Path(sys.executable).resolve().parent.parent / "lib" / version / "site-packages",
        Path(__file__).resolve().parent.parent / ".venv" / "lib" / version / "site-packages",
    ]
    for candidate in candidates:
        if candidate.exists():
            site.addsitedir(str(candidate))
    try:
        from notebooklm import NotebookLM
    except ImportError:
        print("notebooklm-py 未安装。运行: pip install notebooklm-py")
        print("然后运行: notebooklm login (浏览器 Google 登录)")
        sys.exit(1)


ARTIFACTS_DIR = Path(__file__).parent.parent / "workspace" / "artifacts"


def ensure_artifacts_dir(slug: str) -> Path:
    d = ARTIFACTS_DIR / slug
    d.mkdir(parents=True, exist_ok=True)
    return d


def slug_from_path(path: Path) -> str:
    return path.stem.replace(" ", "_")


def create_notebook(client: NotebookLM, input_path: Path, title: str = None) -> str:
    """Create a NotebookLM notebook from a markdown/text file."""
    content = input_path.read_text(encoding="utf-8")
    title = title or f"Omega: {input_path.stem}"

    print(f"  Creating notebook: {title}")
    nb = client.create_notebook(title=title)
    nb_id = nb.id

    # Upload source
    print(f"  Uploading source: {input_path.name} ({len(content)} chars)")
    nb.add_source(text=content, title=input_path.name)

    return nb_id


def generate_slides(client: NotebookLM, nb_id: str, output_dir: Path, slug: str) -> Path:
    """Generate slide deck from notebook."""
    print(f"  Generating slides...")
    nb = client.get_notebook(nb_id)
    slides = nb.create_slides()

    output = output_dir / f"{slug}_slides.pdf"
    slides.download(str(output))
    print(f"  ✓ Slides saved: {output}")
    return output


def generate_audio(client: NotebookLM, nb_id: str, output_dir: Path, slug: str) -> Path:
    """Generate audio overview (podcast) from notebook."""
    print(f"  Generating audio overview (this takes 1-3 minutes)...")
    nb = client.get_notebook(nb_id)
    audio = nb.create_audio_overview()

    # Wait for generation
    while not audio.is_ready():
        time.sleep(10)
        print(f"    waiting... ({audio.status})")
        audio.refresh()

    output = output_dir / f"{slug}_podcast.wav"
    audio.download(str(output))
    print(f"  ✓ Audio saved: {output}")
    return output


def generate_video(client: NotebookLM, nb_id: str, output_dir: Path, slug: str) -> Path:
    """Generate explainer video from notebook."""
    print(f"  Generating video (this takes 2-5 minutes)...")
    nb = client.get_notebook(nb_id)

    try:
        video = nb.create_video()
        while not video.is_ready():
            time.sleep(15)
            print(f"    waiting... ({video.status})")
            video.refresh()

        output = output_dir / f"{slug}_video.mp4"
        video.download(str(output))
        print(f"  ✓ Video saved: {output}")
        return output
    except Exception as e:
        print(f"  ✗ Video generation failed: {e}")
        print(f"    (Video may not be available for all notebook types)")
        return None


def process_file(input_path: Path, gen_type: str = "all"):
    """Process a single file through NotebookLM."""
    slug = slug_from_path(input_path)
    output_dir = ensure_artifacts_dir(slug)

    print(f"\n{'='*60}")
    print(f"Processing: {input_path.name}")
    print(f"Output dir: {output_dir}")
    print(f"Type: {gen_type}")
    print(f"{'='*60}")

    client = NotebookLM()
    nb_id = create_notebook(client, input_path)

    results = {}

    if gen_type in ("slides", "all"):
        results["slides"] = str(generate_slides(client, nb_id, output_dir, slug))

    if gen_type in ("audio", "all"):
        results["audio"] = str(generate_audio(client, nb_id, output_dir, slug))

    if gen_type in ("video", "all"):
        video = generate_video(client, nb_id, output_dir, slug)
        if video:
            results["video"] = str(video)

    # Save manifest
    import json
    manifest = {
        "source": str(input_path),
        "notebook_id": nb_id,
        "artifacts": results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"\n✓ Done. Artifacts at: {output_dir}")
    return results


def main():
    parser = argparse.ArgumentParser(description="NotebookLM 本地生成工具")
    parser.add_argument("--input", help="输入文件路径 (.md / .txt)")
    parser.add_argument("--batch", help="批量处理目录下所有 .md 文件")
    parser.add_argument("--type", choices=["slides", "audio", "video", "all"], default="all",
                        help="生成类型 (default: all)")
    parser.add_argument("--list", action="store_true", help="列出已有 notebooks")
    args = parser.parse_args()

    if args.list:
        client = NotebookLM()
        notebooks = client.list_notebooks()
        print("Notebooks:")
        for nb in notebooks:
            print(f"  [{nb.id[:8]}] {nb.title}")
        return

    if args.input:
        path = Path(args.input)
        if not path.exists():
            print(f"文件不存在: {path}")
            sys.exit(1)
        process_file(path, args.type)

    elif args.batch:
        batch_dir = Path(args.batch)
        if not batch_dir.is_dir():
            print(f"目录不存在: {batch_dir}")
            sys.exit(1)
        files = sorted(batch_dir.glob("*.md"))
        if not files:
            print(f"目录中没有 .md 文件: {batch_dir}")
            return
        print(f"批量处理: {len(files)} 个文件")
        for f in files:
            try:
                process_file(f, args.type)
            except Exception as e:
                print(f"  ✗ 失败: {f.name} — {e}")
                continue

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
