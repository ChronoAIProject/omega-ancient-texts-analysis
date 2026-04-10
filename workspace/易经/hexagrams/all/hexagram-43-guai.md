---
title: "43. 夬"
subtitle: "《易经》单卦映射页"
order: 43
description: "第 43 卦 夬，二进制 `111110`，需经 fold 进入稳定域，归属 动态变易与循环 / 刚健与突破。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷪
- 二进制：`111110`
- 下卦：乾 / `111`
- 上卦：兌 / `110`
- 阳爻数：5
- 连续阳对数：2
- 最长阳串：5
- `X_6` 状态：需经 fold 进入稳定域
- 互补卦：第 23 卦 / `000001`
- 综卦：第 44 卦 / `011111`
- 所属类别：动态变易与循环 / 刚健与突破

## 映射定位

在当前的 Omega 文化映射计划里，第 43 卦 夬 首先不是被当作抽象象义，而是被当作二元词 `111110` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是原始 6-bit 词，而不是稳定词。 它包含长阳串，因此第一层读法不是稳定词，而是需要经 fold 才能进入稳定域的原始词。 它目前横跨的主题类别是 动态变易与循环、刚健与突破，因此其最强对应主要集中在 dynamical-systems、golden-mean-shift、fold-operator、fiber-structure 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它不直接落在 `X_6` 内，因此原文在这里首先对应的是原始词的极端、临界或过载位置，数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。 在 Lean 锚点上，本页最强地落向 `topological_entropy_eq_log_phi` 与 `goldenMeanAdjacency_has_goldenRatio_eigenvector`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` 进入稳定域的通道
- 当前主方向：dynamical-systems、golden-mean-shift、fold-operator、fiber-structure

## 原文锚点

> 夬：揚于王庭，孚號，有厲，告自邑，不利即戎，利有攸往。
> 初九：壯于前趾，往不勝為咎。
> 九二：惕號，莫夜有戎，勿恤。
> 九三：壯于頄，有凶。君子夬夬，獨行遇雨，若濡有慍，无咎。
> 彖曰：
> 夬，決也，剛決柔也。健而說，決而和，揚于王庭，柔乘五剛也。孚號有厲，其危乃光也。告自邑，不利即戎，所尚乃窮也。利有攸往，剛長乃終也。
> 象曰：
> 澤上于天，夬；君子以施祿及下，居德則忌。

## Omega 定理锚点

- `topological_entropy_eq_log_phi` [`Omega.Folding.Entropy`]：`theorem topological_entropy_eq_log_phi :     Tendsto (fun n => Real.log (Nat.fib (n + 2) : ℝ) / (n : ℝ)) atTop (𝓝 (Real.log φ))`。把复杂度增长率压成 `log φ`，适合解释变易与循环的受控熵结构。
- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [`Omega.Graph.TransferMatrix`]：`theorem goldenMeanAdjacency_has_goldenRatio_eigenvector :     ∃ v : Fin 2 → ℝ, v ≠ 0 ∧       Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio...`。把主导增长方向写成黄金比本征向量，适合解释主模态与稳定节律。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_43_guai.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
