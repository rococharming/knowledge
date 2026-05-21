---
title: "探索 .claude 目录"
source: "https://code.claude.com/docs/en/claude-directory"
author:
published:
created: 2026-05-21
description: "Claude Code 读取 CLAUDE.md、settings.json、hooks、skills、commands、subagents、rules 和自动记忆的位置。探索项目中的 .claude 目录以及主目录下的 ~/.claude。"
tags:
  - "clippings"
---
# AI摘要

## 为什么值得读

这份官方文档是理解和自定义 Claude Code 行为的一站式指南，适合任何想精细控制 AI 助手在项目中工作方式的开发者。它清晰解释了`.claude` 目录的结构、每个配置文件的用途和加载时机，以及如何通过设置、规则、技能和子代理来扩展 Claude Code 的能力。

## 如何组织配置

- **项目级与全局级配置**：项目级文件（如 `.claude/CLAUDE.md`、`settings.json`）应提交到 Git 以便团队共享；全局配置（`~/.claude/`）是个人偏好，跨所有项目生效。
- **关键文件速查**：
  - `CLAUDE.md`：每个会话加载的项目指令，适合约定、命令和架构上下文。
  - `rules/*.md`：按主题或路径限定的指令，避免每次加载无用信息。
  - `settings.json`：权限、钩子（hooks）、环境变量和模型默认值。
  - `skills/<name>/SKILL.md`：可复用的提示词，用 `/name` 调用。
  - `agents/*.md`：定义拥有独立提示词和工具的子代理。
  - `.mcp.json`：连接外部工具（MCP 服务器）。

## 你需要知道的核心要点

