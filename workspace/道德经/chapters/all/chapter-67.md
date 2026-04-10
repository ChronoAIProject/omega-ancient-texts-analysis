---
title: "67. 天下皆謂我道大，似不肖夫唯大，故似…"
subtitle: "《道德经》逐章映射页"
order: 67
description: "《道德经》第 67 章原文与 Omega 章节级映射页。"
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 67 章
- 章首：天下皆謂我道大，似不肖。夫唯大，故似不肖。若肖，久矣其細也夫！
- 归属类别：自然与朴素
- 当前主方向：golden-mean-shift、zeckendorf-representation

## 对应说明

第 67 章首先落在「自然与朴素」这条走廊上。它首先确认朴素不是空白，而是带最小充分约束的活结构。 当前最强的 Omega 方向集中在 golden-mean-shift、zeckendorf-representation。

## 原文

> 天下皆謂我道大，似不肖。夫唯大，故似不肖。若肖，久矣其細也夫！
> 我有三寶，持而保之。一曰慈，二曰儉，三曰不敢為天下先。
> 慈故能勇，
> 儉故能廣，
> 不敢為天下先，故能成器長。
> 今舍慈且勇，
> 舍儉且廣，舍後且先，死矣！
> 夫慈以戰則勝，
> 以守則固。天將救之，以慈衛之。

## Omega 对象

- `X_m = {w ∈ {0,1}^m : No11(w)}`
- Zeckendorf 稀疏分解

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) : Fintype.card (X m) = Nat.fib (m + 2)`。把受约束对象家族的规模写成 `|X_m| = F_{m+2}`，适合承接“由一而多”的生成读法。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合承接递归繁衍与层级展开。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自系统自身的 transfer 结构，而不是外加类比。
- `zeckendorf_uniqueness` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y`。说明稀疏 Fibonacci 分解唯一，适合承接知足、限度与稀疏秩序。
- `zeckendorf_injective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m`。说明不同稳定结构对应不同分解，适合承接可辨认的简素秩序。

## 边界说明

- 本章以对象级和定理级映射为主，但仍需把感性意象与严格形式区分开。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_67.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与定理级锚点叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[返回逐章索引](index.qmd) | [返回《道德经》总览](../index.qmd)
