---
title: "53. 漸"
subtitle: "《易经》单卦映射页"
order: 53
description: "第 53 卦 漸，二进制 `001011`，需经 fold 进入稳定域，归属 止静与内省 / 渐进与发展。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷴
- 二进制：`001011`
- 下卦：艮 / `001`
- 上卦：巽 / `011`
- 阳爻数：3
- 连续阳对数：1
- 最长阳串：2
- `X_6` 状态：需经 fold 进入稳定域
- 互补卦：第 54 卦 / `110100`
- 综卦：第 54 卦 / `110100`
- 所属类别：止静与内省 / 渐进与发展

## 映射定位

在当前的 Omega 文化映射计划里，第 53 卦 漸 首先不是被当作抽象象义，而是被当作二元词 `001011` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是原始 6-bit 词，而不是稳定词。 它虽不是极端全阳，但已出现连续阳段，因此其形式位置是 fold 之前的临界或过载态。 它目前横跨的主题类别是 止静与内省、渐进与发展，因此其最强对应主要集中在 golden-mean-shift、zeckendorf-representation、rate-distortion-information-theory、modular-tower-inverse-limit、fibonacci-growth 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它不直接落在 `X_6` 内，因此原文在这里首先对应的是原始词的极端、临界或过载位置，数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。 在 Lean 锚点上，本页最强地落向 `fibonacci_cardinality` 与 `fibonacci_cardinality_recurrence`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` 进入稳定域的通道
- 当前主方向：golden-mean-shift、zeckendorf-representation、rate-distortion-information-theory、modular-tower-inverse-limit、fibonacci-growth

## 原文锚点

> 漸：女歸吉，利貞。
> 初六：鴻漸于干，小子厲，有言，无咎。
> 六二：鴻漸于磐，飲食衎衎，吉。
> 九三：鴻漸于陸，夫征不復，婦孕不育，凶；利禦寇。
> 彖曰：
> 漸之進也，女歸吉也。進得位，往有功也。進以正，可以正邦也。其位剛，得中也。止而巽，動不窮也。
> 象曰：
> 山上有木，漸；君子以居賢德，善俗。

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `zeckendorf_uniqueness` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y`。说明非相邻 Fibonacci 指标分解唯一，适合解释稀疏稳定布局的唯一性。
- `zeckendorf_injective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m`。说明不同稳定词对应不同指标集，适合解释稀疏结构的可辨认性。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_53_jian.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
