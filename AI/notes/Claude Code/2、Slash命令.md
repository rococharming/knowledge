# 一、概述

在`Claude Code`的交互式会话中，`Slash Command`（斜杠命令）是通过`/`调用的一类快捷入口，用于控制会话、切换模型、触发工作流、调用Skill、调用插件能力或执行`MCP Prompt`。

在`Claude Code`中，输入`/`可以查看当前环境可用的命令；输入`/`继续键入字符，可以过滤命令列表。

`Slash`命令大体分为四类：

1. 内建命令（Built-in commands）

`Claude Code CLI`自带的固定逻辑命令，例如`/clear`、`/compact`、`/model`、`/permisssions`、`/help`。

2. Skill命令

由`SKILL.md`定义的可复用能力。Skill可以由用户手动通过`/skill-name`调用，也可以由`Claude Code`在相关场景下自动加载。旧式`.claude/commands/*.md`自定义命令已经并入Skill机制，让然兼容，但新写法推荐使用`.claude/skills/<skill-name>/SKILL.md`。详见[[4、Skill（AI生成）]]。

3. 插件命令 / 插件Skill

插件可以打包Skills、Agents、Hooks、MCP servers等能力。插件中的Skill使用命名空间调用，例如`my-plugin:hello`，这样可以避免与项目或个人`Skill`冲突。详见[[8、Plugin]]。

4. MCP Prompts命令

MCP Server 可以暴露Prompts，这些Prompts会在`Claude Code`会话中表现为`Slash`命令，格式通常是`/mcp__<server-name>__<prompt-name>`，例如`mcp__github__pr_review 456`。详见[[6、MCP]]。


# 二、内置命令与内置Skill的区别

`Claude Code`的`/`菜单既包含内置命令，也包含内置Skill。

- 内置命令：由`Claude Code CLI`固定实现，例如`/clear`、`/model`、`/compact`等。
- 内置Skill：本质是`Anthropic`随`Claude Code`分发的Skill，例如`/batch`、`/debug`、`/loop`、`/simplify`、`claude-api`等。


# 三、常用内置命令速查

> 说明：以下是常见命令。实际可用命令列表以`Claude Code`输入`/`后显示的结果为准。

## 1、会话与上下文

| 命令                        | 说明                                                    |
| ------------------------- | ----------------------------------------------------- |
| `/clear`                  | 开启一个空上下文的新会话。旧会话仍可通过 `/resume` 找回。别名：`/reset`、`/new`。 |
| `/compact [instructions]` | 压缩当前对话上下文，并可附带聚焦说明。适合释放上下文但继续同一任务。                    |
| `/context`                | 可视化当前上下文占用情况/                                         |
| `/resume [session]`       | 恢复历史会话。别名：`/continue`。                                |
| `/branch [name]`          | 把当前会话复制一份，创建一个新的会话分支。别名：`/fork`。                      |
| `/btw <question>`         | 提一个旁路问题，不加入当前对话主历史。                                   |
| `/recap`                  | 立即生成当前会话的一句话总结。                                       |
| `/rename [name]`          | 重命名当前会话。                                              |
| `/rewind`                 | 回退对话或代码到更早的检查点。别名：`/checkpoint`、`/undo`。              |
| `/exit`                   | 退出 CLI。别名：`/quit`。                                    |

## 2、模型、思考强度与使用量


| 命令                      | 说明                                                                |
| ----------------------- | ----------------------------------------------------------------- |
| `/model [model]`        | 选择或切换模型。部分模型支持在选择时调整 effort。                                      |
| `/effort [level\|auto]` | 设置模型思考强度。可选值通常包括 `low`、`medium`、`high`、`xhigh`、`max`，具体取决于模型支持情况。 |
| `/usage`                | 查看会话成本、计划用量限制和活动统计。                                               |
| `/cost`                 | `/usage` 的别名。                                                     |
| `/stats`                | `/usage` 的别名，会打开 Stats 视图。                                        |
| `/fast [on\|off]`       | 开关 fast mode，针对特定模型                                               |

## 3、文件、代码与工程操作

| 命令                    | 说明                                                                 |
| --------------------- | ------------------------------------------------------------------ |
| `/init`               | 为项目初始化 `CLAUDE.md` 指南。                                             |
| `/add-dir <path>`     | 为当前会话增加一个可访问的工作目录。注意大多数 `.claude/` 配置不会从 add-dir 目录自动发现，Skill 是例外。 |
| `/diff`               | 打开交互式 diff 查看器，查看当前 git diff 以及每轮对话带来的改动。                          |
| `/review [PR]`        | 在本地当前会话中审查 Pull Request。现在不推荐使用该命令，推荐安装`code-review`插件进行审查。        |
| `/security-review`    | 专门分析当前分支待提交变更中的安全风险。                                               |
| `/plan [description]` | 进入 plan mode，并可带任务描述。适合在执行前让`Claude Code`研究代码、拆解方案、形成计划。           |

