
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

通过`claude attach xxx`进入后台会话：

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
| `/permissions`               | 管理工具权限规则，包括`allow`、`ask`、`deny`。别名：`/allowed-tools`。               |
| `/mcp`                       | 管理 MCP Server 连接与 OAuth 认证。                                        |
| `/memory`                    | 编辑 `CLAUDE.md` 记忆文件，开启或关闭`auto memory`，并查看 auto-memory entries。    |
| `/agents`                    | 管理 Agent 配置。                                                       |
| `/hooks`                     | 查看 Hooks 配置。                                                       |
| `/plugin`                    | 管理 Claude Code 插件。                                                 |
| `/reload-plugins`            | 重新加载已启用插件，使插件内的 Skills、Agents、Hooks、MCP Servers、LSP Servers 等变更生效。 |
| `/skills`                    | 查看可用 Skills，并可以隐藏某些 Skill。                                         |
| `/ide`                       | 管理 IDE 集成并查看状态。                                                    |
| `/statusline`                | 配置 Claude Code 底部状态栏。                                              |
| `/keybindings`               | 打开或创建快捷键配置文件。                                                      |
| `/theme`                     | 切换 Claude Code 终端主题。                                               |
| `/color [color\|default]`    | 设置当前会话输入栏 / prompt bar 颜色。使用 `default` 可恢复默认颜色。                    |
| `/tui [default\|fullscreen]` | 切换终端 UI 渲染模式。                                                      |
| `/terminal-setup`            | 配置终端快捷键，例如 Shift/Option + Enter 换行等。                               |
| `/sandbox`                   | 切换沙盒模式。仅在支持的平台可用。                                                  |

### （1）/config

`/config`用于打开`Claude Code`的设置界面，如下：

![[Pasted image 20260519195535.png|400]]

