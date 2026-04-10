---
title: "57. 巽"
subtitle: "《易经》单卦映射页"
order: 57
description: "第 57 卦 巽，二进制 `011011`，需经 fold 进入稳定域，归属 渐进与发展 / 聚散与流通。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷸
- 二进制：`011011`
- 下卦：巽 / `011`
- 上卦：巽 / `011`
- 阳爻数：4
- 连续阳对数：2
- 最长阳串：2
- `X_6` 状态：需经 fold 进入稳定域
- 互补卦：第 51 卦 / `100100`
- 综卦：第 58 卦 / `110110`
- 所属类别：渐进与发展 / 聚散与流通

## 映射定位

在当前的 Omega 文化映射计划里，第 57 卦 巽 首先不是被当作抽象象义，而是被当作二元词 `011011` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是原始 6-bit 词，而不是稳定词。 它虽不是极端全阳，但已出现连续阳段，因此其形式位置是 fold 之前的临界或过载态。 它目前横跨的主题类别是 渐进与发展、聚散与流通，因此其最强对应主要集中在 modular-tower-inverse-limit、fibonacci-growth、golden-mean-shift、rate-distortion-information-theory、fold-operator 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它不直接落在 `X_6` 内，因此原文在这里首先对应的是原始词的极端、临界或过载位置，数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。 在 Lean 锚点上，本页最强地落向 `inverse_limit_extensionality` 与 `inverse_limit_bijective`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` 进入稳定域的通道
- 当前主方向：modular-tower-inverse-limit、fibonacci-growth、golden-mean-shift、rate-distortion-information-theory、fold-operator

## 原文锚点

> 巽：小亨。利有攸往。利見大人。
> 初六：進退，利武人之貞。
> 九二：巽在牀下，用史巫紛若，吉无咎。
> 九三：頻巽，吝。
> 彖曰：
> 重巽以申命，剛巽乎中正而志行。柔皆順乎剛，是以小亨，利有攸往，利見大人。
> 象曰：
> 隨風，巽；君子以申命行事。

## Omega 定理锚点

- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) :     a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明整体是否相同完全由全部前缀是否相同决定，适合解释层级兼容。
- `inverse_limit_bijective` [`Omega.Frontier.ConditionalSummary`]：`theorem inverse_limit_bijective :     Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)`。说明 compatible family 与逆极限对象之间是双射，适合解释整体由有限层闭合产生。
- `inverse_limit_left` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_left (F : X.CompatibleFamily) :     X.toFamily (X.ofFamily F) = F`。它为该卦当前的映射走廊提供了可点名的 Lean 形式锚点。
- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_57_xun.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
