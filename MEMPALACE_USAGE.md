# MemPalace Usage Guide

MemPalace 已配置为 Omega 项目的中央知识库 + 跨 session 记忆。

## 当前状态 (2026-04-11)

- **Palace 位置**: `/Users/lexa/Desktop/lexa/omega/omega-palace`
- **Config**: `/Users/lexa/Desktop/lexa/omega/mempalace.yaml`
- **Identity**: `~/.mempalace/identity.txt`
- **总 drawers**: ~10,618
  - `omega` wing: 10,000 drawers (automath, chrono-ai-ceo, papers)
  - `_users_lexa_desktop_lexa_omega` wing: 618 drawers (Claude Code 对话历史, 18 files)

## 三个使用方式

### 1. Claude Code MCP 集成（最重要）

MCP server 已注册到 user scope，所有 Claude Code session 都能直接用：

```bash
# 查看注册状态
claude mcp list

# 应该看到:
#   mempalace: /Users/lexa/.../tools/mempalace_mcp.sh - ✓ Connected
```

每个 session 开始时，Claude 会自动有 `mempalace_search` 等 19 个 tools 可用。

注册命令（已执行）：
```bash
claude mcp add mempalace --scope user -- \
  /Users/lexa/Desktop/lexa/omega/omega-ancient-texts-analysis/tools/mempalace_mcp.sh
```

### 2. Session Wake-up（每次开新 session）

在任何 Claude Code session 开始时，先跑：

```bash
~/.../.venv/bin/mempalace --palace ~/Desktop/lexa/omega/omega-palace wake-up --wing omega
```

会返回 ~870 tokens 的 L0+L1 context（身份 + 关键项目状态）。
把这个贴到 session 开头让 Claude 有背景。

### 3. CLI 搜索（写作前置）

写新文章 / 做新决定前搜一下已有内容：

```bash
MEMP=/Users/lexa/Desktop/lexa/omega/omega-ancient-texts-analysis/.venv/bin/mempalace
PALACE=/Users/lexa/Desktop/lexa/omega/omega-palace

# 找 Lean 定理
$MEMP --palace "$PALACE" search "golden mean shift No11"

# 找过去的决定
$MEMP --palace "$PALACE" search "canonical name rename paper assets"

# 找类似文化映射
$MEMP --palace "$PALACE" search "inverse limit restrict prefix"
```

## 日常维护

### 重新 mine 新增内容

```bash
cd /Users/lexa/Desktop/lexa/omega
MEMP=/Users/lexa/Desktop/lexa/omega/omega-ancient-texts-analysis/.venv/bin/mempalace
PALACE=/Users/lexa/Desktop/lexa/omega/omega-palace

# Mine code/docs (re-indexes any new files)
$MEMP --palace "$PALACE" mine /Users/lexa/Desktop/lexa/omega

# Mine Claude Code conversations
$MEMP --palace "$PALACE" mine ~/.claude/projects/-Users-lexa-Desktop-lexa-omega/ --mode convos
```

### 检查状态

```bash
$MEMP --palace "$PALACE" status
```

## 已完成的集成

- [x] Mine 整个 omega workspace (10K drawers)
- [x] Mine Claude Code conversation history (618 drawers)
- [x] Identity 配置 (`~/.mempalace/identity.txt`)
- [x] MCP server 注册到 Claude Code user scope
- [x] Session wake-up 可用

## 下一步优化

- [ ] 把 `mempalace wake-up` 加入 Claude Code SessionStart hook，自动注入 context
- [ ] 定期（每周）cron 跑 mine 同步新内容
- [ ] 修改 `build_theorem_index.py` 用 MCP tools 而不是 subprocess
- [ ] 配置 room-level 过滤以区分 cultural vs automath 检索

## 注意事项

- Conversation history 存在 `_users_lexa_desktop_lexa_omega` wing，不是默认的 `omega` wing
- 所以 `wake-up --wing omega` **不会**显示对话历史
- 要显式用 `search` 拿对话内容
