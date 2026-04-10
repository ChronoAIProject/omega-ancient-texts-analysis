---
title: "29. 坎 / Kan"
subtitle: "I Ching Hexagram Dossier"
order: 29
description: "Hexagram 29 坎 as `010010`, GMS-valid, categories 困阻与险难 / 聚散与流通."
categories: [i-ching, hexagram-dossier, cultural, omega]
---

## 结构签名

- 卦符：䷜
- 二进制：`010010`
- 下卦：坎 / Water / `010`
- 上卦：坎 / Water / `010`
- 阳爻数：2
- 连续阳对数：0
- 最长阳串：1
- GMS 状态：valid
- 互补卦：第 30 卦 / `101101`
- 综卦：第 29 卦 / `010010`
- 所属类别：困阻与险难 / 聚散与流通

## 映射定位

在当前的 Omega 文化映射计划里，第 29 卦 坎 首先不是被当作抽象象义，而是被当作二元词 `010010` 来读取。该卦直接位于 `X_6` 内，因此不需要先经过 fold 才能进入稳定域。 它包含两个彼此分离的阳位，因此是典型的低密度稳定词，适合承接稀疏与间隔结构。 它目前横跨的主题类别是 困阻与险难、聚散与流通，因此其 strongest reading corridor 集中在 golden-mean-shift、fold-operator、fiber-structure、rate-distortion-information-theory、modular-tower-inverse-limit 这些方向上。

## Omega 对象

- `Word 6 = {0,1}^6`
- `X_6` stable subspace
- 当前主方向：golden-mean-shift, fold-operator, fiber-structure, rate-distortion-information-theory, modular-tower-inverse-limit

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) :     Fintype.card (X m) = Nat.fib (m + 2)`。把稳定词空间的计数压到 `|X_m| = F_{m+2}`，适合解释卦系在单一约束下的增长。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合解释由少量初始状态递归展开的结构。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) :     Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自 golden-mean adjacency 本身，而不是外加修辞。
- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 一旦把原始词折回稳定域，再施一次不会继续改写。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的卦象在 fold 下保持不动，适合区分 stable word 与 raw word。

## 语料状态

- 当前本地语料库还没有该卦的单独原文文件。
- 本页因此暂时采取“结构 dossier”写法：先锁定 binary / theorem / category 位置，再等待原文补齐后扩写。

## 小结

这一页不是终稿长文，而是逐卦展开的正式底稿：它先把卦位、位串、分类交叉和 theorem anchor 锁死，之后再叠加原文细读与更细的传统注疏材料。
