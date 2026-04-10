---
title: "35. 晉"
subtitle: "《易经》单卦映射页"
order: 35
description: "第 35 卦 晉，二进制 `000101`，已在 `X_6` 稳定域内，归属 柔顺与养育 / 明照与分辨。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷢
- 二进制：`000101`
- 下卦：坤 / `000`
- 上卦：離 / `101`
- 阳爻数：2
- 连续阳对数：0
- 最长阳串：1
- `X_6` 状态：已在稳定域内
- 互补卦：第 5 卦 / `111010`
- 综卦：第 36 卦 / `101000`
- 所属类别：柔顺与养育 / 明照与分辨

## 映射定位

在当前的 Omega 文化映射计划里，第 35 卦 晉 首先不是被当作抽象象义，而是被当作二元词 `000101` 来读取。该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。 它包含两个彼此分离的阳位，因此是典型的低密度稳定词，适合承接稀疏与间隔结构。 它目前横跨的主题类别是 柔顺与养育、明照与分辨，因此其最强对应主要集中在 golden-mean-shift、fibonacci-growth、zeckendorf-representation、spectral-theory、modular-tower-inverse-limit、rate-distortion-information-theory 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它已经直接落在 `X_6` 内，因此原文在这里首先对应的是一个稳定词的内部差异，而不是先经过 fold 才能成立的外部修正。 在 Lean 锚点上，本页最强地落向 `fibonacci_cardinality` 与 `fibonacci_cardinality_recurrence`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `X_6` 稳定子空间
- 当前主方向：golden-mean-shift、fibonacci-growth、zeckendorf-representation、spectral-theory、modular-tower-inverse-limit、rate-distortion-information-theory

## 原文锚点

> 晉：康侯用錫馬蕃庶，晝日三接。
> 初六：晉如，摧如，貞吉。罔孚，裕无咎。
> 六二：晉如，愁如，貞吉。受茲介福，于其王母。
> 六三：眾允，悔亡。
> 彖曰：
> 晉，進也。明出地上，順而麗乎大明，柔進而上行。是以康侯用錫馬蕃庶，晝日三接也。
> 象曰：
> 明出地上，晉；君子以自昭明德。

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `zeckendorf_uniqueness` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y`。说明非相邻 Fibonacci 指标分解唯一，适合解释稀疏稳定布局的唯一性。
- `zeckendorf_injective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m`。说明不同稳定词对应不同指标集，适合解释稀疏结构的可辨认性。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_35_jin.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
