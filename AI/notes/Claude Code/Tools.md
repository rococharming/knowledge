
# 一、概述

`Claude Code`内置了一组工具，用于理解、探索、修改和运行代码库中的内容。这些工具共同构成了`Claude Code`执行任务时的基础能力。

这些工具名称不是随意显示的标签，而是配置权限、子代理、hook、skill 时使用的正式工具名。例如：

- 在权限规则中允许或禁止某个工具
- 在子代理中限制可用工具
- 在 hook 中匹配某个工具调用
- 在 skill 中声明可使用的工具
- 在 CLI 参数中配置允许或禁止的工具

如果需要添加自定义工具，可以连接`MCP Server`。

如果需要扩展可复用的提示词工作流，可以编写`skill`。需要注意，`skill`不会新增一个独立工具条目，而是通过已有的工具运行。

# 二、工具总览

## 1、内置工具列表

| 工具                     | 作用                                     | 是否需要权限 |
| ---------------------- | -------------------------------------- | ------ |
| `Agent`                | 启动一个拥有独立上下文窗口的子代理，用于处理任务               | 否      |
| `AskUserQuestion`      | 向用户提出多选问题，用于收集需求或澄清歧义                  | 否      |
| `Bash`                 | 在用户环境中执行 shell 命令                      | 是      |
| `CronCreate`           | 在当前会话中创建一次性或周期性提示任务                    | 否      |
| `CronDelete`           | 根据任务 ID 取消计划任务                         | 否      |
| `CronList`             | 列出当前会话中的计划任务                           | 否      |
| `Edit`                 | 对指定文件进行精确的局部修改                         | 是      |
| `EnterPlanMode`        | 进入计划模式，用于在编码前设计方案                      | 否      |
| `EnterWorktree`        | 创建并进入隔离的 `git worktree`，或进入已有 worktree | 否      |
| `ExitPlanMode`         | 提交计划供用户批准，并退出计划模式                      | 是      |
| `ExitWorktree`         | 退出 worktree 会话，返回原始目录                  | 否      |
| `Glob`                 | 根据文件名模式查找文件                            | 否      |
| `Grep`                 | 在文件内容中搜索匹配模式                           | 否      |
| `ListMcpResourcesTool` | 列出已连接 `MCP Server` 暴露的资源               | 否      |
| `LSP`                  | 通过语言服务器提供代码智能能力                        | 否      |
| `Monitor`              | 在后台运行命令并持续把输出反馈给 Claude                | 是      |
| `NotebookEdit`         | 修改 Jupyter Notebook 单元格                | 是      |
| `PowerShell`           | 原生执行 PowerShell 命令                     | 是      |
| `PushNotification`     | 发送桌面通知；连接远程控制时也可发送手机推送                 | 否      |
| `Read`                 | 读取文件内容                                 | 否      |
| `ReadMcpResourceTool`  | 根据 URI 读取特定 `MCP Resource`             | 否      |
| `RemoteTrigger`        | 创建、更新、运行和列出 claude.ai 上的 `Routines`    | 否      |
| `ScheduleWakeup`       | 为自节奏 `/loop` 安排下一次迭代唤醒时间               | 否      |
| `SendMessage`          | 向 agent team 队友发送消息，或恢复子代理             | 否      |
| `ShareOnboardingGuide` | 上传 `ONBOARDING.md` 并返回可分享的团队入门链接       | 是      |
| `Skill`                | 在主会话中执行一个 `skill`                      | 是      |
| `TaskCreate`           | 创建新的任务列表项                              | 否      |
| `TaskGet`              | 获取某个任务的完整信息                            | 否      |
| `TaskList`             | 列出所有任务及当前状态                            | 否      |
| `TaskOutput`           | 获取后台任务输出，已废弃，推荐使用 `Read` 读取输出文件        | 否      |
| `TaskStop`             | 根据任务 ID 终止正在运行的后台任务                    | 否      |
| `TaskUpdate`           | 更新任务状态、依赖、详情，或删除任务                     | 否      |
| `TeamCreate`           | 创建包含多个队友的 agent team                   | 否      |
| `TeamDelete`           | 解散 agent team 并清理队友进程                  | 否      |
| `TodoWrite`            | 管理会话任务清单；从 `v2.1.142` 起默认被新任务工具替代      | 否      |
| `ToolSearch`           | 启用 tool search 时，搜索并加载延迟工具             | 否      |
| `WaitForMcpServers`    | 等待仍在后台连接的 `MCP Server`                 | 否      |
| `WebFetch`             | 获取指定 URL 内容                            | 是      |
| `WebSearch`            | 执行网络搜索                                 | 是      |
| `Write`                | 创建新文件或完整覆盖已有文件                         | 是      |

