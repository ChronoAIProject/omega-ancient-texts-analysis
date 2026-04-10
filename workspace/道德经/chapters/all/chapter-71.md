---
title: "71. 知不知上，不知知病"
subtitle: "Tao Te Ching Chapter Page"
order: 71
description: "Tao Te Ching chapter 71 with source text and Omega chapter-level mapping."
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 71 章
- 章首：知不知上，不知知病。
- 归属类别：知足与限度
- 当前主方向：golden-mean-shift, zeckendorf-representation, rate-distortion-information-theory

## 对应说明

第 71 章首先落在「知足与限度」这条走廊上。它首先确认 sufficiency 的核心不是贫乏，而是稀疏、不过载、不过界的最优结构。 当前最强的 Omega 方向集中在 golden-mean-shift、zeckendorf-representation、rate-distortion-information-theory。

## 原文

> 知不知上，不知知病。
> 夫唯病病，是以不病。聖人不病，以其病病，是以不病。

## Omega 对象

- `X_m = {w ∈ {0,1}^m : No11(w)}`
- Zeckendorf sparse decomposition
- resolution-error certificate corridor

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) : Fintype.card (X m) = Nat.fib (m + 2)`。把受约束对象家族的规模写成 `|X_m| = F_{m+2}`，适合承接“由一而多”的生成读法。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合承接递归繁衍与层级展开。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自系统自身的 transfer 结构，而不是外加类比。
- `zeckendorf_uniqueness` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y`。说明稀疏 Fibonacci 分解唯一，适合承接知足、限度与稀疏秩序。
- `zeckendorf_injective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m`。说明不同稳定结构对应不同分解，适合承接可辨认的简素秩序。

## 边界说明

- 本章的 strongest claim 是结构级 formal correspondence，不是历史预言或逐句等式翻译。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_71.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与 theorem-level anchor 叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[Back to Chapter Index](index.qmd) | [Back to Tao Te Ching Index](../index.qmd)
