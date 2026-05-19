---
title: Claude Code 内置命令
date: 2026-05-19
tags: [coding-tool, workflow]
source_count: 1
---

# Claude Code 内置命令

> 以下命令以官方 Commands 文档为准，实际可用性以本机输入 `/` 后显示的列表为准。可见性受平台、计划、环境和版本影响。

## 会话与上下文

### /clear [name]
开启空上下文的新对话。旧对话可通过 `/resume` 找回。
- **参数**：`name` 可为旧对话命名
- **别名**：`/reset`、`/new`

### /compact [instructions]
压缩当前对话上下文，可附带聚焦说明。适合释放上下文但继续同一任务。

### /context [all]
可视化当前上下文占用情况，给出优化建议。传入 `all` 展开完整分项信息。

上下文组成：System prompt、System tools、Skills、Messages、Free spaces、Autocompact buffer。

### /resume [session]
恢复历史会话，可按 session ID 或名称恢复。
- **别名**：`/continue`

### /branch [name]
从当前点复制会话分支并切换到新分支，原会话保留。
- **参数**：`name` 为新会话命名
- **别名**：`/fork`
- **注意**：不创建工作区，并行修改同一目录会冲突。适合讨论方案后沉淀为文档，再通过 `claude --worktree` 在不同分支实现

### /btw <question>
旁路提问，不加入主对话历史。适合临时查询不污染上下文。

### /recap
生成当前会话的一句话总结。

### /rename [name]
重命名当前会话。

### /rewind
回退到更早 checkpoint，可选择恢复代码和会话、仅会话或仅代码。
- **注意**：只回退通过文件编辑工具做的修改。Bash 命令、手动修改、其他会话改动不在跟踪范围内。稳定回退请用 Git
- **别名**：`/checkpoint`、`/undo`

### /exit
退出 CLI。如附着在 background session 上会 detach，会话继续后台运行。
- **别名**：`/quit`

### /background [prompt]
将当前会话 detach 到后台，释放终端。可传入额外提示词。
- **别名**：`/bg`
- **管理**：通过 `claude agents` 监控后台 session

### /stop
停止当前 background session。仅在附着到后台会话时可用。

### /focus
切换 focus view，只显示最近一次提示、工具调用摘要和最终回复。减少长任务中的屏幕噪音。
- **要求**：仅 fullscreen 渲染模式可用，通过 `/tui fullscreen` 开启

## 模型、思考强度与使用量

### /model [model]
选择或切换模型。部分模型支持调整 effort。无参数时打开模型选择器。

### /effort [level|auto]
设置模型思考强度。可选 `low`、`medium`、`high`、`xhigh`、`max`，实际可用等级取决于模型。`auto` 恢复默认值。

### /fast [on|off]
开关 fast mode，让模型更快响应。当前仅支持 Opus 4.7 和 Opus 4.6。

### /usage
查看会话成本、计划用量限制和活动统计。
- **别名**：`/cost`

### /stats
`/usage` 的别名，默认进入 Stats 标签页。

## 文件、代码与工程操作

### /init
为项目初始化 `CLAUDE.md` 指南。设置 `CLAUDE_CODE_NEW_INIT=1` 时进入完整交互式初始化流程。

