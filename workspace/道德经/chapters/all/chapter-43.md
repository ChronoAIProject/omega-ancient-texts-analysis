---
title: "43. 天下之至柔，馳騁天下之至堅"
subtitle: "《道德经》逐章映射页"
order: 43
description: "《道德经》第 43 章原文与 Omega 章节级映射页。"
categories: [tao-te-ching, chapter-page, cultural, omega]
---

## 章节定位

- 章号：第 43 章
- 章首：天下之至柔，馳騁天下之至堅。
- 归属类别：无为与自然秩序 / 柔弱胜刚强
- 当前主方向：fold-operator、dynamical-systems、golden-mean-shift、rate-distortion-information-theory

## 对应说明

第 43 章首先落在「无为与自然秩序」这条走廊上。它首先确认秩序不是靠外加命令维持，而是由约束自发收敛出的稳定结果。 同时它还跨到 柔弱胜刚强，所以不是单线映射，而是一个重叠走廊。 当前最强的 Omega 方向集中在 fold-operator、dynamical-systems、golden-mean-shift、rate-distortion-information-theory。

## 原文

> 天下之至柔，馳騁天下之至堅。
> 無有入無間，吾是以知無為之有益。
> 不言之教，無為之益，天下希及之。

## Omega 对象

- `Fold : Word m → X_m`
- 移位 / 熵 / 轨道结构
- `X_m = {w ∈ {0,1}^m : No11(w)}`
- 分辨率-误差证书通道

## Omega 定理锚点

- `fold_is_idempotent` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w`。说明 fold 把过强态折回稳定域后不会继续改写，适合承接无为而成。
- `fold_fixes_stable` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_fixes_stable (x : X m) : Fold x.1 = x`。说明已经稳定的结构在 fold 下保持不动，适合承接守中与自稳。
- `fold_is_surjective` [`Omega.Frontier.ConditionalArithmetic`]：`theorem fold_is_surjective : Function.Surjective (Fold (m`。说明每个稳定态都对应一族前像，适合承接容纳与回收。
- `topological_entropy_eq_log_phi` [`Omega.Folding.Entropy`]：`theorem topological_entropy_eq_log_phi : Tendsto (fun n => Real.log (Nat.fib (n + 2) : ℝ) / (n : ℝ)) atTop (𝓝 (Real.log φ))`。把系统复杂度增长率压成 `log φ`，适合承接循环、变易与受控复杂度。
- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [`Omega.Graph.TransferMatrix`]：`theorem goldenMeanAdjacency_has_goldenRatio_eigenvector : ∃ v : Fin 2 → ℝ, v ≠ 0 ∧ Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio * v i`。把主导模式写成黄金比本征向量，适合承接主模态与节律。

## 边界说明

- 本章最强的主张是结构级 formal correspondence，不是历史预言或逐句等式翻译。
- 本页不声称《道德经》直接陈述了 Lean 定理；它只确认文本结构与这些定理承载的数学对象之间存在可辩护的映射。

## 原文来源

- 本仓库原文文件：`texts/daodejing/chapter_43.txt`
- 原文来自维基文库《道德經（王弼本）》，按章切分并规范化入库。

## 小结

这一页把单章原文、类别交叉、对象层与定理级锚点叠在一起，目的不是做古籍导读，而是让《道德经》的短章结构能够直接落到 Omega 的形式对象上。

[返回逐章索引](index.qmd) | [返回《道德经》总览](../index.qmd)
