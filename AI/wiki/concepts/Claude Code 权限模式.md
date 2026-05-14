---
title: Claude Code 权限模式
date: 2026-05-14
tags: [coding-tool, workflow, security]
source_count: 1
---

# Claude Code 权限模式

权限模式（Permission Mode）用于控制 [[Claude Code]] 在编辑文件、执行命令或发起网络请求前是否需要向用户确认。不同模式对应不同的自主程度：监督越多越安全，确认越少效率越高但风险越大。

## 四种权限模式

### 1. default（默认模式）

最保守的模式，适合日常使用。

- **读取文件**：自动执行
- **编辑文件/运行命令**：执行前逐一确认
- **其他影响操作**：执行前逐一确认

适用场景：新手、敏感项目、生产相关代码，或希望逐步审查每一步操作的场景。

### 2. acceptEdits（自动编辑模式）

在 default 基础上放宽文件操作权限。

- **工作目录内编辑**：自动批准
- **常见文件系统命令**：自动批准（`mkdir`、`touch`、`rm`、`mv`、`cp` 等）
- **超出工作目录的操作**：仍需确认
- **受保护路径操作**：仍需确认
- **敏感 Bash 命令**：仍需确认

适用场景：已比较信任任务方向，希望提高迭代效率，之后通过编辑器或 `git diff` 统一审查改动的场景。

### 3. plan（规划模式）

只读分析模式。

- **代码分析/项目梳理**：自动执行
- **生成修改方案**：自动执行
- **编辑源代码**：禁止
- **探索性命令**：可能执行（用于了解项目）

适用场景：大型改造前的方案设计、陌生项目梳理、代码评审、重构计划制定等。

### 4. bypassPermissions（Yolo 模式）

最高自主性模式，也是最危险的。

- **所有操作**：立即执行，包括受保护路径
- **权限提示**：禁用
- **安全检查**：跳过

启动方式：

```bash
claude --dangerously-skip-permissions
# 或
claude --permission-mode bypassPermissions
```

适用场景：非常确定环境安全、任务边界清晰，且愿意承担误操作风险的场景。**不建议在真实工作目录、生产项目、重要代码仓库或包含敏感凭据的环境中随便使用**。

## 模式切换

进入 Claude Code 会话后，按 `Shift + Tab` 在模式间循环切换：

```
default -> acceptEdits -> plan
```

如果使用 `--dangerously-skip-permissions` 启动，则循环变为：

```
default -> acceptEdits -> plan -> bypassPermissions
```

当前模式会显示在状态栏中。

## 选择建议

| 场景 | 推荐模式 |
|---|---|
| 初次使用/敏感项目 | `default` |
| 熟悉后提高迭代效率 | `acceptEdits` |
| 设计方案/代码评审 | `plan` |
| 临时/隔离环境快速操作 | `bypassPermissions`（谨慎） |

## 来源

- [[Claude Code入门]]
