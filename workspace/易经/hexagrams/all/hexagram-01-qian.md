---
title: "01. 乾"
subtitle: "《易经》单卦映射页"
order: 1
description: "第 1 卦 乾，二进制 `111111`，需经 fold 进入稳定域，归属 创生与纯态。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷀
- 二进制：`111111`
- 下卦：乾 / `111`
- 上卦：乾 / `111`
- 阳爻数：6
- 连续阳对数：3
- 最长阳串：6
- `X_6` 状态：需经 fold 进入稳定域
- 互补卦：第 2 卦 / `000000`
- 综卦：第 1 卦 / `111111`
- 所属类别：创生与纯态

## 映射定位

在当前的 Omega 文化映射计划里，第 1 卦 乾 首先不是被当作抽象象义，而是被当作二元词 `111111` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是原始 6-bit 词，而不是稳定词。 它是整个 6-bit 卦系里的全阳极值词，也是离 `No11` 稳定域最远的极端配置。 它目前横跨的主题类别是 创生与纯态，因此其最强对应主要集中在 golden-mean-shift、fibonacci-growth、modular-tower-inverse-limit 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它不直接落在 `X_6` 内，因此原文在这里首先对应的是原始词的极端、临界或过载位置，数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。 在 Lean 锚点上，本页最强地落向 `fibonacci_cardinality` 与 `fibonacci_cardinality_recurrence`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` 进入稳定域的通道
- 当前主方向：golden-mean-shift、fibonacci-growth、modular-tower-inverse-limit

## 原文锚点

> 乾：元亨。利貞。
> 初九：潛龍勿用。
> 九二：見龍在田，利見大人。
> 九三：君子終日乾乾，夕惕若；厲，无咎。
> 彖曰：
> 大哉乾元，萬物資始，乃統天。雲行雨施，品物流形，大明終始，六位時成。
> 象曰：
> 天行健，君子以自強不息。

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) :     a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明整体是否相同完全由全部前缀是否相同决定，适合解释层级兼容。
- `inverse_limit_bijective` [`Omega.Frontier.ConditionalSummary`]：`theorem inverse_limit_bijective :     Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)`。说明 compatible family 与逆极限对象之间是双射，适合解释整体由有限层闭合产生。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_01_qian.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
