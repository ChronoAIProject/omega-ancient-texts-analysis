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
CLIENT_HTTP_TIMEOUT = 10.0
SLIDES_TIMEOUT = 900
INFOGRAPHIC_TIMEOUT = 900
AUDIO_TIMEOUT = 900
VIDEO_TIMEOUT = 1200
ARTIFACT_CREATE_TIMEOUT = 60
ARTIFACT_DOWNLOAD_TIMEOUT = 180
POLL_RPC_TIMEOUT = 30
POLL_RPC_RETRIES = 3
POLL_ERROR_SLEEP = 5


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


def normalize_slug(stem: str) -> str:
    return stem[:-7] if stem.endswith("_source") else stem


def load_source_content(filepath: Path, language_profile: str) -> str:
    content = filepath.read_text(encoding="utf-8")
    brief = build_generation_brief(language_profile, filepath)
    return f"{brief}\n\n---\n\n{content}"


async def create_notebook_from_file(client, filepath: Path, language_profile: str) -> str:
    """Create a notebook and add the file as a source."""
    title = f"Omega: {normalize_slug(filepath.stem)}"
    content = load_source_content(filepath, language_profile)

    nb = await client.notebooks.create(title=title)
    nb_id = nb.id
    print(f"  Created notebook: {title} [{nb_id[:8]}]")

    await client.sources.add_text(nb_id, title=filepath.name, content=content, wait=True)
    print(f"  Added source: {filepath.name} ({len(content)} chars)")

    # Wait for source processing
    await asyncio.sleep(5)
    return nb_id


async def wait_for_completion_resilient(
    client,
    notebook_id: str,
    task_id: str,
    timeout: float,
    artifact_name: str,
):
    """Poll artifact status with a hard timeout around each RPC call."""
    loop = asyncio.get_running_loop()
    start_time = loop.time()
    current_interval = 2.0
    consecutive_poll_errors = 0
    last_status = None

    while True:
        elapsed = loop.time() - start_time
        remaining = timeout - elapsed
        if remaining <= 0:
            raise TimeoutError(f"{artifact_name} task {task_id} timed out after {timeout}s")

        try:
            status = await asyncio.wait_for(
                client.artifacts.poll_status(notebook_id, task_id),
                timeout=min(POLL_RPC_TIMEOUT, max(1.0, remaining)),
            )
            consecutive_poll_errors = 0
        except Exception as e:
            consecutive_poll_errors += 1
            print(
                f"    poll error {consecutive_poll_errors}/{POLL_RPC_RETRIES}: "
                f"{type(e).__name__}: {e}"
            )
            if consecutive_poll_errors >= POLL_RPC_RETRIES:
                raise TimeoutError(
                    f"{artifact_name} polling failed repeatedly for task {task_id}: {e}"
                ) from e
            await asyncio.sleep(min(POLL_ERROR_SLEEP * consecutive_poll_errors, remaining))
            continue

        if status.is_complete:
            print(f"    status: {status.status}")
            return status
        if status.is_failed:
            detail = status.error or status.error_code or status.status
            raise RuntimeError(f"{artifact_name} task {task_id} failed: {detail}")

        if status.status != last_status:
            print(f"    status: {status.status}")
            last_status = status.status

        sleep_duration = min(current_interval, remaining)
        await asyncio.sleep(sleep_duration)
        current_interval = min(current_interval * 2, 10.0)


async def generate_slides(client, nb_id: str, output_dir: Path, slug: str, slide_language: str):
    """Generate slide deck."""
    print(f"  Generating slides...")
    status = await asyncio.wait_for(
        client.artifacts.generate_slide_deck(nb_id, language=slide_language),
        timeout=ARTIFACT_CREATE_TIMEOUT,
    )
    await wait_for_completion_resilient(client, nb_id, status.task_id, SLIDES_TIMEOUT, "slides")
    output = output_dir / f"{slug}_slides.pdf"
    await asyncio.wait_for(
        client.artifacts.download_slide_deck(nb_id, str(output)),
        timeout=ARTIFACT_DOWNLOAD_TIMEOUT,
    )
    print(f"  ✓ Slides: {output}")
    return output


