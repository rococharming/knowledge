# 一、概述

`Claude Code`支持两种添加自定义skill、agent和hook的方式，以 skill 为例：

| 方式                                         | Skill 名称             | 最适用于                    |
| ------------------------------------------ | -------------------- | ----------------------- |
| **独立配置**（`.claude/` 目录）                    | `/hello`             | 个人工作流、项目级定制、快速实验        |
| **插件**（含 `.claude-plugin/plugin.json` 的目录） | `/plugin-name:hello` | 与团队共享、发布到社区、版本化发布、跨项目复用 |

插件（`Plugin`）属于第二种，它是`Claude Code`用于**打包、复用、分享和分发扩展能力**的机制。它将Skill、Subagent、Hook、MCP服务器、LSP服务器等能力组织成可安装、可版本化、可更新的扩展包，让团队或社区复用同一套`Claude Code`配置，而不必在每个项目中重复维护。

> **核心定位**：Plugin 可以看作 `Claude Code`“应用商店“生态，官方Marketplace提供开箱即用的扩展。开发者也可创建自定义插件并通过Marketplace分发。


# 二、插件目录结构

每个`Plugin`是一个目录，常见结构如下：

| 目录 / 文件           | 位置                  | 用途                                          |
| ----------------- | ------------------- | ------------------------------------------- |
| `.claude-plugin/` | 插件根目录               | 包含 `plugin.json` manifest（组件使用默认位置时可选）      |
| `plugin.json`     | `.claude-plugin/` 内 | 声明插件元数据（名称、描述、版本、组件列表）                      |
| `skills/`         | 插件根目录               | Skill，以 `<name>/SKILL.md` 目录形式存放            |
| `commands/`       | 插件根目录               | Skill，以扁平 Markdown 文件形式存放（新插件推荐用 `skills/`） |
| `agents/`         | 插件根目录               | 自定义 agent 定义                                |
| `hooks/`          | 插件根目录               | `hooks.json` 中的事件处理器                        |
| `.mcp.json`       | 插件根目录               | MCP 服务器配置                                   |
| `.lsp.json`       | 插件根目录               | 代码智能的 LSP 服务器配置                             |
| `monitors/`       | 插件根目录               | `monitors.json` 中的后台监控器配置                   |
| `bin/`            | 插件根目录               | 插件启用时添加到 Bash 工具 `PATH` 的可执行文件              |
| `settings.json`   | 插件根目录               | 插件启用时应用的默认设置                                |

> **常见错误**：不要将 `commands/`、`agents/`、`skills/` 或 `hooks/` 放在 `.claude-plugin/` 目录内。只有 `plugin.json` 放在 `.claude-plugin/` 中，其他所有目录必须在插件根目录下。

一个插件目录结构示例如下：
```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-review/
│       └── SKILL.md
├── agents/
│   └── security-reviewer.md
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
├── monitors/
│   └── monitors.json
├── bin/
│   └── custom-tool
└── settings.json
```

# 三、插件可包含的组件

## 1、Skills

`Plugin`可包含`Skills`（详见[[4、Skill|Skills]]）以扩展`Claude`的能力。

在插件根目录下添加`Skills/`目录，其中包含`SKILL.md`文件的具体 skill 名的目录：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

每个 `SKILL.md` 包含 YAML frontmatter 和指令，必须包含 `description` 以让 Claude 知晓何时使用该 skill：

```YAML
---
description: 审查代码的最佳实践和潜在问题。在审查代码、检查 PR 或分析代码质量时使用。
---

审查代码时，检查：
1. 代码组织和结构
2. 错误处理
3. 安全问题
4. 测试覆盖率
```

安装插件后，运行 `/reload-plugins` 加载 Skill。Skill 使用**命名空间**（如 `/my-plugin:code-review`）避免不同插件间的命令名冲突。

## 2、Subagents

`Plugin`可包含`Subagents`（详见[[5、Subagent|Subagents]]）。`Subagent`是**面向特定任务的专用子代理**，用于把复杂任务拆给更专业的`Claude`实例处理，例如代码审查、安全分析、测试分析、架构设计等。

目录示例：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-review/
│       └── SKILL.md
└── agents/
    └── security-reviewer.md
