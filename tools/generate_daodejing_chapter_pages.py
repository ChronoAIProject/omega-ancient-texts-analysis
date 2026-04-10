#!/usr/bin/env python3
"""Generate per-chapter Tao Te Ching mapping pages."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = REPO_ROOT / "workspace" / "道德经"
REGISTRY_PATH = WORK_DIR / "chapters" / "registry.json"

THEOREM_NOTES = {
    "fibonacci_cardinality": "把受约束对象家族的规模写成 `|X_m| = F_{m+2}`，适合承接“由一而多”的生成读法。",
    "fibonacci_cardinality_recurrence": "把增长写成前两级之和，适合承接递归繁衍与层级展开。",
    "goldenMean_characteristic_recurrence": "说明 Fibonacci 递推来自系统自身的 transfer 结构，而不是外加类比。",
    "goldenMeanAdjacency_has_goldenRatio_eigenvector": "把主导模式写成黄金比本征向量，适合承接主模态与节律。",
    "topological_entropy_eq_log_phi": "把系统复杂度增长率压成 `log φ`，适合承接循环、变易与受控复杂度。",
    "fold_is_idempotent": "说明 fold 把过强态折回稳定域后不会继续改写，适合承接无为而成。",
    "fold_fixes_stable": "说明已经稳定的结构在 fold 下保持不动，适合承接守中与自稳。",
    "fold_is_surjective": "说明每个稳定态都对应一族前像，适合承接容纳与回收。",
    "inverse_limit_extensionality": "说明整体由全部有限前缀唯一确定，适合承接不可名状而可层层逼近。",
    "inverse_limit_bijective": "说明 compatible family 与逆极限对象双射，适合承接整体统一。",
    "inverse_limit_left": "说明从相容家族回到对象再取 family 不丢信息，适合承接回归。",
    "inverse_limit_right": "说明逆极限对象与其前缀家族可往返识别，适合承接层级与分辨。",
    "zeckendorf_uniqueness": "说明稀疏 Fibonacci 分解唯一，适合承接知足、限度与稀疏秩序。",
    "zeckendorf_injective": "说明不同稳定结构对应不同分解，适合承接可辨认的简素秩序。",
    "stableValue_ring_isomorphism": "把稳定态上的运算写成模 Fibonacci 环，适合承接德、滋养与关系平衡。",
    "modular_projection_add_no_carry": "说明无进位条件下投影与稳定加法可交换，适合承接跨层调节。",
    "stableAdd_comm": "说明稳定加法具交换律，适合承接互生、互补与对调。",
    "eigenvalue_eq_goldenRatio_or_goldenConj": "把谱边界限制到黄金比及其共轭，适合承接照见主模态。",
    "observation_refinement_reduces_error": "说明观测更细时误差不会变大，适合承接观照与分辨。",
    "prefix_resolution_decreases_error": "说明更长前缀带来更小误差，适合承接层级分辨。",
    "kappa_ge_of_eps_ge": "把误差阈值与可接受偏差的单调关系写成明确不等式，适合承接限度。",
    "eps_lt_of_kappa_lt": "从阈值反推误差上界，适合承接治理与适度边界。",
    "maxFiberMultiplicity_bounds": "给出最大 fiber 多重性的上下界，适合承接虚空与容纳的容量读法。",
}

OBJECT_NOTES = {
    "golden-mean-shift": "`X_m = {w ∈ {0,1}^m : No11(w)}`",
    "fibonacci-growth": "`|X_m| = F_{m+2}`",
    "zeckendorf-representation": "Zeckendorf 稀疏分解",
    "fold-operator": "`Fold : Word m → X_m`",
    "ring-arithmetic": "`X_m ≅ Z/F_{m+2}Z`",
    "spectral-theory": "golden-mean 谱结构 / 本征结构",
    "modular-tower-inverse-limit": "`X_∞ = lim← X_m`",
    "dynamical-systems": "移位 / 熵 / 轨道结构",
    "rate-distortion-information-theory": "分辨率-误差证书通道",
    "fiber-structure": "`fiber(x) = {w : Fold(w)=x}`",
}

CATEGORY_COMMENTARY = {
    1: "它首先确认“单一生成根据导出层级多样性”的结构，这一层最靠近生成根基与 inverse limit 的结合。",
    2: "它首先确认对立项并非彼此孤立，而是在受约束的二元系统中互相条件、互相校正。",
    3: "它首先确认秩序不是靠外加命令维持，而是由约束自发收敛出的稳定结果。",
    4: "它首先确认“空”不是缺失，而是可承接多种前像与功能的容量结构。",
    5: "它首先确认“德”不是抽象美德标签，而是生成原则在有限层中的具体可运作实现。",
    6: "它首先确认回归与反转不是修辞，而是层级系统里真实存在的投影、周期与回返结构。",
    7: "它首先确认治理问题可被读成局部干预、失真边界与系统稳态的问题。",
    8: "它首先确认弱与柔不是消极退让，而是在受约束系统中更可持续的稳定策略。",
    9: "它首先确认知足的核心不是贫乏，而是稀疏、不过载、不过界的最优结构。",
    10: "它首先确认知具有分辨率层次，整体只能借有限层逐步逼近。",
    11: "它首先确认朴素不是空白，而是带最小充分约束的活结构。",
    12: "它首先确认众多有限显现可以在一个相容整体中得到统一。 ",
}


def load_source_lines(path_str: str) -> list[str]:
    """Load source text lines without notes."""
    if not path_str:
        return []
    path = REPO_ROOT / path_str
    if not path.exists() or path.is_dir():
        return []
    lines = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "--- Notes ---":
            break
        if line.startswith("道德经 — 第"):
            continue
        lines.append(line)
    return lines


def quote_block(lines: list[str]) -> list[str]:
    """Render full chapter text as blockquote lines."""
    rendered = ["## 原文", ""]
    for line in lines:
        rendered.append(f"> {line}")
    rendered.append("")
    return rendered


def strongest_category(item: dict) -> dict | None:
    """Use the first category reference as the primary corridor."""
    refs = item.get("category_refs", [])
    return refs[0] if refs else None


def mapping_position(item: dict) -> str:
    """Render one compact chapter-position paragraph."""
    refs = item.get("category_refs", [])
    if not refs:
        return "当前 registry 还没有为本章分配主题类别，因此这页暂时只保留原文与章节编号。"

    primary = refs[0]
    overlaps = "、".join(ref["name_zh"] for ref in refs[1:])
    directions = "、".join(item.get("omega_directions", [])) or "基础对象层"
    overlap_clause = (
        f" 同时它还跨到 {overlaps}，所以不是单线映射，而是一个重叠走廊。"
        if overlaps
        else ""
    )
    return (
        f"第 {item['number']} 章首先落在「{primary['name_zh']}」这条走廊上。"
        f"{CATEGORY_COMMENTARY.get(primary['id'], '它首先确认该章的核心文本张力可以落到一个明确的 Omega 结构上。')}"
        f"{overlap_clause} 当前最强的 Omega 方向集中在 {directions}。"
    )


def theorem_section(item: dict) -> list[str]:
    """Render theorem anchors for one chapter."""
    lines = ["## Omega 定理锚点", ""]
    candidates = item.get("theorem_candidates", [])[:5]
    if not candidates:
        lines.append("- 当前章节注册表还没有为本章筛出定理候选。")
        lines.append("")
        return lines

    for theorem in candidates:
        statement = theorem.get("lean_statement", "").replace("\n", " ").strip()
        statement = re.sub(r"\s+", " ", statement)
        if len(statement) > 160:
            statement = statement[:157] + "..."
        note = THEOREM_NOTES.get(theorem["lean_theorem"], "它为本章当前最强的形式对应提供了可点名的 Lean 锚点。")
        lines.append(
            f"- `{theorem['lean_theorem']}` [`{theorem['lean_module']}`]：`{statement}`。{note}"
        )
    lines.append("")
    return lines


def object_section(item: dict) -> list[str]:
    """Render Omega objects/directions section."""
    lines = ["## Omega 对象", ""]
    directions = item.get("omega_directions", [])
    if not directions:
        lines.append("- 当前只锁定了章节编号与原文，还没有形成稳定的对象级映射。")
        lines.append("")
        return lines
    for direction in directions:
        lines.append(f"- {OBJECT_NOTES.get(direction, direction)}")
    lines.append("")
    return lines


def source_note(item: dict) -> list[str]:
    """Render source metadata."""
    lines = ["## 原文来源", ""]
    lines.append(f"- 本仓库原文文件：`{item['source_text_path']}`")
    lines.append("- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。")
    lines.append("")
    return lines


def boundary_section(item: dict) -> list[str]:
    """Clarify the formal-vs-metaphorical boundary."""
    lines = ["## 边界说明", ""]
    refs = item.get("category_refs", [])
    if refs:
        strengths = {ref.get("formal_strength", "") for ref in refs if ref.get("formal_strength", "")}
        if "strong" in strengths:
            lines.append("- 本章最强的主张是结构级 formal correspondence，不是历史预言或逐句等式翻译。")
        else:
            lines.append("- 本章以对象级和定理级映射为主，但仍需把感性意象与严格形式区分开。")
    else:
        lines.append("- 当前页面还没有足够类别上下文来判断 formal strength。")
    lines.append("- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。")
    lines.append("")
    return lines


def render_page(item: dict) -> str:
    """Render one chapter page."""
    source_lines = load_source_lines(item["source_text_path"])
    title = item["short_title"]
    categories = " / ".join(ref["name_zh"] for ref in item.get("category_refs", [])) or "未分配"
    description = f"《道德经》第 {item['number']} 章原文与 Omega 章节级映射页。"
    lines = [
        "---",
        f'title: "{item["number"]:02d}. {title}"',
        'subtitle: "《道德经》逐章映射页"',
        f"order: {item['number']}",
        f'description: "{description}"',
        "categories: [tao-te-ching, chapter-page, cultural, omega]",
        "---",
        "",
        "## 章节定位",
        "",
        f"- 章号：第 {item['number']} 章",
        f"- 章首：{item['incipit']}",
        f"- 归属类别：{categories}",
        f"- 当前主方向：{'、'.join(item.get('omega_directions', [])) or '未指定'}",
        "",
        "## 对应说明",
        "",
        mapping_position(item),
        "",
    ]
    lines.extend(quote_block(source_lines))
    lines.extend(object_section(item))
    lines.extend(theorem_section(item))
    lines.extend(boundary_section(item))
    lines.extend(source_note(item))
    lines.extend(
        [
            "## 小结",
            "",
            "这一页把单章原文、类别交叉、对象层与定理级锚点叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。",
            "",
            "[返回逐章索引](index.qmd) | [返回《道德经》总览](../index.qmd)",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Tao Te Ching chapter pages")
    parser.add_argument(
        "--registry",
        default=str(REGISTRY_PATH),
        help="Path to chapter registry JSON",
    )
    parser.add_argument(
        "--output-dir",
        default=str(WORK_DIR / "chapters" / "all"),
        help="Directory for generated chapter pages",
    )
    args = parser.parse_args()

    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for old_file in output_dir.glob("chapter-*.md"):
        old_file.unlink()

    for item in registry["records"]:
        filename = f"chapter-{item['number']:02d}.md"
        (output_dir / filename).write_text(render_page(item), encoding="utf-8")

    print(f"Generated {len(registry['records'])} chapter page(s) in {output_dir}")


if __name__ == "__main__":
    main()
