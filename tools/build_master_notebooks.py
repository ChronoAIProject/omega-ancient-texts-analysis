#!/usr/bin/env python3
"""Build master NotebookLM notebooks per work.

Each work gets ONE notebook containing ALL content as sources:
- 易经: 64 hexagram dossiers + 12 category essays + source texts
- 道德经: 12 category essays + (future) per-chapter analyses
- 黄帝内经: 12 category essays
- 孙子兵法: 10 category essays
- 几何原本: 8 category essays
- Omega Papers: 9 paper introductions + key theorems

Master notebooks produce "flagship" videos that explain the entire system,
not just individual parts. Individual notebooks remain for granular content.

Usage:
    python tools/build_master_notebooks.py --list
    python tools/build_master_notebooks.py --work iching
    python tools/build_master_notebooks.py --all
"""

import argparse
import asyncio
import sys
from pathlib import Path

from notebooklm import NotebookLMClient

ROOT = Path(__file__).parent.parent
WORKSPACE = ROOT / "workspace"
SHOWCASE = ROOT.parent / "Omega-paper-series"

WORKS = {
    "iching": {
        "zh_name": "易经",
        "en_name": "The Mathematics of the I Ching",
        "title": "Omega Master: The I Ching as 6-bit Binary System",
        "sources": [
            # Source texts (if exist)
            ("i-ching-source", ROOT / "texts" / "yijing", "*.txt"),
            # Category essays
            ("i-ching-categories", WORKSPACE / "易经" / "generated", "*.md"),
            # Hexagram dossiers (Codex-generated)
            ("i-ching-hexagrams", SHOWCASE / "cultural" / "i-ching" / "hexagrams", "*.md"),
        ],
        "description": "All 64 hexagrams as binary words in {0,1}^6, with 21 GMS-valid (F_8), Omega theorem anchors, and category mappings.",
    },
    "daodejing": {
        "zh_name": "道德经",
        "en_name": "The Mathematics of the Tao Te Ching",
        "title": "Omega Master: Tao Te Ching Generative Structure",
        "sources": [
            ("daodejing-source", ROOT / "texts" / "daodejing", "*.txt"),
            ("daodejing-categories", WORKSPACE / "道德经" / "generated", "*.md"),
        ],
        "description": "All 81 chapters mapped through 12 thematic categories onto golden-mean shift, Fibonacci growth, and inverse limit structures.",
    },
    "neijing": {
        "zh_name": "黄帝内经",
        "en_name": "The Mathematics of the Huangdi Neijing",
        "title": "Omega Master: Huangdi Neijing Multiscale Medicine",
        "sources": [
            ("neijing-categories", WORKSPACE / "黄帝内经" / "generated", "*.md"),
        ],
        "description": "93 selected chapters as a multiscale coupled system mapping to dynamical systems, modular tower, and rate-distortion theory.",
    },
    "sunzi": {
        "zh_name": "孙子兵法",
        "en_name": "The Mathematics of the Art of War",
        "title": "Omega Master: Sun Tzu Strategic Dynamics",
        "sources": [
            ("sunzi-categories", WORKSPACE / "孙子兵法" / "generated", "*.md"),
        ],
        "description": "13 chapters as strategic dynamics mapping to fold operators, spectral theory, and information-constrained optimization.",
    },
    "euclid": {
        "zh_name": "几何原本",
        "en_name": "The Mathematics of Euclid's Elements",
        "title": "Omega Master: Euclid as Constrained Generation",
        "sources": [
            ("euclid-categories", WORKSPACE / "几何原本" / "generated", "*.md"),
        ],
        "description": "13 books read as a constrained generation grammar, from postulates through exhaustion to solid geometry.",
    },
    "papers": {
        "zh_name": "Omega 论文集",
        "en_name": "Omega Research Papers Overview",
        "title": "Omega Master: The Full Research Program",
        "sources": [
            # Paper READMEs and main.tex files
            ("papers", SHOWCASE / "papers", "*/README.md"),
        ],
        "description": "All 9 Gen 2 submitted papers viewed as a single research program deriving from x²=x+1.",
    },
}


