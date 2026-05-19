---
title: Claude Code 命令类型
date: 2026-05-19
tags: [coding-tool, workflow]
source_count: 1
---

# Claude Code 命令类型

Claude Code 的 Slash Command 分为五类，它们在实现机制、使用方式和扩展能力上有本质区别。

## 1. 内置命令（Built-in Commands）

由 Claude Code CLI 程序固定实现的行为，不是普通 Prompt。

**特点**：
- 行为由 CLI 代码直接控制
- 所有用户环境统一可用（不受版本计划影响的部分）
- 执行效率高，不经过模型推理

**示例**：`/clear`、`/compact`、`/model`、`/permissions`、`/help`、`/status`

## 2. 内置 Skill（Bundled Skills）

官方随产品分发的 Prompt-based workflow，本质是将一套工作流提示交给 Claude，让 Claude 结合工具完成任务。

**特点**：
- 出现在 `/` 菜单中，与内置命令并列
- 由模型读取 Skill 说明后自主执行
- 可以调用工具、访问文件、执行多步骤任务

**示例**：`/batch`、`/debug`、`/loop`、`/simplify`、`/claude-api`、`/fewer-permission-prompts`

## 3. 自定义 Skill

用户或项目团队创建的可复用命令。

**创建方式**：
- 推荐：`.claude/skills/<skill-name>/SKILL.md`
- 兼容：`.claude/commands/<command>.md`

**特点**：
- Skill 支持目录结构、辅助文件、自动触发、可见性控制
- 自定义命令已合并进 Skills 体系
- 同一 Skill 可通过多个文件定义，以 `.claude/skills/` 为准

## 4. 插件命令 / 插件 Skill

插件可打包 Skills、Agents、Hooks、MCP servers、LSP servers、monitors 等组件。

**调用格式**：`/<plugin-name>:<skill-name>`

**特点**：
- 避免与项目或个人 Skill 命名冲突
- 适合团队级能力整体分发
- 安装后自动出现在 `/` 菜单中

## 5. MCP Prompts 命令

MCP Server 可以暴露 Prompts，这些 Prompts 在 Claude Code 会话中表现为 Slash Command。

**调用格式**：`/mcp__<server-name>__<prompt-name>`

**特点**：
- 从已连接的 MCP Server 动态发现
- 取决于 MCP Server 的配置和暴露能力
- 需要 `/mcp` 管理连接和 OAuth 认证

## 命令可见性影响因素

并非所有命令在所有环境中都可见，以下因素会影响 `/` 菜单的显示：

- **平台**：macOS、Windows、Linux 支持度不同
- **账号计划**：部分功能受订阅计划限制
- **环境变量**：特定功能开关
- **Web/Remote 功能**：是否启用远程功能
- **MCP Server 连接**：是否连接了暴露 Prompts 的 Server
- **插件安装**：是否安装了包含 Skill 的插件
- **版本**：当前 Claude Code 版本是否支持

## 相关页面

- [[Claude Code 内置命令]] — 内置命令完整速查
- [[Claude Code]] — Claude Code 实体页面

## 来源

- [[Slash Command]]