## 2、工具能力的来源

`Claude Code`的工具能力主要来自三类：

|来源|说明|示例|
|---|---|---|
|内置工具|`Claude Code` 默认提供的文件、搜索、编辑、执行、任务等能力|`Read`、`Edit`、`Bash`、`Grep`|
|`MCP Server`|外部服务暴露的工具和资源|GitHub MCP、数据库 MCP、内部 API MCP|
|`skill`|可复用的提示词工作流和参考资料|部署检查、代码审查流程、文档生成规范|

注意：

- `MCP Server`可以增加新的外部工具
- `skill`通过已有的`Skill`工具运行，不会变成新的工具名
- 内置工具名会直接用于权限规则、子代理、hook和CLI配置


# 三、权限规则和工具配置

## 1、工具名的配置场景

大多数情况下，用户与`Claude Code`对话时不需要直接指定工具名。`Claude Code`会根据任务自动选择工具。

**但在配置权限和行为边界时，需要显式使用工具名**。

常见配置位置包括：

- 配置文件的`permissions.allow`，允许某些工具或工具的调用范围
- 配置文件的`permissions.deny`，禁止某些工具或工具的调用范围
- 执行`/permissions`命令在交互界面中管理权限
- 命令行启动时传入`--allowedTools`指定允许的工具
- 命令行启动时传入`--disallowedTools`指定禁止的工具
- Agent SDK 的 `allowedTools`，SDK中配置允许工具
- Agent SDK 的 `disallowedTools`，SDK中配置禁止工具
- 子代理 frontmatter 的 `tools`限制子代理可使用工具
- 子代理 frontmatter 的 `disallowedTools`限制子代理不可使用工具
- skill frontmatter 的`allowed-tools`限制 skill 可使用工具
- hook 的 `if`条件，根据工具调用匹配 hook

> Agent SDK 是面向开发者的接口，用来在自己程序创建、运行和约束`Claude Agent`。

## 2、权限规则格式

权限规则通常使用：

```text
ToolName(specifier)
```

其中：

- `ToolName`是工具名
- `specifier`是该工具支持的匹配范围
- 不同工具支持的`specifier`格式不同

常见规则如下：

| 规则格式                           | 适用工具                          | 匹配含义               |
| ------------------------------ | ----------------------------- | ------------------ |
| `Bash(npm run *)`              | `Bash`、`Monitor`              | 匹配 shell 命令模式      |
| `PowerShell(Get-ChildItem *)`  | `PowerShell`                  | 匹配 PowerShell 命令模式 |
| `Read(~/secrets/**)`           | `Read`、`Grep`、`Glob`、`LSP`    | 匹配读取路径             |
| `Edit(/src/**)`                | `Edit`、`Write`、`NotebookEdit` | 匹配编辑路径             |
| `Skill(deploy *)`              | `Skill`                       | 匹配 skill 名称        |
| `Agent(Explore)`               | `Agent`                       | 匹配子代理类型            |
| `WebFetch(domain:example.com)` | `WebFetch`                    | 匹配可访问域名            |
| `WebSearch`                    | `WebSearch`                   | 允许或禁止整个搜索工具        |

不在表格中的工具，例如 `ExitPlanMode`、`ShareOnboardingGuide`，通常只接受裸工具名，不支持括号里的匹配范围。

## 3、Edit(...)的读权限影响

如果配置了：

```text
Edit(/src/**)
```

这条规则不仅允许编辑`/src/**`，也会**自动授予同一路径下的读取权限**。

因此，不需要额外写：

```text
Read(/src/**)
```

## 4、hook matcher 与权限规则的区别

权限规则使用`ToolName(specifier)`，`hook`的`matcher`字段使用裸工具名，例如：

```text
Bash
Edit
Read
```

也就是说：

- 权限规则关注“是否允许某个工具在某个范围内运行”
- hook matcher 关注“某个工具调用发生时是否触发hook”





# PowerShell 工具（待补充） ^powershell-tool