### /add-dir <path>
为当前会话添加额外工作目录。
- **注意**：默认不加载 `CLAUDE.md` 等记忆文件（需设置 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`）
- **例外**：add-dir 目录中的 `.claude/skills/` 会被自动加载

### /diff
打开交互式 diff 查看器，显示当前 git diff 和每轮对话带来的改动。左右键切换 Git diff / 单轮改动，上下键浏览文件。

### /review [PR]
审查 Pull Request 或当前分支改动。
- 不传参数：审查当前分支对应 PR，或基于当前分支改动
- 传 PR 号或 URL：审查指定 PR

### /security-review
分析当前分支改动中的安全风险。关注注入、鉴权、权限、数据泄露、敏感信息、安全边界。

### /plan [description]
进入 plan mode，适合执行前研究代码、拆解方案、形成计划。

### /goal [condition|clear]
设置持续执行目标，Claude 跨多个 turn 工作直到条件满足。`/goal clear` 清除当前目标。

## 配置、权限与集成

### /config
打开设置界面。可调整 theme、model、output style 等。
- **别名**：`/settings`

主要设置项包括：Auto-compact、Show tips、Reduce motion、Thinking mode、Prompt suggestions、Session recap、Rewind code、Verbose output、Terminal progress bar、Show turn duration、Default permission mode、Worktree base ref、Respect .gitignore in file picker、Theme、Language、Editor mode 等。

### /permissions
管理工具权限规则（`allow`/`ask`/`deny`）。
- **别名**：`/allowed-tools`

### /mcp
管理 MCP Server 连接与 OAuth 认证。排查工具或 Prompt 未出现的原因。

### /memory
编辑 `CLAUDE.md` 记忆文件，开启/关闭 auto-memory，查看 auto-memory entries。

### /agents
管理 Agent 配置。Agent 是有特定职责、工具权限、提示词配置的子代理，适合配置可复用的专业 subagent。

### /hooks
查看 Hooks 配置。Hooks 可在工具调用前后、会话结束等事件时自动执行，适合做自动格式化、日志记录、权限增强、通知。

### /plugin
管理 Claude Code 插件。插件可打包 Skills、Agents、Hooks、MCP servers、LSP servers、monitors。

### /reload-plugins
重新加载已启用插件，使变更立即生效。

### /skills
列出可用 Skills，可按 token 数排序，隐藏某些 Skill。

### /ide
管理 IDE 集成状态。连接后可共享当前打开文件、选中代码、IDE 诊断信息，支持 diff viewing、selection context、diagnostic sharing。
- **前提**：对应 IDE 需安装 Claude Code 插件

### /statusline
配置底部状态栏，显示会话状态、项目状态、Git 状态、上下文用量、token 用量等。

配置方式：
1. **自动生成**：`/statusline <自然语言描述>`
2. **手动脚本**：创建脚本（如 `~/.claude/statusline.sh`），在 `~/settings.json` 中配置

详见 [[Claude Code 状态栏配置]]。

### /keybindings
打开或创建快捷键配置文件。

### /theme
切换终端主题。

### /color [color|default]
设置当前会话输入栏颜色。`default` 恢复默认。

### /tui [default|fullscreen]
切换终端 UI 渲染模式。
- `default`：传统 CLI 滚动模式，兼容性好
- `fullscreen`：TUI 模式，输入框固定底部，支持 `/focus`

### /terminal-setup
配置终端快捷键兼容性，如 `Shift + Enter` 换行、`Option + Enter` 换行、visual bell 等。

### /sandbox
切换沙盒模式，隔离 Bash 命令对子进程、文件系统、网络的访问。
- **与权限模式的区别**：权限决定执行前是否确认，沙盒决定运行后能访问什么
- 适合在受控环境运行构建、测试、安装依赖

## 账号、诊断与辅助

### /login / /logout
登录/登出 Anthropic 账号。

### /status
查看版本、模型、账号、连接状态等。

### /doctor
检查安装与配置健康状态。

### /help
查看帮助与可用命令。

### /feedback [report]
向团队提交反馈。
- **别名**：`/bug`

### /release-notes
查看更新日志，支持选择具体版本。

### /export [filename]
导出当前会话到文件或剪贴板。

### /copy [N]
复制 Claude 的回复。`N` 表示倒数第 N 次回复。含代码块时可选择复制单个代码块或整段。

### /mobile
显示移动端下载二维码。
- **别名**：`/ios`、`/android`

### /tasks
查看和管理后台任务。
- **别名**：`/bashes`

### /insights
生成会话分析报告，分析项目领域、交互模式、常见摩擦点和使用模式。

### /powerup
通过交互式课程和动画演示快速了解功能。

### /stickers
订阅 Claude Code 贴纸。

### /team-onboarding
根据过去 30 天使用习惯生成团队上手指南。

## 相关页面

- [[Claude Code 命令类型]] — Slash Command 五类分类详解
- [[Claude Code]] — Claude Code 实体页面
- [[Claude Code 权限模式]] — 权限模式详解

## 来源

- [[Slash Command]]
