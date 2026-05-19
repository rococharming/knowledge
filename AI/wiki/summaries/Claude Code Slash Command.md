---
title: Claude Code Slash Command
date: 2026-05-19
tags: [coding-tool, workflow]
source_count: 1
---

# Claude Code Slash Command

Claude Code 的 Slash Command（斜杠命令）是通过 `/` 调用的快捷入口，用于控制会话、切换模型、管理权限、压缩上下文、触发工作流、调用 Skill、管理插件或执行 MCP Server 暴露的 Prompt。

## 核心内容

### 命令分类体系

Slash Command 分为五类：

1. **内置命令** — CLI 固定实现，如 `/clear`、`/model`
2. **内置 Skill** — Prompt-based workflow，如 `/batch`、`/debug`
3. **自定义 Skill** — 通过 `.claude/skills/` 创建
4. **插件命令** — 插件打包的 Skill，格式为 `/<plugin>:<skill>`
5. **MCP Prompts** — MCP Server 暴露的 Prompts，格式为 `/mcp__<server>__<prompt>`

### 内置命令速查

素材按功能将内置命令分为五大类：

- **会话与上下文**：`/clear`、`/compact`、`/context`、`/resume`、`/branch`、`/btw`、`/recap`、`/rename`、`/rewind`、`/exit`、`/background`、`/stop`、`/focus`
- **模型与使用量**：`/model`、`/effort`、`/fast`、`/usage`、`/stats`
- **文件与工程**：`/init`、`/add-dir`、`/diff`、`/review`、`/security-review`、`/plan`、`/goal`
- **配置与集成**：`/config`、`/permissions`、`/mcp`、`/memory`、`/agents`、`/hooks`、`/plugin`、`/reload-plugins`、`/skills`、`/ide`、`/statusline`、`/keybindings`、`/theme`、`/color`、`/tui`、`/terminal-setup`、`/sandbox`
- **账号与辅助**：`/login`、`/logout`、`/status`、`/doctor`、`/help`、`/feedback`、`/release-notes`、`/export`、`/copy`、`/mobile`、`/tasks`、`/insights`、`/powerup`、`/stickers`、`/team-onboarding`

### 内置 Skill 速查

- `/batch` — 大规模并行改造
- `/claude-api` — Claude API 开发参考
- `/debug` — 诊断 Claude Code 自身问题
- `/loop` — 循环运行 Prompt
- `/simplify` — 代码简化审查
- `/fewer-permission-prompts` — 生成权限 allowlist

## 关键要点

- 命令可见性受平台、计划、环境变量、Web/Remote 功能、MCP Server 连接、插件安装和版本影响
- `/branch` 会复制会话上下文但不创建工作区，并行修改同一目录会导致冲突
- `/rewind` 只回退通过文件编辑工具做的修改，Bash 命令和手动修改不在跟踪范围内
- `/statusline` 支持自动生成和手动脚本两种方式配置底部状态栏

## 相关页面

- [[Claude Code 内置命令]] — 所有内置命令的详细速查
- [[Claude Code 命令类型]] — Slash Command 五类分类详解
- [[Claude Code 状态栏配置]] — statusline 配置脚本与步骤

## 来源

- [[Slash Command]]
