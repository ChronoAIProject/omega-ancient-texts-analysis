---
title: "01. 乾 / Qian"
subtitle: "I Ching Hexagram Dossier"
order: 1
description: "Hexagram 1 乾 as `111111`, fold-required, categories 创生与纯态."
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷀
- 二进制：`111111`
- 下卦：乾 / Heaven / `111`
- 上卦：乾 / Heaven / `111`
- 阳爻数：6
- 连续阳对数：3
- 最长阳串：6
- GMS 状态：not valid
- 互补卦：第 2 卦 / `000000`
- 综卦：第 1 卦 / `111111`
- 所属类别：创生与纯态

## 映射定位

在当前的 Omega 文化映射计划里，第 1 卦 乾 首先不是被当作抽象象义，而是被当作二元词 `111111` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是 raw 6-bit word，而不是 stable word。 它是整个 6-bit 卦系里的全阳极值词，也是离 `No11` 稳定域最远的极端配置。 它目前横跨的主题类别是 创生与纯态，因此其 strongest reading corridor 集中在 golden-mean-shift、fibonacci-growth、modular-tower-inverse-limit 这些方向上。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` entry corridor
- 当前主方向：golden-mean-shift, fibonacci-growth, modular-tower-inverse-limit

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) :     a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明整体是否相同完全由全部前缀是否相同决定，适合解释层级兼容。
- `inverse_limit_bijective` [`Omega.Frontier.ConditionalSummary`]：`theorem inverse_limit_bijective :     Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)`。说明 compatible family 与逆极限对象之间是双射，适合解释整体由有限层闭合产生。

## 语料状态

- 已有本地原文文件：`texts/yijing/hexagram_01_qian.txt`
- 这一页可以继续往完整逐卦长文扩展，不需要再补基础元数据。

## 小结

这一页不是终稿长文，而是逐卦展开的正式底稿：它先把卦位、位串、分类交叉和 theorem anchor 锁死，之后再叠加原文细读与更细的传统注疏材料。
