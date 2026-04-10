---
title: "06. 谷神不死，是謂玄牝玄牝之門，是謂天…"
subtitle: "《道德经》逐章映射页"
order: 6
description: "《道德经》第 6 章原文与 Omega 章节级映射页。"
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 6 章
- 章首：谷神不死，是謂玄牝。玄牝之門，是謂天地根。緜緜若存，用之不勤。
- 归属类别：虚空与容纳 / 玄同与整体统一
- 当前主方向：fiber-structure、zeckendorf-representation、modular-tower-inverse-limit、spectral-theory、dynamical-systems

## 对应说明

第 6 章首先落在「虚空与容纳」这条走廊上。它首先确认“空”不是缺失，而是可承接多种前像与功能的容量结构。 同时它还跨到 玄同与整体统一，所以不是单线映射，而是一个重叠走廊。 当前最强的 Omega 方向集中在 fiber-structure、zeckendorf-representation、modular-tower-inverse-limit、spectral-theory、dynamical-systems。

## 原文

> 谷神不死，是謂玄牝。玄牝之門，是謂天地根。緜緜若存，用之不勤。

## Omega 对象

- `fiber(x) = {w : Fold(w)=x}`
- Zeckendorf 稀疏分解
- `X_∞ = lim← X_m`
- golden-mean 谱结构 / 本征结构
- 移位 / 熵 / 轨道结构

## Omega 定理锚点

- `maxFiberMultiplicity_bounds` [`Omega.Combinatorics.FibonacciCube`]：`theorem maxFiberMultiplicity_bounds (m : Nat) : m / 2 + 1 ≤ X.maxFiberMultiplicity m ∧ X.maxFiberMultiplicity m ≤ Nat.fib (m + 2)`。给出最大 fiber 多重性的上下界，适合承接虚空与容纳的容量读法。
- `maxFiberMultiplicity_eight` [`Omega.Folding.MaxFiberHigh`]：`theorem maxFiberMultiplicity_eight : maxFiberMultiplicity 8 = 8`。它为本章当前最强的形式对应提供了可点名的 Lean 锚点。
- `maxFiberMultiplicity_nine` [`Omega.Folding.MaxFiberHigh`]：`theorem maxFiberMultiplicity_nine : maxFiberMultiplicity 9 = 10`。它为本章当前最强的形式对应提供了可点名的 Lean 锚点。
- `zeckendorf_uniqueness` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y`。说明稀疏 Fibonacci 分解唯一，适合承接知足、限度与稀疏秩序。
- `zeckendorf_injective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m`。说明不同稳定结构对应不同分解，适合承接可辨认的简素秩序。

## 边界说明

- 本章最强的主张是结构级 formal correspondence，不是历史预言或逐句等式翻译。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_06.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与定理级锚点叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[返回逐章索引](index.qmd) | [返回《道德经》总览](../index.qmd)
