---
title: "23. 剝"
subtitle: "《易经》单卦映射页"
order: 23
description: "第 23 卦 剝，二进制 `000001`，已在 `X_6` 稳定域内，归属 动态变易与循环。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷖
- 二进制：`000001`
- 下卦：坤 / `000`
- 上卦：艮 / `001`
- 阳爻数：1
- 连续阳对数：0
- 最长阳串：1
- `X_6` 状态：已在稳定域内
- 互补卦：第 43 卦 / `111110`
- 综卦：第 24 卦 / `100000`
- 所属类别：动态变易与循环

## 映射定位

在当前的 Omega 文化映射计划里，第 23 卦 剝 首先不是被当作抽象象义，而是被当作二元词 `000001` 来读取。该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。 它只保留一个孤立阳位，因此属于最小非零稳定激活，可视作稀疏启动态。 它目前横跨的主题类别是 动态变易与循环，因此其最强对应主要集中在 dynamical-systems、golden-mean-shift、fold-operator 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它已经直接落在 `X_6` 内，因此原文在这里首先对应的是一个稳定词的内部差异，而不是先经过 fold 才能成立的外部修正。 在 Lean 锚点上，本页最强地落向 `topological_entropy_eq_log_phi` 与 `goldenMeanAdjacency_has_goldenRatio_eigenvector`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `X_6` 稳定子空间
- 当前主方向：dynamical-systems、golden-mean-shift、fold-operator

## 原文锚点

> 剝：不利。有攸往。
> 初六：剝牀以足，蔑貞凶。
> 六二：剝牀以辨，蔑貞凶。
> 六三：剝之，无咎。
> 彖曰：
> 剝，剝也，柔變剛也。不利有攸往，小人長也。順而止之，觀象也。君子尚消息盈虛，天行也。
> 象曰：
> 山附地上，剝；上以厚下，安宅。

## Omega 定理锚点

- `topological_entropy_eq_log_phi` [`Omega.Folding.Entropy`]：`theorem topological_entropy_eq_log_phi :     Tendsto (fun n => Real.log (Nat.fib (n + 2) : ℝ) / (n : ℝ)) atTop (𝓝 (Real.log φ))`。把复杂度增长率压成 `log φ`，适合解释变易与循环的受控熵结构。
- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [`Omega.Graph.TransferMatrix`]：`theorem goldenMeanAdjacency_has_goldenRatio_eigenvector :     ∃ v : Fin 2 → ℝ, v ≠ 0 ∧       Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio...`。把主导增长方向写成黄金比本征向量，适合解释主模态与稳定节律。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_23_bo.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
