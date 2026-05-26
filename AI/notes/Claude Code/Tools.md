
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






# PowerShell 工具（待补充） ^powershell-tool
