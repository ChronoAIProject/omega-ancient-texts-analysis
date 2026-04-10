---
title: "28. 知其雄，守其雌，為天下谿為天下谿，…"
subtitle: "Tao Te Ching Chapter Page"
order: 28
description: "Tao Te Ching chapter 28 with source text and Omega chapter-level mapping."
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 28 章
- 章首：知其雄，守其雌，為天下谿。為天下谿，常德不離，復歸於嬰兒。
- 归属类别：虚空与容纳 / 自然与朴素
- 当前主方向：fiber-structure, zeckendorf-representation, golden-mean-shift

## 对应说明

第 28 章首先落在「虚空与容纳」这条走廊上。它首先确认“空”不是缺失，而是可承接多种前像与功能的容量结构。 同时它还跨到 自然与朴素，所以不是单线映射，而是一个重叠走廊。 当前最强的 Omega 方向集中在 fiber-structure、zeckendorf-representation、golden-mean-shift。

## 原文

> 知其雄，守其雌，為天下谿。為天下谿，常德不離，復歸於嬰兒。
> 知其白，守其黑，為天下式。
> 為天下式，常德不忒，
> 復歸於無極。
> 知其榮，守其辱，為天下谷，常德乃足，復歸於樸。
> 樸散則為器，聖人用之，則為官長，
> 故大制不割。

## Omega 对象

- `fiber(x) = {w : Fold(w)=x}`
- Zeckendorf sparse decomposition
- `X_m = {w ∈ {0,1}^m : No11(w)}`

## Omega 定理锚点

- `maxFiberMultiplicity_bounds` [`Omega.Combinatorics.FibonacciCube`]：`theorem maxFiberMultiplicity_bounds (m : Nat) : m / 2 + 1 ≤ X.maxFiberMultiplicity m ∧ X.maxFiberMultiplicity m ≤ Nat.fib (m + 2)`。给出最大 fiber 多重性的上下界，适合承接虚空与容纳的容量读法。
- `maxFiberMultiplicity_eight` [`Omega.Folding.MaxFiberHigh`]：`theorem maxFiberMultiplicity_eight : maxFiberMultiplicity 8 = 8`。它为本章当前最强的形式对应提供了可点名的 Lean 锚点。
- `maxFiberMultiplicity_nine` [`Omega.Folding.MaxFiberHigh`]：`theorem maxFiberMultiplicity_nine : maxFiberMultiplicity 9 = 10`。它为本章当前最强的形式对应提供了可点名的 Lean 锚点。
- `zeckendorf_uniqueness` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y`。说明稀疏 Fibonacci 分解唯一，适合承接知足、限度与稀疏秩序。
- `zeckendorf_injective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m`。说明不同稳定结构对应不同分解，适合承接可辨认的简素秩序。

## 边界说明

- 本章以对象级和 theorem-level 映射为主，但仍需把感性意象与严格形式区分开。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_28.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与 theorem-level anchor 叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[Back to Chapter Index](index.qmd) | [Back to Tao Te Ching Index](../index.qmd)