| 设置项                                       |                 当前值 | 含义                                                                                                                        |
| ----------------------------------------- | ------------------: | ------------------------------------------------------------------------------------------------------------------------- |
| `Auto-compact`                            |              `true` | 自动压缩上下文。会话变长、上下文接近上限时，Claude Code 会把较早内容压缩成摘要，避免上下文被耗尽。                                                                   |
| `Show tips`                               |              `true` | 是否在等待 Claude 处理时显示提示，例如 `Tip: Use git worktrees to run multiple Claude sessions in parallel.`                             |
| `Reduce motion`                           |             `false` | 是否减少终端界面的动画效果，例如 spinner、loading 动画、闪烁或 shimmer 效果。只影响显示，不影响模型能力。                                                         |
| `Thinking mode`                           |              `true` | 是否默认启用 extended thinking。对应设置项是 `alwaysThinkingEnabled`。                                                                  |
| `Prompt suggestions`                      |              `true` | 是否显示 prompt 建议，帮助你快速输入常见任务或继续操作。                                                                                          |
| `Session recap`                           |              `true` | 是否显示会话回顾。你离开终端一段时间再回来时，Claude Code 可以显示一行当前会话摘要。                                                                          |
| `Rewind code (checkpoints)`               |              `true` | 是否启用代码回退 / checkpoint 功能。Claude Code 修改代码时可以记录检查点，方便回滚。                                                                   |
| `Verbose output`                          |             `false` | 是否显示更详细的会话记录。关闭时输出更紧凑；开启后会显示更多工具调用和过程信息。                                                                                  |
| `Terminal progress bar`                   |              `true` | 是否在支持的终端里显示任务进度条。只影响终端显示，不影响执行速度或权限。                                                                                      |
| `Show turn duration`                      |              `true` | 是否显示每一轮耗时，例如 `Cooked for 4s`、`Baked for 2s`。对应 `showTurnDuration`。                                                        |
| `Default permission mode`                 |           `Default` | 默认权限模式，决定 Claude Code 执行编辑、Bash、工具调用等操作时如何请求确认。有效值包括 `default`、`acceptEdits`、`plan`、`auto`、`dontAsk`、`bypassPermissions`。 |
| `Worktree base ref`                       |             `fresh` | 创建 Claude Code 隔离 worktree 时使用的基准引用。`fresh` 通常表示从远端默认分支如 `origin/main` 创建干净起点；`head` 表示从当前本地 `HEAD` 创建。                   |
| `Use auto mode during plan`               |              `true` | Plan Mode 中是否使用 Auto Mode 语义。开启后，在支持 Auto Mode 的情况下，Plan 阶段可以采用更自动化的权限处理逻辑。                                               |
| `Respect .gitignore in file picker`       |              `true` | 在 `@` 文件选择器中是否尊重 `.gitignore`。开启后，被 `.gitignore` 忽略的文件一般不会出现在文件建议里。                                                       |
| `Skip the /copy picker`                   |             `false` | 执行 `/copy` 时是否跳过选择器。`false` 表示执行 `/copy` 时通常会让你选择要复制的内容。                                                                  |
| `Open agents view by default`             |             `false` | 是否默认打开 agents 后台任务视图。你截图里的 agents 视图可以显示当前 session、后台运行任务、已完成任务等。                                                         |
| `← opens agents`                          |              `true` | 是否允许在 fullscreen 界面中按左方向键 `←` 打开 agents 视图。右方向键 `→` 可以返回当前会话。                                                             |
| `Auto-update channel`                     |            `latest` | Claude Code 自动更新通道。`latest` 更快获得新功能和修复；`stable` 更偏稳定。                                                                     |
| `Theme`                                   |         `Dark mode` | Claude Code 的界面主题。当前是深色模式。终端主题相关配置也可以参考终端配置文档。                                                                            |
| `Local notifications`                     |              `Auto` | 本地通知策略。通常用于 Claude 完成任务、需要输入或发生重要状态变化时的系统通知；`Auto` 表示由 Claude Code 根据环境自动决定。                                              |
| `Output style`                            |           `default` | 输出风格。控制 Claude Code 回复的默认表达风格。`default` 表示使用默认输出样式。                                                                       |
| `Language`                                | `Default (English)` | Claude Code UI / 默认交互语言。当前是默认英文。注意这不等于你不能用中文提问；你仍然可以直接用中文和它对话。                                                            |
| `Editor mode`                             |            `normal` | 输入编辑模式。`normal` 是普通编辑模式；如果切换到 Vim 模式，输入框会更接近 Vim keybindings。终端配置文档中也提到可以配置 Vim keybindings。                              |
| `Show last response in external editor`   |             `false` | 是否在外部编辑器里显示 Claude 的上一条回复。关闭时，上一条回复只在 Claude Code 界面中显示。                                                                  |
| `Show PR status footer`                   |              `true` | 是否在底部显示 PR 状态信息。适合在 GitHub PR / 分支工作流中查看当前 PR 相关状态。                                                                       |
| `Model`                                   |   `kimi-for-coding` | 当前 Claude Code 实际使用的模型名称。你这里显示的是第三方 / 兼容网关映射后的模型名，不一定是 Anthropic 官方模型名。                                                   |
| `Auto-connect to IDE (external terminal)` |             `false` | 在外部终端启动 Claude Code 时，是否自动连接 IDE。关闭时不会自动连接，需要你手动或通过相关集成连接。                                                                |
| `Claude in Chrome enabled by default`     |              `true` | 是否默认启用 Claude in Chrome 相关能力。开启后，相关浏览器集成功能在支持环境下默认可用。                                                                     |
| `Use custom API key: ...`                 |              `true` | 是否使用自定义 API key。为 `true`说明当前 Claude Code 使用了自定义 API key；                                                                  |

### （2）/permissions

`permissions`用于管理`Claude Code`的工具权限规则。

它可以管理三类规则：

| 规则    | 说明         |
| ----- | ---------- |
| allow | 自动允许某些工具调用 |
| ask   | 执行前询问你     |
| deny  | 拒绝某些工具调用   |

![[Pasted image 20260519210640.png|500]]

在权限界面中，可以查看、添加和删除规则、管理Workspace（工作目录）、并查看`auto`模式下最近拒绝的操作（Recently denied）。


### （3）/mcp

`/mcp`用于管理 MCP Server 连接和 OAuth 认证。

常见用途包括：

- 查看当前 MCP Server 是否已连接
- 处理需要认证的 MCP Server
- 管理 OAuth 登录状态
- 排查 MCP 工具或 Prompt 没出现的原因

