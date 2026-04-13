# Omega Ancient Texts Analysis

> 古典著作自动化分析管线 — Omega 数学理论 x AI x 社交网络自动发布

## 内容分层架构

```
Level 0 ─── Omega 研究院首页 (https://the-omega-institute.github.io/Omega-paper-series/)
             │
Level 1 ─── 7 支 Master 旗舰视频（每支覆盖一部完整经典，中文）
             │   易经 · 道德经 · 黄帝内经 · 孙子兵法 · 几何原本 · 庄子 · 论文总览
             │
Level 2 ─── 10 支 Synthesis 跨文本综合视频
             │   每支追踪 1 个 Omega 定理跨 6 部经典 + Gen 2 论文
             │
Level 3 ─── 76 支 Category 类别视频
             │   每部经典拆成 8-12 个主题类别
             │
Level 4 ─── 145+ 支 Per-Unit 逐卦/逐章视频（持续生成中）
                 易经 64 卦 · 道德经 81 章
```

**宣发策略**: Master 首发 → Synthesis 次发 → Category 日常 → Per-Unit 冲量

**宣发/Agent 对接详见**: [AGENT_INTEGRATION.md](AGENT_INTEGRATION.md)（含 API endpoint、文件命名规则、n8n 对接方案、文案模板）

## 产出在哪里

本项目的产出分布在**两个 repo + 三个 GitHub Release**：

### 文章源码和工具 → 本库

```
workspace/
├── 道德经/          classification.json + 12 篇 category essay
├── 易经/            classification.json + 12 篇 category essay
├── 黄帝内经/        classification.json + 12 篇 category essay
├── 孙子兵法/        classification.json + 10 篇 category essay
├── 几何原本/        classification.json + 8 篇 category essay
├── 庄子/            classification.json + 12 篇 category essay
├── synthesis/       10 篇跨文本综合 essay（每篇追踪 1 个 Omega 定理跨 6 部经典）
├── artifacts/       本地缓存的 NotebookLM 视频/slides/infographic
texts/               古典原文语料库（易经 64 卦、道德经 81 章等）
tools/               自动化脚本（见下方工具列表）
```

### 展示网站 → [Omega-paper-series](https://github.com/the-omega-institute/Omega-paper-series)

- **网站**: https://the-omega-institute.github.io/Omega-paper-series/
- 348 个渲染页面：76 篇 category essay + 10 篇 synthesis + 9 篇论文 + 166 个逐卦/逐章 dossier + indexes
- i18n 双语切换（EN/中文）
- 7 支旗舰 master 视频嵌入首页

### 视频/Slides → GitHub Releases（不在 repo 文件里）

