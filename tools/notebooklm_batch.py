#!/usr/bin/env python3
"""NotebookLM 批量生成 — slides, infographic, audio, video.

Usage:
    python tools/notebooklm_batch.py --batch workspace/道德经/generated/ --type slides
    python tools/notebooklm_batch.py --batch workspace/道德经/generated/ --type infographic
    python tools/notebooklm_batch.py --batch workspace/道德经/generated/ --type all
    python tools/notebooklm_batch.py --list
"""

import argparse
import asyncio
import json
import site
import sys
import time
from pathlib import Path

try:
    from notebooklm import NotebookLMClient
except ModuleNotFoundError:
    version = f"python{sys.version_info.major}.{sys.version_info.minor}"
    candidates = [
        Path(sys.executable).resolve().parent.parent / "lib" / version / "site-packages",
        Path(__file__).resolve().parent.parent / ".venv" / "lib" / version / "site-packages",
    ]
    for candidate in candidates:
        if candidate.exists():
            site.addsitedir(str(candidate))
    from notebooklm import NotebookLMClient

ARTIFACTS_DIR = Path(__file__).parent.parent / "workspace" / "artifacts"
MAX_RETRIES = 3
RETRY_DELAY = 10
DEFAULT_LANGUAGE_PROFILE = "zh_primary_bilingual"


def build_generation_brief(language_profile: str, filepath: Path) -> str:
    if language_profile == "en":
        return (
            f"# Media Generation Brief\n\n"
            f"Source file: {filepath.name}\n\n"
            f"- Primary language: English\n"
            f"- Keep theorem names and technical vocabulary exact.\n"
        )
    if language_profile == "zh":
        return (
            f"# 媒体生成说明\n\n"
            f"源文件: {filepath.name}\n\n"
            f"- 主语言: 中文\n"
            f"- 原文引文优先保留中文\n"
            f"- 定理名可保留英文\n"
        )
    return (
        f"# 媒体生成说明 / Media Generation Brief\n\n"
        f"源文件 / Source: {filepath.name}\n\n"
        f"- 主语言 / Primary language: 中文\n"
        f"- 辅助语言 / Secondary language: English\n"
        f"- 中文负责叙事、古籍原文、社交媒体传播适配\n"
        f"- English only for theorem names, key terms, and short rigor summaries\n"
        f"- Do not turn the main narration into English\n"
        f"- Keep classical quotations in Chinese whenever possible\n"
    )


def load_source_content(filepath: Path, language_profile: str) -> str:
    content = filepath.read_text(encoding="utf-8")
    brief = build_generation_brief(language_profile, filepath)
    return f"{brief}\n\n---\n\n{content}"


async def create_notebook_from_file(client, filepath: Path, language_profile: str) -> str:
    """Create a notebook and add the file as a source."""
    title = f"Omega: {filepath.stem}"
    content = load_source_content(filepath, language_profile)

    nb = await client.notebooks.create(title=title)
    nb_id = nb.id
    print(f"  Created notebook: {title} [{nb_id[:8]}]")

    await client.sources.add_text(nb_id, title=filepath.name, content=content, wait=True)
    print(f"  Added source: {filepath.name} ({len(content)} chars)")

    # Wait for source processing
    await asyncio.sleep(5)
    return nb_id


async def generate_slides(client, nb_id: str, output_dir: Path, slug: str, slide_language: str):
    """Generate slide deck."""
    print(f"  Generating slides...")
    status = await client.artifacts.generate_slide_deck(nb_id, language=slide_language)
    await client.artifacts.wait_for_completion(nb_id, status.task_id, timeout=300)
    output = output_dir / f"{slug}_slides.pdf"
    await client.artifacts.download_slide_deck(nb_id, str(output))
    print(f"  ✓ Slides: {output}")
    return output


async def generate_infographic(client, nb_id: str, output_dir: Path, slug: str, slide_language: str):
    """Generate infographic."""
    print(f"  Generating infographic...")
    status = await client.artifacts.generate_infographic(nb_id, language=slide_language)
    await client.artifacts.wait_for_completion(nb_id, status.task_id, timeout=300)
    output = output_dir / f"{slug}_infographic.png"
    await client.artifacts.download_infographic(nb_id, str(output))
    print(f"  ✓ Infographic: {output}")
    return output


async def generate_audio(client, nb_id: str, output_dir: Path, slug: str):
    """Generate audio overview."""
    print(f"  Generating audio (1-3 min)...")
    status = await client.artifacts.generate_audio(nb_id)
    await client.artifacts.wait_for_completion(nb_id, status.task_id, timeout=600)
    output = output_dir / f"{slug}_audio.wav"
    await client.artifacts.download_audio(nb_id, str(output))
    print(f"  ✓ Audio: {output}")
    return output


