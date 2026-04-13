# Omega 内容架构 + 宣发对接文档

> 给宣发团队 / n8n 自动化 / AI agents 的对接指南

## 内容分层架构

```
Level 0 ─── Omega 研究院首页
             │
Level 1 ─── 7 支 Master 旗舰视频（每支覆盖一部完整经典）
             │   易经 · 道德经 · 黄帝内经 · 孙子兵法 · 几何原本 · 庄子 · 论文总览
             │
Level 2 ─── 10 支 Synthesis 跨文本综合视频
             │   每支追踪 1 个 Omega 定理跨 6 部经典
             │   例: "No11 与知止之美" / "Fold 算子与反转之动"
             │
Level 3 ─── 76 支 Category 类别视频
             │   每部经典拆成 8-12 个主题类别
             │   例: 道德经 "道体与不可名状" / 易经 "创生与纯态"
             │
Level 4 ─── 145+ 支 Per-Unit 逐卦/逐章视频
                 易经 64 卦 · 道德经 81 章（持续生成中）
```

### 每层的用途

| Level | 内容 | 视频数 | 时长 | 适合平台 | 发布频率 |
|:---:|---|---:|---|---|---|
| 1 | Master 旗舰 | 7 | 3-5 min | YouTube 长视频、LinkedIn、公众号 | 每部经典 1 支，首发用 |
| 2 | Synthesis 综合 | 10 | 2-4 min | X/Twitter、知乎、YouTube | 每周 2-3 支 |
| 3 | Category 类别 | 76 | 2-3 min | X/Twitter、抖音、小红书 | 每天 1-2 支 |
| 4 | Per-Unit 逐卦/章 | 145+ | 1-2 min | 抖音、小红书、Shorts | 批量发，冲量 |

## 宣发策略建议

### 第一周: 旗舰首发

```
Day 1:  易经 Master + "64 卦就是完整的 6-bit 二进制系统" 文案
Day 2:  道德经 Master + "道生一就是 x²=x+1 的递归展开" 文案
Day 3:  庄子 Master + "逍遥游的数学：逆极限自由" 文案
Day 4:  黄帝内经 Master + "中医是多尺度耦合系统" 文案
Day 5:  孙子兵法 Master + "不战而屈：率失真最优策略" 文案
Day 6:  几何原本 Master + "欧几里得作为受约束构造语法" 文案
Day 7:  论文总览 Master + "9 篇论文从一个方程推演" 文案
```

### 第二周起: Synthesis + Category 交替

```
周一/三/五: Synthesis 综合（高传播力，跨文本独特内容）
周二/四/六: Category 类别（深度内容，建立专业形象）
每天:       1-2 支 Per-Unit 逐卦/逐章（冲量，SEO 长尾）
```

### 文案提取方式

每支视频都有对应的 `.md` 文章，可自动提取：
- **标题**: 文件名 slug 或 YAML front matter `title`
- **摘要**: 文章第一段（`## 摘要` 后的段落）
- **关键词**: YAML front matter `categories`
- **原文金句**: `## 原文精选` 下的中文引文

## GitHub Release 资源获取

### 三个 Release

| Release Tag | 内容 | Assets |
|---|---|---:|
| `cultural-media-v1` | 文化视频 + synthesis + category + per-unit | 176+ |
| `papers-media-v1` | 9 篇论文视频 + slides | 19 |
| `master-videos-v1` | 7 支旗舰 master 视频 | 13 |

### API 获取 asset 列表

```bash
# 列出某个 release 的所有 assets
gh api repos/the-omega-institute/Omega-paper-series/releases/tags/cultural-media-v1 \
  --jq '.assets[] | {name, size, download_url: .browser_download_url}'
```

**返回格式:**
```json
{
  "name": "category_01_generative_ground_video.mp4",
  "size": 40156789,
  "download_url": "https://github.com/the-omega-institute/Omega-paper-series/releases/download/cultural-media-v1/category_01_generative_ground_video.mp4"
}
```

### 直链格式

```
https://github.com/the-omega-institute/Omega-paper-series/releases/download/{release-tag}/{filename}
```

**示例:**
```
# Master 旗舰视频（中文）
https://github.com/the-omega-institute/Omega-paper-series/releases/download/master-videos-v1/master_The_Mathematics_of_the_I_Ching_video.mp4

# Synthesis 综合视频
https://github.com/the-omega-institute/Omega-paper-series/releases/download/cultural-media-v1/synthesis_01_no11_golden_mean_shift_video.mp4

# Category 类别视频
https://github.com/the-omega-institute/Omega-paper-series/releases/download/cultural-media-v1/category_01_generative_ground_video.mp4

# Slides PDF
https://github.com/the-omega-institute/Omega-paper-series/releases/download/cultural-media-v1/category_01_generative_ground_slides.pdf
```

