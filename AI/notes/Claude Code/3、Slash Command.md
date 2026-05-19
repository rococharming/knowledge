# 一、概述

在 `Claude Code` 的交互式会话中，`Slash Command`（斜杠命令）是通过 `/` 调用的一类快捷入口，用于控制会话、切换模型、管理权限、压缩上下文、触发工作流、调用 Skill、管理插件，或者执行 MCP Server 暴露的 Prompt。

在`Claude Code`中，输入`/`可以查看当前环境可用的命令；输入`/`继续键入字符，可以过滤命令列表。命令名后面的文本会作为参数传递给该命令。

> `Claude Code` 的命令列表不是对所有用户都完全一样。某些命令是否出现，取决于平台、账号计划、环境变量、是否启用了 Web/Remote 功能、是否连接了 MCP Server、是否安装了插件，以及当前版本是否支持

`Slash Command`大体分为五类：

1. 内置命令（Built-in commands）

由 `Claude Code CLI` 固定实现的命令，例如 `/clear`、`/compact`、`/model`、`/permissions`、`/help`、`/status` 等。

这些命令的行为通常由 CLI 程序本身实现，不是一个普通 Prompt。

2. 内置Skill（Bundled Skill）

`Claude Code` 官方随产品分发了一些 Skill，例如 `/batch`、`/debug`、`/loop`、`/simplify`、`/claude-api`、`/fewer-permission-prompts`。

它们会和内置命令一起出现在 `/` 菜单中，但本质上是 Prompt-based workflow：Claude 会读取对应 Skill 的说明，然后结合工具完成任务。

3. 自定义Skill

可以使用 Skill 来创建可复用命令。创建 `.claude/skills/<skill-name>/SKILL.md` 后，通常就可以通过 `/<skill-name>` 调用。

旧式 `.claude/commands/*.md` 自定义命令仍然兼容，但 custom commands 已经合并进 Skills，`.claude/commands/deploy.md` 和 `.claude/skills/deploy/SKILL.md` 都可以创建 `/deploy`，但 Skill 支持目录结构、辅助文件、自动触发、可见性控制等更多能力，因此现在更推荐使用 Skill。

关于 Skill 的更详细介绍参考[[5、Skill|Skill]]。

4. 插件命令 / 插件 Skill

插件可以打包 Skills、Agents、Hooks、MCP servers、LSP servers、monitors 等组件。插件中的 Skill 安装后也会变成 `/<plugin-name>:<skill-name>` 形式的快捷入口，这样可以避免与项目或个人 Skill 冲突。

关于插件的更详细介绍参考[[8、Plugin|Plugin]]。

 5. MCP Prompts 命令

MCP Server 可以暴露Prompts，这些 Prompts 会在 `Claude Code` 会话中表现为 Slash Command。格式通常是`/mcp__<server-name>__<prompt-name>`。

这些命令会从已连接的 MCP Server 动态发现。

关于MCP的更详细介绍参考[[6、MCP|MCP]]。



# 二、常用内置命令速查

> 说明：以下命令以当前官方 Commands 文档为准，但实际可用情况仍以你本机在 `Claude Code` 中输入 `/` 后显示的列表为准。命令可见性会受到平台、计划和环境影响。

## 1、会话与上下文

| 命令                        | 说明                                                                         |
| ------------------------- | -------------------------------------------------------------------------- |
| `/clear [name]`           | 开启一个空上下文的新对话。旧对话仍可通过 `/resume` 找回。可传入名称name，用于给旧对话命名。别名：`/reset`、`/new`。   |
| `/compact [instructions]` | 压缩当前对话上下文，并可附带聚焦说明。适合释放上下文但继续同一任务。                                         |
| `/context [all]`          | 可视化当前上下文占用情况，并给出上下文优化建议。传入`all`可以展开更完整的分项信息。                               |
| `/resume [session]`       | 恢复历史会话，可按 session ID 或名称恢复。别名：`/continue`。                                 |
| `/branch [name]`          | 从当前点复制一份会话分支，并切换到新分支。别名：`/fork`。                                           |
| `/btw <question>`         | 提一个旁路问题，不加入当前对话主历史。                                                        |
| `/recap`                  | 立即生成当前会话的一句话总结。                                                            |
| `/rename [name]`          | 重命名当前会话。                                                                   |
| `/rewind`                 | 回退对话或代码到更早的检查点。别名：`/checkpoint`、`/undo`。                                   |
| `/exit`                   | 退出 CLI。别名：`/quit`。如果当前附着在 background session 上，`/exit` 会 detach，会话继续在后台运行。 |
| `/background [prompt]`    | 将当前会话 detach 成后台 agent，释放当前终端。可传入一条额外提示词prompt。别名：`/bg`。                   |
| `/stop`                   | 停止当前 background session。只在附着到后台会话时可用。                                      |
| `/focus`                  | 切换 focus view，只显示最近一次提示、工具调用摘要和最终回复。仅在 fullscreen 渲染模式中可用。                 |

