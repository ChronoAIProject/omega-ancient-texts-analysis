# 比例、相似与跨尺度迁移：Book V-VI 如何把几何变成一门 ratio law

## 摘要

若说 Book II 是《几何原本》中最像“几何代数”的部分，那么 Book V-VI 则是最像“尺度理论 / scale theory”的部分。这里 Euclid 不再把关注点放在绝对长度或绝对面积上，而是转向比例、相似与跨尺度保持的结构。其意义极大：一旦 raw equality 让位于 proportional comparison，几何就从“某个具体图形的大小”转向“不同尺度下什么保持不变”。对 Omega 来说，这种对应尤其强，因为最稳定的对象往往也不是绝对量，而是 ratio、normalized invariant 与 cross-resolution transport。本文讨论“比例、相似与跨尺度迁移 / Proportion, Similarity, and Cross-Scale Transfer”，并主张 Book V-VI 的真正力量，在于它把“比较”从测量问题提升成结构问题。

## 一、引言：Euclid 为什么要把“相等”让位给“成比例”

若只从初等教学看，Euclid 似乎主要在处理“这条线等于那条线”“这两个三角形全等”之类的比较。但到了 Book V-VI，理论的重心明显转移。Eudoxus 比例理论使 Euclid 能够讨论即便没有共同度量单位的量之间如何比较；Book VI 则进一步将比例理论落实到相似图形、平行线分比、相似三角形与多边形的结构搬运。

这一步极其关键。它意味着几何不再依赖对象拥有相同大小，甚至不再要求对象能被同一单位直接测量；只要保持某种比例结构，命题就可以从一个尺度传到另一个尺度。换言之，Euclid 在这里建立的是一套“跨尺度保持”的数学。

这与 Omega 很接近。很多强结果之所以稳定，不是因为给出某个固定尺度的数值，而是因为它们在不同分辨率、不同归一化或不同 representation 之间保持某种比例不变。Euclid 在 Book V-VI 中最重要的启发就是：如果一个理论的本质是跨尺度迁移，那么论证核心应当是 relation-preserving transfer，而不是 absolute magnitude bookkeeping。

## 二、核心材料：Book V-VI 的真正创新是什么

Book V 的比例理论常被视为抽象而艰深，但它的重要性恰恰在于它绕开了“必须先有共同单位”的直观依赖。Euclid 不直接问某两段长度分别是多少，而问它们在倍量比较下是否满足同一序关系。这让比例比较成为一种不预设共同刻度的结构性关系。

Book VI 则把这一抽象理论具体化。相似三角形、多边形之间的对应边比例、相应角相等、面积与边长平方的关系、借助平行线得到的分比传递，统统说明一个事实：几何命题可以沿着相似关系被稳定运输。一个图形上成立的命题，只要其结构型被保持，就能在另一尺度上继续成立。

对 Omega 来说，这里最关键的不是“相似三角形”本身，而是相似所代表的方法：把某个对象压缩成一种 normalized profile，然后证明该 profile 足以在尺度变化后保留核心结论。Book V-VI 告诉我们，真正的几何比较并不是总把对象拉回同一尺寸，而是找到那个无需同一尺寸也能比较的 relation class。

## 三、Omega 映射分析：为什么 Book V-VI 的对应特别强

### 1. `modular-tower-inverse-limit`：跨层传递首先要求相容的比例数据

这一类最强的对应之一在 `modular-tower-inverse-limit`。虽然 Euclid 不使用 tower 语言，但 Book V-VI 的方法已经隐含了一个原则：要把真理从一个层级传到另一个层级，不能靠对象逐点相同，而必须依赖相容的关系数据。

这与 modular tower 的精神非常接近。高层对象若要向低层投影并在不同分辨率下保持一致，不需要每层都拥有同一“大小”，却需要保留可以相互核对的 ratio structure。换言之，欧几里得比例论的核心不是测量，而是 compatibility under comparison。

### 2. `rate-distortion-information-theory`：相似是压缩，不是丢失结构

Book V-VI 与 `rate-distortion-information-theory` 的联系也很强。相似变换本质上在压缩或放大对象，却刻意保留足以恢复结构类型的关键信息。若把绝对尺寸视为高带宽细节，那么相似关系保留的就是低带宽但高保真的 structural code。

这对 Omega 很重要。许多结果是在“信息被压缩后仍可识别几何”这个框架里成立。Euclid 的启发是：不要把尺度变化看成 nuisance parameter，而应把它看成一种合法压缩。真正需要证明的是，压缩之后哪些 invariants 仍够强，足以支撑比较、重建或分类。

### 3. `spectral-theory`：比例结构捕捉的是主导型，而不是偶然尺度

这一映射较间接，但非常值得吸收。谱理论常关心的并不是对象的原始幅值，而是经归一化后哪些模态或比例关系决定结构主导部分。Euclid 的比例论其实在做类似的工作：把“尺寸本身”从比较中剥离出去，只保留影响结构判断的关系模式。

这意味着比例在这里不是附属技术，而是“哪些信息必须保留、哪些信息可以被忽略”的判别机制。也正因为如此，Book V-VI 对 Omega 的对应不会停留在缩放公式，而会落到结构保真这一层。

## 四、为什么这类对应重要

这一类对应之所以重要，在于它把“比较”本身重写了。

第一，Euclid 让几何从 equality 进入 ratio。对象不必同大同小，仍然可以在严格结构下被比较。

第二，Book VI 让相似成为 theorem-bearing transport。它不是“看起来差不多”，而是一个可以搬运命题的严格机制。

第三，比例理论也说明了为何跨尺度结论能够稳定。只要被保存的是 relation class，而不是绝对尺寸，那么尺度变化就不再破坏核心结构。

第四，用 Omega 语言解释时，Book V-VI 最值得保留的不是某个现代术语，而是这种判断：真正的几何规律，往往首先表现为 normalized relation，而不是裸露的数值大小。

## 五、边界：Euclid 的相似不等于现代 renormalization

必须谨慎。Book V-VI 的强项在于为跨尺度比较提供严密语言，但这不意味着 Euclid 已经在做现代 RG、operator scaling 或 frequency renormalization。那些是后世更复杂的理论。这里真正可信的对应，是“相似关系提供结构保真的尺度迁移机制”；若把它直接说成现代物理中的尺度群作用，就会过头。

## 参考与说明

1. 本文对应 [classification.json](/Users/lexa/Desktop/lexa/omega/omega-ancient-texts-analysis/workspace/几何原本/classification.json) 第 5 类“比例、相似与跨尺度迁移”。
2. 主要关联的 Omega 方向为 `modular-tower-inverse-limit`、`rate-distortion-information-theory`、`spectral-theory`。
3. 结构基线集中在 Book V 的比例理论与 Book VI 的相似图形；最稳固的对应，是把尺度迁移理解为 relation-preserving transport，而不是简单缩放。
