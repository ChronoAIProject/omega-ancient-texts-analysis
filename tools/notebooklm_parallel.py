#!/usr/bin/env python3
"""Parallel NotebookLM generation — fire all, recover later.

Instead of waiting for each video to complete (serial, 2hr/item),
this script:
  1. Creates notebooks + triggers ALL artifact types for N items in parallel
  2. Does NOT wait for video completion — just fires the task
  3. A separate recovery pass downloads whatever completed

Usage:
    # Trigger generation for all missing hexagrams (parallel, async)
    python tools/notebooklm_parallel.py --book 易经 --type chapter

    # Trigger for all missing content
    python tools/notebooklm_parallel.py

    # Recovery pass — download all server-completed videos
    python tools/notebooklm_parallel.py --recover

    # Limit concurrency (default 5)
    python tools/notebooklm_parallel.py --parallel 3
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

try:
    from notebooklm import NotebookLMClient
except ModuleNotFoundError:
    venv = Path.home() / "venvs" / "notebooklm" / "lib"
    for sp in venv.rglob("site-packages"):
        sys.path.insert(0, str(sp))
    from notebooklm import NotebookLMClient

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = REPO_ROOT / "workspace"
ARTIFACTS = WORKSPACE / "artifacts"
REGISTRY = WORKSPACE / "publish_registry.json"

# Timeouts for individual operations (not polling — just task creation)
CREATE_TIMEOUT = 120
SLIDES_POLL_TIMEOUT = 600
AUDIO_POLL_TIMEOUT = 600
# Video: fire and forget — don't poll, recover later
VIDEO_FIRE_TIMEOUT = 120  # just the create call, not completion


def load_registry():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def find_source_md(entry):
    """Find source markdown for an entry."""
    article = entry.get("article")
    if article:
        p = WORKSPACE / article
        if p.is_file():
            return p
    # Search by ID
    item_id = entry["id"]
    for pattern in [f"*{item_id}*.md", f"*{item_id.replace('-', '_')}*.md"]:
        for src in WORKSPACE.rglob(pattern):
            if "generated" in str(src) or "hexagrams" in str(src) or "chapters" in str(src):
                return src
    return None


def find_artifact_dir(item_id):
    for d in ARTIFACTS.rglob(item_id):
        if d.is_dir():
            return d
    return None


def build_brief(language, filepath):
    if language == "en":
        return f"# Media Generation Brief\n\nSource: {filepath.name}\n\n- Primary: English\n"
    return (
        f"# 媒体生成说明\n\n源文件: {filepath.name}\n\n"
        f"- 主语言: 中文\n- 辅助: English (theorem names only)\n"
        f"- 原文引文保留中文\n"
    )


async def trigger_one(client, entry, semaphore, results):
    """Create notebook + trigger slides+audio+video for one item. Non-blocking."""
    item_id = entry["id"]
    language = entry.get("language", "zh")

    async with semaphore:
        source = find_source_md(entry)
        if not source:
            results.append({"id": item_id, "status": "skip", "reason": "no source md"})
            return

        artifact_dir = find_artifact_dir(item_id)
        if not artifact_dir:
            results.append({"id": item_id, "status": "skip", "reason": "no artifact dir"})
            return

        # Skip if already has video
        video = artifact_dir / f"{item_id}_video.mp4"
        if video.is_file() and video.stat().st_size > 10_000_000:
            results.append({"id": item_id, "status": "skip", "reason": "video exists"})
            return

        try:
            # Load or create notebook
            manifest_path = artifact_dir / "manifest.json"
            manifest = {}
            if manifest_path.exists():
                try:
                    manifest = json.loads(manifest_path.read_text())
                except json.JSONDecodeError:
                    pass

            nb_id = manifest.get("notebook_id")
            reused = False

            if nb_id:
                try:
                    await asyncio.wait_for(client.notebooks.get(nb_id), timeout=30)
                    reused = True
                except Exception:
                    nb_id = None

            if not nb_id:
                content = source.read_text(encoding="utf-8")
                brief = build_brief(language, source)
                full_content = f"{brief}\n\n---\n\n{content}"
                title = f"Omega: {item_id}"
                nb = await asyncio.wait_for(
                    client.notebooks.create(title=title), timeout=CREATE_TIMEOUT
                )
                nb_id = nb.id
                await client.sources.add_text(
                    nb_id, title=source.name, content=full_content, wait=True
                )
                await asyncio.sleep(3)

            slide_lang = "en" if language == "en" else "zh"
            tasks_fired = []

            # Trigger slides (if missing)
            slides_path = artifact_dir / f"{item_id}_slides.pdf"
            if not slides_path.is_file():
                try:
                    s = await asyncio.wait_for(
                        client.artifacts.generate_slide_deck(nb_id, language=slide_lang),
                        timeout=CREATE_TIMEOUT,
                    )
                    tasks_fired.append(f"slides:{s.task_id[:8]}")
                except Exception as e:
                    tasks_fired.append(f"slides:err:{e}")

            # Trigger audio (if missing)
            audio_path = artifact_dir / f"{item_id}_audio.wav"
            if not audio_path.is_file():
                try:
                    s = await asyncio.wait_for(
                        client.artifacts.generate_audio(nb_id),
                        timeout=CREATE_TIMEOUT,
                    )
                    tasks_fired.append(f"audio:{s.task_id[:8]}")
                except Exception as e:
                    tasks_fired.append(f"audio:err:{e}")

            # Trigger video — FIRE AND FORGET
            try:
                s = await asyncio.wait_for(
                    client.artifacts.generate_video(nb_id, language=slide_lang),
                    timeout=VIDEO_FIRE_TIMEOUT,
                )
                tasks_fired.append(f"video:{s.task_id[:8]}")
            except Exception as e:
                tasks_fired.append(f"video:err:{e}")

            # Update manifest
            manifest["notebook_id"] = nb_id
            manifest["source"] = str(source)
            manifest["language_profile"] = "zh_primary_bilingual" if language == "zh" else "en"
            manifest["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            status = "triggered" if any("err" not in t for t in tasks_fired) else "error"
            nb_label = f"reused:{nb_id[:8]}" if reused else f"new:{nb_id[:8]}"
            print(f"  ✓ {item_id} [{nb_label}] → {', '.join(tasks_fired)}")
            results.append({"id": item_id, "status": status, "tasks": tasks_fired})

        except Exception as e:
            print(f"  ✗ {item_id}: {type(e).__name__}: {str(e)[:60]}")
            results.append({"id": item_id, "status": "error", "error": str(e)[:100]})


async def recover_videos(client):
    """Download all server-completed videos that we don't have locally."""
    recovered = 0
    checked = 0
    for mf in sorted(ARTIFACTS.rglob("manifest.json")):
        try:
            manifest = json.loads(mf.read_text())
        except:
            continue
        nb_id = manifest.get("notebook_id")
        if not nb_id:
            continue
        name = mf.parent.name
        if "_source" in name:
            continue

        video_path = mf.parent / f"{name}_video.mp4"
        if video_path.is_file() and video_path.stat().st_size > 10_000_000:
            continue

        checked += 1
        try:
            raw = await client.artifacts._list_raw(nb_id)
            videos = [a for a in raw if isinstance(a, list) and len(a) > 4
                      and a[2] == 3 and a[4] == 3]  # VIDEO + COMPLETED
            if videos:
                await client.artifacts.download_video(nb_id, str(video_path))
                size_mb = video_path.stat().st_size / (1024 * 1024)
                print(f"  ✓ {name}: {size_mb:.1f}MB")
                recovered += 1

            # Also grab slides + audio if missing
            slides_path = mf.parent / f"{name}_slides.pdf"
            if not slides_path.is_file():
                try:
                    await client.artifacts.download_slide_deck(nb_id, str(slides_path))
                    print(f"  ✓ {name}: slides recovered")
                except:
                    pass

            audio_path = mf.parent / f"{name}_audio.wav"
            if not audio_path.is_file():
                try:
                    await client.artifacts.download_audio(nb_id, str(audio_path))
                    print(f"  ✓ {name}: audio recovered")
                except:
                    pass

        except Exception:
            pass

        if checked % 20 == 0:
            print(f"  ... checked {checked}")

    print(f"\nChecked: {checked}, Recovered: {recovered} videos")
    return recovered