async def generate_video(client, nb_id: str, output_dir: Path, slug: str):
    """Generate video."""
    print(f"  Generating video (2-5 min)...")
    try:
        status = await client.artifacts.generate_video(nb_id)
        await client.artifacts.wait_for_completion(nb_id, status.task_id, timeout=600)
        output = output_dir / f"{slug}_video.mp4"
        await client.artifacts.download_video(nb_id, str(output))
        print(f"  ✓ Video: {output}")
        return output
    except Exception as e:
        print(f"  ✗ Video failed: {e}")
        return None


async def process_file(client, filepath: Path, gen_type: str = "all", language_profile: str = DEFAULT_LANGUAGE_PROFILE):
    """Process a single file through NotebookLM."""
    slug = filepath.stem
    output_dir = ARTIFACTS_DIR / slug
    output_dir.mkdir(parents=True, exist_ok=True)
    slide_language = "en" if language_profile == "en" else "zh"

    print(f"\n{'='*60}")
    print(f"Processing: {filepath.name}")
    print(f"Language profile: {language_profile}")
    print(f"{'='*60}")

    nb_id = await create_notebook_from_file(client, filepath, language_profile)
    results = {"source": str(filepath), "notebook_id": nb_id, "language_profile": language_profile}

    generators = {
        "slides": lambda c, n, o, s: generate_slides(c, n, o, s, slide_language),
        "infographic": lambda c, n, o, s: generate_infographic(c, n, o, s, slide_language),
        "audio": generate_audio,
        "video": generate_video,
    }

    if gen_type == "all":
        types_to_run = ["slides", "infographic", "audio"]  # skip video by default (slow)
    else:
        types_to_run = [gen_type]

    for t in types_to_run:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                path = await generators[t](client, nb_id, output_dir, slug)
                if path:
                    results[t] = str(path)
                break
            except Exception as e:
                if attempt < MAX_RETRIES:
                    print(f"  ⟳ {t} attempt {attempt} failed, retrying in {RETRY_DELAY}s... ({e})")
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    print(f"  ✗ {t} failed after {MAX_RETRIES} attempts: {e}")
                    results[t] = f"error: {e}"

    manifest = {**results, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")}
    (output_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"  Done → {output_dir}")
    return results


async def list_notebooks(client):
    """List existing notebooks."""
    nbs = await client.notebooks.list()
    print(f"{len(nbs)} notebooks:")
    for nb in nbs:
        print(f"  [{nb.id[:8]}] {nb.title}")


async def main_async(args):
    async with await NotebookLMClient.from_storage() as client:
        if not client.is_connected:
            await client.refresh_auth()
        if not client.is_connected:
            print("NotebookLM 未连接。请运行: notebooklm login")
            sys.exit(1)

        print(f"NotebookLM connected ✓\n")

        if args.list:
            await list_notebooks(client)
            return

        if args.input:
            path = Path(args.input)
            if not path.exists():
                print(f"文件不存在: {path}")
                sys.exit(1)
            await process_file(client, path, args.type)

        elif args.batch:
            batch_dir = Path(args.batch)
            files = sorted(batch_dir.glob("*.md"))
            if not files:
                print(f"没有 .md 文件: {batch_dir}")
                return
            print(f"批量处理: {len(files)} 个文件, 类型: {args.type}\n")
            for i, f in enumerate(files):
                print(f"\n[{i+1}/{len(files)}]")
                try:
                    await process_file(client, f, args.type, args.language_profile)
                except Exception as e:
                    print(f"  ✗ 失败: {f.name} — {e}")
                    continue


def main():
    parser = argparse.ArgumentParser(description="NotebookLM 批量生成")
    parser.add_argument("--input", help="单个文件")
    parser.add_argument("--batch", help="批量处理目录")
    parser.add_argument("--type", choices=["slides", "infographic", "audio", "video", "all"], default="all")
    parser.add_argument(
        "--language-profile",
        choices=["zh_primary_bilingual", "zh", "en"],
        default=DEFAULT_LANGUAGE_PROFILE,
        help="媒体语言策略 (default: zh_primary_bilingual)",
    )
    parser.add_argument("--list", action="store_true", help="列出 notebooks")
    args = parser.parse_args()

    if not any([args.input, args.batch, args.list]):
        parser.print_help()
        return

    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
