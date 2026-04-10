---
title: "50. 出生入死"
subtitle: "《道德经》逐章映射页"
order: 50
description: "《道德经》第 50 章原文与 Omega 章节级映射页。"
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 50 章
- 章首：出生入死。
- 归属类别：回归与循环
- 当前主方向：dynamical-systems、modular-tower-inverse-limit

## 对应说明

第 50 章首先落在「回归与循环」这条走廊上。它首先确认回归与反转不是修辞，而是层级系统里真实存在的投影、周期与回返结构。 当前最强的 Omega 方向集中在 dynamical-systems、modular-tower-inverse-limit。

## 原文

> 出生入死。
> 生之徒，十有三；死之徒，十有三；人之生，動之死地，亦十有三。夫何故？以其生生之厚。蓋聞善攝生者，陸行不遇兕虎，入軍不被甲兵；兕無所投其角，虎無所措其爪，兵無所容其刃。夫何故？以其無死地。

## Omega 对象

- 移位 / 熵 / 轨道结构
- `X_∞ = lim← X_m`

## Omega 定理锚点

- `topological_entropy_eq_log_phi` [`Omega.Folding.Entropy`]：`theorem topological_entropy_eq_log_phi : Tendsto (fun n => Real.log (Nat.fib (n + 2) : ℝ) / (n : ℝ)) atTop (𝓝 (Real.log φ))`。把系统复杂度增长率压成 `log φ`，适合承接循环、变易与受控复杂度。
- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [`Omega.Graph.TransferMatrix`]：`theorem goldenMeanAdjacency_has_goldenRatio_eigenvector : ∃ v : Fin 2 → ℝ, v ≠ 0 ∧ Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio * v i`。把主导模式写成黄金比本征向量，适合承接主模态与节律。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自系统自身的 transfer 结构，而不是外加类比。
- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) : a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明整体由全部有限前缀唯一确定，适合承接不可名状而可层层逼近。
- `inverse_limit_bijective` [`Omega.Frontier.ConditionalSummary`]：`theorem inverse_limit_bijective : Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)`。说明 compatible family 与逆极限对象双射，适合承接整体统一。

## 边界说明

- 本章最强的主张是结构级 formal correspondence，不是历史预言或逐句等式翻译。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_50.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与定理级锚点叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[返回逐章索引](index.qmd) | [返回《道德经》总览](../index.qmd)
