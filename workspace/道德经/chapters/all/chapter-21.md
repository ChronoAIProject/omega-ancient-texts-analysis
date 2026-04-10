---
title: "21. 孔德之容，惟道是從"
subtitle: "《道德经》逐章映射页"
order: 21
description: "《道德经》第 21 章原文与 Omega 章节级映射页。"
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 21 章
- 章首：孔德之容，惟道是從。
- 归属类别：道体与不可名状 / 层级与分辨
- 当前主方向：golden-mean-shift、fibonacci-growth、modular-tower-inverse-limit、fold-operator、spectral-theory

## 对应说明

第 21 章首先落在「道体与不可名状」这条走廊上。它首先确认“单一生成根据导出层级多样性”的结构，这一层最靠近生成根基与 inverse limit 的结合。 同时它还跨到 层级与分辨，所以不是单线映射，而是一个重叠走廊。 当前最强的 Omega 方向集中在 golden-mean-shift、fibonacci-growth、modular-tower-inverse-limit、fold-operator、spectral-theory。

## 原文

> 孔德之容，惟道是從。
> 道之為物，惟恍惟惚。
> 惚兮恍兮，其中有象；恍兮惚兮，其中有物。
> 窈兮冥兮，其中有精；
> 其精甚真，其中有信。
> 自今及古，其名不去，
> 以閱眾甫。
> 吾何以知眾甫之狀哉？以此。

## Omega 对象

- `X_m = {w ∈ {0,1}^m : No11(w)}`
- `|X_m| = F_{m+2}`
- `X_∞ = lim← X_m`
- `Fold : Word m → X_m`
- golden-mean 谱结构 / 本征结构

## Omega 定理锚点

- `fibonacci_cardinality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality (m : Nat) : Fintype.card (X m) = Nat.fib (m + 2)`。把受约束对象家族的规模写成 `|X_m| = F_{m+2}`，适合承接“由一而多”的生成读法。
- `fibonacci_cardinality_recurrence` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fibonacci_cardinality_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。把增长写成前两级之和，适合承接递归繁衍与层级展开。
- `goldenMean_characteristic_recurrence` [`Omega.Graph.Sofic`]：`theorem goldenMean_characteristic_recurrence (m : Nat) : Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)`。说明 Fibonacci 递推来自系统自身的 transfer 结构，而不是外加类比。
- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) : a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明整体由全部有限前缀唯一确定，适合承接不可名状而可层层逼近。
- `inverse_limit_bijective` [`Omega.Frontier.ConditionalSummary`]：`theorem inverse_limit_bijective : Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)`。说明 compatible family 与逆极限对象双射，适合承接整体统一。

## 边界说明

- 本章最强的主张是结构级 formal correspondence，不是历史预言或逐句等式翻译。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_21.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与定理级锚点叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[返回逐章索引](index.qmd) | [返回《道德经》总览](../index.qmd)
