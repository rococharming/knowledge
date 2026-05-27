---
title: Claude Code Memory 系统
date: 2026-05-28
tags: [coding-tool, memory, workflow]
source_count: 1
---

# Claude Code Memory 系统

本文档系统梳理了 Claude Code 跨会话持久化记忆的完整机制，包括手动维护的 `CLAUDE.md` 和自动维护的 `auto memory` 两大体系。

## 核心架构

Claude Code 每次会话从新的上下文窗口开始，跨会话保留背景主要依赖两类机制：

| 机制 | 维护者 | 定位 |
|---|---|---|
| `CLAUDE.md` | 用户手动编写 | 事先约定：编码规范、工作流、项目规则 |
| `auto memory` | Claude Code 自动维护 | 使用中学习：调试经验、构建命令、偏好 |

两者互补：`CLAUDE.md` 保证基础行为一致，`auto memory` 让 Claude Code 逐渐适应具体项目和使用者习惯。

## CLAUDE.md 体系

`CLAUDE.md` 是提供跨会话持久指令的 Markdown 文件，支持多级作用范围：

- **托管策略**（系统级）：组织统一指令
- **用户指令**（`~/.claude/CLAUDE.md`）：个人全局偏好
- **项目指令**（`./CLAUDE.md`）：项目团队共享规则
- **本地指令**（`./CLAUDE.local.md`）：个人本地偏好（应加入 `.gitignore`）

加载规则：从当前目录向上查找，上层先加载，越靠近当前目录的指令越晚出现、优先级越高。支持 `@path` 导入其他文件，递归深度最多 5 层。

`.claude/rules/` 可将规则按路径拆分，通过 `YAML frontmatter` 的 `paths` 字段限定生效范围。

## Auto Memory 体系

`auto memory` 让 Claude Code 自动跨会话积累项目知识，包括构建命令、调试经验、代码风格偏好、工作流习惯等。

- 默认**开启**，可通过 `/memory` 命令、项目设置或环境变量控制
- 存储于 `~/.claude/projects/<project>/memory/`
- `MEMORY.md` 为索引文件（启动时加载前 200 行或 25 KB）
- 主题文件（如 `debugging.md`）按需读取

## 关键主题页面

- [[CLAUDE.md]] — CLAUDE.md 的完整概念与规则体系
- [[Auto Memory]] — 自动记忆的机制、启用方式与存储结构
- [[Claude Code 记忆配置]] — 记忆系统的配置与使用步骤

## 来源

- [[Memory]]
