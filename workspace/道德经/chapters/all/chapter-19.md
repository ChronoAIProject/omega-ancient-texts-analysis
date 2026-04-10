---
title: "19. 絕聖棄智，民利百倍，絕仁棄義，民復…"
subtitle: "Tao Te Ching Chapter Page"
order: 19
description: "Tao Te Ching chapter 19 with source text and Omega chapter-level mapping."
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 19 章
- 章首：絕聖棄智，民利百倍；絕仁棄義，民復孝慈；絕巧棄利，盜賊無有。此三者以為文不足，故令有所屬﹕見素抱樸，少私寡欲。
- 归属类别：治国之道 / 自然与朴素
- 当前主方向：fold-operator, rate-distortion-information-theory, golden-mean-shift, zeckendorf-representation

## 对应说明

第 19 章首先落在「治国之道」这条走廊上。它首先确认治理问题可被读成局部干预、失真边界与系统稳态的问题。 同时它还跨到 自然与朴素，所以不是单线映射，而是一个重叠走廊。 当前最强的 Omega 方向集中在 fold-operator、rate-distortion-information-theory、golden-mean-shift、zeckendorf-representation。

## 原文

> 絕聖棄智，民利百倍；絕仁棄義，民復孝慈；絕巧棄利，盜賊無有。此三者以為文不足，故令有所屬﹕見素抱樸，少私寡欲。

## Omega 对象

- `Fold : Word m → X_m`
- resolution-error certificate corridor
- `X_m = {w ∈ {0,1}^m : No11(w)}`
- Zeckendorf sparse decomposition

## Omega 定理锚点

- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 把过强态折回稳定域后不会继续改写，适合承接无为而成。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的结构在 fold 下保持不动，适合承接守中与自稳。
- `fold_is_surjective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_surjective : Function.Surjective (Fold (m`。说明每个稳定态都对应一族前像，适合承接容纳与回收。
- `observation_refinement_reduces_error` [`Omega.Frontier.ConditionalArithmetic`]：`theorem observation_refinement_reduces_error {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ] (μ : PMF α) (obs₁ : α → β) (obs₂ : α → γ) (f : γ → β) (hRef ...`。说明观测更细时误差不会变大，适合承接观照与分辨。
- `prefix_resolution_decreases_error` [`Omega.Frontier.ConditionalArithmetic`]：`theorem prefix_resolution_decreases_error {m₁ m₂ n : Nat} (μ : PMF (Word n)) (h₁ : m₁ ≤ n) (h₂ : m₂ ≤ n) (hm : m₁ ≤ m₂) (P : Set (Word n)) : SPG.prefixScanEr...`。说明更长前缀带来更小误差，适合承接层级分辨。

## 边界说明

- 本章以对象级和 theorem-level 映射为主，但仍需把感性意象与严格形式区分开。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_19.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与 theorem-level anchor 叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[Back to Chapter Index](index.qmd) | [Back to Tao Te Ching Index](../index.qmd)