```

一个 `Subagent` 通常是一个 Markdown 文件，包含 YAML frontmatter 和具体指令：

```YAML
---
name: security-reviewer
description: 专门审查代码中的安全风险。在检查认证、权限、输入校验、命令执行、依赖风险、敏感信息泄露时使用。
tools:
  - Read
  - Grep
  - Glob
---

你是一个安全审查专用 Subagent。

审查代码时重点检查：

1. 输入校验是否充分
2. 是否存在命令注入、SQL 注入、路径穿越等风险
3. 是否泄露密钥、token、密码或其他敏感信息
4. 鉴权和权限边界是否清晰
5. 错误信息是否暴露内部实现
6. 第三方依赖是否存在明显安全隐患

输出格式：

- 风险等级：High / Medium / Low
- 问题位置：文件路径 + 相关代码
- 问题说明：为什么这是风险
- 修复建议：如何修改


```

安装插件后，运行：`/reload-plugins`即可加载`Subagent`。

`Subagent` 也会使用插件命名空间，避免不同插件之间的 agent 名称冲突。例如：`/my-plugin:security-reviewer`，或者由`Claude`在合适的任务场景中自动委派给对应的 `Subagent`。

## 3、Hooks
`Plugin` 可包含 `Hooks`（详见 [[7、Hook|Hooks]]）。`Hook`是在`Claude Code`生命周期的特定时机自动执行的脚本、命令或检查逻辑，用于实现自动化流程、约束行为、格式化代码、安全拦截等。

常见用途：

1. 在`Claude Code`修改文件后自动格式化代码
2. 在执行危险命令前进行拦截
3. 在提交或修改代码后自动运行测试
4. 在会话开始或结束时执行初始化 / 清理逻辑
5. 在用户提交 Prompt 后追加规则或进行检查

插件中的`Hooks`通常放在`hooks`目录下，并使用`hooks.json`配置：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-review/
│       └── SKILL.md
├── agents/
│   └── security-reviewer.md
└── hooks/
    └── hooks.json
```

`hooks.json`示例：

```JSON
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix"
          }
        ]
      }
    ]
  }
}
```

这个例子表示：

当`Claude`使用`Write`或`Edit`工具修改文件后，自动读取被修改的文件路径，并执行：

```Bash
npm run lint:fix <file_path>
```


## 4、MCP Servers

`Plugin`可包含`MCP Servers`（详见[[6、MCP|MCP]]）。`MCP Server`用于把外部工具、数据源或服务暴露给`Claude Code`，让`Claude`可以调用这些能力。

常见用途：

1. 连接 GitHub、GitLab 等代码托管平台
2. 连接数据库、API、内部系统
3. 暴露自定义工具给`Claude`调用
4. 暴露项目资源，让`Claude`可以通过`@`引用
5. 暴露可复用`Prompt`，让`Claude Code`中出现对应命令

目录示例：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-review/
│       └── SKILL.md
├── agents/
│   └── security-reviewer.md
├── hooks/
│   └── hooks.json
└── .mcp.json
```

Plugin 通过根目录的 `.mcp.json` 文件配置 MCP 服务器。

`.mcp.json`示例：

```JSON
{
  "mcpServers": {
    "github": {
	   "type": "http",
	   "url": "https://api.githubcopilot.com/mcp",
	   "headers": {
		  "Authorization": "Bearer YOUR_GITHUB_PAT"
	   }
    }
  }
}
```

## 5、LSP Servers

`Plugin` 可包含 `LSP Servers`。`LSP`是`Language Server Protocol`的缩写，用于为`Claude Code`提供类似IDE的代码智能能力，例如类型信息、诊断信息、跳转定义、引用查找、补全等。

目录示例：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-review/
│       └── SKILL.md
├── agents/
│   └── security-reviewer.md
├── hooks/
│   └── hooks.json
├── .mcp.json
└── .lsp.json
```

Plugin 通过根目录的 `.lsp.json` 文件配置 LSP 连接。

例如配置`Rust`的LSP连接：

```json
{
	"rust": {
		"command": "rust-analyer",
		"args": [],
		"extensionToLanguage": {
			".rs": "rust"
		}
	}
}
```

其中：

