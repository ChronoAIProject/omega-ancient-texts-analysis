---
title: "32. 恆"
subtitle: "《易经》单卦映射页"
order: 32
description: "第 32 卦 恆，二进制 `011100`，需经 fold 进入稳定域，归属 交感与关系。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷟
- 二进制：`011100`
- 下卦：巽 / `011`
- 上卦：震 / `100`
- 阳爻数：3
- 连续阳对数：1
- 最长阳串：3
- `X_6` 状态：需经 fold 进入稳定域
- 互补卦：第 42 卦 / `100011`
- 综卦：第 31 卦 / `001110`
- 所属类别：交感与关系

## 映射定位

在当前的 Omega 文化映射计划里，第 32 卦 恆 首先不是被当作抽象象义，而是被当作二元词 `011100` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是原始 6-bit 词，而不是稳定词。 它包含长阳串，因此第一层读法不是稳定词，而是需要经 fold 才能进入稳定域的原始词。 它目前横跨的主题类别是 交感与关系，因此其最强对应主要集中在 ring-arithmetic、spectral-theory、fold-operator 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它不直接落在 `X_6` 内，因此原文在这里首先对应的是原始词的极端、临界或过载位置，数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。 在 Lean 锚点上，本页最强地落向 `stableValue_ring_isomorphism` 与 `modular_projection_add_no_carry`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` 进入稳定域的通道
- 当前主方向：ring-arithmetic、spectral-theory、fold-operator

## 原文锚点

> 恆：亨，无咎。利貞，利有攸往。
> 初六：浚恆，貞凶，无攸利。
> 九二：悔亡。
> 九三：不恆其德，或承之羞，貞吝。
> 彖曰：
> 恆，久也。剛上而柔下，雷風相與，巽而動，剛柔皆應，恆。恆亨无咎，利貞；久于其道也，天地之道，恆久而不已也。利有攸往，終則有始也。日月得天，而能久照，四時變化，而能久成，聖人久于其道，而天下化成；觀其所恆，而天地萬物之情可見矣！
> 象曰：
> 雷風，恆；君子以立不易方。

## Omega 定理锚点

- `stableValue_ring_isomorphism` [`Omega.Frontier.ConditionalArithmetic`]：`theorem stableValue_ring_isomorphism (m : Nat) :     (∀ x y : X m, stableValue (X.stableAdd x y) =       (stableValue x + stableValue y) % Nat.fib (m + 2)) ∧...`。把稳定态关系写成模 Fibonacci 环上的封闭运算，适合解释损/益和互补调节。
- `modular_projection_add_no_carry` [`Omega.Frontier.ConditionalArithmetic`]：`theorem modular_projection_add_no_carry (x y : X (m + 1))     (h : stableValue x + stableValue y < Nat.fib (m + 3)) :     X.modularProject (X.stableAdd x y) ...`。说明低分辨率投影与稳定加法在无进位条件下可交换，适合解释跨层关系运算。
- `stableAdd_comm` [`Omega.Folding.FiberArithmetic`]：`theorem stableAdd_comm (x y : X m) :     stableAdd x y = stableAdd y x`。说明稳定加法具交换律，适合解释关系中的互补与对调。
- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [`Omega.Graph.TransferMatrix`]：`theorem goldenMeanAdjacency_has_goldenRatio_eigenvector :     ∃ v : Fin 2 → ℝ, v ≠ 0 ∧       Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio...`。把主导增长方向写成黄金比本征向量，适合解释主模态与稳定节律。
- `eigenvalue_eq_goldenRatio_or_goldenConj` [`Omega.Graph.TransferMatrix`]：`theorem eigenvalue_eq_goldenRatio_or_goldenConj     {μ : ℝ} (hμ : μ ^ 2 = μ + 1) :     μ = Real.goldenRatio ∨ μ = Real.goldenConj`。把满足 `μ² = μ + 1` 的本征值限制到黄金比及其共轭，适合解释谱边界。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_32_heng.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
