---
title: "05. 需"
subtitle: "《易经》单卦映射页"
order: 5
description: "第 5 卦 需，二进制 `111010`，需经 fold 进入稳定域，归属 困阻与险难。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷄
- 二进制：`111010`
- 下卦：乾 / `111`
- 上卦：坎 / `010`
- 阳爻数：4
- 连续阳对数：1
- 最长阳串：3
- `X_6` 状态：需经 fold 进入稳定域
- 互补卦：第 35 卦 / `000101`
- 综卦：第 6 卦 / `010111`
- 所属类别：困阻与险难

## 映射定位

在当前的 Omega 文化映射计划里，第 5 卦 需 首先不是被当作抽象象义，而是被当作二元词 `111010` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是原始 6-bit 词，而不是稳定词。 它包含长阳串，因此第一层读法不是稳定词，而是需要经 fold 才能进入稳定域的原始词。 它目前横跨的主题类别是 困阻与险难，因此其最强对应主要集中在 golden-mean-shift、fold-operator、fiber-structure 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它不直接落在 `X_6` 内，因此原文在这里首先对应的是原始词的极端、临界或过载位置，数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。 在 Lean 锚点上，本页最强地落向 `fibonacci_cardinality` 与 `fibonacci_cardinality_recurrence`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` 进入稳定域的通道
- 当前主方向：golden-mean-shift、fold-operator、fiber-structure

## 原文锚点

> 需：有孚，光亨。貞吉，利涉大川。
> 初九：需于郊，利用恆，无咎。
> 九二：需于沙，小有言，終吉。
> 九三：需于泥，致寇至。
> 彖曰：
> 需，須也，險在前也；剛健而不陷，其義不困窮矣。需，有孚，光亨，貞吉，位乎天位，以正中也。利涉大川，往有功也。
> 象曰：
> 雲上於天，需；君子以飲食宴樂。

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 一旦把原始词折回稳定域，再施一次不会继续改写。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的卦象在 fold 下保持不动，适合区分 stable word 与 raw word。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_05_xu.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