如果某个 MCP Server 暴露了 prompts，它们会以 `/mcp__<server>__<prompt>` 形式出现在 Slash Command 中。


### （4）/memory

`/memory`用于编辑`CLAUDE.md`记忆文件，开启或关闭 auto-memory，并查看 auto-memory entries。

![[Pasted image 20260519211918.png|500]]


### （5）/agents

`/agents` 用于管理 Agent 配置。

Agent 可以理解为有特定职责、工具权限、提示词配置的子代理。比如专门做代码搜索、测试修复、文档整理、架构分析等。

`/agents`适合在项目中配置可复用的专业subagent。

![[Pasted image 20260519212207.png|500]]

在`/agents`页面下可以查看运行中的子代理、创建子代理。

### （6）/hooks

`/hooks`用于查看工具事件相关的 Hooks 配置。

Hooks 可以在特定事件发生时自动执行，比如工具调用前、工具调用后、会话结束等。它适合用来做自动格式化、日志记录、权限增强、通知等自动化操作。

![[Pasted image 20260519213124.png|500]]

### （7）/plugin

`/plugin`用于管理`Claude Code`插件。

插件可以打包多种扩展能力，包括：

- Skills
- Agents
- MCP servers
- LSP servers
- monitors

![[Pasted image 20260519213157.png|500]]

插件适合把一组项目或团队常用能力整体分发。


### （8）/reload-plugins

`/reload-plugins` 用于重新加载已启用插件，使插件中的变更立即生效，而不必重启 Claude Code。

它会报告重新加载的组件数量，并提示加载错误。

### （9）/skills

`/skills` 用于列出当前可用的 Skills。

在列表中可以：

- 查看 skills
- 按 token 数排序
- 隐藏某些 Skill，使其不再出现在 `/` 菜单或不再被 Claude 自动使用

![[Pasted image 20260519213425.png|500]]

### （10）/ide

`ide`用于管理`Claude Code`和`IDE`的连接状态。

它主要解决的是：**你虽然在 Terminal 里运行 Claude Code，但希望 Claude Code 能和当前打开的编辑器协同工作**。

连接 IDE 后，Claude Code 不只是一个普通终端程序，还能和编译器共享更多上下文，例如当前打开的文件、选中的代码、IDE诊断信息，并可以把diff展示到 IDE 的 diff viewer中。Claude Code 的 VS Code 和 JetBrains 集成都支持这类能力，包括 diff viewing、selection context、diagnostic sharing 等。

> 前提：对应 IDE 要安装 Claude Code 插件

执行`/ide`后，Claude Code 会打开 IDE 集成管理界面，用来查看当前是否已经连接 IDE，或者选择要连接的 IDE。

如下图所示：

![[Pasted image 20260519215748.png|500]]

在 IDE 中选中对应代码，Claude Code可以直接感知并操作，修改的代码会以diff view 形式显示在 VS Code 中：

![[Pasted image 20260519220044.png|500]]

### （11）/statusline

`/statusline`用于配置`Claude Code`的底部状态栏。

它的核心作用是：**把你关心的会话状态、项目状态、Git 状态、上下文用量、token 用量等信息，固定显示在 Claude Code 底部，方便随时查看**。

可以把它理解成 Claude Code 里的“终端状态栏”，例如一个示例：

```
模型 | 推理强度 | Thinking | 版本
当前项目路径 | Git 分支
上下文使用情况 | 上下文窗口大小 | token 用量
本轮输入输出 | cache 写入 | cache 读取
```

`statusline`的两种配置方式：

1. 用`/statusline`自动生成

最简单的方式是直接在`Claude Code`中输入自然语言描述：

```
/statusline 显示当前模型名称、Git 分支和上下文使用百分比，并用进度条展示上下文占用情况
```

Claude Code 会根据描述生成脚本，并自动更新配置。

这种方式适合简单状态栏。

2. 手动写脚本

如果状态栏比较复杂，比如多字段、带颜色、带进度条的状态栏，更适合手动写脚本。

一般流程：

- 创建脚本，例如 `~/.claude/statusline.sh`

