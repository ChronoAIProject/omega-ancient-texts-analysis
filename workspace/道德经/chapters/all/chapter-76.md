---
title: "76. 人之生也柔弱，其死也堅強"
subtitle: "Tao Te Ching Chapter Page"
order: 76
description: "Tao Te Ching chapter 76 with source text and Omega chapter-level mapping."
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 76 章
- 章首：人之生也柔弱，其死也堅強。
- 归属类别：柔弱胜刚强
- 当前主方向：golden-mean-shift, fold-operator, rate-distortion-information-theory

## 对应说明

第 76 章首先落在「柔弱胜刚强」这条走廊上。它首先确认弱与柔不是消极退让，而是在受约束系统中更可持续的稳定策略。 当前最强的 Omega 方向集中在 golden-mean-shift、fold-operator、rate-distortion-information-theory。

## 原文

> 人之生也柔弱，其死也堅強。
> 萬物草木之生也柔脆，其死也枯槁。
> 故堅強者死之徒，柔弱者生之徒。
> 是以兵強則不勝，
> 木強則兵。
> 強大處下，
> 柔弱處上。

## Omega 对象

- `X_m = {w ∈ {0,1}^m : No11(w)}`
- `Fold : Word m → X_m`
- resolution-error certificate corridor

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) : Fintype.card (X m) = Nat.fib (m + 2)`。把受约束对象家族的规模写成 `|X_m| = F_{m+2}`，适合承接“由一而多”的生成读法。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合承接递归繁衍与层级展开。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自系统自身的 transfer 结构，而不是外加类比。
- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 把过强态折回稳定域后不会继续改写，适合承接无为而成。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的结构在 fold 下保持不动，适合承接守中与自稳。

## 边界说明

- 本章以对象级和 theorem-level 映射为主，但仍需把感性意象与严格形式区分开。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_76.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与 theorem-level anchor 叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[Back to Chapter Index](index.qmd) | [Back to Tao Te Ching Index](../index.qmd)
