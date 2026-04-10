---
title: "22. 賁"
subtitle: "《易经》单卦映射页"
order: 22
description: "第 22 卦 賁，二进制 `101001`，已在 `X_6` 稳定域内，归属 变革与重构 / 明照与分辨。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷕
- 二进制：`101001`
- 下卦：離 / `101`
- 上卦：艮 / `001`
- 阳爻数：3
- 连续阳对数：0
- 最长阳串：1
- `X_6` 状态：已在稳定域内
- 互补卦：第 47 卦 / `010110`
- 综卦：第 21 卦 / `100101`
- 所属类别：变革与重构 / 明照与分辨

## 映射定位

在当前的 Omega 文化映射计划里，第 22 卦 賁 首先不是被当作抽象象义，而是被当作二元词 `101001` 来读取。该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。 它以三阳达到了 `No11` 允许的最大阳密度，因此是交替或近交替结构中的高密度稳定态。 它目前横跨的主题类别是 变革与重构、明照与分辨，因此其最强对应主要集中在 fold-operator、fiber-structure、dynamical-systems、spectral-theory、modular-tower-inverse-limit、rate-distortion-information-theory 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它已经直接落在 `X_6` 内，因此原文在这里首先对应的是一个稳定词的内部差异，而不是先经过 fold 才能成立的外部修正。 在 Lean 锚点上，本页最强地落向 `fold_is_idempotent` 与 `fold_fixes_stable`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `X_6` 稳定子空间
- 当前主方向：fold-operator、fiber-structure、dynamical-systems、spectral-theory、modular-tower-inverse-limit、rate-distortion-information-theory

## 原文锚点

> 賁：亨。小利有攸往。
> 初九：賁其趾，舍車而徒。
> 六二：賁其須。
> 九三：賁如濡如，永貞吉。
> 彖曰：
> 賁，亨；柔來而文剛，故亨。分剛上而文柔，故小利有攸往。剛柔交錯，天文也；文明以止，人文也。觀乎天文，以察時變；觀乎人文，以化成天下。
> 象曰：
> 山下有火，賁；君子以明庶政，无敢折獄。

## Omega 定理锚点

- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 一旦把原始词折回稳定域，再施一次不会继续改写。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的卦象在 fold 下保持不动，适合区分 stable word 与 raw word。
- `fold_is_surjective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_surjective : Function.Surjective (Fold (m`。说明每个稳定态都可作为某个前像族的代表点，适合解释 fiber 结构。
- `maxFiberMultiplicity_bounds` [`Omega.Combinatorics.FibonacciCube`]：`theorem maxFiberMultiplicity_bounds (m : Nat) :     m / 2 + 1 ≤ X.maxFiberMultiplicity m ∧     X.maxFiberMultiplicity m ≤ Nat.fib (m + 2)`。给出最大 fiber 多重性的上下界，适合解释哪些稳定卦吸纳能力更强。
- `maxFiberMultiplicity_eight` [`Omega.Folding.MaxFiberHigh`]：`theorem maxFiberMultiplicity_eight : maxFiberMultiplicity 8 = 8`。给出窗口 8 上的精确最大 fiber 多重性，适合解释吸纳规模的可计算性。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_22_bi.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
