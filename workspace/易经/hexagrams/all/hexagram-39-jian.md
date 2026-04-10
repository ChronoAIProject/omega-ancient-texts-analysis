---
title: "39. 蹇"
subtitle: "《易经》单卦映射页"
order: 39
description: "第 39 卦 蹇，二进制 `001010`，已在 `X_6` 稳定域内，归属 困阻与险难。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷦
- 二进制：`001010`
- 下卦：艮 / `001`
- 上卦：坎 / `010`
- 阳爻数：2
- 连续阳对数：0
- 最长阳串：1
- `X_6` 状态：已在稳定域内
- 互补卦：第 38 卦 / `110101`
- 综卦：第 40 卦 / `010100`
- 所属类别：困阻与险难

## 映射定位

在当前的 Omega 文化映射计划里，第 39 卦 蹇 首先不是被当作抽象象义，而是被当作二元词 `001010` 来读取。该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。 它包含两个彼此分离的阳位，因此是典型的低密度稳定词，适合承接稀疏与间隔结构。 它目前横跨的主题类别是 困阻与险难，因此其最强对应主要集中在 golden-mean-shift、fold-operator、fiber-structure 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它已经直接落在 `X_6` 内，因此原文在这里首先对应的是一个稳定词的内部差异，而不是先经过 fold 才能成立的外部修正。 在 Lean 锚点上，本页最强地落向 `fibonacci_cardinality` 与 `fibonacci_cardinality_recurrence`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `X_6` 稳定子空间
- 当前主方向：golden-mean-shift、fold-operator、fiber-structure

## 原文锚点

> 蹇：利西南，不利東北；利見大人，貞吉。
> 初六：往蹇，來譽。
> 六二：王臣蹇蹇，匪躬之故。
> 九三：往蹇來反。
> 彖曰：
> 蹇，難也，險在前也。見險而能止，知矣哉！蹇利西南，往得中也；不利東北，其道窮也。利見大人，往有功也。當位貞吉，以正邦也。蹇之時用大矣哉！
> 象曰：
> 山上有水，蹇；君子以反身修德。

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 一旦把原始词折回稳定域，再施一次不会继续改写。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的卦象在 fold 下保持不动，适合区分 stable word 与 raw word。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_39_jian.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