def collect_sources(work_key):
    work = WORKS[work_key]
    sources = []
    for source_name, path, pattern in work["sources"]:
        if not path.exists():
            print(f"  [skip] {path} — does not exist")
            continue
        if "/" in pattern:
            files = sorted(path.glob(pattern))
        else:
            files = sorted(path.glob(pattern))
        print(f"  [found] {len(files)} files in {path.name} matching {pattern}")
        for f in files:
            try:
                content = f.read_text(encoding="utf-8")
                sources.append({
                    "title": f"{source_name}: {f.stem}",
                    "content": content,
                    "source_file": str(f),
                })
            except Exception as e:
                print(f"  [error] {f}: {e}")
    return sources


async def build_master(work_key: str):
    if work_key not in WORKS:
        print(f"Unknown work: {work_key}")
        return
    work = WORKS[work_key]

    print(f"\n{'='*60}")
    print(f"Building master notebook: {work['title']}")
    print(f"{'='*60}")

    sources = collect_sources(work_key)
    if not sources:
        print(f"  No sources found for {work_key}")
        return

    print(f"  Total sources: {len(sources)}")
    total_chars = sum(len(s["content"]) for s in sources)
    print(f"  Total chars: {total_chars}")

    async with await NotebookLMClient.from_storage() as c:
        # Check if master already exists
        nbs = await c.notebooks.list()
        existing_title = f"Omega Master: {work['en_name']}"
        for nb in nbs:
            if nb.title == existing_title:
                print(f"  Master notebook already exists: {nb.id[:8]}")
                return nb.id

        # Create new master notebook
        nb = await c.notebooks.create(title=existing_title)
        print(f"  Created notebook: {existing_title} [{nb.id[:8]}]")

        # Add sources (NotebookLM limit is typically 50 sources per notebook)
        # If more, concatenate into chunks
        if len(sources) <= 50:
            for i, src in enumerate(sources):
                try:
                    await c.sources.add_text(
                        nb.id,
                        title=src["title"][:100],
                        content=src["content"],
                        wait=False,
                    )
                    if (i + 1) % 10 == 0:
                        print(f"    added {i+1}/{len(sources)} sources")
                    await asyncio.sleep(0.3)
                except Exception as e:
                    print(f"    [error] {src['title']}: {e}")
        else:
            # Concatenate into mega-sources of ~50 each
            chunks = [sources[i:i+50] for i in range(0, len(sources), 50)]
            for ci, chunk in enumerate(chunks):
                combined = "\n\n---\n\n".join(
                    f"# {s['title']}\n\n{s['content']}" for s in chunk
                )
                try:
                    await c.sources.add_text(
                        nb.id,
                        title=f"{work_key}_chunk_{ci+1}",
                        content=combined,
                        wait=False,
                    )
                    print(f"    added chunk {ci+1}/{len(chunks)} ({len(combined)} chars)")
                except Exception as e:
                    print(f"    [error] chunk {ci}: {e}")

        # Wait for sources to process, then trigger generation
        print(f"  Waiting 10s for source processing...")
        await asyncio.sleep(10)

        try:
            await c.artifacts.generate_video(nb.id)
            print(f"  ✓ video triggered")
        except Exception as e:
            print(f"  video trigger error: {e}")

        try:
            await c.artifacts.generate_infographic(nb.id, language="en")
            print(f"  ✓ infographic triggered")
        except Exception as e:
            print(f"  infographic trigger error: {e}")

        try:
            await c.artifacts.generate_slide_deck(nb.id, language="en")
            print(f"  ✓ slides triggered")
        except Exception as e:
            print(f"  slides trigger error: {e}")

        return nb.id


async def main_async(args):
    if args.list:
        print("Available master notebooks:")
        for key, work in WORKS.items():
            print(f"  {key:12s}  {work['zh_name']:8s}  {work['en_name']}")
        return

    if args.work:
        await build_master(args.work)
    elif args.all:
        for key in WORKS:
            await build_master(key)
            await asyncio.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="Build master NotebookLM notebooks")
    parser.add_argument("--work", help="Work key (iching, daodejing, neijing, sunzi, euclid, papers)")
    parser.add_argument("--all", action="store_true", help="Build all master notebooks")
    parser.add_argument("--list", action="store_true", help="List available works")
    args = parser.parse_args()

    if not any([args.work, args.all, args.list]):
        parser.print_help()
        return

    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
