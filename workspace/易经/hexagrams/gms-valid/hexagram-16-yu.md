---
title: "16. 豫"
subtitle: "《易经》单卦映射页"
order: 16
description: "第 16 卦 豫，二进制 `000100`，已在 `X_6` 稳定域内，归属 止静与内省。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷏
- 二进制：`000100`
- 下卦：坤 / `000`
- 上卦：震 / `100`
- 阳爻数：1
- 连续阳对数：0
- 最长阳串：1
- `X_6` 状态：已在稳定域内
- 互补卦：第 9 卦 / `111011`
- 综卦：第 15 卦 / `001000`
- 所属类别：止静与内省

## 映射定位

在当前的 Omega 文化映射计划里，第 16 卦 豫 首先不是被当作抽象象义，而是被当作二元词 `000100` 来读取。该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。 它只保留一个孤立阳位，因此属于最小非零稳定激活，可视作稀疏启动态。 它目前横跨的主题类别是 止静与内省，因此其最强对应主要集中在 golden-mean-shift、zeckendorf-representation、rate-distortion-information-theory 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它已经直接落在 `X_6` 内，因此原文在这里首先对应的是一个稳定词的内部差异，而不是先经过 fold 才能成立的外部修正。 在 Lean 锚点上，本页最强地落向 `fibonacci_cardinality` 与 `fibonacci_cardinality_recurrence`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `X_6` 稳定子空间
- 当前主方向：golden-mean-shift、zeckendorf-representation、rate-distortion-information-theory

## 原文锚点

> alt=䷏ 坤下震上
> 豫：利建侯行師。
> 初六：鳴豫，凶。
> 六二：介于石，不終日，貞吉。
> 彖曰：
> 豫，剛應而志行，順以動，豫。豫，順以動，故天地如之，而況建侯行師乎？天地以順動，故日月不過，而四時不忒；聖人以順動，則刑罰清而民服。豫之時義大矣哉！
> 象曰：
> 雷出地奮，豫。先王以作樂崇德，殷薦之上帝，以配祖考。

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `zeckendorf_uniqueness` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y`。说明非相邻 Fibonacci 指标分解唯一，适合解释稀疏稳定布局的唯一性。
- `zeckendorf_injective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m`。说明不同稳定词对应不同指标集，适合解释稀疏结构的可辨认性。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_16_yu.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