async def main_async(args):
    async with await NotebookLMClient.from_storage(timeout=30.0) as client:
        if not client.is_connected:
            await client.refresh_auth()
        if not client.is_connected:
            print("NotebookLM 未连接。请运行: notebooklm login")
            sys.exit(1)
        print("NotebookLM connected ✓\n")

        if args.recover:
            await recover_videos(client)
            return

        registry = load_registry()
        items = [e for e in registry if not e.get("ready")]

        if args.book:
            items = [e for e in items if e.get("book") == args.book]
        if args.type:
            items = [e for e in items if e.get("type") == args.type]
        if args.max > 0:
            items = items[:args.max]

        print(f"Triggering {len(items)} items (parallel={args.parallel})\n")

        semaphore = asyncio.Semaphore(args.parallel)
        results = []
        tasks = [trigger_one(client, entry, semaphore, results) for entry in items]
        await asyncio.gather(*tasks)

        triggered = sum(1 for r in results if r["status"] == "triggered")
        skipped = sum(1 for r in results if r["status"] == "skip")
        errors = sum(1 for r in results if r["status"] == "error")
        print(f"\nDone: {triggered} triggered, {skipped} skipped, {errors} errors")
        print(f"\nRun with --recover in 30-60 min to download completed videos.")


def main():
    parser = argparse.ArgumentParser(description="Parallel NotebookLM generation")
    parser.add_argument("--book", help="Filter by book (e.g. 易经)")
    parser.add_argument("--type", help="Filter by type (chapter/category/synthesis/master)")
    parser.add_argument("--parallel", type=int, default=5, help="Max concurrent triggers")
    parser.add_argument("--max", type=int, default=0, help="Max items (0=all)")
    parser.add_argument("--recover", action="store_true", help="Recovery mode: download completed videos")
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
