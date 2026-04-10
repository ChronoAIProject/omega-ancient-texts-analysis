#!/usr/bin/env python3
"""Build mini-master NotebookLM notebooks per category.

Each classical text's 12 categories get their own "mini-master" notebook
containing:
- The category essay (overview)
- All per-unit dossiers for that category (hexagrams for I Ching, chapters for Tao Te Ching)

This gives us 24 mini-masters (12 易经 + 12 道德经) instead of 145 individual notebooks,
avoiding NotebookLM rate limits while preserving deep-dive content.

Each mini-master generates:
- 1 video (zh) — "how this category maps to Omega, with all units"
- 1 infographic (zh)
- 1 slide deck (zh)

Usage:
    python tools/build_mini_masters.py --text iching      # just 易经
    python tools/build_mini_masters.py --text daodejing   # just 道德经
    python tools/build_mini_masters.py --all              # both
"""

import argparse
import asyncio
import json
import re
from pathlib import Path

from notebooklm import NotebookLMClient

ROOT = Path(__file__).parent.parent
WORKSPACE = ROOT / "workspace"
SHOWCASE = ROOT.parent / "Omega-paper-series"


def load_iching_categories():
    """Load I Ching category → hexagram mapping from classification.json."""
    classif = json.loads((WORKSPACE / "易经" / "classification.json").read_text())
    cats = {}
    for c in classif["categories"]:
        cats[c["id"]] = {
            "name_zh": c["name_zh"],
            "name_en": c["name_en"],
            "hexagrams": c["hexagrams"],  # list of hexagram numbers
        }
    return cats


def load_daodejing_categories():
    """Load 道德经 category → chapter mapping."""
    classif_file = WORKSPACE / "daodejing_omega_classification.json"
    if not classif_file.exists():
        classif_file = WORKSPACE / "道德经" / "classification.json"
    classif = json.loads(classif_file.read_text())
    cats = {}
    for c in classif["categories"]:
        cats[c["id"]] = {
            "name_zh": c["name_zh"],
            "name_en": c["name_en"],
            "chapters": c["chapters"],
        }
    return cats


def find_iching_hexagram_file(hex_num: int) -> Path | None:
    """Find the hexagram dossier file for a given number."""
    pattern = f"hexagram-{hex_num:02d}-*.md"
    matches = list((SHOWCASE / "cultural" / "i-ching" / "hexagrams").glob(pattern))
    return matches[0] if matches else None


def find_daodejing_chapter_file(ch_num: int) -> Path | None:
    """Find the chapter dossier file for 道德经."""
    patterns = [f"chapter-{ch_num:02d}.md", f"chapter_{ch_num:02d}.md", f"chapter-{ch_num}.md"]
    for p in patterns:
        f = SHOWCASE / "cultural" / "tao-te-ching" / "chapters" / p
        if f.exists():
            return f
    return None


def find_iching_category_essay(cat_id: int) -> Path | None:
    """Find the category essay file."""
    pattern = f"category_{cat_id:02d}_*.md"
    matches = list((WORKSPACE / "易经" / "generated").glob(pattern))
    return matches[0] if matches else None


def find_daodejing_category_essay(cat_id: int) -> Path | None:
    pattern = f"category_{cat_id:02d}_*.md"
    matches = list((WORKSPACE / "道德经" / "generated").glob(pattern))
    return matches[0] if matches else None


async def build_mini_master(client, work: str, cat_id: int, cat_info: dict):
    """Build one mini-master notebook."""
    if work == "iching":
        title = f"Omega Mini: 易经 {cat_info['name_zh']}"
        essay_path = find_iching_category_essay(cat_id)
        unit_paths = [find_iching_hexagram_file(h) for h in cat_info["hexagrams"]]
        unit_type = "卦"
    else:  # daodejing
        title = f"Omega Mini: 道德经 {cat_info['name_zh']}"
        essay_path = find_daodejing_category_essay(cat_id)
        unit_paths = [find_daodejing_chapter_file(c) for c in cat_info["chapters"]]
        unit_type = "章"

    unit_paths = [p for p in unit_paths if p is not None]

    print(f"\n[{work}] Cat {cat_id:02d}: {cat_info['name_zh']}")
    print(f"  Essay: {'✓' if essay_path else '✗'}")
    print(f"  {unit_type} dossiers: {len(unit_paths)}")

    # Check if already exists
    nbs = await client.notebooks.list()
    existing = next((nb for nb in nbs if nb.title == title), None)
    if existing:
        print(f"  [skip] already exists: {existing.id[:8]}")
        return existing.id

    # Create notebook
    nb = await client.notebooks.create(title=title)
    nb_id = nb.id
    print(f"  Created: {nb_id[:8]}")

    # Add essay first
    if essay_path:
        content = essay_path.read_text()
        try:
            await client.sources.add_text(
                nb_id,
                title=f"[category essay] {essay_path.stem}",
                content=content,
                wait=True,
                wait_timeout=60,
            )
            print(f"    + essay")
        except Exception as e:
            print(f"    essay error: {str(e)[:60]}")

    # Add each unit dossier
    for up in unit_paths:
        content = up.read_text()
        try:
            await client.sources.add_text(
                nb_id,
                title=f"[{unit_type}] {up.stem}",
                content=content,
                wait=False,
            )
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"    unit error ({up.stem}): {str(e)[:60]}")

    print(f"    added {len(unit_paths)} unit sources")
    await asyncio.sleep(5)  # let sources settle

    # Trigger zh generation
    for kind, fn in [
        ("video", lambda: client.artifacts.generate_video(nb_id, language="zh")),
        ("infographic", lambda: client.artifacts.generate_infographic(nb_id, language="zh")),
        ("slides", lambda: client.artifacts.generate_slide_deck(nb_id, language="zh")),
    ]:
        try:
            await fn()
            print(f"    ✓ {kind} triggered")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"    ✗ {kind}: {str(e)[:60]}")

    return nb_id


async def main_async(args):
    async with await NotebookLMClient.from_storage() as client:
        if args.text in ("iching", "all"):
            print("\n=== Building 易经 mini-masters ===")
            cats = load_iching_categories()
            for cat_id, info in cats.items():
                await build_mini_master(client, "iching", cat_id, info)
                await asyncio.sleep(3)

        if args.text in ("daodejing", "all"):
            print("\n=== Building 道德经 mini-masters ===")
            cats = load_daodejing_categories()
            for cat_id, info in cats.items():
                await build_mini_master(client, "daodejing", cat_id, info)
                await asyncio.sleep(3)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", choices=["iching", "daodejing", "all"], default="all")
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
