#!/usr/bin/env python3
"""Generate per-hexagram structural dossiers for the I Ching."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

THEOREM_NOTES = {
    "fibonacci_cardinality": "把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。",
    "fibonacci_cardinality_recurrence": "把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。",
    "goldenMean_characteristic_recurrence": "说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。",
    "goldenMeanAdjacency_has_goldenRatio_eigenvector": "把主导增长方向写成黄金比本征向量，适合解释主模态与稳定节律。",
    "topological_entropy_eq_log_phi": "把复杂度增长率压成 `log φ`，适合解释变易与循环的受控熵结构。",
    "fold_is_idempotent": "说明 fold 一旦把原始词折回稳定域，再施一次不会继续改写。",
    "fold_fixes_stable": "说明已经稳定的卦象在 fold 下保持不动，适合区分 stable word 与 raw word。",
    "fold_is_surjective": "说明每个稳定态都可作为某个前像族的代表点，适合解释 fiber 结构。",
    "inverse_limit_extensionality": "说明整体是否相同完全由全部前缀是否相同决定，适合解释层级兼容。",
    "inverse_limit_bijective": "说明 compatible family 与逆极限对象之间是双射，适合解释整体由有限层闭合产生。",
    "zeckendorf_uniqueness": "说明非相邻 Fibonacci 指标分解唯一，适合解释稀疏稳定布局的唯一性。",
    "zeckendorf_injective": "说明不同稳定词对应不同指标集，适合解释稀疏结构的可辨认性。",
    "stableValue_ring_isomorphism": "把稳定态关系写成模 Fibonacci 环上的封闭运算，适合解释损/益和互补调节。",
    "modular_projection_add_no_carry": "说明低分辨率投影与稳定加法在无进位条件下可交换，适合解释跨层关系运算。",
    "stableAdd_comm": "说明稳定加法具交换律，适合解释关系中的互补与对调。",
    "eigenvalue_eq_goldenRatio_or_goldenConj": "把满足 `μ² = μ + 1` 的本征值限制到黄金比及其共轭，适合解释谱边界。",
    "observation_refinement_reduces_error": "说明观测更细时误差不会变大，适合解释察势、观照与信息分辨率。",
    "prefix_resolution_decreases_error": "说明更长前缀带来更小扫描误差，适合解释逐层分辨。",
    "maxFiberMultiplicity_bounds": "给出最大 fiber 多重性的上下界，适合解释哪些稳定卦吸纳能力更强。",
    "maxFiberMultiplicity_eight": "给出窗口 8 上的精确最大 fiber 多重性，适合解释吸纳规模的可计算性。",
}


def slugify(text: str) -> str:
    """Return a filesystem-safe ASCII slug."""
    return (
        text.lower()
        .replace("ü", "u")
        .replace(" ", "-")
        .replace("'", "")
    )


def feature_sentence(item: dict) -> str:
    """Create a short structural reading from binary features."""
    yang_count = item["yang_count"]
    if item["binary"] == "000000":
        return "它是整个 6-bit 卦系里的 zero word，也是唯一完全没有阳位的稳定词。"
    if item["binary"] == "111111":
        return "它是整个 6-bit 卦系里的全阳极值词，也是离 `No11` 稳定域最远的极端配置。"
    if item["gms_valid"] and yang_count == 1:
        return "它只保留一个孤立阳位，因此属于最小非零稳定激活，可视作稀疏启动态。"
    if item["gms_valid"] and yang_count == 2:
        return "它包含两个彼此分离的阳位，因此是典型的低密度稳定词，适合承接稀疏与间隔结构。"
    if item["gms_valid"] and yang_count == 3:
        return "它以三阳达到了 `No11` 允许的最大阳密度，因此是交替或近交替结构中的高密度稳定态。"
    if not item["gms_valid"] and item["max_one_run"] >= 3:
        return "它包含长阳串，因此第一层读法不是 stable word，而是需要经 fold 才能进入稳定域的 raw word。"
    if not item["gms_valid"]:
        return "它虽不是极端全阳，但已出现连续阳段，因此其形式位置是 fold 之前的临界或过载态。"
    return "它位于《易经》位串系统中的一个中间结构位置，适合从分类交叉与 theorem anchor 两侧同时读取。"


def mapping_position(item: dict) -> str:
    """Create the main mapping paragraph."""
    categories = item["category_refs"]
    category_names = "、".join(ref["name_zh"] for ref in categories) if categories else "当前分类之外"
    directions = "、".join(item["omega_directions"]) if item["omega_directions"] else "基础位串结构"
    stable_clause = (
        "该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。"
        if item["gms_valid"]
        else "该卦不在 `X_6` 内，因此其第一层数学位置是 raw 6-bit word，而不是 stable word。"
    )
    return (
        f"在当前的 Omega 文化映射计划里，第 {item['number']} 卦 {item['name_zh']} 首先不是被当作抽象象义，"
        f"而是被当作二元词 `{item['binary']}` 来读取。{stable_clause} "
        f"{feature_sentence(item)} 它目前横跨的主题类别是 {category_names}，"
        f"因此其 strongest reading corridor 集中在 {directions} 这些方向上。"
    )


def load_source_lines(path_str: str) -> list[str]:
    """Load source-text lines without local notes."""
    if not path_str:
        return []
    path = REPO_ROOT / path_str
    if not path.exists():
        return []

    lines = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "--- Notes ---":
            break
        lines.append(line)
    return lines


def source_anchor_lines(path_str: str) -> list[str]:
    """Select compact source anchors for the page."""
    lines = load_source_lines(path_str)
    if not lines:
        return []

    content = []
    heading_pattern = re.compile(r"^.+\s—\s第\d+卦$")
    for line in lines:
        if heading_pattern.match(line):
            continue
        if line == "易經：":
            continue
        if re.fullmatch(r"[乾兌离離震巽坎艮坤无妄需訟訟比剝復夬姤咸恆遯晉明夷家人睽蹇解損益困井革鼎旅渙中孚小過既濟未濟]+下[乾兌离離震巽坎艮坤无妄需訟訟比剝復夬姤咸恆遯晉明夷家人睽蹇解損益困井革鼎旅渙中孚小過既濟未濟]+上", line):
            continue
        content.append(line)

    anchors = []
    before_commentary = []
    for line in content:
        if line in {"彖曰：", "象曰：", "文言曰："}:
            break
        before_commentary.append(line)
    anchors.extend(before_commentary[:4])

    for marker in ("彖曰：", "象曰："):
        if marker in content:
            idx = content.index(marker)
            anchors.append(marker)
            if idx + 1 < len(content):
                anchors.append(content[idx + 1])

    return anchors[:8]


def source_anchor_section(item: dict) -> list[str]:
    """Render source anchors if available."""
    lines = ["## 原文锚点", ""]
    anchors = source_anchor_lines(item.get("source_text_path", ""))
    if not anchors:
        lines.append("- 当前页还没有抽出原文锚点。")
        lines.append("")
        return lines

    for line in anchors:
        lines.append(f"> {line}")
    lines.append("")
    return lines


def source_mapping_comment(item: dict) -> str:
    """Explain how the source anchors connect to the math mapping."""
    theorem_names = [candidate["lean_theorem"] for candidate in item.get("theorem_candidates", [])[:2]]
    theorem_clause = (
        f"在 Lean 锚点上，本页最强地落向 `{theorem_names[0]}` 与 `{theorem_names[1]}`。"
        if len(theorem_names) >= 2
        else f"在 Lean 锚点上，本页目前主要落向 `{theorem_names[0]}`。"
        if theorem_names
        else "在 Lean 锚点上，本页目前仍以类别级对应为主。"
    )
    if item["gms_valid"]:
        domain_clause = (
            "它已经直接落在 `X_6` 内，因此原文在这里首先对应的是一个稳定词的内部差异，"
            "而不是先经过 fold 才能成立的外部修正。"
        )
    else:
        domain_clause = (
            "它不直接落在 `X_6` 内，因此原文在这里首先对应的是 raw word 的极端、临界或过载位置，"
            "数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。"
        )
    return (
        "这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。"
        f"{domain_clause} {theorem_clause}"
    )


def theorem_section(item: dict) -> list[str]:
    """Render a compact theorem-anchor section."""
    lines = ["## Omega 定理锚点", ""]
    candidates = item.get("theorem_candidates", [])[:5]
    if not candidates:
        lines.append("- 当前 registry 尚未为该卦筛出定理候选，需回到上层分类继续补强。")
        lines.append("")
        return lines

    for theorem in candidates:
        statement = theorem.get("lean_statement", "").replace("\n", " ").strip()
        if len(statement) > 160:
            statement = statement[:157] + "..."
        note = THEOREM_NOTES.get(theorem["lean_theorem"], "它为该卦当前的映射走廊提供了可点名的 Lean 形式锚点。")
        lines.append(
            f"- `{theorem['lean_theorem']}` [`{theorem['lean_module']}`]：`{statement}`。{note}"
        )
    lines.append("")
    return lines


def corpus_status(item: dict) -> list[str]:
    """Render source information compactly."""
    lines = ["## 原文来源", ""]
    if item["source_text_path"]:
        lines.append(f"- 本仓库原文文件：`{item['source_text_path']}`")
        lines.append("- 原文来自维基文库《周易》分卦页，经规范化后入库。")
    else:
        lines.append("- 当前仓库还没有该卦的单独原文文件。")
        lines.append("- 当前页面仍只显示结构层和 theorem 层映射。")
    lines.append("")
    return lines


def render_dossier(item: dict) -> str:
    """Render one per-hexagram dossier."""
    category_names = " / ".join(ref["name_zh"] for ref in item["category_refs"]) or "Unassigned"
    description = (
        f"Hexagram {item['number']} {item['name_zh']} as `{item['binary']}`, "
        f"{'GMS-valid' if item['gms_valid'] else 'fold-required'}, categories {category_names}."
    )
    lines = [
        "---",
        f'title: "{item["number"]:02d}. {item["name_zh"]} / {item["pinyin"].title()}"',
        'subtitle: "I Ching Hexagram Page"',
        f"order: {item['number']}",
        f'description: "{description}"',
        "categories: [i-ching, hexagram-dossier, cultural, omega]",
        "---",
        "",
        "## 结构签名",
        "",
        f"- 卦符：{item['symbol']}",
        f"- 二进制：`{item['binary']}`",
        f"- 下卦：{item['lower_trigram']['name_zh']} / {item['lower_trigram']['name_en']} / `{item['lower_trigram']['bits']}`",
        f"- 上卦：{item['upper_trigram']['name_zh']} / {item['upper_trigram']['name_en']} / `{item['upper_trigram']['bits']}`",
        f"- 阳爻数：{item['yang_count']}",
        f"- 连续阳对数：{item['adjacent_one_pairs']}",
        f"- 最长阳串：{item['max_one_run']}",
        f"- GMS 状态：{'valid' if item['gms_valid'] else 'not valid'}",
        f"- 互补卦：第 {item['complement_hexagram']} 卦 / `{item['complement_binary']}`",
        f"- 综卦：第 {item['reverse_hexagram']} 卦 / `{item['reverse_binary']}`",
        f"- 所属类别：{category_names}",
        "",
        "## 映射定位",
        "",
        mapping_position(item),
        "",
        "## 对应说明",
        "",
        source_mapping_comment(item),
        "",
        "## Omega 对象",
        "",
        "- `Word 6 = {0,1}^6`",
        f"- {'`X_6` stable subspace' if item['gms_valid'] else '`Fold : Word 6 → X_6` entry corridor'}",
        f"- 当前主方向：{', '.join(item['omega_directions']) if item['omega_directions'] else '基础位串结构'}",
        "",
    ]
    lines.extend(source_anchor_section(item))
    lines.extend(theorem_section(item))
    lines.extend(corpus_status(item))
    lines.extend(
        [
            "## 小结",
            "",
            "这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与 theorem anchor 放在同一坐标系里，"
            "重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。",
            "",
            "[Back to Hexagram Index](index.qmd) | [Back to I Ching Index](../index.qmd)",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate I Ching hexagram dossiers")
    parser.add_argument(
        "--registry",
        default=str(REPO_ROOT / "workspace" / "易经" / "hexagrams" / "registry.json"),
        help="Path to registry.json",
    )
    parser.add_argument(
        "--output-dir",
        default=str(REPO_ROOT / "workspace" / "易经" / "hexagrams" / "gms-valid"),
        help="Directory for generated dossiers",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate dossiers for all 64 hexagrams instead of only GMS-valid ones",
    )
    args = parser.parse_args()

    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    records = registry["records"]
    if not args.all:
        records = [item for item in records if item["gms_valid"]]

    for item in records:
        filename = f"hexagram-{item['number']:02d}-{slugify(item['pinyin'])}.md"
        (output_dir / filename).write_text(render_dossier(item), encoding="utf-8")

    print(f"Generated {len(records)} dossier(s) in {output_dir}")


if __name__ == "__main__":
    main()
