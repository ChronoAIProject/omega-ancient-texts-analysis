#!/usr/bin/env python3
"""Generate per-hexagram structural dossiers for the I Ching."""

from __future__ import annotations

import argparse
import json
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
    """Render text-source status honestly."""
    lines = ["## 语料状态", ""]
    if item["source_text_path"]:
        lines.append(f"- 已有本地原文文件：`{item['source_text_path']}`")
        lines.append("- 这一页可以继续往完整逐卦长文扩展，不需要再补基础元数据。")
    else:
        lines.append("- 当前本地语料库还没有该卦的单独原文文件。")
        lines.append("- 本页因此暂时采取“结构 dossier”写法：先锁定 binary / theorem / category 位置，再等待原文补齐后扩写。")
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
        'subtitle: "I Ching Hexagram Dossier"',
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
        "## Omega 对象",
        "",
        "- `Word 6 = {0,1}^6`",
        f"- {'`X_6` stable subspace' if item['gms_valid'] else '`Fold : Word 6 → X_6` entry corridor'}",
        f"- 当前主方向：{', '.join(item['omega_directions']) if item['omega_directions'] else '基础位串结构'}",
        "",
    ]
    lines.extend(theorem_section(item))
    lines.extend(corpus_status(item))
    lines.extend(
        [
            "## 小结",
            "",
            "这一页不是终稿长文，而是逐卦展开的正式底稿：它先把卦位、位串、分类交叉和 theorem anchor 锁死，"
            "之后再叠加原文细读与更细的传统注疏材料。",
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