示例：

```shell
#!/usr/bin/env bash

input="$(cat)"

# ---------- Colors ----------
RESET="\033[0m"
BOLD="\033[1m"

BLUE="\033[38;5;39m"
GREEN="\033[38;5;82m"
YELLOW="\033[38;5;220m"
ORANGE="\033[38;5;208m"
PURPLE="\033[38;5;141m"
CYAN="\033[38;5;51m"
RED="\033[38;5;203m"
GRAY="\033[38;5;245m"
LIGHT_GRAY="\033[38;5;250m"

# ---------- Basic fields ----------
MODEL="$(echo "$input" | jq -r '.model.display_name // .model.id // "unknown-model"')"
EFFORT="$(echo "$input" | jq -r '.effort.level // "n/a"')"
THINKING_ENABLED="$(echo "$input" | jq -r '.thinking.enabled // false')"
VERSION="$(echo "$input" | jq -r '.version // "unknown"')"

DIR="$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "."')"

# ---------- Git branch ----------
if git -C "$DIR" rev-parse --git-dir >/dev/null 2>&1; then
  BRANCH="$(git -C "$DIR" branch --show-current 2>/dev/null)"
  if [ -z "$BRANCH" ]; then
    BRANCH="$(git -C "$DIR" rev-parse --short HEAD 2>/dev/null)"
  fi
else
  BRANCH="no-git"
fi

# ---------- Thinking ----------
if [ "$THINKING_ENABLED" = "true" ]; then
  THINKING="Thinking"
  THINKING_COLOR="$PURPLE"
else
  THINKING="No Thinking"
  THINKING_COLOR="$GRAY"
fi

# ---------- Context window ----------
USED_PCT_RAW="$(echo "$input" | jq -r '.context_window.used_percentage // 0')"
FREE_PCT_RAW="$(echo "$input" | jq -r '.context_window.remaining_percentage // 0')"

USED_PCT="${USED_PCT_RAW%.*}"
FREE_PCT="${FREE_PCT_RAW%.*}"

WINDOW_SIZE="$(echo "$input" | jq -r '.context_window.context_window_size // 0')"
TOTAL_IN="$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')"
TOTAL_OUT="$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')"

# ---------- Current API usage ----------
CUR_IN="$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0')"
CUR_OUT="$(echo "$input" | jq -r '.context_window.current_usage.output_tokens // 0')"
CUR_CRT="$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')"
CUR_RD="$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')"

# ---------- Format tokens ----------
fmt_tokens() {
  local n="$1"

  if [ -z "$n" ] || [ "$n" = "null" ]; then
    echo "0"
  elif [ "$n" -ge 1000000 ] 2>/dev/null; then
    awk -v n="$n" 'BEGIN { printf "%.1fM", n/1000000 }'
  elif [ "$n" -ge 1000 ] 2>/dev/null; then
    awk -v n="$n" 'BEGIN { printf "%.0fK", n/1000 }'
  else
    echo "$n"
  fi
}

# ---------- Compact progress bar ----------
BAR_WIDTH=10
FILLED=$((USED_PCT * BAR_WIDTH / 100))
EMPTY=$((BAR_WIDTH - FILLED))

BAR=""
if [ "$FILLED" -gt 0 ]; then
  printf -v FILL "%${FILLED}s"
  BAR="${FILL// /█}"
fi

if [ "$EMPTY" -gt 0 ]; then
  printf -v PAD "%${EMPTY}s"
  BAR="${BAR}${PAD// /░}"
fi

# ---------- Output ----------
echo -e "${BLUE}${BOLD}${MODEL}${RESET} ${GRAY}|${RESET} ${YELLOW}${EFFORT}${RESET} ${GRAY}|${RESET} ${THINKING_COLOR}${THINKING}${RESET} ${GRAY}|${RESET} ${GREEN}v${VERSION}${RESET}"

echo -e "${CYAN}${DIR}${RESET} ${GRAY}|${RESET} ${ORANGE}${BRANCH}${RESET}"

echo -e "${PURPLE}Cxt:${RESET} ${LIGHT_GRAY}${BAR}${RESET} ${YELLOW}${USED_PCT}%${RESET}/${CYAN}${FREE_PCT}%${RESET} ${GRAY}|${RESET} ${BLUE}Size:${RESET} $(fmt_tokens "$WINDOW_SIZE") ${GRAY}|${RESET} ${GREEN}In:${RESET}$(fmt_tokens "$TOTAL_IN") ${ORANGE}Out:${RESET}$(fmt_tokens "$TOTAL_OUT")"

echo -e "${GRAY}Usage:${RESET} ${GREEN}In:${RESET}$(fmt_tokens "$CUR_IN") ${ORANGE}Out:${RESET}$(fmt_tokens "$CUR_OUT") ${YELLOW}Crt:${RESET}$(fmt_tokens "$CUR_CRT") ${CYAN}Rd:${RESET}$(fmt_tokens "$CUR_RD")"
```