- **指令覆盖顺序**：企业托管设置 > CLI 标志 > 环境变量 > 配置文件。
- **本地数据安全**：会话记录（`projects/<project>/<session>.jsonl`）以明文存储，包含所有工具调用内容。可通过 `cleanupPeriodDays` 缩短保留期，或设置 `CLAUDE_CODE_SKIP_PROMPT_HISTORY` 跳过写入。
- **清理项目数据**：使用 `claude project purge` 命令可按项目删除会话记录、自动记忆等，不影响全局配置和插件。
- **文件大小建议**：`CLAUDE.md` 控制在 200 行以内，过长可能降低 Claude 的遵从性。更具体的任务指令应放入技能或规则中。
- **调试配置**：若设置未生效，参考[调试配置文档](https://code.claude.com/docs/en/debug-your-config)进行排查。

---

# 原始正文

Claude Code 从项目目录和主目录下的 `~/.claude` 中读取指令、设置、技能、子代理和记忆。将项目文件提交到 git 以便与团队共享；`~/.claude` 中的文件是个人配置，适用于你所有的项目。

在 Windows 上，`~/.claude` 解析为 `%USERPROFILE%\.claude`。如果你设置了 [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/en/env-vars)，本页中所有 `~/.claude` 路径都将位于该目录下。

大多数用户只编辑 `CLAUDE.md` 和 `settings.json`。目录的其余部分是可选的：根据需要添加技能、规则或子代理。

## 探索目录

点击树形结构中的文件，查看每个文件的作用、加载时机以及示例。

交互式探索器在大屏幕上效果最佳。或者参见下方的[文件参考表](#file-reference)。



CLAUDE.md 已选中

your-project / CLAUDE.md

CLAUDE.md

Claude 每次会话都会读取的项目指令

需提交

加载时机

在每个会话开始时加载到上下文中

项目特定的指令，塑造 Claude 在此仓库中的工作方式。将你的约定、常用命令和架构上下文放在这里，以便 Claude 与你的团队保持相同的假设。

小贴士

● 控制在 200 行以内。较长的文件仍会完整加载，但可能会降低遵从性

● CLAUDE.md 会加载到每个会话中。如果某些内容仅与特定任务相关，请将其移至 [skill](https://code.claude.com/docs/en/skills) 或按路径限定的 [rule](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)，使其仅在需要时加载

● 列出你最常使用的命令，如构建、测试和格式化，这样 Claude 无需你每次拼写就能知道它们

● 运行 `/memory` 可在会话中打开并编辑 CLAUDE.md

● 也可以放在 `.claude/CLAUDE.md` 中，如果你希望保持项目根目录整洁

此示例适用于 TypeScript 和 React 项目。它列出了构建和测试命令、Claude 应遵循的框架约定，以及导出风格和文件布局等项目特定规则。

```
# 项目约定

## 命令
- 构建：`npm run build`
- 测试：`npm test`
- 代码检查：`npm run lint`

## 技术栈
- TypeScript，启用严格模式
- React 19，仅使用函数组件

## 规则
- 使用命名导出，不使用默认导出
- 测试与源码放在一起：`foo.ts` -> `foo.test.ts`
- 所有 API 路由返回 `{ data, error }` 格式
```

[完整文档 →](https://code.claude.com/docs/en/memory)

## 未显示的内容

探索器涵盖了你编写和编辑的文件。还有一些相关文件位于其他位置：

| 文件 | 位置 | 用途 |
| --- | --- | --- |
| `managed-settings.json` | 系统级，因操作系统而异 | 企业强制执行的设置，你无法覆盖。参见[服务器托管设置](https://code.claude.com/docs/en/server-managed-settings)。 |
| `CLAUDE.local.md` | 项目根目录 | 你对此项目的私人偏好，与 CLAUDE.md 一起加载。手动创建并将其添加到 `.gitignore`。 |
| 已安装插件 | `~/.claude/plugins` | 克隆的市场、已安装的插件版本，以及每个插件的数据，由 `claude plugin` 命令管理。孤立版本在插件更新或卸载 7 天后删除。参见[插件缓存](https://code.claude.com/docs/en/plugins-reference#plugin-caching-and-file-resolution)。 |

`~/.claude` 还保存 Claude Code 工作时写入的数据：转录、提示历史、文件快照、缓存和日志。参见下方的[应用程序数据](#application-data)。

## 选择正确的文件

不同类型的自定义项位于不同的文件中。使用此表来找到更改应归属的位置。

| 你想 | 编辑 | 范围 | 参考 |
| --- | --- | --- | --- |
| 为 Claude 提供项目上下文和约定 | `CLAUDE.md` | 项目或全局 | [Memory](https://code.claude.com/docs/en/memory) |
| 允许或阻止特定的工具调用 | `settings.json` 中的 `permissions` 或 `hooks` | 项目或全局 | [Permissions](https://code.claude.com/docs/en/permissions)、[Hooks](https://code.claude.com/docs/en/hooks) |
| 在工具调用前后运行脚本 | `settings.json` 中的 `hooks` | 项目或全局 | [Hooks](https://code.claude.com/docs/en/hooks) |
| 为会话设置环境变量 | `settings.json` 中的 `env` | 项目或全局 | [Settings](https://code.claude.com/docs/en/settings#available-settings) |
| 将个人覆盖项保留在 git 之外 | `settings.local.json` | 仅限项目 | [Settings scopes](https://code.claude.com/docs/en/settings#settings-files) |
| 添加一个可通过 `/name` 调用的提示词或功能 | `skills/<name>/SKILL.md` | 项目或全局 | [Skills](https://code.claude.com/docs/en/skills) |
| 定义一个拥有自己工具的专用子代理 | `agents/*.md` | 项目或全局 | [Subagents](https://code.claude.com/docs/en/sub-agents) |
| 通过 MCP 连接外部工具 | `.mcp.json` | 仅限项目 | [MCP](https://code.claude.com/docs/en/mcp) |
| 更改 Claude 格式化响应的方式 | `output-styles/*.md` | 项目或全局 | [Output styles](https://code.claude.com/docs/en/output-styles) |

## 文件参考

此表列出了探索器涵盖的每个文件。项目范围文件位于仓库下的 `.claude/` 中（对于 `CLAUDE.md`、`.mcp.json` 和 `.worktreeinclude`，则位于根目录）。全局范围文件位于 `~/.claude/` 中，适用于所有项目。

以下几项可以覆盖你在这些文件中设置的内容：

- 你的组织部署的[托管设置](https://code.claude.com/docs/en/server-managed-settings)优先于所有其他设置
- CLI 标志（如 `--permission-mode` 或 `--settings`）会覆盖该会话的 `settings.json`
- 某些环境变量优先于其等效设置，但情况各异：请查看[环境变量参考](https://code.claude.com/docs/en/env-vars)了解每个变量的详情

参见[设置优先级](https://code.claude.com/docs/en/settings#settings-precedence)了解完整的优先级顺序。

点击文件名可在上方探索器中打开该节点。

| 文件 | 范围 | 提交 | 作用 | 参考 |
| --- | --- | --- | --- | --- |
| [`CLAUDE.md`](#ce-claude-md) | 项目和全局 | ✓ | 每次会话加载的指令 | [Memory](https://code.claude.com/docs/en/memory) |
| [`rules/*.md`](#ce-rules) | 项目和全局 | ✓ | 按主题限定的指令，可选按路径控制 | [Rules](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) |
| [`settings.json`](#ce-settings-json) | 项目和全局 | ✓ | 权限、钩子、环境变量、模型默认值 | [Settings](https://code.claude.com/docs/en/settings) |
| [`settings.local.json`](#ce-settings-local-json) | 仅限项目 |  | 你的个人覆盖项，自动加入 gitignore | [Settings scopes](https://code.claude.com/docs/en/settings#settings-files) |
| [`.mcp.json`](#ce-mcp-json) | 仅限项目 | ✓ | 团队共享的 MCP 服务器 | [MCP scopes](https://code.claude.com/docs/en/mcp#mcp-installation-scopes) |
| [`.worktreeinclude`](#ce-worktreeinclude) | 仅限项目 | ✓ | 要复制到新工作树的 gitignore 文件 | [Worktrees](https://code.claude.com/docs/en/worktrees#copy-gitignored-files-into-worktrees) |
| [`skills/<name>/SKILL.md`](#ce-skills) | 项目和全局 | ✓ | 可复用的提示词，通过 `/name` 调用或自动调用 | [Skills](https://code.claude.com/docs/en/skills) |
| [`commands/*.md`](#ce-commands) | 项目和全局 | ✓ | 单文件提示词；与技能机制相同 | [Skills](https://code.claude.com/docs/en/skills) |
| [`output-styles/*.md`](#ce-output-styles) | 项目和全局 | ✓ | 自定义系统提示词部分 | [Output styles](https://code.claude.com/docs/en/output-styles) |
| [`agents/*.md`](#ce-agents) | 项目和全局 | ✓ | 拥有自己提示词和工具的子代理定义 | [Subagents](https://code.claude.com/docs/en/sub-agents) |
| [`agent-memory/<name>/`](#ce-agent-memory) | 项目和全局 | ✓ | 子代理的持久记忆 | [Persistent memory](https://code.claude.com/docs/en/sub-agents#enable-persistent-memory) |
| [`~/.claude.json`](#ce-claude-json) | 仅限全局 |  | 应用状态、OAuth、UI 开关、个人 MCP 服务器 | [Global config](https://code.claude.com/docs/en/settings#global-config-settings) |
| [`projects/<project>/memory/`](#ce-global-projects) | 仅限全局 |  | 自动记忆：Claude 跨会话的笔记 | [Auto memory](https://code.claude.com/docs/en/memory#auto-memory) |
| [`keybindings.json`](#ce-keybindings) | 仅限全局 |  | 自定义键盘快捷键 | [Keybindings](https://code.claude.com/docs/en/keybindings) |
| [`themes/*.json`](#ce-themes) | 仅限全局 |  | 自定义颜色主题 | [Custom themes](https://code.claude.com/docs/en/terminal-config#create-a-custom-theme) |

## 排查配置问题

如果某个设置、钩子或文件未生效，请参见[调试你的配置](https://code.claude.com/docs/en/debug-your-config)了解检查命令和按症状分类的查找表。

## 应用程序数据

除了你编写的配置外，`~/.claude` 还保存 Claude Code 在会话期间写入的数据。这些文件是纯文本。任何通过工具处理的内容都会记录在磁盘上的转录中：文件内容、命令输出、粘贴的文本。

### 自动清理

以下路径中的文件在启动时，一旦超过 [`cleanupPeriodDays`](https://code.claude.com/docs/en/settings#available-settings) 即被删除。默认值为 30 天。

| `~/.claude/` 下的路径 | 内容 |
| --- | --- |
| `projects/<project>/<session>.jsonl` | 完整对话转录：每条消息、每次工具调用和工具结果 |
| `projects/<project>/<session>/subagents/` | [子代理](https://code.claude.com/docs/en/sub-agents)对话转录，随父会话转录过期一并删除 |
| `projects/<project>/<session>/tool-results/` | 溢出到单独文件的大型工具输出 |
| `file-history/<session>/` | Claude 修改文件前的编辑前快照，用于[检查点恢复](https://code.claude.com/docs/en/checkpointing) |
| `plans/` | [计划模式](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode)期间写入的计划文件 |
| `debug/` | 每次会话的调试日志，仅在以 `--debug` 启动或运行 `/debug` 时写入 |
| `paste-cache/`、`image-cache/` | 大型粘贴内容和附加图像的内容 |
| `session-env/` | 每次会话的环境元数据 |
| `tasks/` | 任务工具写入的每次会话任务列表 |
| `shell-snapshots/` | Bash 工具捕获的 shell 环境。在干净退出时删除。清理会清除崩溃后遗留的所有内容。 |
| `backups/` | 配置迁移前 `~/.claude.json` 的时间戳副本 |
| `feedback-bundles/` | 在第三方提供商上运行 `/feedback` 时写入的脱敏转录归档，用于发送到你的 Anthropic 客户团队 |

### 保留直至你手动删除

以下路径不受自动清理覆盖，会无限期保留。

| `~/.claude/` 下的路径 | 内容 |
| --- | --- |
| `history.jsonl` | 你输入的每个提示词，带时间戳和项目路径。用于按上箭头回忆。 |
| `stats-cache.json` | `/usage` 显示的聚合 token 和成本计数 |
| `remote-settings.json` | 你的组织的[服务器托管设置](https://code.claude.com/docs/en/server-managed-settings)的缓存副本。仅在你的组织配置它们时存在。每次启动时刷新。 |
| `todos/` | 旧版每次会话任务列表。当前版本不再写入；可以安全删除。 |

根据你使用的功能，还会出现其他小型缓存和锁文件，可以安全删除。

### 纯文本存储

转录和历史记录在静态时未加密。唯一的保护是操作系统文件权限。如果工具读取 `.env` 文件或命令打印凭据，该值将写入 `projects/<project>/<session>.jsonl`。为了减少暴露：

- 降低 `cleanupPeriodDays` 以缩短转录的保留时间
- 设置 [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](https://code.claude.com/docs/en/env-vars) 环境变量以跳过在任何模式下写入转录和提示历史。在非交互模式下，你可以改为传递 `--no-session-persistence` 和 `-p`，或在 Agent SDK 中设置 `persistSession: false`。
- 使用[权限规则](https://code.claude.com/docs/en/permissions)拒绝读取凭据文件

### 清除本地数据

运行 `claude project purge` 可删除 Claude Code 为一个项目保存的状态：

- `projects/` 下的转录和自动记忆
- 每次会话的 `tasks/`、`debug/` 和 `file-history/` 条目
- `history.jsonl` 中匹配的提示词行
- `~/.claude.json` 中的项目条目

该命令会打印完整的删除计划，并在删除任何内容前请求确认。

预览计划而不删除任何内容：

```shellscript
claude project purge ~/work/my-repo --dry-run
```

通过单个确认提示删除：

```shellscript
claude project purge ~/work/my-repo
```

省略路径以从交互式列表中选择一个项目。

在脚本中跳过确认提示：

```shellscript
claude project purge ~/work/my-repo --yes
```

传递 `--all` 而不是路径以一次性清除所有项目的状态，这将直接删除 `history.jsonl` 而不是过滤它。传递 `-i` 以逐个步骤浏览删除计划。

该命令不会动 `shell-snapshots/` 和 `backups/`，因为它们不是项目范围的，并在计划输出中警告它们。如果没有状态匹配给定路径，则以状态 1 退出。

你也可以手动删除上述任何应用程序数据路径。新会话不受影响。下表显示了删除过去会话会丢失什么。

| 删除 | 你会丢失 |
| --- | --- |
| `~/.claude/projects/` | 过去会话的恢复、继续和回退功能 |
| `~/.claude/history.jsonl` | 按上箭头提示词回忆 |
| `~/.claude/file-history/` | 过去会话的检查点恢复 |
| `~/.claude/stats-cache.json` | `/usage` 显示的历史总计 |
| `~/.claude/remote-settings.json` | 无影响。下次启动时重新获取。 |
| `~/.claude/debug/`、`~/.claude/plans/`、`~/.claude/paste-cache/`、`~/.claude/image-cache/`、`~/.claude/session-env/`、`~/.claude/tasks/`、`~/.claude/shell-snapshots/`、`~/.claude/backups/` | 无用户可见影响 |
| `~/.claude/todos/` | 无影响。旧版目录，当前版本不再写入。 |

不要删除 `~/.claude.json`、`~/.claude/settings.json` 或 `~/.claude/plugins/`：这些保存了你的认证、偏好设置和已安装插件。

## 相关资源

- [管理 Claude 的记忆](https://code.claude.com/docs/en/memory)：编写和组织 CLAUDE.md、规则和自动记忆
- [配置设置](https://code.claude.com/docs/en/settings)：设置权限、钩子、环境变量和模型默认值
- [创建技能](https://code.claude.com/docs/en/skills)：构建可复用的提示词和工作流
- [配置子代理](https://code.claude.com/docs/en/sub-agents)：定义拥有自己上下文的专用代理