|字段|含义|
|---|---|
|`rust`|LSP Server 名称|
|`command`|启动语言服务器的命令|
|`args`|启动命令的参数；这里为空数组|
|`extensionToLanguage`|文件扩展名到语言 ID 的映射|
>安装插件的用户必须在本机安装了对应的**语言服务器二进制文件**，例如安装`rust-analyzer`。

## 6、后台监控器
`Plugin`可包含后台监控器，也就是`Background Monitors`。后台监控器用于在`Claude Code`会话期间持续运行某个命令，并把命令输出作为通知传递给`Claude Code`，让`Claude Code`可以感知日志变化、状态变化、文件变化或外部任务进度。

目录示例：

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── code-review/
│       └── SKILL.md
├── agents/
│   └── security-reviewer.md
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
└── monitors/
    └── monitors.json
```

Plugin 通过 `monitors/monitors.json` 配置后台监控器。插件启用时会自动启动这些监控器。每个 monitor 会在会话期间运行一个 shell 命令，并把每一行 `stdout` 输出传给 `Claude` 作为通知。

 `monitors/monitors.json` 文件示例：
 
```json
[
  {
    "name": "watch-error-log",
    "description": "监听本地应用日志中的错误信息",
    "command": "tail -f logs/app.log | grep --line-buffer -i \"error\" "
  }
]
```

`command` 的每行 stdout 输出在会话期间以**通知形式**送达 Claude。收到后，Claude 可以根据当前任务上下文决定怎么处理。

## 7、默认配置

`Plugin`可在根目录包含`settings.json`文件，用于在插件启用时附带一组插件默认配置。

`settings.json`示例：

```JSON
"agent": "security-reviewer"
```

这个配置表示：插件启用后，默认使用插件内的 `security-reviewer` agent 作为主线程 agent。

目前根目录的`settings.json`只支持两个键：

|键|作用|
|---|---|
|`agent`|指定插件中的某个自定义 agent 作为主线程 agent|
|`subagentStatusLine`|配置 subagent 状态栏显示行为|
> `settings.json` 中的设置优先于 `plugin.json` 中声明的 `settings`。未知键会被静默忽略。


# 四、Marketplace与插件管理

## 1、概述

`Marketplace` 是 Claude Code 的插件分发源，可以理解为“插件仓库”或“插件目录”。它用于集中管理一组可安装的 `Plugin`。用户可以通过 `/plugin` 浏览、安装、启用、禁用、卸载和更新插件。

## 2、官方 Anthropic Marketplace

官方 Anthropic Marketplace（`claude-plugins-official`）在启动`Claude Code`时**自动可用**。
运行 `/plugin` 进入 **Marketplaces** 标签页可看到现有的 marketplaces：

![[Pasted image 20260507163749.png]]

### （1）浏览与安装

运行 `/plugin` 进入 **Discover** 标签页浏览可用插件，或在 [claude.com/plugins](https://claude.com/plugins) 查看目录。选择插件后可选择安装范围：

![[Pasted image 20260507163854.png]]

| 范围           | 说明                                                    |
| ------------ | ----------------------------------------------------- |
| **User**（默认） | 为你自己在所有项目中安装（添加到`~/.claude/settings.json`）            |
| **Project**  | 为本仓库的所有协作者安装（添加到 `.claude/settings.json`）             |
| **Local**    | 仅为你自己在本仓库安装（不与协作者共享，添加到`.claude/settings.local.json`） |
也可以通过`/plugin`命令安装：

```bash
/plugin install superpowers@claude-plugins-official
```

注意，`settings.json` / `settings.local.json` **只是配置文件**，里面记录“启用了哪些插件、作用域是什么”等信息；**插件包本体会被 Claude Code 复制到插件缓存目录里**。通常在`~/.claude/plugins/cache/`下。

安装完成后，执行`/reload-plugins`应用插件。

例如，我在个人项目（Local）范围安装了`superpowers`插件，此时在当前项目的`settings.local.json`就增加了一条配置记录：

```json
"enabledPlugins": {
	"superpowers@claude-plugins-official": true
}
```

### （2）Marketplace 问题排查

若`Claude Code`报告在任何 marketplace 中未找到该插件，可通过如下方式排查：

1. 更新marketplace：：`/plugin marketplace update claude-plugins-official`
2. 若还没添加marketplace：`/plugin marketplace add anthropics/claude-plugins-official`
3. 重新尝试安装插件

## 3、Marketplace 插件类别
### （1）代码智能（LSP）

代码智能插件为`Claude Code`启用内置的LSP工具，让 Claude 在处理代码时获得语义级理解能力。

LSP 是三层架构：

```text
Claude → Claude Code 内置 LSP 客户端 → 本机语言服务器 → 项目代码
```

主要能力：

| 能力       | 说明                                                                                  |
| -------- | ----------------------------------------------------------------------------------- |
| **自动诊断** | 每次编辑文件后，语言服务器分析变更并返回错误 / 警告；Claude 可在同一轮修改中发现并修复问题。出现"发现诊断"指示器时，按 **Ctrl+O** 内联查看详情 |
| **代码导航** | 跳转到定义、查找引用、查看类型信息、发现类型错误、获取符号信息、查找实现、分析调用层级                                         |

支持的语言：

| 语言         | Claude Code 插件      | 所需语言服务器二进制                   |
| ---------- | ------------------- | ---------------------------- |
| C / C++    | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Kotlin     | `kotlin-lsp`        | `kotlin-language-server`     |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

> 若 `/plugin` 的 **Errors 标签页**中出现 `Executable not found in $PATH`，需安装对应的语言服务器二进制文件。

### （2）外部集成

捆绑预配置的 MCP 服务器：

| 类别 | 插件 |
|------|------|
| 源代码管理 | `github`、`gitlab` |
| 项目管理 | `atlassian`（Jira / Confluence）、`asana`、`linear`、`notion` |
| 设计 | `figma` |
| 基础设施 | `vercel`、`firebase`、`supabase` |
| 通信 | `slack` |
| 监控 | `sentry` |

### （3）开发工作流

| 插件                  | 说明                           |
| ------------------- | ---------------------------- |
| `commit-commands`   | Git 提交工作流（commit、push、PR 创建） |
| `pr-review-toolkit` | 审查拉取请求的专用 Agent              |
| `agent-sdk-dev`     | 使用 Claude Agent SDK 构建的工具    |
| `plugin-dev`        | 创建自己插件的工具包                   |

### （4）输出风格

| 插件                         | 说明             |
| -------------------------- | -------------- |
| `explanatory-output-style` | 对实现选择提供教学性洞察   |
| `learning-output-style`    | 交互式学习模式，用于技能构建 |

## 4、添加 Marketplace

使用 `/plugin marketplace add` 可以从不同来源添加 Marketplace。

需要注意，被添加的`Marketplace`源中通常需要包含：`.claude-plugin/marketplace.json`：

![[Pasted image 20260507170420.png]]

这个文件用于描述`Marketplace`的名称、作者信息以及其中包含哪些插件。

使用 `/plugin marketplace add` 从不同来源添加：

|来源|格式|示例|
|---|---|---|
|GitHub 仓库|`owner/repo`|`anthropics/claude-code`|
|Git URL|完整 Git URL|`https://gitlab.com/company/plugins.git`|
|本地路径|包含 `.claude-plugin/marketplace.json` 的目录，或直接指向 `marketplace.json`|`./my-marketplace`|
|远程 URL|直接指向托管的 `marketplace.json` 文件|`https://example.com/marketplace.json`|

支持特定分支或标签：

```bash
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

## 5、管理已安装的插件

运行 `/plugin` 进入 **Installed** 标签页查看、启用、禁用、更新或卸载插件。也可用命令：

```bash
/plugin disable plugin-name@marketplace-name
/plugin enable plugin-name@marketplace-name
/plugin uninstall plugin-name@marketplace-name
```

## 6、自动更新

Claude Code 可在启动时自动更新 marketplace 及其已安装的插件。官方 Anthropic marketplace **默认启用**自动更新，第三方和本地开发 marketplace **默认禁用**。

要完全禁用自动更新，设置 `DISABLE_AUTOUPDATER` 环境变量。要在禁用 Claude Code 自动更新的同时**保持插件自动更新**：

```shell
export DISABLE_AUTOUPDATER=1
export FORCE_AUTOUPDATE_PLUGINS=1
```

需要注意，设置`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`会关闭非必要网络流量，它包含`DISABLE_AUTOUPDATER=1`。


## 五、自定义插件（待补充）