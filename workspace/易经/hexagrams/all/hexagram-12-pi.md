---
title: "12. 否"
subtitle: "《易经》单卦映射页"
order: 12
description: "第 12 卦 否，二进制 `000111`，需经 fold 进入稳定域，归属 创生与纯态。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷋
- 二进制：`000111`
- 下卦：坤 / `000`
- 上卦：乾 / `111`
- 阳爻数：3
- 连续阳对数：1
- 最长阳串：3
- `X_6` 状态：需经 fold 进入稳定域
- 互补卦：第 11 卦 / `111000`
- 综卦：第 11 卦 / `111000`
- 所属类别：创生与纯态

## 映射定位

在当前的 Omega 文化映射计划里，第 12 卦 否 首先不是被当作抽象象义，而是被当作二元词 `000111` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是原始 6-bit 词，而不是稳定词。 它包含长阳串，因此第一层读法不是稳定词，而是需要经 fold 才能进入稳定域的原始词。 它目前横跨的主题类别是 创生与纯态，因此其最强对应主要集中在 golden-mean-shift、fibonacci-growth、modular-tower-inverse-limit 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它不直接落在 `X_6` 内，因此原文在这里首先对应的是原始词的极端、临界或过载位置，数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。 在 Lean 锚点上，本页最强地落向 `fibonacci_cardinality` 与 `fibonacci_cardinality_recurrence`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` 进入稳定域的通道
- 当前主方向：golden-mean-shift、fibonacci-growth、modular-tower-inverse-limit

## 原文锚点

> alt=䷋ 坤下乾上
> 否之匪人，不利君子貞，大往小來。
> 初六，拔茅茹以其彙，貞吉。亨。
> 六二，包承，小人吉，大人否。亨。
> 彖曰：
> 否之匪人，不利君子貞，大往小來。則是天地不交而萬物不通也，上下不交而天下无邦也。內陰而外陽，內柔而外剛，內小人而外君子，小人道長，君子道消也。
> 象曰：
> 天地不交，否；君子以儉德辟難，不可榮以祿。

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) :     a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明整体是否相同完全由全部前缀是否相同决定，适合解释层级兼容。
- `inverse_limit_bijective` [`Omega.Frontier.ConditionalSummary`]：`theorem inverse_limit_bijective :     Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)`。说明 compatible family 与逆极限对象之间是双射，适合解释整体由有限层闭合产生。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_12_pi.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