## 4、 配置、权限与集成

| 命令                           | 说明                                                                 |
| ---------------------------- | ------------------------------------------------------------------ |
| `/config`                    | 打开设置界面。别名：`/settings`。                                             |
| `/permissions`               | 管理工具权限规则。别名：`/allowed-tools`。                                      |
| `/mcp`                       | 管理 MCP Server 连接与 OAuth 认证。                                        |
| `/memory`                    | 编辑 `CLAUDE.md` 记忆文件，开启或关闭自动记忆。                                     |
| `/agents`                    | 管理 Agent 配置。                                                       |
| `/hooks`                     | 查看 Hooks 配置。                                                       |
| `/plugin`                    | 管理 Claude Code 插件。                                                 |
| `/reload-plugins`            | 重新加载已启用插件，使插件内的 Skills、Agents、Hooks、MCP Servers、LSP Servers 等变更生效。 |
| `/ide`                       | 管理 IDE 集成并查看状态。                                                    |
| `/statusline`                | 配置 Claude Code 底部状态栏。                                              |
| `/keybindings`               | 打开或创建快捷键配置文件。                                                      |
| `/theme`                     | 切换 Claude Code 终端主题。                                               |
| `/color [color\|default]`    | 设置当前会话输入栏 / prompt bar 颜色。使用 `default` 可恢复默认颜色。                    |
| `/tui [default\|fullscreen]` | 切换终端 UI 渲染模式。                                                      |
| `/terminal-setup`            | 配置终端快捷键，例如 Shift/Option + Enter 换行等。                               |
| `/sandbox`                   | 切换沙盒模式。仅在支持的平台可用。                                                  |

## 5、账号、诊断与辅助

| 命令                   | 说明                                        |
| -------------------- | ----------------------------------------- |
| `/login`             | 登录 Anthropic 账号。                          |
| `/logout`            | 登出当前账号。                                   |
| `/status`            | 查看版本、模型、账号、连接状态等。                         |
| `/doctor`            | 检查 Claude Code 安装与配置健康状态。                 |
| `/help`              | 查看帮助与可用命令。                                |
| `/feedback [report]` | 向 Claude Code 团队提交反馈。别名：`/bug`。           |
| `/release-notes`     | 查看 Claude Code 更新日志。                      |
| `/export [filename]` | 导出当前会话到文件或剪贴板。                            |
| `/copy [N]`          | 复制最近一次或第 N 近的 Claude 回复。                  |
| `/mobile`            | 显示移动端二维码。别名：`/ios`、`/android`。            |
| `/tasks`             | 查看和管理后台任务。别名：`/bashes`。                   |
| `/insights`          | 生成`Claude Code`会话分析报告，例如分析常做什么、常见摩擦点和使用模式 |
| `/powerup`           | 通过简短的交互式课程和动画演示，快速了解 Claude Code 功能。      |
| `/sticks`            | 订阅`Claude Code`贴纸                         |

## 6、团队协作与上手
| 命令                 | 说明                                                                     |
| ------------------ | ---------------------------------------------------------------------- |
| `/team-onboarding` | 根据你过去 30 天的 Claude Code 使用习惯，生成一份给同事上手 Claude Code 的指南。适合团队内部推广或沉淀工作流。 |

# 四、内置Skill命令速查

`Claude Code`官方内置了一些 Skill，它们会和内置命令一起显示在 `/` 菜单中，但本质是 Prompt-based workflow。

| 命令                                              | 说明                                                                                                                       |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `/batch <instruction>`                          | \|大规模并行改造。它会先研究代码库，把任务拆成5-30个独立单元，给你看计划。等你同意后，会在独立的git worktree里启动多个后台agent并行干活、跑测试、开PR。适合大型迁移、跨很多文件重构。\|                |
| `/claude-api [migrate\|managed-agents-onboard]` | 为 Claude API / Anthropic SDK 开发加载参考材料，覆盖 tool use、streaming、batches、structured outputs 等。也可用于迁移旧模型调用或引导创建 Managed Agent。 |
| `/debug [description]`                          | 为当前会话开启 debug logging，并读取 debug log 排查问题。如果不是用 `claude --debug` 启动，则从执行 `/debug` 那一刻开始记录日志。                              |
| `/loop [interval] [prompt]`                     | 在当前会话保持打开时循环运行 Prompt。可指定间隔，也可让 Claude 自行控制节奏。别名：`/proactive`。                                                           |
| `/simplify [focus]`                             | 检查最近变更的文件，寻找代码复用、质量和效率问题，并尝试修复。                                                                                          |
| `/fewer-permission-prompts`                     | 分析你过去常用的只读命令和 MCP 工具调用，自动生成一组推荐的允许规则，减少以后反复弹出的权限确认。适合觉得 Claude Code 经常问“是否允许执行这个命令？”时使用。                                 |