async def generate_infographic(client, nb_id: str, output_dir: Path, slug: str, slide_language: str):
    """Generate infographic."""
    print(f"  Generating infographic...")
    status = await asyncio.wait_for(
        client.artifacts.generate_infographic(nb_id, language=slide_language),
        timeout=ARTIFACT_CREATE_TIMEOUT,
    )
    await wait_for_completion_resilient(
        client, nb_id, status.task_id, INFOGRAPHIC_TIMEOUT, "infographic"
    )
    output = output_dir / f"{slug}_infographic.png"
    await asyncio.wait_for(
        client.artifacts.download_infographic(nb_id, str(output)),
        timeout=ARTIFACT_DOWNLOAD_TIMEOUT,
    )
    print(f"  ✓ Infographic: {output}")
    return output


async def generate_audio(client, nb_id: str, output_dir: Path, slug: str):
    """Generate audio overview."""
    print(f"  Generating audio (1-3 min)...")
    status = await asyncio.wait_for(
        client.artifacts.generate_audio(nb_id),
        timeout=ARTIFACT_CREATE_TIMEOUT,
    )
    await wait_for_completion_resilient(client, nb_id, status.task_id, AUDIO_TIMEOUT, "audio")
    output = output_dir / f"{slug}_audio.wav"
    await asyncio.wait_for(
        client.artifacts.download_audio(nb_id, str(output)),
        timeout=ARTIFACT_DOWNLOAD_TIMEOUT,
    )
    print(f"  ✓ Audio: {output}")
    return output


async def generate_video(client, nb_id: str, output_dir: Path, slug: str):
    """Generate video."""
    print(f"  Generating video (2-5 min)...")
    try:
        status = await asyncio.wait_for(
            client.artifacts.generate_video(nb_id),
            timeout=ARTIFACT_CREATE_TIMEOUT,
        )
        await wait_for_completion_resilient(client, nb_id, status.task_id, VIDEO_TIMEOUT, "video")
        output = output_dir / f"{slug}_video.mp4"
        await asyncio.wait_for(
            client.artifacts.download_video(nb_id, str(output)),
            timeout=ARTIFACT_DOWNLOAD_TIMEOUT,
        )
        print(f"  ✓ Video: {output}")
        return output
    except Exception as e:
        print(f"  ✗ Video failed: {e}")
        return None


def resolve_types(gen_type: str, gen_types: list[str] | None) -> list[str]:
    if gen_types:
        return gen_types
    if gen_type == "all":
        return ["slides", "infographic", "audio", "video"]
    return [gen_type]


def collect_existing_artifacts(output_dir: Path, slug: str) -> dict[str, str]:
    mapping = {
        "slides": output_dir / f"{slug}_slides.pdf",
        "infographic": output_dir / f"{slug}_infographic.png",
        "audio": output_dir / f"{slug}_audio.wav",
        "video": output_dir / f"{slug}_video.mp4",
    }
    return {name: str(path) for name, path in mapping.items() if path.exists()}


