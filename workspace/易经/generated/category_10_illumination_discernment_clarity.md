# 明照与分辨：以 Omega 框架重读《易经》蒙、观、贲、离、晋、明夷、睽、困、旅

## 摘要

本文讨论《易经》“明照与分辨 / Illumination, Discernment, and Clarity”这一类中的九卦，并以 Omega 的 `spectral theory`、`modular-tower inverse limit` 与 `rate-distortion` 为主要形式参照。本类的关键，不只是“亮”与“不亮”，而是系统如何在复杂表象中分出主次、在不同分辨率下看到不同内容。离与晋代表照明，明夷与困代表光被遮蔽，观与蒙代表观看与未明，睽与旅则让视野进入差异与异地。Omega 的 spectral decomposition 在这里提供了最好的形式类比： illumination 就是把混杂模式分解出主导成分，discernment 则是知道在何种 resolution 上看什么。本文主张：离与 spectral decomposition 的对应最强；观/蒙与 resolution-level 的差异次之；明夷、困、睽、旅则说明“看不清”并不等于没有结构，而常是模式被遮蔽、失真或偏置。

## 一、形式框架：照明就是模式分离

spectral theory 的直觉很简单：复杂对象之所以可理解，不是因为它瞬间变简单了，而是因为我们能把不同模式分离出来，知道什么是 dominant mode，什么是 residual fluctuation。这与《易经》所谓“明”极近。真正的明不是总亮，而是能辨。

因此，本类与一般“光明意象”不同。它真正对应的是 discernment under structured complexity。离、观、蒙这些卦并不是单纯比喻认知，而是在问：当系统同时含多种信号时，怎样才能看出其主导结构？

## 二、离、晋、明夷：光之显、升、藏

离 `101101` 是双火，晋 `000101` 是日出地上，明夷 `101000` 则是光入地下。三者合起来，几乎就是 illumination 的全周期：光被点亮、光向上显、光被遮蔽。若用 spectral language 说，就是主模态何时占优、何时上升、何时被背景噪声或遮挡压低。

离与 spectral decomposition 的对应最强，因为火象本身就体现“使可见与不可见分开”。晋则像 dominant mode 增强的过程，明夷则像主模态仍在，但被埋到低可见度层。重要的是：明夷并不等于无光，这和谱中的 subdominant persistence 十分相近。

## 三、观与蒙：看见不是同一个层级上的事情

观 `000011` 与蒙 `010001` 是本类中最清楚的 resolution 对照。观要求拉开距离、从较高位置审视；蒙则处于未开之初，信息已在，但辨识能力尚不足。用 modular tower 来说，它们像处在不同分辨率层：观偏向 coarse global pattern，蒙偏向 local but under-resolved signal。

这说明《易经》的认识论并非二分法。不是“看见/看不见”而已，而是“你在什么层上看”。这也是为什么观与蒙都与 illumination 有关，却完全不是一个状态。Omega 的 tower 思想恰好把这种差异严格化。

## 四、睽、困、旅：分辨总在不顺处被测试

睽 `110101` 是乖离中的看法分岐，困 `010110` 是受困中的视野受压，旅 `001101` 是异地中的临时观察。三卦共同说明，discernment 从来不是在完美条件下被锻炼出来的，恰恰相反，它往往在系统偏离本位、信息受限、立场错位时变得最重要。

rate-distortion 在这里提供了强支持。信息不足、噪声过高、编码受限时，系统并非完全不能认知，而是只能以某种有损方式保留主结构。困与旅的“明”正像这种情形：你看不到全部，但仍必须提取足够可靠的主信号。

## 五、贲：美与装饰为何也属于分辨问题

贲 `101001` 表面上更像审美卦，但它出现在本类非常合理。装饰并不只是增加表面，而是重新排列可见性，让某些模式前置、某些模式后退。从这个角度看，贲像一种特定的 rendering。系统的结构未必改变很多，但其可见部分被重新组织了。

这也提醒我们，spectral illumination 不总是“越裸越真”。有时结构必须经过合适的表面编排，才真正变得可辨。贲因此是 illumination 的一个 subtler case。

## 六、边界：明照不是“离卦 = 特征值”

本类很容易因为“光”“明”“观”之类词汇而被过度技术化。必须承认，spectral theory 在这里首先是 formal analogue，而非文本原义。最强对应集中在两个层次：

1. illumination = separating dominant from residual structure
2. resolution = different levels reveal different features

离、观、蒙最适合落在这两个层次上；其余卦则围绕光的显藏、视野的受限、表面可见性的组织方式展开。只要守住这个边界，就不会把《易经》误写成现代信号处理教材。

## Omega 定理锚点

- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [`Omega.Graph.TransferMatrix`]：`theorem goldenMeanAdjacency_has_goldenRatio_eigenvector : ∃ v : Fin 2 → ℝ, v ≠ 0 ∧ Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio * v i`。说明 golden-mean adjacency 具有黄金比本征向量，支撑本文把主导增长率与稳定结构联系起来。
- `inverse_limit_extensionality` [`Omega.Frontier.ConditionalArithmetic`]：`theorem inverse_limit_extensionality (a b : X.XInfinity) : a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m`。说明无限对象是否相同，完全由全部有限前缀是否一致决定，支撑本文的层级拼接与兼容家族读法。
- `observation_refinement_reduces_error` [`Omega.Frontier.ConditionalArithmetic`]：`theorem observation_refinement_reduces_error {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ] (μ : PMF α) (obs₁ : α → β) (obs₂ : α → γ) (f : γ → β) (hRef ...`。说明观测更细时误差不会变大，支撑本文把分辨、静观、察势写成信息分辨率问题。

这些定理不替代文本解释，但它们把本文最核心的对应从“方向级相似”推进到了“可点名的 Lean 形式结果”。

## 结论

《易经》的“明照与分辨”不是单纯赞美光亮，而是关心一个更深的问题：复杂世界中的结构如何变得可辨。Omega 的 spectral theory 与 modular tower 给出了极强的形式帮助。离让我们看到 illumination 是模式分离，观/蒙让我们看到理解依赖分辨率，明夷/困/旅则让我们看到失真与遮蔽不是结构消失，而是可见度改变。由此再读“观”“离”“明夷”，会发现《易经》其实早已在思考一种分层认知理论。

## 参考与说明

1. 本文类别与映射依据见 `workspace/易经/classification.json` 第10类“明照与分辨”。
2. Omega 方向主要涉及 spectral theory、modular-tower inverse limit 与 rate-distortion。
3. 本类 strongest correspondence 集中在 illumination 作为 dominant-mode separation 的结构意义。
