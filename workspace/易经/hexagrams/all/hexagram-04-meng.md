---
title: "04. 蒙 / Meng"
subtitle: "I Ching Hexagram Dossier"
order: 4
description: "Hexagram 4 蒙 as `010001`, GMS-valid, categories 动态变易与循环 / 明照与分辨."
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷃
- 二进制：`010001`
- 下卦：坎 / Water / `010`
- 上卦：艮 / Mountain / `001`
- 阳爻数：2
- 连续阳对数：0
- 最长阳串：1
- GMS 状态：valid
- 互补卦：第 49 卦 / `101110`
- 综卦：第 3 卦 / `100010`
- 所属类别：动态变易与循环 / 明照与分辨

## 映射定位

在当前的 Omega 文化映射计划里，第 4 卦 蒙 首先不是被当作抽象象义，而是被当作二元词 `010001` 来读取。该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。 它包含两个彼此分离的阳位，因此是典型的低密度稳定词，适合承接稀疏与间隔结构。 它目前横跨的主题类别是 动态变易与循环、明照与分辨，因此其 strongest reading corridor 集中在 dynamical-systems、golden-mean-shift、fold-operator、spectral-theory、modular-tower-inverse-limit、rate-distortion-information-theory 这些方向上。

## Omega 对象

- `Word 6 = {0,1}^6`
- `X_6` stable subspace
- 当前主方向：dynamical-systems, golden-mean-shift, fold-operator, spectral-theory, modular-tower-inverse-limit, rate-distortion-information-theory

## Omega 定理锚点

- `topological_entropy_eq_log_phi` [`Omega.Folding.Entropy`]：`theorem topological_entropy_eq_log_phi :     Tendsto (fun n => Real.log (Nat.fib (n + 2) : ℝ) / (n : ℝ)) atTop (𝓝 (Real.log φ))`。把复杂度增长率压成 `log φ`，适合解释变易与循环的受控熵结构。
- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [`Omega.Graph.TransferMatrix`]：`theorem goldenMeanAdjacency_has_goldenRatio_eigenvector :     ∃ v : Fin 2 → ℝ, v ≠ 0 ∧       Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio...`。把主导增长方向写成黄金比本征向量，适合解释主模态与稳定节律。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。

## 语料状态

- 当前本地语料库还没有该卦的单独原文文件。
- 本页因此暂时采取“结构 dossier”写法：先锁定 binary / theorem / category 位置，再等待原文补齐后扩写。

## 小结

这一页不是终稿长文，而是逐卦展开的正式底稿：它先把卦位、位串、分类交叉和 theorem anchor 锁死，之后再叠加原文细读与更细的传统注疏材料。