def load_manifest(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        return {}
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


async def resolve_notebook_id(
    client,
    filepath: Path,
    output_dir: Path,
    language_profile: str,
    force_new_notebook: bool,
) -> str:
    manifest_path = output_dir / "manifest.json"
    manifest = load_manifest(manifest_path)

    if not force_new_notebook:
        existing_id = manifest.get("notebook_id")
        same_source = manifest.get("source") == str(filepath)
        same_profile = manifest.get("language_profile") == language_profile
        if existing_id and same_source and same_profile:
            try:
                await asyncio.wait_for(
                    client.notebooks.get(existing_id),
                    timeout=min(POLL_RPC_TIMEOUT, ARTIFACT_CREATE_TIMEOUT),
                )
                print(f"  Reusing notebook: [{existing_id[:8]}]")
                return existing_id
            except Exception as e:
                print(f"  Existing notebook unusable, creating a new one... ({e})")

    return await create_notebook_from_file(client, filepath, language_profile)


async def process_file(
    client,
    filepath: Path,
    gen_type: str = "all",
    language_profile: str = DEFAULT_LANGUAGE_PROFILE,
    gen_types: list[str] | None = None,
    force_new_notebook: bool = False,
):
    """Process a single file through NotebookLM."""
    slug = normalize_slug(filepath.stem)
    # After restructure_artifacts.py, artifact dirs live under per-book
    # subdirectories (e.g. artifacts/易经/hexagram-01-qian/).
    # Search for existing dir first; fall back to flat ARTIFACTS_DIR.
    existing = list(ARTIFACTS_DIR.rglob(slug))
    existing_dirs = [p for p in existing if p.is_dir()]
    if existing_dirs:
        output_dir = existing_dirs[0]
    else:
        output_dir = ARTIFACTS_DIR / slug
    output_dir.mkdir(parents=True, exist_ok=True)
    slide_language = "en" if language_profile == "en" else "zh"
    types_to_run = resolve_types(gen_type, gen_types)

    print(f"\n{'='*60}")
    print(f"Processing: {filepath.name}")
    print(f"Language profile: {language_profile}")
    print(f"Types: {', '.join(types_to_run)}")
    print(f"{'='*60}")

    nb_id = await resolve_notebook_id(
        client, filepath, output_dir, language_profile, force_new_notebook
    )
    results = {"source": str(filepath), "notebook_id": nb_id, "language_profile": language_profile}

    generators = {
        "slides": lambda c, n, o, s: generate_slides(c, n, o, s, slide_language),
        "infographic": lambda c, n, o, s: generate_infographic(c, n, o, s, slide_language),
        "audio": generate_audio,
        "video": generate_video,
    }

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

    manifest_path = output_dir / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            manifest = {}
    manifest.update(
        {
            "source": str(filepath),
            "notebook_id": nb_id,
            "language_profile": language_profile,
            **collect_existing_artifacts(output_dir, slug),
            **results,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"  Done → {output_dir}")
    return results


async def list_notebooks(client):
    """List existing notebooks."""
    nbs = await client.notebooks.list()
    print(f"{len(nbs)} notebooks:")
    for nb in nbs:
        print(f"  [{nb.id[:8]}] {nb.title}")


async def main_async(args):
    async with await NotebookLMClient.from_storage(timeout=CLIENT_HTTP_TIMEOUT) as client:
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
            await process_file(
                client,
                path,
                args.type,
                args.language_profile,
                args.types,
                args.force_new_notebook,
            )

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
                    await process_file(
                        client,
                        f,
                        args.type,
                        args.language_profile,
                        args.types,
                        args.force_new_notebook,
                    )
                except Exception as e:
                    print(f"  ✗ 失败: {f.name} — {e}")
                    continue


def main():
    parser = argparse.ArgumentParser(description="NotebookLM 批量生成")
    parser.add_argument("--input", help="单个文件")
    parser.add_argument("--batch", help="批量处理目录")
    parser.add_argument("--type", choices=["slides", "infographic", "audio", "video", "all"], default="all")
    parser.add_argument(
        "--types",
        nargs="+",
        choices=["slides", "infographic", "audio", "video"],
        help="显式指定多个生成类型，例如: --types slides infographic",
    )
    parser.add_argument(
        "--language-profile",
        choices=["zh_primary_bilingual", "zh", "en"],
        default=DEFAULT_LANGUAGE_PROFILE,
        help="媒体语言策略 (default: zh_primary_bilingual)",
    )
    parser.add_argument(
        "--force-new-notebook",
        action="store_true",
        help="忽略已有 manifest 中的 notebook_id，强制重新创建 notebook",
    )
    parser.add_argument("--list", action="store_true", help="列出 notebooks")
    args = parser.parse_args()

    if not any([args.input, args.batch, args.list]):
        parser.print_help()
        return

    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
