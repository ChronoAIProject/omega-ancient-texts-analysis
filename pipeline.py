#!/usr/bin/env python3
"""Omega Ancient Texts Analysis Pipeline.

核心流程: 输入作品名 → 自动获取/拆解 → Omega 数学分析 → NotebookLM 视频生成

Usage:
    python pipeline.py 易经
    python pipeline.py 道德经 --chapters 1-5
    python pipeline.py 红楼梦 --chapters 1-3
    python pipeline.py --list
    python pipeline.py 易经 --dry-run
"""

import argparse
import json
import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import yaml

AUTOMATH_ROOT = Path(__file__).parent.parent / "automath"
NOTEBOOKLM_DISPATCH = AUTOMATH_ROOT / "tools" / "notebooklm-oracle" / "notebooklm_dispatch.py"

# 支持的经典著作及其拆解策略
KNOWN_WORKS = {
    "易经": {
        "en": "I Ching / Book of Changes",
        "units": "hexagram",
        "total": 64,
        "decompose": "64 hexagrams, each with 卦辞 + 爻辞 + 象辞",
    },
    "道德经": {
        "en": "Tao Te Ching",
        "units": "chapter",
        "total": 81,
        "decompose": "81 chapters, each a self-contained philosophical unit",
    },
    "红楼梦": {
        "en": "Dream of the Red Chamber",
        "units": "chapter",
        "total": 120,
        "decompose": "120 chapters, narrative structure with embedded poetry",
    },
    "论语": {
        "en": "Analerta",
        "units": "book",
        "total": 20,
        "decompose": "20 books, each with multiple dialogues",
    },
    "几何原本": {
        "en": "Euclid's Elements",
        "units": "book",
        "total": 13,
        "decompose": "13 books, axiomatic deductive structure",
    },
    "孙子兵法": {
        "en": "The Art of War",
        "units": "chapter",
        "total": 13,
        "decompose": "13 chapters on military strategy",
    },
}


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def parse_chapter_range(spec: str, total: int) -> list[int]:
    """Parse chapter range like '1-5' or '1,3,5' or 'all'."""
    if spec == "all":
        return list(range(1, total + 1))
    chapters = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-", 1)
            chapters.extend(range(int(a), int(b) + 1))
        else:
            chapters.append(int(part))
    return [c for c in chapters if 1 <= c <= total]


