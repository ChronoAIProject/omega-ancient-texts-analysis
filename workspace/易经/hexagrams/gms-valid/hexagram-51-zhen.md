---
title: "51. 震"
subtitle: "《易经》单卦映射页"
order: 51
description: "第 51 卦 震，二进制 `100100`，已在 `X_6` 稳定域内，归属 渐进与发展。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷲
- 二进制：`100100`
- 下卦：震 / `100`
- 上卦：震 / `100`
- 阳爻数：2
- 连续阳对数：0
- 最长阳串：1
- `X_6` 状态：已在稳定域内
- 互补卦：第 57 卦 / `011011`
- 综卦：第 52 卦 / `001001`
- 所属类别：渐进与发展

## 映射定位

在当前的 Omega 文化映射计划里，第 51 卦 震 首先不是被当作抽象象义，而是被当作二元词 `100100` 来读取。该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。 它包含两个彼此分离的阳位，因此是典型的低密度稳定词，适合承接稀疏与间隔结构。 它目前横跨的主题类别是 渐进与发展，因此其最强对应主要集中在 modular-tower-inverse-limit、fibonacci-growth、golden-mean-shift 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它已经直接落在 `X_6` 内，因此原文在这里首先对应的是一个稳定词的内部差异，而不是先经过 fold 才能成立的外部修正。 在 Lean 锚点上，本页最强地落向 `inverse_limit_extensionality` 与 `inverse_limit_bijective`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `X_6` 稳定子空间
- 当前主方向：modular-tower-inverse-limit、fibonacci-growth、golden-mean-shift

## 原文锚点

> 震：亨。震來虩虩，笑言啞啞。震驚百里，不喪匕鬯。
> 初九：震來虩虩，后笑言啞啞，吉。
> 六二：震來厲，億喪貝，躋于九陵，勿逐，七日得。
> 六三：震蘇蘇，震行无眚。
> 彖曰：
> 震，亨。震來虩虩，恐致福也。笑言啞啞，后有則也。震驚百里，驚遠而懼邇也。出可以守宗廟社稷，以為祭主也。
> 象曰：
> 洊雷，震；君子以恐懼修省。

## Omega 定理锚点

- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) :     a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明整体是否相同完全由全部前缀是否相同决定，适合解释层级兼容。
- `inverse_limit_bijective` [`Omega.Frontier.ConditionalSummary`]：`theorem inverse_limit_bijective :     Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)`。说明 compatible family 与逆极限对象之间是双射，适合解释整体由有限层闭合产生。
- `inverse_limit_left` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_left (F : X.CompatibleFamily) :     X.toFamily (X.ofFamily F) = F`。它为该卦当前的映射走廊提供了可点名的 Lean 形式锚点。
- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_51_zhen.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
