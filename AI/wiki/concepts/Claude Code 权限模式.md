---
title: Claude Code 权限模式
date: 2026-05-17
tags: [coding-tool, workflow, security]
source_count: 2
---

# Claude Code 权限模式

权限模式（Permission Mode）用于控制 [[Claude Code]] 在编辑文件、执行命令或发起网络请求前是否需要向用户确认。不同模式对应不同的自主程度：监督越多越安全，确认越少效率越高但风险越大。

## 权限模式总览

| 模式 | 无需询问即可执行 | 适合场景 |
|---|---|---|
| `default` | 仅读取 | 初次使用、敏感工作 |
| `acceptEdits` | 读取、文件编辑和常用文件系统命令 | 迭代代码并在事后统一审阅 |
| `plan` | 仅读取 | 修改前先探索代码库并制定方案 |
| `auto` | 所有操作，但经后台分类器检查 | 长任务、减少权限提示打断 |
| `dontAsk` | 仅预批准工具和只读 Bash 命令 | 受限 CI、脚本环境 |
| `bypassPermissions` | 所有操作（跳过安全检查） | 隔离容器、虚拟机、临时沙箱 |

> 在除 `bypassPermissions` 以外的所有模式下，对[[#^protected-path|受保护路径]]的写入永远不会自动批准。

## 六种权限模式详解

### 1. default（默认模式）

最保守的模式，适合日常使用。

- **读取文件**：自动执行
- **编辑文件/运行命令**：执行前逐一确认
- **安装依赖**：执行前逐一确认
- **发起网络请求**：执行前逐一确认

适用场景：新手、敏感项目、生产相关代码。

### 2. acceptEdits（自动编辑模式）

在 default 基础上放宽文件操作权限。

- **工作目录内编辑**：自动批准（含 `mkdir`、`touch`、`rm`、`mv`、`cp`、`sed` 等常见命令）
- **安全包装命令**：经 `timeout`、`nice`、`nohup` 或环境变量前缀（如 `LANG=C`）包装后也可自动批准
- **超出工作目录的操作**：仍需确认
- **写入受保护路径**：仍需确认
- **其他 Bash 命令**：仍需确认

适用场景：已比较信任任务方向，希望提高迭代效率，之后通过编辑器或 `git diff` 统一审查改动。

### 3. plan（规划模式）

只读分析模式，**先研究、后修改**。

- **代码分析/项目梳理**：自动执行
- **生成修改方案**：自动执行
- **编辑源代码**：禁止
- **探索性命令**：可能执行（用于了解项目），但权限提示规则与 default 一致

方案准备好后，Claude Code 会展示计划，用户可选择：
- 批准并在 `auto` 模式下执行
- 批准并进入 `acceptEdits`
- 批准并手动审阅每次编辑
- 继续规划并给出反馈

可按 `Ctrl + G` 用默认编辑器打开拟议方案直接修改。若启用 `showClearContextOnPlanAccept`，批准时可选择清除规划上下文。

适用场景：大型改造前的方案设计、陌生项目梳理、代码评审、重构计划制定。

### 4. auto（自动模式）

更自动化的权限模式，通过**独立分类器模型**在后台判断高风险操作。

- **只读操作**：自动批准
- **工作目录内普通文件编辑**：自动批准
- **受保护路径写入**：仍受限
- **其他操作**：交给分类器判断，若被阻止会尝试替代方案

暂停条件：分类器连续阻止 3 次，或会话累计阻止 20 次，会恢复权限提示。

**使用条件**（v2.1.83+）：
- 套餐：Max、Team、Enterprise 或 API（Pro 不可用）
- 管理员需在管理设置中启用
- 模型：Sonnet 4.6、Opus 4.6/4.7 等指定模型
- 提供商：仅限 Anthropic API

适用场景：已信任任务大方向，希望减少中途确认打断的长任务。

### 5. dontAsk（非交互模式）

完全非交互式模式，核心规则：**原本需要询问的操作直接拒绝**。

只有两类操作可执行：
1. 匹配 `permissions.allow` 的操作
2. 只读 Bash 命令（`ls`、`cat`、`pwd`、`grep`、`find` 等）

> 显式的 `ask` 规则在 dontAsk 模式下也不会触发提示，而是直接拒绝。

适用场景：受限 CI 环境、脚本环境等完全非交互场景。

### 6. bypassPermissions（跳过权限模式）

权限最宽松、风险最高的模式，禁用权限提示和安全检查，工具调用立即执行。

- **所有操作**：立即执行
- **受保护路径**：从 v2.1.126 开始也允许写入
- **根目录/主目录删除**：仍会触发提示（如 `rm -rf /`、`rm -rf ~`）

启动方式：
```bash
claude --permission-mode bypassPermissions
# 或
claude --dangerously-skip-permissions
```

限制：
- 不支持在 root/sudo 下启动（除非识别为沙箱环境）
- 需通过 `--allow-dangerously-skip-permissions` 才出现在模式循环中
- 管理员可通过 managed settings 禁用

适用场景：容器、虚拟机、临时沙箱环境。**不建议在真实主机、重要项目或有敏感凭据的环境中使用**。

## 模式切换

### 会话期间切换

按 `Shift + Tab` 循环切换：
```
default -> acceptEdits -> plan
```

- `auto`：满足条件时出现在循环中
- `bypassPermissions`：需通过特定参数启动后才出现在循环中
- `dontAsk`：永远不会出现在循环中

### 启动时切换

```bash
claude --permission-mode plan
```

也适用于非交互式运行：
```bash
claude -p "run tests" --permission-mode dontAsk
```

### 配置文件设置

用户级 `~/settings.json`：
```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

项目级 `.claude/settings.json`：
```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

## 受保护的路径

在除 `bypassPermissions` 以外的所有模式下，以下路径的写入永远不会自动批准：

**受保护目录：**
- `.git`
- `.vscode`
- `.idea`
- `.husky`
- `.claude`（除 `.claude/commands`、`.claude/agents`、`.claude/skills`、`.claude/worktree` 外）

**受保护文件：**
- `.gitconfig`、`.gitmodules`
- `.bashrc`、`.bash_profile`、`.zshrc`、`.zsh_profile`、`profile`
- `.ripgreprc`
- `.mcp.json`、`.claude.json`

不同模式下的行为：

| 模式 | 写入受保护路径时的行为 |
|---|---|
| `default` | 提示确认 |
| `acceptEdits` | 提示确认 |
| `plan` | 提示确认 |
| `auto` | 交给分类器判断 |
| `dontAsk` | 直接拒绝 |
| `bypassPermissions` | 允许 |

## 选择建议

| 场景 | 推荐模式 |
|---|---|
| 初次使用/敏感项目 | `default` |
| 熟悉后提高迭代效率 | `acceptEdits` |
| 设计方案/代码评审 | `plan` |
| 长任务、减少中断 | `auto`（需满足条件） |
| CI/脚本环境 | `dontAsk` |
| 临时/隔离环境快速操作 | `bypassPermissions`（谨慎） |

## 来源

- [[Claude Code入门]]
- [[Permission Mode]]
