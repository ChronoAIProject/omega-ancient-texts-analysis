---
title: "49. 革"
subtitle: "《易经》单卦映射页"
order: 49
description: "第 49 卦 革，二进制 `101110`，需经 fold 进入稳定域，归属 变革与重构。"
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷰
- 二进制：`101110`
- 下卦：離 / `101`
- 上卦：兌 / `110`
- 阳爻数：4
- 连续阳对数：1
- 最长阳串：3
- `X_6` 状态：需经 fold 进入稳定域
- 互补卦：第 4 卦 / `010001`
- 综卦：第 50 卦 / `011101`
- 所属类别：变革与重构

## 映射定位

在当前的 Omega 文化映射计划里，第 49 卦 革 首先不是被当作抽象象义，而是被当作二元词 `101110` 来读取。该卦不在 `X_6` 内，因此其第一层数学位置是原始 6-bit 词，而不是稳定词。 它包含长阳串，因此第一层读法不是稳定词，而是需要经 fold 才能进入稳定域的原始词。 它目前横跨的主题类别是 变革与重构，因此其最强对应主要集中在 fold-operator、fiber-structure、dynamical-systems 这些方向上。

## 对应说明

这一页保留原文，不是为了把卦辞和爻辞逐句翻译成公式，而是为了固定该卦的语义张力实际落在什么结构位置上。它不直接落在 `X_6` 内，因此原文在这里首先对应的是原始词的极端、临界或过载位置，数学上要先经过 `Fold : Word 6 → X_6` 才能进入稳定域。 在 Lean 锚点上，本页最强地落向 `fold_is_idempotent` 与 `fold_fixes_stable`。

## Omega 对象

- `Word 6 = {0,1}^6`
- `Fold : Word 6 → X_6` 进入稳定域的通道
- 当前主方向：fold-operator、fiber-structure、dynamical-systems

## 原文锚点

> 革：巳日乃孚，元亨。利貞。悔亡。
> 初九：鞏用黃牛之革。
> 六二：巳日乃革之，征吉，无咎。
> 九三：征凶，貞厲，革言三就，有孚。
> 彖曰：
> 革，水火相息，二女同居，其志不相得，曰革。巳日乃孚；革而信也。文明以說，大亨以正，革而當，其悔乃亡。天地革而四時成，湯武革命，順乎天而應乎人，革之時義大矣哉！
> 象曰：
> 澤中有火，革；君子以治歷明時。

## Omega 定理锚点

- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 一旦把原始词折回稳定域，再施一次不会继续改写。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的卦象在 fold 下保持不动，适合区分 stable word 与 raw word。
- `fold_is_surjective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_surjective : Function.Surjective (Fold (m`。说明每个稳定态都可作为某个前像族的代表点，适合解释 fiber 结构。
- `maxFiberMultiplicity_bounds` [`Omega.Combinatorics.FibonacciCube`]：`theorem maxFiberMultiplicity_bounds (m : Nat) :     m / 2 + 1 ≤ X.maxFiberMultiplicity m ∧     X.maxFiberMultiplicity m ≤ Nat.fib (m + 2)`。给出最大 fiber 多重性的上下界，适合解释哪些稳定卦吸纳能力更强。
- `maxFiberMultiplicity_eight` [`Omega.Folding.MaxFiberHigh`]：`theorem maxFiberMultiplicity_eight : maxFiberMultiplicity 8 = 8`。给出窗口 8 上的精确最大 fiber 多重性，适合解释吸纳规模的可计算性。

## 原文来源

- 本仓库原文文件：`texts/yijing/hexagram_49_ge.txt`
- 原文来自维基文库《周易》分卦页，经规范化后入库。

## 小结

这一页已经构成逐卦层的正式发布单元：它把原文锚点、位串结构、类别交叉与定理锚点放在同一坐标系里，重点不是替代传统注疏，而是展示该卦与 Omega 数学结构之间最可点名的映射位置。

[返回六十四卦索引](index.qmd) | [返回《易经》总览](../index.qmd)