上述的一些命令在[[1、Claude Code入门|Claude Code入门]]中已经详细介绍，下面是一些新命令的补充介绍：

### （1）/context

`/context`用于可视化当前会话的上下文占用情况。

示例

![[Pasted image 20260519143634.png|400]]

通过上图，可以看到当前上下文的使用情况，包括 System prompt、System tools、Skills、Messages、Free spaces以及Autocompact buffer的占比。其中的 Autocompact buffer 是为自动压缩上下文预留的一块安全缓冲区。


### （2）/branch

`/branch`常用于**在保留当前会话上下文的前提下，尝试另一条对话路线**。它会复制当前会话上下文内容并进入新的对话，新会话从当前会话节点继续，原会话仍然保留，之后可通过`/resume`切回原会话。

`/branch`后可跟`name`参数，用于给新会话取名字。

![[Pasted image 20260519145213.png|500]]

`/branch`适合用于方案设计、对比、评估、解释，但不适合多个会话并行修改同一个项目目录。因为`/branch`不会创建独立工作区，如果两个会话在同一个目录并行修改同一批文件，会出现互相覆盖的问题。

不过，我们可以通过`/branch`讨论不同方案并沉淀为文档，之后通过`claude --worktree`在不同的 worktree 读取方案，并各自实现：

```shell
claude --worktree solution-a
claude --worktree solution-b
```

`--worktree` 会创建独立的 Git worktree，让两个方案在不同目录和不同分支中实现，避免互相干扰。

### （3）/btw 

 `/btw`是`Claude Code`的临时旁路提问命令。它的作用是：

> 在不污染主对话上下文的情况下，基于当前上下文问一个临时问题。

基本用法：

```text
/btw 你的问题
```

示例：

```text
/btw 刚才那个配置文件叫什么名字？
/btw 这个项目里测试命令是什么？
```


### （4）/recap

`/recap`是`Claude Code`里用于**生成当前会话回顾摘要**的命令。让 Claude Code 根据当前会话历史，快速总结“我们之前做了什么、现在进展到哪里、接下来该做什么”。

### （5）/rewind

`/rewind`是`Claude Code`的回退命令，用于打开 checkpoint 回退菜单，把对话或代码恢复到之前的某个点。

![[Pasted image 20260519154625.png|500]]

选择某个点之后，会继续让你选择恢复的内容：恢复代码和会话、恢复会话、恢复代码等。

![[Pasted image 20260519154721.png|500]]


`/rewind`可以回退两类东西：

- Conversation：当前 Claude Code 会话历史、上下文、消息记录
- Code：Claude Code 通过文件编辑工具修改过的文件状态

但注意，`/rewind`只回退`Claude Code`跟踪到的编辑行为，主要是**通过文件编辑工具做的修改**。对于 Bash 命令、你在编辑器中手动改的内容、其他终端或其他 Claude 会话改的内容，不能完全依赖 `/rewind`。因此，如果想稳定的回退代码，还是使用`Git`。


### （6）/background

`/background`把当前会话挂到后台继续跑，当前终端可以释放出来。`/background [prompt]`在挂到后台前，再给 Claude Code 发送一条额外指令。

![[Pasted image 20260519155224.png|500]]

通过执行：

```shell
claude agents
```

可以监控和管理后台 session。

![[Pasted image 20260519155647.png|500]]


### （7）/stop

`/stop`只在附着在后台会话时可用，用于停止当前的 background session。

通过`claude attch xxx`进入后台会话：

![[Pasted image 20260519182641.png|500]]

进入会话后，可执行`/stop`关闭当前后台会话：

![[Pasted image 20260519182731.png|500]]


### （8）/focus

`/focus`用于切换`focus view`。`focus view`会把界面简化成：

- 最近一次用户提示
- 一行工具调用摘要
- 最终回复

它适合在长任务或工具调用很多的场景下减少屏幕噪音。但它只在`fullscreen`渲染模式中可用，开启`fullscreen`需要执行`/tui fullscreen`。


## 2、模型、思考强度与使用量

| 命令                    | 说明                                                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `/model [model]`        | 选择或切换模型。部分模型支持在选择时调整 effort。无参数时打开模型选择器。                                                 |
| `/effort [level\|auto]` | 设置模型思考强度。可选值包括 `low`、`medium`、`high`、`xhigh`、`max`；实际可用等级取决于模型。`auto` 表示恢复模型默认值。 |
| `/fast [on\|off]`       | 开关 fast mode，针对特定模型                                                                                              |
| `/usage`                | 查看会话成本、计划用量限制和活动统计。别名：`/cost`。                                                                     |
| `/stats`                | `/usage` 的别名，但打开的 Stats 视图。                                                                                    |
### （1）/stats

