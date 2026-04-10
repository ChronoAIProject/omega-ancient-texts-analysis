---
title: "77. 天之道，其猶張弓與？高者抑之，下者…"
subtitle: "《道德经》逐章映射页"
order: 77
description: "《道德经》第 77 章原文与 Omega 章节级映射页。"
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 77 章
- 章首：天之道，其猶張弓與？高者抑之，下者舉之；有餘者損之，不足者補之。天之道，損有餘而補不足。
- 归属类别：知足与限度
- 当前主方向：golden-mean-shift、zeckendorf-representation、rate-distortion-information-theory

## 对应说明

第 77 章首先落在「知足与限度」这条走廊上。它首先确认知足的核心不是贫乏，而是稀疏、不过载、不过界的最优结构。 当前最强的 Omega 方向集中在 golden-mean-shift、zeckendorf-representation、rate-distortion-information-theory。

## 原文

> 天之道，其猶張弓與？高者抑之，下者舉之；有餘者損之，不足者補之。天之道，損有餘而補不足。
> 人之道則不然，
> 損不足以奉有餘。
> 孰能有餘以奉天下？唯有道者。
> 是以聖人為而不恃，功成而不處，其不欲見賢。

## Omega 对象

- `X_m = {w ∈ {0,1}^m : No11(w)}`
- Zeckendorf 稀疏分解
- 分辨率-误差证书通道

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) : Fintype.card (X m) = Nat.fib (m + 2)`。把受约束对象家族的规模写成 `|X_m| = F_{m+2}`，适合承接“由一而多”的生成读法。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合承接递归繁衍与层级展开。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自系统自身的 transfer 结构，而不是外加类比。
- `zeckendorf_uniqueness` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y`。说明稀疏 Fibonacci 分解唯一，适合承接知足、限度与稀疏秩序。
- `zeckendorf_injective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m`。说明不同稳定结构对应不同分解，适合承接可辨认的简素秩序。

## 边界说明

- 本章最强的主张是结构级 formal correspondence，不是历史预言或逐句等式翻译。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_77.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与定理级锚点叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[返回逐章索引](index.qmd) | [返回《道德经》总览](../index.qmd)
