#!/usr/bin/env python3
"""Clean up failed artifacts and regenerate all cultural content in Chinese.

Cultural notebooks (easily identified by "Omega: category_" prefix) should
ALL generate Chinese infographic/slides/video since the source articles are
bilingual with Chinese primary.

Usage:
    python tools/regenerate_chinese.py --cleanup     # delete failed artifacts
    python tools/regenerate_chinese.py --trigger     # trigger zh generation
    python tools/regenerate_chinese.py --all         # both
"""

import argparse
import asyncio
from notebooklm import NotebookLMClient
from notebooklm.rpc.types import ArtifactStatus


def is_cultural(title: str) -> bool:
    """Cultural content notebooks (Chinese primary)."""
    return title.startswith("Omega: category_") or title.startswith("Omega: hexagram_") or "category_" in title.lower()


async def cleanup_failed(client):
    """Delete all FAILED artifacts (status=4) from cultural notebooks."""
    nbs = await client.notebooks.list()
    cultural = [nb for nb in nbs if is_cultural(nb.title)]
    print(f"Cleaning up {len(cultural)} cultural notebooks...")

    deleted = {"infographic": 0, "video": 0, "slides": 0, "audio": 0}
    for nb in cultural:
        for kind, list_fn in [
            ("infographic", client.artifacts.list_infographics),
            ("video", client.artifacts.list_video),
            ("slides", client.artifacts.list_slide_decks),
            ("audio", client.artifacts.list_audio),
        ]:
            try:
                items = await list_fn(nb.id)
                for item in items:
                    status = getattr(item, 'status', 0)
                    if status == ArtifactStatus.FAILED:  # 4
                        try:
                            await client.artifacts.delete(nb.id, item.id)
                            deleted[kind] += 1
                        except Exception as e:
                            pass
                await asyncio.sleep(0.2)
            except:
                pass

    print(f"\nDeleted FAILED artifacts: {deleted}")


async def trigger_chinese(client, only_missing=True):
    """Trigger zh generation for all cultural notebooks."""
    nbs = await client.notebooks.list()
    cultural = [nb for nb in nbs if is_cultural(nb.title)]
    print(f"Triggering Chinese generation for {len(cultural)} notebooks...")

    triggered = {"infographic": 0, "video": 0, "slides": 0}
    for nb in cultural:
        # Check what's missing
        try:
            if only_missing:
                infos = await client.artifacts.list_infographics(nb.id)
                has_complete_info = any(getattr(i, 'status', 0) == 3 for i in infos)
                if has_complete_info:
                    continue

            try:
                await client.artifacts.generate_infographic(nb.id, language="zh")
                triggered["infographic"] += 1
                await asyncio.sleep(1)
            except Exception as e:
                pass

            # Videos: only if missing
            if only_missing:
                vids = await client.artifacts.list_video(nb.id)
                has_complete_vid = any(getattr(v, 'status', 0) == 3 for v in vids)
                if not has_complete_vid:
                    try:
                        await client.artifacts.generate_video(nb.id, language="zh")
                        triggered["video"] += 1
                        await asyncio.sleep(1)
                    except:
                        pass

            # Slides: only if missing
            if only_missing:
                sld = await client.artifacts.list_slide_decks(nb.id)
                has_complete_sld = any(getattr(s, 'status', 0) == 3 for s in sld)
                if not has_complete_sld:
                    try:
                        await client.artifacts.generate_slide_deck(nb.id, language="zh")
                        triggered["slides"] += 1
                        await asyncio.sleep(1)
                    except:
                        pass

            print(f"  [done] {nb.title[:55]}")
        except Exception as e:
            print(f"  [error] {nb.title[:40]}: {str(e)[:60]}")

    print(f"\nTriggered: {triggered}")


async def main_async(args):
    async with await NotebookLMClient.from_storage() as client:
        if args.cleanup or args.all:
            await cleanup_failed(client)
        if args.trigger or args.all:
            await trigger_chinese(client)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleanup", action="store_true", help="Delete FAILED artifacts")
    parser.add_argument("--trigger", action="store_true", help="Trigger zh generation for missing")
    parser.add_argument("--all", action="store_true", help="Both cleanup + trigger")
    args = parser.parse_args()
    if not any([args.cleanup, args.trigger, args.all]):
        parser.print_help()
        return
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
