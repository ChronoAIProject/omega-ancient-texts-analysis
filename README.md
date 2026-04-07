# Omega Ancient Texts Analysis

> 古典著作自动化分析管线 — Omega 数学理论 x AI x 社交网络自动发布

## 概述

本项目构建一条端到端自动化管线：

1. **文本采集** — 从公共领域获取经典古代著作（《易经》《道德经》《几何原本》等）
2. **数学分析** — 使用 Omega 纯数学理论（基于 x²=x+1 的形式化框架）对文本进行结构性分析
3. **LLM 生成** — AI 自动生成分析报告、解读文章、多媒体内容
4. **自动发布** — 通过 n8n 工作流自动发布到社交网络（Twitter/X、LinkedIn、YouTube 等）

## 架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  Text Source │────>│ Omega Engine │────>│ LLM Content │────>│ Social Pub   │
│  古典文本    │     │  数学分析     │     │  内容生成    │     │  自动发布     │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘
       │                   │                    │                    │
   texts/             analysis/            content/             n8n/
   corpus/            omega-bridge/        templates/           workflows/
```

## 目录结构

```
omega-ancient-texts-analysis/
├── texts/                  # 古典文本语料库
│   ├── yijing/            # 《易经》
│   ├── daodejing/         # 《道德经》
│   ├── elements/          # 《几何原本》
│   └── ...
├── analysis/              # Omega 数学分析模块
│   ├── omega_bridge.py    # automath Lean4 结果桥接
│   ├── structural.py      # 结构对应分析
│   └── mapping.py         # 文本-数学映射
├── content/               # LLM 内容生成
│   ├── prompts/           # 分析提示词模板
│   ├── templates/         # 输出格式模板
│   └── generator.py       # 内容生成管线
├── publish/               # 社交网络发布
│   ├── platforms/         # 各平台适配器
│   └── scheduler.py       # 发布调度
├── n8n/                   # n8n 自动化工作流
│   └── workflows/         # 导出的 n8n 工作流 JSON
├── pipeline.py            # 主管线入口
├── config.yaml            # 管线配置
└── CLAUDE.md              # AI 工作规范
```

## 关联项目

- [automath](https://github.com/the-omega-institute/automath) — Omega 数学发现引擎（Lean 4 形式化证明）
- [chrono-ai-ceo](https://github.com/ChronoAIProject/chrono-ai-ceo) — 公司战略仓库
- Ada 的 n8n 自动化工作流 — 对外发布自动化

## 技术栈

- Python 3.10+
- n8n（工作流自动化）
- NotebookLM（多媒体生成）
- OpenAI API / Claude API（LLM 分析）
- Lean 4 结果桥接（via automath discovery export）

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 运行单篇分析
python pipeline.py --text texts/yijing/hexagram_01.txt

# 批量分析
python pipeline.py --all

# 生成内容 + 发布
python pipeline.py --all --publish
```

## 路线图

### Phase 1 (2026-04-07 ~ 04-13): 基础架构
- [ ] 文本语料库搭建（至少 3 部经典著作）
- [ ] Omega 数学分析桥接模块
- [ ] LLM 内容生成管线
- [ ] 基础 n8n 工作流

### Phase 2 (2026-04-14 ~ 04-20): 自动化闭环
- [ ] 社交网络自动发布
- [ ] NotebookLM 多媒体整合
- [ ] 定时调度 + 监控

### Phase 3: 规模化
- [ ] 更多古典文本覆盖
- [ ] 多语言内容生成
- [ ] 社区互动自动化

## License

MIT