| Release | 内容 | Assets | 链接 |
|---|---|---:|---|
| `cultural-media-v1` | 文化内容视频+slides+infographic | 170+ | [→ 打开](https://github.com/the-omega-institute/Omega-paper-series/releases/tag/cultural-media-v1) |
| `papers-media-v1` | 9 篇 Gen 2 论文视频+slides | 19 | [→ 打开](https://github.com/the-omega-institute/Omega-paper-series/releases/tag/papers-media-v1) |
| `master-videos-v1` | 7 支旗舰中文 master 视频 | 19 | [→ 打开](https://github.com/the-omega-institute/Omega-paper-series/releases/tag/master-videos-v1) |

**视频直链格式:**
```
https://github.com/the-omega-institute/Omega-paper-series/releases/download/{release-tag}/{filename}
```

## 当前进度

### 内容 (2026-04-13)

| 古典著作 | 分类数 | Category Essay | 逐章/逐卦 Dossier | Master 视频 |
|---|---:|---:|---:|:---:|
| 道德经 | 12 | 12 | 81 章 | 中文 |
| 易经 | 12 | 12 | 64 卦 + 21 GMS-valid | 中文 |
| 黄帝内经 | 12 | 12 | — | 中文 |
| 孙子兵法 | 10 | 10 | — | 中文 |
| 几何原本 | 8 | 8 | — | 中文 |
| 庄子 | 12 | 12 | — | 中文 |
| **跨文本综合** | — | **10** | — | — |
| **合计** | **66** | **76** | **166** | **7** |

### NotebookLM 多媒体

- ~270 个 NotebookLM notebooks（masters + mini-masters + categories + 64 卦 individual + 81 章 individual + synthesis + papers）
- 视频持续生成中，`sync_artifacts.sh` 自动下载+上传到 Release
- 预期总可发布视频: **~238 支**

### 基础设施

- MemPalace MCP server 注册到 Claude Code（26,524 drawers 语义搜索）
- 16 个 theorem 反向索引（数学侧导航）
- Broken-image handler（优雅降级未生成的 infographic）

## 管线架构

```
古典原文 (texts/)
    ↓
Claude 分类 (classification.json)
    ↓
Codex 生成文章 (workspace/{work}/generated/*.md)
    ↓
Claude 审核 (无 backflow / 定理锚点准确)
    ↓
NotebookLM 生成视频/slides/infographic
    ↓  tools/notebooklm_batch.py
    ↓  tools/build_master_notebooks.py
    ↓  tools/build_mini_masters.py
    ↓
sync_artifacts.sh → 下载到 workspace/artifacts/
    ↓
upload_to_github_release.py → 智能路由到 3 个 Release
    ↓
Omega-paper-series 展示网站自动嵌入（链接预埋）
    ↓
Ada n8n 工作流 → 社交网络自动发布
```

## 工具列表

| 脚本 | 功能 |
|---|---|
| `tools/notebooklm_batch.py` | 批量上传文章到 NotebookLM + 触发视频/slides/infographic 生成（支持 zh/en 语言 profile） |
| `tools/notebooklm_local.py` | 单文件 NotebookLM 处理 |
| `tools/build_master_notebooks.py` | 为每部作品创建 1 个 master notebook（所有内容作为 sources） |
| `tools/build_mini_masters.py` | 为每个 category 创建 mini-master notebook（category essay + 相关 dossiers） |
| `tools/sync_artifacts.sh` | 从 NotebookLM 下载新 artifacts + 上传到 GitHub Release（可 cron 挂） |
| `tools/upload_to_github_release.py` | 智能路由上传：cultural/papers/master 三个 release 自动分流 |
| `tools/rename_paper_assets.py` | 将 NotebookLM 自动命名的论文文件重命名为 canonical 前缀 |
| `tools/regenerate_chinese.py` | 清理 FAILED artifacts + 用 `language="zh"` 重新触发 |
| `tools/build_theorem_index.py` | 通过 MemPalace 语义搜索生成 theorem → cultural citations 反向索引 |
| `tools/mempalace_mcp.sh` | MemPalace MCP server wrapper（注册到 Claude Code） |

## 快速开始

```bash
# 1. 安装依赖
python3 -m venv .venv
.venv/bin/pip install notebooklm-py mempalace pyyaml

# 2. NotebookLM 登录（一次性）
notebooklm login

# 3. 查看已有 notebooks
.venv/bin/python3 tools/notebooklm_batch.py --list

# 4. 批量生成某部作品的视频
.venv/bin/python3 tools/notebooklm_batch.py --batch workspace/庄子/generated/ --type slides

# 5. 同步+上传到 Release
bash tools/sync_artifacts.sh --once

# 6. 持续轮询（每 60s）
bash tools/sync_artifacts.sh
```

## 关联项目

| 项目 | 说明 |
|---|---|
| [automath](https://github.com/the-omega-institute/automath) | Omega 数学发现引擎 — 10,588+ Lean 4 定理 |
| [Omega-paper-series](https://github.com/the-omega-institute/Omega-paper-series) | 统一展示站点 — 论文 + 文化解读 + 视频 |
| [chrono-ai-ceo](https://github.com/ChronoAIProject/chrono-ai-ceo) | Chrono AI 公司战略仓库 |

## License

MIT