- 在`~/settings.json`中添加`statusLine`配置

```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0,
    "refreshInterval": 5
  }
}
```

之后，启动`Claude Code`，就可以看到如下的状态栏了：

![[Pasted image 20260519224809.png]]


### （12）/keybindings

`/keybindings` 用于打开或创建快捷键配置文件。它适合在你想自定义 Claude Code 的键盘操作时使用，比如调整某些快捷键或适配自己的终端习惯。

### （13）/theme

`/theme` 用于切换 Claude Code 终端主题。

![[Pasted image 20260519225804.png|500]]


### （14）/color

`/color [color|default]` 用于设置当前会话框的颜色。

![[Pasted image 20260519225853.png|500]]

例如，下面设置为了紫色：

![[Pasted image 20260519225924.png|500]]


### （15）/tui

`/tui [default|fullscreen]`用于设置**终端UI渲染模式**。

`default`是普通终端渲染模式。它更接近传统CLI程序：内容直接打印在当前终端的滚动区里。优点是简单、兼容性好，终端历史记录也更自然；缺点是长任务、复杂工具调用、多轮输出时，界面可能比较乱，也更容易闪烁。

`fullscreen` 会启用 fullscreen / alt-screen renderer，使 Claude Code 以更完整的 TUI 方式运行，输入框固定在底部，适合长任务和复杂工具调用场景。`/focus` 等功能需要 fullscreen renderer 才能使用。

![[Pasted image 20260519230701.png|500]]

### （16）/terminal-setup

`/terminal-setup` 用于配置当前终端与 Claude Code 的快捷键兼容性，典型用途是让 `Shift + Enter` 可以在输入框中插入换行，而不是提交 prompt。

在 macOS Terminal.app 里，`Option` 键默认可能被当作用来输入特殊字符的键，比如 `Option + Enter`用于换行。

`bell`是终端里的提醒机制，以前可能是发出提示音，现在切换成 `visual bell` 后，提醒会以视觉方式出现，比如窗口闪一下、标签页提示、Dock 图标出现提醒点等，而不是发出声音。

![[Pasted image 20260519231137.png|500]]



### （17）/sandbox

`/sandbox`用于切换或配置`Claude Code`的沙盒模式。沙盒模式会在支持的平台上隔离Bash命令，限制命令对子进程、文件系统、网络的访问范围。它和权限模式不同：**权限模式决定执行前是否需要确认，沙盒决定命令运行后能访问什么**。沙盒适合在更受控的环境中运行构建、测试、安装依赖或未知脚本，降低对宿主环境的影响。

执行`/sandbox`的界面如下：

![[Pasted image 20260519231725.png|500]]

这里有三个选项：

- Sandbox BashTool, with auto-allow：Bash 命令优先放进沙盒里运行，并且在沙盒内运行的命令可以自动允许。
- Sandbox BashTool, with regular permissions：Bash 命令会放进沙盒里运行，但仍然按照普通权限规则询问你。
- No Sandbox：不开启沙盒

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
| `/stickers`            | 订阅`Claude Code`贴纸                         |

### （1）/status

`/status` 用于打开 Settings 界面的 Status 标签页，查看当前 Claude Code 状态。它可以在 Claude 正在响应时执行，不需要等待当前响应结束。

![[Pasted image 20260519232240.png|500]]

### （2）/doctor

