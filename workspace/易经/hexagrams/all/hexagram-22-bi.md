---
title: "22. 賁 / Bi"
subtitle: "I Ching Hexagram Dossier"
order: 22
description: "Hexagram 22 賁 as `101001`, GMS-valid, categories 变革与重构 / 明照与分辨."
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷕
- 二进制：`101001`
- 下卦：離 / Flame / `101`
- 上卦：艮 / Mountain / `001`
- 阳爻数：3
- 连续阳对数：0
- 最长阳串：1
- GMS 状态：valid
- 互补卦：第 47 卦 / `010110`
- 综卦：第 21 卦 / `100101`
- 所属类别：变革与重构 / 明照与分辨

## 映射定位

在当前的 Omega 文化映射计划里，第 22 卦 賁 首先不是被当作抽象象义，而是被当作二元词 `101001` 来读取。该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。 它以三阳达到了 `No11` 允许的最大阳密度，因此是交替或近交替结构中的高密度稳定态。 它目前横跨的主题类别是 变革与重构、明照与分辨，因此其 strongest reading corridor 集中在 fold-operator、fiber-structure、dynamical-systems、spectral-theory、modular-tower-inverse-limit、rate-distortion-information-theory 这些方向上。

## Omega 对象

- `Word 6 = {0,1}^6`
- `X_6` stable subspace
- 当前主方向：fold-operator, fiber-structure, dynamical-systems, spectral-theory, modular-tower-inverse-limit, rate-distortion-information-theory

## Omega 定理锚点

- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 一旦把原始词折回稳定域，再施一次不会继续改写。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的卦象在 fold 下保持不动，适合区分 stable word 与 raw word。
- `fold_is_surjective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_surjective : Function.Surjective (Fold (m`。说明每个稳定态都可作为某个前像族的代表点，适合解释 fiber 结构。
- `maxFiberMultiplicity_bounds` [`Omega.Combinatorics.FibonacciCube`]：`theorem maxFiberMultiplicity_bounds (m : Nat) :     m / 2 + 1 ≤ X.maxFiberMultiplicity m ∧     X.maxFiberMultiplicity m ≤ Nat.fib (m + 2)`。给出最大 fiber 多重性的上下界，适合解释哪些稳定卦吸纳能力更强。
- `maxFiberMultiplicity_eight` [`Omega.Folding.MaxFiberHigh`]：`theorem maxFiberMultiplicity_eight : maxFiberMultiplicity 8 = 8`。给出窗口 8 上的精确最大 fiber 多重性，适合解释吸纳规模的可计算性。

## 语料状态

- 当前本地语料库还没有该卦的单独原文文件。
- 本页因此暂时采取“结构 dossier”写法：先锁定 binary / theorem / category 位置，再等待原文补齐后扩写。

## 小结

这一页不是终稿长文，而是逐卦展开的正式底稿：它先把卦位、位串、分类交叉和 theorem anchor 锁死，之后再叠加原文细读与更细的传统注疏材料。
