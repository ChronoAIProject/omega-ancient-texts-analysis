---
title: "57. 巽 / Xun"
subtitle: "I Ching Hexagram Dossier"
order: 57
description: "Hexagram 57 巽 as `011011`, fold-required, categories 渐进与发展 / 聚散与流通."
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷸
- 二进制：`011011`
- 下卦：巽 / Wind / `011`
- 上卦：巽 / Wind / `011`
- 阳爻数：4
- 连续阳对数：2
- 最长阳串：2
- GMS 状态：not valid
- 互补卦：第 51 卦 / `100100`
- 综卦：第 58 卦 / `110110`
- 所属类别：渐进与发展 / 聚散与流通

## 映射定位

在当前的 Omega 文化映射计划里，第 57 卦 巽 首先不是被当作抽象象义，而是被当作二元词 `011011` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是 raw 6-bit word，而不是 stable word。 它虽不是极端全阳，但已出现连续阳段，因此其形式位置是 fold 之前的临界或过载态。 它目前横跨的主题类别是 渐进与发展、聚散与流通，因此其 strongest reading corridor 集中在 modular-tower-inverse-limit、fibonacci-growth、golden-mean-shift、rate-distortion-information-theory、fold-operator 这些方向上。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` entry corridor
- 当前主方向：modular-tower-inverse-limit, fibonacci-growth, golden-mean-shift, rate-distortion-information-theory, fold-operator

## Omega 定理锚点

- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) :     a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明整体是否相同完全由全部前缀是否相同决定，适合解释层级兼容。
- `inverse_limit_bijective` [`Omega.Frontier.ConditionalSummary`]：`theorem inverse_limit_bijective :     Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)`。说明 compatible family 与逆极限对象之间是双射，适合解释整体由有限层闭合产生。
- `inverse_limit_left` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_left (F : X.CompatibleFamily) :     X.toFamily (X.ofFamily F) = F`。它为该卦当前的映射走廊提供了可点名的 Lean 形式锚点。
- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。

## 语料状态

- 当前本地语料库还没有该卦的单独原文文件。
- 本页因此暂时采取“结构 dossier”写法：先锁定 binary / theorem / category 位置，再等待原文补齐后扩写。

## 小结

这一页不是终稿长文，而是逐卦展开的正式底稿：它先把卦位、位串、分类交叉和 theorem anchor 锁死，之后再叠加原文细读与更细的传统注疏材料。
