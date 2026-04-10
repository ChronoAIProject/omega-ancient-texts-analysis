#!/usr/bin/env python3
"""Inject concise theorem-anchor sections into generated cultural essays."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from analysis.theorem_profiles import DIRECTION_PROFILES

SECTION_TITLE = "## Omega 定理锚点"

THEOREM_NOTES = {
    "fibonacci_cardinality": "把稳定词空间的计数严格写成 `|X_m| = F_{m+2}`，是本文讨论卦系受约束增长的基础等式。",
    "fibonacci_cardinality_recurrence": "把允许状态的增长写成前两级之和，支撑“由少数初始状态递归展开”的读法。",
    "goldenMean_characteristic_recurrence": "从 golden-mean transfer structure 再次得到同一递推，说明 Fibonacci 增长来自系统本身的本征结构。",
    "goldenMeanAdjacency_has_goldenRatio_eigenvector": "说明 golden-mean adjacency 具有黄金比本征向量，支撑本文把主导增长率与稳定结构联系起来。",
    "topological_entropy_eq_log_phi": "把系统复杂度增长率写成 `log φ`，支撑本文关于变易具有受控节律而非任意散乱的判断。",
    "fold_is_idempotent": "说明 fold 一旦把词折回稳定域，再施加一次不会继续改写，因此可把稳定态看成真正的吸引结果。",
    "fold_fixes_stable": "说明已经稳定的卦象在 fold 下保持不变，区分“被折回的过强态”与“本身稳定态”。",
    "fold_is_surjective": "说明每个稳定态都能作为某个原始词的折回结果，因此稳定卦象可被视作一个 fiber 的代表点。",
    "inverse_limit_extensionality": "说明无限对象是否相同，完全由全部有限前缀是否一致决定，支撑本文的层级拼接与兼容家族读法。",
    "inverse_limit_bijective": "把兼容家族与逆极限对象之间的双射写清，支撑“整体由有限层逼近并唯一确定”的判断。",
    "inverse_limit_left": "说明由 compatible family 回到对象再取 family 不会丢失信息，支撑多层分辨率的回返一致性。",
    "inverse_limit_right": "说明逆极限对象与其有限前缀家族之间可往返识别，支撑“整体不是另加对象，而是前缀系统的闭合”。",
    "zeckendorf_uniqueness": "说明非相邻 Fibonacci 指标分解是唯一的，支撑本文关于稀疏稳定布局具有唯一性的判断。",
    "zeckendorf_injective": "说明不同稳定词会给出不同 Zeckendorf 指标集，强化了稀疏结构的可辨识性。",
    "stableValue_ring_isomorphism": "把稳定态上的加法与乘法对应到模 Fibonacci 数环，是本文把关系和平衡写成封闭运算的核心锚点。",
    "modular_projection_add_no_carry": "说明在无进位条件下，投影与稳定加法可交换，支撑跨分辨率的关系运算读法。",
    "stableAdd_comm": "说明稳定加法满足交换律，使损/益这类互补调节可被视作同一封闭运算中的位置变化。",
    "eigenvalue_eq_goldenRatio_or_goldenConj": "说明满足 `μ² = μ + 1` 的本征值只能落在黄金比与其共轭上，给出谱结构的硬边界。",
    "characteristic_polynomial_witness": "把递推与谱约束压回特征多项式层面，支撑本文把主导模式写成可验证对象。",
    "observation_refinement_reduces_error": "说明观测更细时误差不会变大，支撑本文把分辨、静观、察势写成信息分辨率问题。",
    "prefix_resolution_decreases_error": "说明更长前缀提供更小扫描误差，支撑本文关于分辨率层级的论述。",
    "scanError_hasCertificate": "说明误差界不是口头直觉，而是有证书可验证的界。",
    "prefixScanError_hasCertificate": "说明前缀分辨率下的误差界同样可被证书化验证。",
    "kappa_ge_of_eps_ge": "把误差阈值与可允许偏差之间的单调关系写成明确不等式，是本文讨论信息流通边界时的形式支点。",
    "eps_lt_of_kappa_lt": "从阈值条件反推可接受误差上界，支撑本文关于压缩与失真边界的判断。",
    "maxFiberMultiplicity_bounds": "给出最大 fiber 多重性的上下界，支撑本文把某些稳定卦象写成更强吸引子的判断。",
    "maxFiberMultiplicity_eight": "给出 8 级窗口上最大 fiber 多重性的精确值，适合说明高吸纳稳定态并非修辞而是可计算事实。",
    "maxFiberMultiplicity_nine": "给出 9 级窗口上最大 fiber 多重性的精确值，支撑 fiber 结构随分辨率扩展的讨论。",
    "maxFiberMultiplicity_ten": "给出 10 级窗口上最大 fiber 多重性的精确值，说明高吸纳结构可继续延伸到更高分辨率。",
    "maxFiberMultiplicity_fibonacci_bound": "说明最大 fiber 多重性本身也受 Fibonacci 型递推控制，支撑本文把吸引强度写成递归增长。",
}

DIRECTION_NOTES = {
    "golden-mean-shift": "它给出 `No11` 稳定域的正式约束，是本文把卦象稳定性写成二元结构条件的基础。",
    "fibonacci-growth": "它把允许状态的增长写成明确递推，支撑本文关于创生、扩展与层级增殖的判断。",
    "zeckendorf-representation": "它把稀疏稳定布局写成唯一分解，支撑本文关于节制、稀疏、非相邻配置的判断。",
    "fold-operator": "它说明非稳定态如何被折回稳定域，是本文关于过强态归于平衡的核心形式结构。",
    "ring-arithmetic": "它把稳定态之间的关系写成封闭运算，而不是停留在抽象比喻层。",
    "spectral-theory": "它把关系网络中的主导模式写成可验证的谱结构，支撑本文关于交感、照明与主模态的论述。",
    "modular-tower-inverse-limit": "它说明整体如何由各级有限前缀兼容生成，支撑本文的层级拼接与分辨率读法。",
    "dynamical-systems": "它把周期、增长率与轨道行为形式化，支撑本文关于变易和循环的判断。",
    "rate-distortion-information-theory": "它把分辨率、误差与证书界联系起来，支撑本文关于观察、限度与流通的分析。",
    "fiber-structure": "它量化稳定态能吸纳多少前像，支撑本文关于 attractor 与多重性层级的判断。",
}


def build_anchor_section(category: dict) -> str:
    """Render a concise theorem-anchor section from grouped theorem mappings."""
    bullets = []
    seen = set()
    for group in category.get("direction_groups", []):
        theorem = None
        for candidate in group.get("candidates", []):
            theorem_name = candidate["lean_theorem"]
            if theorem_name not in seen:
                theorem = candidate
                seen.add(theorem_name)
                break

        if theorem is None:
            continue
        theorem_name = theorem["lean_theorem"]
        module_name = theorem["lean_module"]
        note = THEOREM_NOTES.get(theorem_name, DIRECTION_NOTES.get(group["direction"], "它为本文对应的 Omega 结构提供了形式锚点。"))
        statement = theorem.get("lean_statement", "").replace("\n", " ").strip()
        statement = re.sub(r"\s+", " ", statement)
        if len(statement) > 160:
            statement = statement[:157] + "..."
        bullets.append(
            f"- `{theorem_name}` [`{module_name}`]：`{statement}`。{note}"
        )

    lines = [SECTION_TITLE, ""]
    lines.extend(bullets)
    lines.append("")
    lines.append("这些定理不替代文本解释，但它们把本文最核心的对应从“方向级相似”推进到了“可点名的 Lean 形式结果”。")
    lines.append("")
    return "\n".join(lines)


def replace_or_insert_anchor_section(article_text: str, anchor_section: str) -> str:
    """Replace an existing anchor section or insert one before the conclusion."""
    pattern = re.compile(r"^## Omega 定理锚点\s*\n.*?(?=^## )", re.MULTILINE | re.DOTALL)
    if pattern.search(article_text):
        return pattern.sub(anchor_section + "\n", article_text, count=1)

    if "\n## 结论\n" in article_text:
        return article_text.replace("\n## 结论\n", "\n" + anchor_section + "\n## 结论\n", 1)
    if "\n## 参考与说明\n" in article_text:
        return article_text.replace("\n## 参考与说明\n", "\n" + anchor_section + "\n## 参考与说明\n", 1)
    return article_text.rstrip() + "\n\n" + anchor_section + "\n"


def main():
    parser = argparse.ArgumentParser(description="Inject theorem anchors into generated essays")
    parser.add_argument("--work", default="易经", help="Work name under workspace/")
    parser.add_argument(
        "--theorem-map",
        help="Optional explicit path to omega_theorem_map.json",
    )
    args = parser.parse_args()

    work_dir = REPO_ROOT / "workspace" / args.work
    theorem_map_path = Path(args.theorem_map) if args.theorem_map else work_dir / "omega_theorem_map.json"
    generated_dir = work_dir / "generated"

    theorem_map = json.loads(theorem_map_path.read_text(encoding="utf-8"))
    category_by_id = {item["id"]: item for item in theorem_map.get("category_mappings", [])}

    updated = 0
    for article_path in sorted(generated_dir.glob("category_*.md")):
        match = re.search(r"category_(\d+)_", article_path.name)
        if not match:
            continue
        category_id = int(match.group(1))
        category = category_by_id.get(category_id)
        if not category:
            continue

        original = article_path.read_text(encoding="utf-8")
        updated_text = replace_or_insert_anchor_section(original, build_anchor_section(category))
        if updated_text != original:
            article_path.write_text(updated_text, encoding="utf-8")
            updated += 1

    print(f"Updated {updated} article(s) in {generated_dir}")


if __name__ == "__main__":
    main()