def decompose_work(work_name: str, chapters: list[int], config: dict) -> list[dict]:
    """Decompose a literary work into analysis units.

    For each unit, generate a structured text segment that includes:
    - Original text (fetched or from local corpus)
    - Context and metadata
    - Omega analysis prompt
    """
    work = KNOWN_WORKS.get(work_name)
    if not work:
        print(f"[ERROR] Unknown work: {work_name}")
        print(f"  Supported: {', '.join(KNOWN_WORKS.keys())}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"作品: {work_name} ({work['en']})")
    print(f"拆解: {work['decompose']}")
    print(f"处理: {len(chapters)} {work['units']}(s)")
    print(f"{'='*60}")

    units = []
    texts_dir = Path("texts") / work_name.lower().replace(" ", "_")
    texts_dir.mkdir(parents=True, exist_ok=True)

    for ch in chapters:
        # Check local corpus first
        local_files = list(texts_dir.glob(f"*{ch:02d}*")) + list(texts_dir.glob(f"*{ch}*"))
        if local_files:
            text_content = local_files[0].read_text(encoding="utf-8")
            source = str(local_files[0])
        else:
            # Generate analysis prompt for LLM to work with
            text_content = None
            source = "llm-generated"

        units.append({
            "work": work_name,
            "work_en": work["en"],
            "unit_type": work["units"],
            "unit_number": ch,
            "text_content": text_content,
            "source": source,
            "output_dir": str(texts_dir / f"{work['units']}_{ch:03d}"),
        })

    return units


def generate_analysis_pdf(unit: dict, config: dict) -> Path:
    """Generate a PDF analysis document for one unit using LLM.

    The PDF will be fed to NotebookLM for video generation.
    """
    output_dir = Path(unit["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / "analysis.pdf"
    tex_path = output_dir / "analysis.tex"

    if pdf_path.exists():
        print(f"  [跳过] PDF already exists: {pdf_path}")
        return pdf_path

    # Build analysis document
    work = unit["work"]
    ch = unit["unit_number"]
    unit_type = unit["unit_type"]

    omega_intro = textwrap.dedent(f"""\
    \\section{{Omega 数学框架}}

    Omega 项目从单一方程 $x^2 = x + 1$（黄金比例多项式）出发，
    通过形式化验证（Lean 4）推导出覆盖 9 个数学分支的 10,588+ 条机器验证定理。
    核心结构包括：黄金平均移位、Zeckendorf 表示、Fibonacci 增长、
    折叠算子、模塔与逆极限、谱理论等。

    本分析将 {work} 第 {ch} {unit_type} 的结构特征
    与 Omega 形式化结果进行对应分析。
    """)

    text_section = ""
    if unit["text_content"]:
        # Escape LaTeX special chars in text content
        escaped = unit["text_content"].replace("\\", "\\textbackslash{}")
        for ch_special in ["&", "%", "$", "#", "_", "{", "}"]:
            escaped = escaped.replace(ch_special, f"\\{ch_special}")
        text_section = f"\\section{{原文}}\n\n\\begin{{quote}}\n{escaped}\n\\end{{quote}}\n"

    tex_content = textwrap.dedent(f"""\
    \\documentclass[12pt]{{article}}
    \\usepackage{{ctex}}
    \\usepackage{{amsmath,amssymb}}
    \\usepackage{{geometry}}
    \\geometry{{a4paper,margin=2.5cm}}

    \\title{{Omega 数学视角下的《{work}》\\\\
    第 {unit['unit_number']} {unit_type} 结构分析}}
    \\author{{The Omega Institute — AI Mathematical Discovery Engine}}
    \\date{{\\today}}

    \\begin{{document}}
    \\maketitle

    \\begin{{abstract}}
    本文运用 Omega 纯数学框架（基于 $x^2 = x + 1$）分析《{work}》
    第 {unit['unit_number']} {unit_type} 的内在数学结构。
    所有数学结论均可追溯至 Lean 4 形式化证明。
    \\end{{abstract}}

    {text_section}

    {omega_intro}

    \\section{{结构对应分析}}

    \\textit{{（此部分将由 LLM 基于 Omega 定理库自动生成）}}

    % TODO: 自动填充 - 由 LLM 分析文本结构并映射到 Omega 定理

    \\section{{结论}}

    \\textit{{（自动生成）}}

    \\end{{document}}
    """)

    tex_path.write_text(tex_content, encoding="utf-8")
    print(f"  [生成] LaTeX: {tex_path}")

    # Compile PDF
    try:
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "-output-directory", str(output_dir), str(tex_path)],
            capture_output=True, text=True, timeout=60,
        )
        if pdf_path.exists():
            print(f"  [编译] PDF: {pdf_path}")
        else:
            print(f"  [WARN] PDF compilation may have issues, check {output_dir}")
    except FileNotFoundError:
        print(f"  [WARN] xelatex not found, LaTeX saved at {tex_path}")
    except subprocess.TimeoutExpired:
        print(f"  [WARN] xelatex timed out for {tex_path}")

    return pdf_path


def dispatch_to_notebooklm(pdf_path: Path, unit: dict, config: dict) -> dict:
    """Send analysis PDF to NotebookLM for video generation.

    Uses automath's notebooklm_dispatch.py to generate slides + audio.
    """
    if not NOTEBOOKLM_DISPATCH.exists():
        print(f"  [ERROR] NotebookLM dispatch not found: {NOTEBOOKLM_DISPATCH}")
        print(f"         Ensure automath is cloned at {AUTOMATH_ROOT}")
        return {"status": "error", "reason": "notebooklm_dispatch.py not found"}

    if not pdf_path.exists():
        print(f"  [SKIP] No PDF to dispatch: {pdf_path}")
        return {"status": "skipped", "reason": "no pdf"}

    work = unit["work"]
    ch = unit["unit_number"]
    print(f"  [NotebookLM] Dispatching: {work} #{ch} → slides + audio")

    try:
        result = subprocess.run(
            ["python3", str(NOTEBOOKLM_DISPATCH), "--paper", str(pdf_path.parent)],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode == 0:
            print(f"  [NotebookLM] Done: {result.stdout.strip()[-200:]}")
            return {"status": "success", "output": result.stdout}
        else:
            print(f"  [NotebookLM] Error: {result.stderr.strip()[-200:]}")
            return {"status": "error", "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}


def run_pipeline(work_name: str, chapters: list[int], config: dict, dry_run: bool = False) -> list[dict]:
    """Run full pipeline: decompose → analyze → generate PDF → NotebookLM video."""
    units = decompose_work(work_name, chapters, config)
    results = []

    for i, unit in enumerate(units):
        ch = unit["unit_number"]
        print(f"\n--- [{i+1}/{len(units)}] {work_name} {unit['unit_type']} {ch} ---")

        if dry_run:
            print(f"  [DRY RUN] Would process {unit['unit_type']} {ch}")
            results.append({"unit": unit, "status": "dry_run"})
            continue

        # Step 1: Generate analysis PDF
        pdf_path = generate_analysis_pdf(unit, config)

        # Step 2: Dispatch to NotebookLM
        nb_result = dispatch_to_notebooklm(pdf_path, unit, config)

        results.append({
            "unit": unit,
            "pdf": str(pdf_path),
            "notebooklm": nb_result,
        })

        # Progress report every 20s for long runs
        if (i + 1) % 5 == 0:
            print(f"\n[进度] {i+1}/{len(units)} units processed")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Omega 古典著作分析管线: 输入作品名 → 自动拆解 → 数学分析 → NotebookLM 视频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        Examples:
          python pipeline.py 易经                    # 全部 64 卦
          python pipeline.py 道德经 --chapters 1-5   # 前 5 章
          python pipeline.py 红楼梦 --chapters 1,5,12 # 指定章节
          python pipeline.py --list                   # 列出支持的作品
        """),
    )
    parser.add_argument("work", nargs="?", help="作品名（如：易经、道德经、红楼梦）")
    parser.add_argument("--chapters", default="all", help="章节范围: 1-5, 1,3,5, or all (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="只显示计划，不执行")
    parser.add_argument("--list", action="store_true", help="列出支持的作品")
    parser.add_argument("--config", default="config.yaml", help="Config file path")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.list:
        print("支持的经典著作:\n")
        for name, info in KNOWN_WORKS.items():
            print(f"  {name:8s}  {info['en']:30s}  {info['total']:>3d} {info['units']}(s)")
            print(f"  {'':8s}  {info['decompose']}")
            print()
        return

    if not args.work:
        parser.print_help()
        return

    work = KNOWN_WORKS.get(args.work)
    if not work:
        print(f"[ERROR] 未知作品: {args.work}")
        print(f"  支持: {', '.join(KNOWN_WORKS.keys())}")
        sys.exit(1)

    chapters = parse_chapter_range(args.chapters, work["total"])
    print(f"[配置] NotebookLM dispatch: {NOTEBOOKLM_DISPATCH}")
    print(f"[配置] automath: {AUTOMATH_ROOT}")

    results = run_pipeline(args.work, chapters, config, dry_run=args.dry_run)

    print(f"\n{'='*60}")
    print(f"完成: {args.work} — {len(results)} units processed")
    success = sum(1 for r in results if r.get("notebooklm", {}).get("status") == "success")
    print(f"  NotebookLM 成功: {success}/{len(results)}")


if __name__ == "__main__":
    main()
