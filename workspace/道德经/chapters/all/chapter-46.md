---
title: "46. 天下有道，卻走馬以糞"
subtitle: "《道德经》逐章映射页"
order: 46
description: "《道德经》第 46 章原文与 Omega 章节级映射页。"
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 46 章
- 章首：天下有道，卻走馬以糞。
- 归属类别：治国之道 / 知足与限度
- 当前主方向：fold-operator、rate-distortion-information-theory、golden-mean-shift、zeckendorf-representation

## 对应说明

第 46 章首先落在「治国之道」这条走廊上。它首先确认治理问题可被读成局部干预、失真边界与系统稳态的问题。 同时它还跨到 知足与限度，所以不是单线映射，而是一个重叠走廊。 当前最强的 Omega 方向集中在 fold-operator、rate-distortion-information-theory、golden-mean-shift、zeckendorf-representation。

## 原文

> 天下有道，卻走馬以糞。
> 天下無道，戎馬生於郊。
> 禍莫大於不知足；咎莫大於欲得。故知足之足，常足矣。

## Omega 对象

- `Fold : Word m → X_m`
- 分辨率-误差证书通道
- `X_m = {w ∈ {0,1}^m : No11(w)}`
- Zeckendorf 稀疏分解

## Omega 定理锚点

- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 把过强态折回稳定域后不会继续改写，适合承接无为而成。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的结构在 fold 下保持不动，适合承接守中与自稳。
- `fold_is_surjective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_surjective : Function.Surjective (Fold (m`。说明每个稳定态都对应一族前像，适合承接容纳与回收。
- `observation_refinement_reduces_error` [`Omega.Frontier.ConditionalArithmetic`]：`theorem observation_refinement_reduces_error {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ] (μ : PMF α) (obs₁ : α → β) (obs₂ : α → γ) (f : γ → β) (hRef ...`。说明观测更细时误差不会变大，适合承接观照与分辨。
- `prefix_resolution_decreases_error` [`Omega.Frontier.ConditionalArithmetic`]：`theorem prefix_resolution_decreases_error {m₁ m₂ n : Nat} (μ : PMF (Word n)) (h₁ : m₁ ≤ n) (h₂ : m₂ ≤ n) (hm : m₁ ≤ m₂) (P : Set (Word n)) : SPG.prefixScanEr...`。说明更长前缀带来更小误差，适合承接层级分辨。

## 边界说明

- 本章最强的主张是结构级 formal correspondence，不是历史预言或逐句等式翻译。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_46.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与定理级锚点叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[返回逐章索引](index.qmd) | [返回《道德经》总览](../index.qmd)
