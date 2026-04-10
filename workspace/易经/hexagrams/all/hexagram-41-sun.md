---
title: "41. 損 / Sun"
subtitle: "I Ching Hexagram Dossier"
order: 41
description: "Hexagram 41 損 as `110001`, fold-required, categories 交感与关系 / 节制与平衡."
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷨
- 二进制：`110001`
- 下卦：兌 / Lake / `110`
- 上卦：艮 / Mountain / `001`
- 阳爻数：3
- 连续阳对数：1
- 最长阳串：2
- GMS 状态：not valid
- 互补卦：第 31 卦 / `001110`
- 综卦：第 42 卦 / `100011`
- 所属类别：交感与关系 / 节制与平衡

## 映射定位

在当前的 Omega 文化映射计划里，第 41 卦 損 首先不是被当作抽象象义，而是被当作二元词 `110001` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是 raw 6-bit word，而不是 stable word。 它虽不是极端全阳，但已出现连续阳段，因此其形式位置是 fold 之前的临界或过载态。 它目前横跨的主题类别是 交感与关系、节制与平衡，因此其 strongest reading corridor 集中在 ring-arithmetic、spectral-theory、fold-operator、zeckendorf-representation、golden-mean-shift 这些方向上。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` entry corridor
- 当前主方向：ring-arithmetic, spectral-theory, fold-operator, zeckendorf-representation, golden-mean-shift

## Omega 定理锚点

- `stableValue_ring_isomorphism` [`Omega.Frontier.ConditionalArithmetic`]：`theorem stableValue_ring_isomorphism (m : Nat) :     (∀ x y : X m, stableValue (X.stableAdd x y) =       (stableValue x + stableValue y) % Nat.fib (m + 2)) ∧...`。把稳定态关系写成模 Fibonacci 环上的封闭运算，适合解释损/益和互补调节。
- `modular_projection_add_no_carry` [`Omega.Frontier.ConditionalArithmetic`]：`theorem modular_projection_add_no_carry (x y : X (m + 1))     (h : stableValue x + stableValue y < Nat.fib (m + 3)) :     X.modularProject (X.stableAdd x y) ...`。说明低分辨率投影与稳定加法在无进位条件下可交换，适合解释跨层关系运算。
- `stableAdd_comm` [`Omega.Folding.FiberArithmetic`]：`theorem stableAdd_comm (x y : X m) :     stableAdd x y = stableAdd y x`。说明稳定加法具交换律，适合解释关系中的互补与对调。
- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [`Omega.Graph.TransferMatrix`]：`theorem goldenMeanAdjacency_has_goldenRatio_eigenvector :     ∃ v : Fin 2 → ℝ, v ≠ 0 ∧       Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio...`。把主导增长方向写成黄金比本征向量，适合解释主模态与稳定节律。
- `eigenvalue_eq_goldenRatio_or_goldenConj` [`Omega.Graph.TransferMatrix`]：`theorem eigenvalue_eq_goldenRatio_or_goldenConj     {μ : ℝ} (hμ : μ ^ 2 = μ + 1) :     μ = Real.goldenRatio ∨ μ = Real.goldenConj`。把满足 `μ² = μ + 1` 的本征值限制到黄金比及其共轭，适合解释谱边界。

## 语料状态

- 当前本地语料库还没有该卦的单独原文文件。
- 本页因此暂时采取“结构 dossier”写法：先锁定 binary / theorem / category 位置，再等待原文补齐后扩写。

## 小结

这一页不是终稿长文，而是逐卦展开的正式底稿：它先把卦位、位串、分类交叉和 theorem anchor 锁死，之后再叠加原文细读与更细的传统注疏材料。