`/stats`用于查看`Claude Code`的使用统计信息，它本质上等价于`/usage`，只是打开时默认进入`Stats`标签页。

![[Pasted image 20260519160905.png|500]]


### （2）/fast

`/fast` 是 Claude Code 里的快速模式开关命令，用于开启或关闭 Fast mode。开启后，可以让模型更快响应，但消耗更快。

```text
/fast [on|off]
```

Fast mode 当前只支持 Opus 4.7 和 Opus 4.6。



## 3、文件、代码与工程操作

| 命令                          | 说明                                                                    |
| --------------------------- | --------------------------------------------------------------------- |
| `/init`                     | 为项目初始化 `CLAUDE.md` 指南。设置 `CLAUDE_CODE_NEW_INIT=1` 时，会进入更完整的交互式初始化流程。  |
| `/add-dir <path>`           | 为当前会话增加一个可访问的工作目录。注意：大多数 `.claude/` 配置不会从 add-dir 目录自动发现，Skill 是重要例外。 |
| `/diff`                     | 打开交互式 diff 查看器，查看当前 git diff 以及每轮对话带来的改动。                             |
| `/review [PR]`              | 在本地当前会话中审查 Pull Request。                                              |
| `/security-review`          | 专门分析当前分支待提交变更中的安全风险。                                                  |
| `/plan [description]`       | 进入 plan mode，并可带任务描述。适合在执行前让`Claude Code`研究代码、拆解方案、形成计划。              |
| `/goal [condition\|clear]` | 设置一个目标，让`Claude`跨多个 turn 持续工作直到条件满足，也可以通过`/goal clear`清除当前目标。         |

### （1）/add-dir

`/add-dir <path>`用于在当前`Claude Code`会话中额外添加一个工作目录，让`Claude Code`可以访问这个目录里的文件。

默认情况下，`Claude Code`主要在你启动它的项目目录里工作。如果你还想让它读取或编辑另一个相关项目，就可以通过`/add-dir <path>`将指定目录加入工作目录。

通过`/add-dir`添加额外目录，默认不会加载这些目录的`CLAUDE.md`等记忆文件，如果要加载，需要设置环境变量 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`。

大多数`.claude/`配置也不会从该目录中发现，但 Skill 是重要例外，add-dir 目录中的 `.claude/skills/` 会被自动加载。


### （2）/diff

`/diff`是`Claude Code`的查看改动命令，用于打开一个交互式 diff 查看器，帮助你看清楚当前工作区里发生了哪些代码变化。它会显示当前`git diff`以及每轮对话带来的改动，通过左右方向键在当前 Git diff 和单轮 Claude 改动之间切换，用上下方向键浏览文件。

![[Pasted image 20260519180001.png|500]]


### （3）/review

`/review [PR]`是`Claude Code`的代码审查命令，用来让`Claude Code`在当前本地会话中审查一个`Pull Request`或当前分支的改动。这里的 `[PR]` 是可选参数。你不传时，它会尽量根据当前分支判断；你传时，就是明确告诉`Claude Code`要审查哪个 PR。

如果直接执行：

```text
/review
```

如果没有 PR，则会基于当前分支的改动进行代码审查。

如果在本地分支上开发完功能，已经 push 到远程并创建了 PR。此时在`Claude Code`中执行 `/review`，它会尝试审查当前分支对应的 PR 。

如果执行：

```text
/review 123
```

或者传入 PR URL：

```text
/review https://github.com/owner/repo/pull/123
```

则让`Claude Code`审查指定的PR。

### （4）/security-review

`/security-review`是`Claude Code`里的安全审查命令，用于分析当前分支里的改动，重点查找安全漏洞。

和`/review`的区别：

|命令|关注重点|
|---|---|
|`/review`|逻辑 bug、代码质量、测试、可维护性、边界情况|
|`/security-review`|注入、鉴权、权限、数据泄露、敏感信息、安全边界|

### （5）/plan 

`/plan`用于进入plan mode，并可带任务描述。适合在执行前让 `Claude Code` 研究代码、拆解方案、形成计划。


### （6）/goal

`/goal`是`Claude Code`的持续执行目标命令。它会给`Claude Code`设置一个完成条件，让`Claude Code`不需要你每一步都继续催促，而是持续工作，直到这个条件被满足。

基本用法：

```text
/goal [condition]
```

例如：

```text
/goal 所有测试通过，并且 cargo clippy 没有警告
```

意思是：`Claude Code`会持续修改、运行、检查，直到“所有测试通过，并且 cargo clippy 没有警告”这个条件满足。

## 4、 配置、权限与集成

| 命令                           | 说明                                                                 |
| ---------------------------- | ------------------------------------------------------------------ |
| `/config`                    | 打开设置界面。可调整 theme、model、output style 等。别名：`/settings`。              |
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

