---
title: "70. 吾言甚易知，甚易行天下莫能知，莫能行"
subtitle: "Tao Te Ching Chapter Page"
order: 70
description: "Tao Te Ching chapter 70 with source text and Omega chapter-level mapping."
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 70 章
- 章首：吾言甚易知，甚易行。天下莫能知，莫能行。
- 归属类别：层级与分辨
- 当前主方向：modular-tower-inverse-limit, fold-operator, spectral-theory

## 对应说明

第 70 章首先落在「层级与分辨」这条走廊上。它首先确认 knowing 具有分辨率层次，整体只能借有限层逐步逼近。 当前最强的 Omega 方向集中在 modular-tower-inverse-limit、fold-operator、spectral-theory。

## 原文

> 吾言甚易知，甚易行。天下莫能知，莫能行。
> 言有宗，事有君。
> 夫唯無知，是以不我知。
> 知我者希，則我者貴。
> 是以聖人被褐懷玉。

## Omega 对象

- `X_∞ = lim← X_m`
- `Fold : Word m → X_m`
- golden-mean spectral / eigen-structure

## Omega 定理锚点

- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) : a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明整体由全部有限前缀唯一确定，适合承接不可名状而可层层逼近。
- `inverse_limit_bijective` [`Omega.Frontier.ConditionalSummary`]：`theorem inverse_limit_bijective : Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)`。说明 compatible family 与逆极限对象双射，适合承接整体统一。
- `inverse_limit_left` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_left (F : X.CompatibleFamily) : X.toFamily (X.ofFamily F) = F`。说明从相容家族回到对象再取 family 不丢信息，适合承接回归。
- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 把过强态折回稳定域后不会继续改写，适合承接无为而成。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的结构在 fold 下保持不动，适合承接守中与自稳。

## 边界说明

- 本章的 strongest claim 是结构级 formal correspondence，不是历史预言或逐句等式翻译。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_70.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与 theorem-level anchor 叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[Back to Chapter Index](index.qmd) | [Back to Tao Te Ching Index](../index.qmd)