`/doctor` 用于诊断 Claude Code 安装与配置健康状态。

![[Pasted image 20260519232505.png|500]]

### （3）/help

`/help` 用于查看帮助与可用命令。

它适合快速确认当前版本、当前环境下有哪些 Slash Command 可用。

### （4）/feedback

`/feedback [report]` 用于向`Claude Code`团队提交反馈。

### （5）/release-notes

`/release-notes` 用于查看 Claude Code 更新日志。

它会打开交互式版本选择器，可以选择某个具体版本查看更新内容，也可以查看所有版本。


### （6）/export

`/export [filename]` 用于导出当前会话。

常用形式：

```text
/export
/export session-notes.txt
```

不传文件名时，会打开对话框，让你选择复制到剪贴板或保存为文件；传入文件名时，会直接写入对应文件。


### （7）/copy

`/copy [N]` 用于复制 Claude 的回复。

常用形式：

```
/copy
/copy 2
```

`/copy` 复制最近一次 Claude 回复；`/copy 2` 复制倒数第二次 Claude 回复。

如果回复中包含代码块，会打开交互式选择器，让你选择复制单个代码块或整段回复。

### （8）/mobile

`/mobile` 用于显示 Claude mobile app 的下载二维码。

### （9）/tasks

`/tasks` 用于查看和管理后台任务。

它适合查看当前 session 中仍在运行的后台任务，例如长时间运行的命令、测试、构建等。

### （10）/insights

`/insights` 用于生成 Claude Code 会话分析报告。

它会分析你的 Claude Code sessions，包括项目领域、交互模式和常见摩擦点。

适合用来回答：

- 我最近主要用 Claude Code 做什么？
- 哪些任务最常出现问题？
- 我的使用模式有什么可以优化的地方？
- 哪些项目或命令最常被使用？

### （11）/powerup

`/powerup` 用于通过简短的交互式课程和动画演示，快速了解 Claude Code 功能。

它适合刚开始使用 Claude Code，或者想系统了解新功能时使用。


### （12）/stickers

`/stickers` 用于订购 Claude Code 贴纸。

## 6、团队协作与上手

| 命令                 | 说明                                                                     |
| ------------------ | ---------------------------------------------------------------------- |
| `/team-onboarding` | 根据你过去 30 天的 Claude Code 使用习惯，生成一份给同事上手 Claude Code 的指南。适合团队内部推广或沉淀工作流。 |

# 三、内置Skill命令速查

`Claude Code` 内置了一些 Skill。它们会和内置命令一起显示在 `/` 菜单中，但本质是 Prompt-based workflow。内置命令通常是 CLI 固定逻辑；内置 Skill 则是把一套工作流提示交给 Claude，让 Claude 结合工具完成任务。

| 命令                                              | 说明                                                                                                                       |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `/batch <instruction>`                          | \|大规模并行改造。它会先研究代码库，把任务拆成5-30个独立单元，给你看计划。你同意后，会在独立的git worktree里启动多个后台agent并行干活、跑测试、开PR。适合大型迁移、跨很多文件重构。\|                 |
| `/claude-api [migrate\|managed-agents-onboard]` | 为 Claude API / Anthropic SDK 开发加载参考材料，覆盖 tool use、streaming、batches、structured outputs 等。也可用于迁移旧模型调用或引导创建 Managed Agent。 |
| `/debug [description]`                          | 用于诊断 Claude Code 自身的问题。开启 debug logging，并读取 debug log 排查问题。如果不是用 `claude --debug` 启动，则从执行 `/debug` 那一刻开始记录日志。            |
| `/loop [interval] [prompt]`                     | 在当前会话保持打开时循环运行 Prompt。可指定间隔，也可让 Claude 自行控制节奏。别名：`/proactive`。                                                           |
| `/simplify [focus]`                             | 检查最近变更的文件，寻找代码复用、质量和效率问题，并尝试修复。会并行启动三个 review agents，聚合发现后应用修复。                                                          |
| `/fewer-permission-prompts`                     | 分析你过去常用的只读 Bash 和 MCP 工具调用，自动生成一组推荐 allowlist，写入项目 `.claude/settings.json`，减少以后反复出现的权限确认。                                |