### 文件命名规则

```
{type}_{id}_{slug}_{media_type}.{ext}

type:       category | synthesis | master | hexagram | daodejing
id:         01-12 (category), 01-10 (synthesis), 01-64 (hexagram)
slug:       英文描述 (snake_case)
media_type: video | slides | infographic | audio
ext:        mp4 | pdf | png | wav
```

## n8n / Agent 对接方案

### 方案 A: 定时轮询 GitHub Release（推荐）

```
[n8n Cron Trigger: 每 6 小时]
    ↓
[HTTP Request: GET GitHub Release API]
    ↓
[Compare with 上次已发布列表]
    ↓
[Filter 新增 assets]
    ↓
[For each 新视频:]
    ├─ [提取文案: GET 对应 .md 文件从 repo]
    ├─ [生成平台适配文案: X=280字 / 微博=140字 / LinkedIn=长文]
    └─ [发布到各平台]
```

**GitHub Release API endpoint:**
```
GET https://api.github.com/repos/the-omega-institute/Omega-paper-series/releases/tags/cultural-media-v1
Header: Accept: application/vnd.github+json
```

### 方案 B: GitHub Webhook (实时)

在 Omega-paper-series repo 设置 webhook:
- Event: `release`
- Payload URL: Ada 的 n8n webhook endpoint
- 每次有新 asset 上传时触发

### 方案 C: Agent 直接调用

如果 Ada 的 agent 能执行 shell:

```bash
# 获取所有视频 URL
gh api repos/the-omega-institute/Omega-paper-series/releases/tags/cultural-media-v1 \
  --jq '.assets[] | select(.name | endswith("_video.mp4")) | .browser_download_url'

# 获取对应文章内容（用于生成文案）
gh api repos/the-omega-institute/Omega-paper-series/contents/cultural/tao-te-ching/articles/category_01_generative_ground.md \
  --jq '.content' | base64 -d
```

### 文案模板

**X/Twitter (280 字):**
```
🔬 {title_zh}

{摘要第一句}

"{原文金句}" —— {经典名}

从 x²=x+1 出发，这不是隐喻，而是形式结构对应。

🎬 {video_url}
🌐 {page_url}

#Omega #数学 #{经典tag}
```

**微博 (140 字):**
```
【{title_zh}】{摘要精简版}。"{原文金句}"。视频链接: {video_url} #Omega数学 #{经典tag}
```

**LinkedIn (长文):**
```
{title_en}

{English abstract paragraph}

Key insight: {mapping_rationale first sentence}

Watch the full analysis: {video_url}
Read the paper: {page_url}

#Mathematics #AI #CulturalHeritage #Omega
```

## 内容状态 API

查看当前所有可用内容:

```bash
# 全部 master 视频
gh api repos/the-omega-institute/Omega-paper-series/releases/tags/master-videos-v1 \
  --jq '.assets[] | select(.name | endswith("_video.mp4")) | .name'

# 全部 synthesis 视频
gh api repos/the-omega-institute/Omega-paper-series/releases/tags/cultural-media-v1 \
  --jq '.assets[] | select(.name | startswith("synthesis_") and endswith("_video.mp4")) | .name'

# 全部 category 视频
gh api repos/the-omega-institute/Omega-paper-series/releases/tags/cultural-media-v1 \
  --jq '.assets[] | select(.name | startswith("category_") and endswith("_video.mp4")) | .name'

# 统计
gh api repos/the-omega-institute/Omega-paper-series/releases/tags/cultural-media-v1 \
  --jq '.assets | length'
```

## 新内容生成后的自动流转

当我们这边生成新内容后，流转路径：

```
1. Codex/Claude 生成新文章 → workspace/{work}/generated/
2. 上传到 NotebookLM → tools/notebooklm_batch.py
3. NotebookLM 后台生成视频 (3-5 min)
4. sync_artifacts.sh 下载到本地 → workspace/artifacts/
5. upload_to_github_release.py 上传到 GitHub Release
6. ← Ada n8n 轮询检测到新 asset
7. ← n8n 提取文案 + 发布到社交平台
```

**步骤 1-5 已自动化。** 步骤 6-7 需要 Ada 的 n8n 工作流对接。

## 联系方式

- 内容管线: Lexa (@Lexa)
- 自动化发布: Ada
- 数学审核: automath Lean 4 验证（自动）
- Showcase 网站: https://the-omega-institute.github.io/Omega-paper-series/
