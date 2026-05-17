---
title: Claude Code 权限模式系统
date: 2026-05-17
tags: [coding-tool, workflow, security]
source_count: 1
---

# Claude Code 权限模式系统

Claude Code 提供六种权限模式（Permission Mode），在便利性和监督性之间做权衡。越严格的模式越适合敏感项目，越宽松的模式越适合长任务和批量修改。

## 核心内容

### 六种权限模式

| 模式 | 核心特征 | 适合场景 |
|---|---|---|
| `default` | 仅读取自动，其余逐一确认 | 初次使用、敏感项目 |
| `acceptEdits` | 工作目录内文件编辑和常见命令自动批准 | 迭代开发、事后审阅 |
| `plan` | 只读分析，生成方案但不修改代码 | 方案设计、代码评审 |
| `auto` | 分类器后台判断高风险操作 | 长任务、减少中断 |
| `dontAsk` | 非交互式，未预批准的操作直接拒绝 | CI、脚本环境 |
| `bypassPermissions` | 跳过所有权限检查 | 隔离容器、沙箱 |

详见 [[Claude Code 权限模式]]。

### 切换方式

三种切换途径：

1. **会话中**：按 `Shift + Tab` 循环切换（`dontAsk` 和未启用的模式不在循环中）
2. **启动时**：`claude --permission-mode <mode>`，也支持 `-p` 非交互式运行
3. **配置文件**：用户级 `~/settings.json` 或项目级 `.claude/settings.json`

### 受保护路径

`.git`、`.vscode`、`.bashrc`、`.zshrc`、`.mcp.json` 等关键目录和文件的写入在大多数模式下受保护，`bypassPermissions` 除外。不同模式下触发确认、分类器判断或直接拒绝。

详见 [[Claude Code 权限模式#受保护的路径]]。

## 关键要点

- `auto` 模式需要特定套餐、模型和版本（v2.1.83+），且为研究预览功能
- `dontAsk` 模式下显式的 `ask` 规则也会直接拒绝而非提示
- `bypassPermissions` 禁止在 root/sudo 下启动（沙箱环境除外）
- 权限规则（`allow`/`ask`/`deny`）在 `bypassPermissions` 下不生效

## 来源

- [[Permission Mode]]
