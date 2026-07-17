---
title: Claude Code 权限模式
date: 2026-07-17
tags: [coding-tool, workflow]
source_count: 1
---

# Claude Code 权限模式

Claude Code 的 Permission Mode 控制会话在编辑文件、执行命令或发起网络请求前是否需要确认。选择权限模式的核心取舍是安全性与效率：监督越多越安全，确认越少越高效但误操作风险更高。

## 常见模式

| 模式 | 含义 | 适用场景 |
|---|---|---|
| `default` | 默认模式。可读取文件，编辑文件、运行命令或其他可能产生影响的操作前会先确认。 | 日常任务、边界不完全明确的改动。 |
| `acceptEdits` | 自动编辑模式。允许自动批准工作目录内的文件创建和编辑。 | 已确认修改范围，主要需要连续落地代码或文档。 |
| `plan` | 计划模式。偏只读，用于阅读、分析代码和给出方案，不直接编辑文件。 | 需求不清、需要先做架构分析或方案评审。 |
| `bypassPermissions` | 跳过权限检查，也称 Yolo 模式。工具调用会立即执行。 | 环境安全、任务边界清晰且用户愿意承担误操作风险时。 |

进入会话后可用 <kbd>Shift</kbd> + <kbd>Tab</kbd> 在权限模式之间循环切换。

## `bypassPermissions`

`bypassPermissions` 自主性最高，风险也最大。可以通过启动参数进入：

```shell
claude --dangerously-skip-permissions
```

也可以显式指定权限模式：

```shell
claude --permission-mode bypassPermissions
```

## 选择建议

- 不确定需求或要先评估代码结构时，先用 `plan`。
- 日常开发默认用 `default`，保留关键操作确认。
- 修改范围已明确且希望减少打断时，用 `acceptEdits`。
- 只有在环境可控、任务明确且能接受误操作风险时，才使用 `bypassPermissions`。

## 相关页面

- [[Claude Code]]
- [[Claude Code 常用命令]]
- [[Claude Code 入门实战流程]]

## 来源

- [[Claude Code入门]]
