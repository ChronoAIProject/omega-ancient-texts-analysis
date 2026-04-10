---
title: "47. 困"
subtitle: "《易经》单卦映射页"
order: 47
description: "第 47 卦 困，二进制 `010110`，需经 fold 进入稳定域，归属 困阻与险难 / 明照与分辨 / 聚散与流通。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷮
- 二进制：`010110`
- 下卦：坎 / `010`
- 上卦：兌 / `110`
- 阳爻数：3
- 连续阳对数：1
- 最长阳串：2
- `X_6` 状态：需经 fold 进入稳定域
- 互补卦：第 22 卦 / `101001`
- 综卦：第 48 卦 / `011010`
- 所属类别：困阻与险难 / 明照与分辨 / 聚散与流通

## 映射定位

在当前的 Omega 文化映射计划里，第 47 卦 困 首先不是被当作抽象象义，而是被当作二元词 `010110` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是原始 6-bit 词，而不是稳定词。 它虽不是极端全阳，但已出现连续阳段，因此其形式位置是 fold 之前的临界或过载态。 它目前横跨的主题类别是 困阻与险难、明照与分辨、聚散与流通，因此其最强对应主要集中在 golden-mean-shift、fold-operator、fiber-structure、spectral-theory、modular-tower-inverse-limit、rate-distortion-information-theory 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它不直接落在 `X_6` 内，因此原文在这里首先对应的是原始词的极端、临界或过载位置，数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。 在 Lean 锚点上，本页最强地落向 `fibonacci_cardinality` 与 `fibonacci_cardinality_recurrence`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` 进入稳定域的通道
- 当前主方向：golden-mean-shift、fold-operator、fiber-structure、spectral-theory、modular-tower-inverse-limit、rate-distortion-information-theory

## 原文锚点

> alt=䷮ 坎下兌上
> 困：亨，貞大人吉，无咎，有言不信。
> 初六：臀困于株木，入于幽谷，三歲不覿。
> 九二：困于酒食，朱紱方來，利用亨祀，征凶，无咎。
> 彖曰：
> 困，剛掩也。險以說，困而不失其所，亨；其唯君子乎？ 貞大人吉，以剛中也。有言不信，尚口乃窮也。
> 象曰：
> 澤无水，困；君子以致命遂志。

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 一旦把原始词折回稳定域，再施一次不会继续改写。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的卦象在 fold 下保持不动，适合区分 stable word 与 raw word。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_47_kun.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
