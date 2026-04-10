---
title: "39. 昔之得一者，"
subtitle: "Tao Te Ching Chapter Page"
order: 39
description: "Tao Te Ching chapter 39 with source text and Omega chapter-level mapping."
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 39 章
- 章首：昔之得一者，
- 归属类别：虚空与容纳
- 当前主方向：fiber-structure, zeckendorf-representation

## 对应说明

第 39 章首先落在「虚空与容纳」这条走廊上。它首先确认“空”不是缺失，而是可承接多种前像与功能的容量结构。 当前最强的 Omega 方向集中在 fiber-structure、zeckendorf-representation。

## 原文

> 昔之得一者，
> 天得一以清，地得一以寧，神得一以靈，谷得一以盈，萬物得一以生，侯王得一以為天下貞。其致之，
> 天無以清將恐裂，
> 地無以寧將恐發，神無以靈將恐歇，谷無以盈將恐竭，萬物無以生將恐滅，侯王無以貴高將恐蹶。故貴以賤為本，高以下為基。是以侯王自稱孤﹑寡﹑不穀。此非以賤為本邪？非乎？故致數輿無輿，不欲琭琭如玉，珞珞如石。

## Omega 对象

- `fiber(x) = {w : Fold(w)=x}`
- Zeckendorf sparse decomposition

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

- 本仓库原文文件：`texts/daodejing/chapter_39.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与 theorem-level anchor 叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[Back to Chapter Index](index.qmd) | [Back to Tao Te Ching Index](../index.qmd)
