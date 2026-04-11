#!/usr/bin/env python3
"""Regenerate paper infographics using the synthesis brief template.

Earlier infographic generation for paper notebooks failed because sources
were raw paper abstract/README text. Synthesis notebooks succeeded because
their sources had a pre-baked structured brief (metadata + NotebookLM
instructions + content). This script applies that same pattern to the
9 Gen 2 papers.

For each paper:
1. Build a structured source from paper README + .qmd front matter
2. Create a fresh NotebookLM notebook (parallel to any existing one)
3. Trigger zh infographic generation

Usage:
    python tools/regenerate_paper_infographics.py            # all 9
    python tools/regenerate_paper_infographics.py --paper zero-jitter-information-clocks-parry-gibbs-rigidity
    python tools/regenerate_paper_infographics.py --dry-run
"""

import argparse
import asyncio
import re
import site
import sys
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


ROOT = Path(__file__).parent.parent
SHOWCASE = ROOT.parent / "Omega-paper-series"
PAPERS_DIR = SHOWCASE / "papers"
QMD_DIR = SHOWCASE / "science" / "gen2"

# Canonical asset prefix per paper slug (matches what .qmd pages expect)
PAPER_PREFIXES = {
    "zero-jitter-information-clocks-parry-gibbs-rigidity": "zero_jitter_information_clocks",
    "zeckendorf-streaming-normalization-automata-rairo": "zeckendorf_streaming_normalization_automata",
    "resolution-folding-core-symbolic-dynamics": "resolution_folding_core_symbolic",
    "grg-shell-geometry-from-stationary-detector-thermality": "grg_shell_geometry_from",
    "folded-rotation-histogram-certificates": "folded_rotation_histogram_certificates",
    "folded-rotation-histogram": "folded_rotation_histogram",
    "fibonacci-stabilization-sharp-threshold-conjugacy-nonlinearity": "fibonacci_stabilization_sharp_threshold",
    "fibonacci-moduli-cross-resolution-arithmetic": "fibonacci_moduli_cross_resolution",
    "branch-cubic-regular-s4-closure-prym-ray-class": "branch_cubic_regular_s4",
}


def extract_front_matter(qmd_path: Path) -> dict:
    content = qmd_path.read_text(encoding="utf-8")
    m = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    fm = {}
    if m:
        for line in m.group(1).split('\n'):
            if ':' in line and not line.startswith('-'):
                k, _, v = line.partition(':')
                fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def extract_abstract(qmd_path: Path) -> str:
    content = qmd_path.read_text(encoding="utf-8")
    m = re.search(r'## Abstract\s*\n\n(.*?)\n\n', content, re.DOTALL)
    return m.group(1).strip() if m else ""


def build_paper_source(slug: str, prefix: str) -> tuple[str, str]:
    """Return (title, structured_source_content) for a paper."""
    qmd = QMD_DIR / f"{slug}.qmd"
    readme = PAPERS_DIR / slug / "README.md"

    fm = extract_front_matter(qmd) if qmd.exists() else {}
    abstract = extract_abstract(qmd) if qmd.exists() else ""
    readme_text = readme.read_text(encoding="utf-8") if readme.exists() else ""

    paper_title = fm.get("title", slug)
    subtitle = fm.get("subtitle", "")
    journal = fm.get("target-journal", "international journal")
    status = fm.get("status", "Submitted")
    theorems = fm.get("theorems", "?")

    # Structured brief following synthesis pattern
    brief = f"""# Omega Paper: {paper_title}

## 核心元数据 / Core Metadata

- 论文标题 / Paper title: {paper_title}
- 副标题 / Subtitle: {subtitle}
- 目标期刊 / Target journal: {journal}
- 状态 / Status: {status}
- 机器验证定理数 / Machine-verified theorems: {theorems}
- 论文 slug: {slug}
- 规范资源前缀 / Canonical asset prefix: {prefix}

## 论文所属程序 / Research Program

本论文属于 Omega 研究项目：从单个方程 `x² = x + 1` 出发，系统推导所有数学必然后果。
全部定理经 Lean 4 机器验证，零额外公理。

This paper is part of the Omega research program: starting from a single equation
`x² = x + 1`, systematically deriving what mathematically must follow. Every
theorem machine-verified in Lean 4, zero axioms beyond core logic.

## NotebookLM 生成说明 / Generation Instructions

### 语言策略 / Language

- 主语言 / Primary: 中文 (Chinese)
- 辅助语言 / Secondary: English
- 中文负责主叙事、可视化标题、核心概念解释
- English 保留 theorem names, paper title, key mathematical objects
- 不要把整个 infographic 变成纯英文
- Do NOT make the entire infographic English

### 受众 / Audience

- 中文数学爱好者和研究者
- 国际数学研究社区 (英文术语保留)
- 社交媒体传播（微博、知乎、Twitter/X）

### 输出重点 / Output Focus

For the infographic:
1. 论文要解决的核心问题 (Core problem the paper addresses) — 中文为主
2. 主要定理陈述 (Main theorem statements) — 中英并列
3. 关键数学对象 (Key mathematical objects) — 保留英文名
4. 与 Omega 框架 `x² = x + 1` 的连接 — 中文解释

### Visual Style

- 优雅、学术、但可传播
- 中文标题大字，英文术语小字
- 数学符号精确
- 避免 AI slop（无意义装饰、空洞短语）

---

## 论文摘要 / Abstract

{abstract}

---

## 完整 README 内容 / Full README

{readme_text}
"""
    title = f"Omega Paper Infographic: {slug}"
    return title, brief


async def regenerate_paper(client, slug: str, dry_run: bool = False):
    if slug not in PAPER_PREFIXES:
        print(f"  ✗ unknown paper slug: {slug}")
        return
    prefix = PAPER_PREFIXES[slug]
    title, source = build_paper_source(slug, prefix)

    print(f"\n[{slug}]")
    print(f"  Source: {len(source)} chars")

    if dry_run:
        print(f"  [DRY RUN] would create notebook: {title}")
        return

    # Check if already exists
    nbs = await client.notebooks.list()
    existing = next((nb for nb in nbs if nb.title == title), None)
    if existing:
        print(f"  [exists] {existing.id[:8]}, will reuse and retrigger")
        nb_id = existing.id
    else:
        nb = await client.notebooks.create(title=title)
        nb_id = nb.id
        print(f"  Created: {nb_id[:8]}")

        await client.sources.add_text(
            nb_id,
            title=f"{slug}_structured_source.md",
            content=source,
            wait=True,
            wait_timeout=120,
        )
        print(f"  ✓ source added")

    # Trigger zh infographic + slides + video (use synthesis pattern end-to-end)
    try:
        status = await client.artifacts.generate_infographic(nb_id, language="zh")
        print(f"  ✓ infographic triggered: task={status.task_id[:8] if status.task_id else status.status}")
    except Exception as e:
        print(f"  ✗ infographic trigger failed: {str(e)[:100]}")


async def main_async(args):
    async with await NotebookLMClient.from_storage() as client:
        slugs = [args.paper] if args.paper else list(PAPER_PREFIXES.keys())
        for slug in slugs:
            try:
                await regenerate_paper(client, slug, dry_run=args.dry_run)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"  ✗ {slug} failed: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper", help="Single paper slug (default: all 9)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
