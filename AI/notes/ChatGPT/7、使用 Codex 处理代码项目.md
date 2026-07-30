---
title: 使用 Codex 处理代码项目
date: 2026-07-30
tags: [AI, ChatGPT, Codex]
aliases:
  - ChatGPT App Codex
  - Codex代码项目
---

# 一、Codex

ChatGPT 桌面 App 内的 `Codex` 是面向软件开发的工作方式。它能读取代码库、修改文件、运行命令、检查 Diff，并根据测试结果继续迭代。

它与 ChatGPT Work 有部分重叠，但 Codex 会显示更多开发细节：

- 当前项目和 Git 状态
- 文件修改
- 命令与终端输出
- Review Pane
- Staged 与 Unstaged 变更
- Pull Request 信息

本篇只介绍 App 内的 Codex。终端形态可以参考 [[补充资料/1、Codex  CLI|Codex CLI]]，第三方模型接入不属于本系列主线。

# 二、打开项目

## 1、选择目录

在 ChatGPT 下拉菜单中选择 **Codex**，然后打开需要处理的代码目录。

本地 Project 可以附加多个文件夹，但 Primary Folder 决定：

- 新 Chat 的默认工作目录
- Git 操作的默认仓库
- `AGENTS.md` 的自动发现
- Skills 和 `.codex/config.toml` 的自动发现
- 本地环境配置的位置

打开目录前，应先确认其中没有与任务无关的敏感文件。

## 2、选择环境

创建 Codex Chat 时可以选择：

| 环境 | 工作方式 | 适合场景 |
|---|---|---|
| Local | 直接操作当前项目目录 | 单一任务、需要立刻使用现有环境 |
| Worktree | 在独立 Git Worktree 中操作 | 并行任务、隔离未完成修改 |
| Cloud | 在配置好的远程环境中执行 | 脱离本机运行、远程继续 |

Local 与 Worktree 都运行在当前电脑上。Worktree 只是隔离 Git 工作目录，不代表云端执行。

> [!todo] 待补截图
> 截取新建 Codex Chat 时的 Local、Worktree 和 Cloud 选择入口。

# 三、任务流程

## 1、理解

先让 Codex 确认项目结构、任务目标和限制，不要在信息不足时立即修改。

示例：

```text
请先检查这个项目的入口、构建命令和现有测试。
说明你对登录流程的理解，并列出导致回归的可能位置。
现在不要修改文件。
```

Codex 可以读取仓库中的 `AGENTS.md` 和相关文档，但仍应在提示中说明当前任务独有的要求。

## 2、规划

复杂任务可以先使用 `/plan` 或直接要求给出执行方案。

计划至少应说明：

- 修改范围
- 不应改变的行为
- 需要运行的检查
- 可能存在的风险
- 完成标准

计划用于确认方向，不等于代码已经实现。

## 3、修改

确认方案后，让 Codex完成范围明确的改动。

示例：

```text
按刚才的方案修复登录跳转。
只修改路由判断和对应测试，保持接口与页面样式不变。
不要提交或推送 Git。
```

任务执行时，Codex 会根据 Permission Mode 决定哪些文件和命令可以直接处理，哪些操作需要审批。

## 4、验证

不要只以“文件已经修改”为完成标准。应要求 Codex 运行与风险相称的验证：

```text
运行登录模块的单元测试和项目类型检查。
如果测试失败，先判断是本次修改导致还是环境问题。
最后列出实际运行的命令和结果。
```

应用界面、浏览器交互或桌面行为还需要对应的视觉或运行时验证，不能只凭代码检查宣称成功。

# 四、终端

每个本地 Codex Chat 都有与当前 Project 或 Worktree 对应的集成终端。点击右上角终端图标或按 <kbd>Ctrl</kbd> + <kbd>`</kbd> 打开。

终端适合：

- 查看 `git status`
- 运行构建和测试
- 启动开发服务器
- 检查日志
- 执行 App 没有直接提供的 Git 操作

ChatGPT 可以读取当前终端输出，因此可以让它结合失败信息继续诊断。

```bash
git status
npm test
npm run lint
```

这些只是常见例子，真实项目应以仓库文档和 `AGENTS.md` 中声明的命令为准。

# 五、Review Pane

## 1、查看变更

Review Pane 展示的是当前 Git 仓库的状态，不仅包含 Codex 修改的内容，也可能包含你自己或其他工具产生的未提交修改。

常见视图包括：

- Unstaged
- Staged
- Commit
- Branch
- Last turn

因此，在接受修改前要先确认哪些变更属于当前任务。

## 2、代码审查

在 Git 仓库中可以输入 `/review`，选择：

- Review against a base branch
- Review uncommitted changes
- Review a commit
- Custom review instructions

Review 默认只报告问题，不修改工作区。发现问题后，可以要求提供证据或只修复指定 Finding。

## 3、行内反馈

在 Diff 中悬停到具体代码行，点击 `+` 可以留下行内评论。完成评论后，再发送明确指令：

```text
处理我留下的行内评论，保持改动范围最小。
```

行内评论比“把代码再优化一下”更容易保持修改边界。

## 4、Git 操作

Review Pane 可以按 Hunk、文件或整个 Diff 执行 Stage、Unstage 和 Revert，也能在支持时提交、推送或创建 Pull Request。

这些操作会改变 Git 状态。执行 Revert、Commit、Push 或创建 PR 前，应确认目标范围和远端影响。

> [!todo] 待补截图
> 截取 Review Pane 的 Unstaged、Staged 和行内评论入口，使用不含公司代码的示例仓库。

# 六、本地环境

Local Environment 可以为 Codex Project 定义：

- **Setup Script**：创建 Worktree 后安装依赖或完成初始化。
- **Actions**：运行测试、启动开发服务器等常用操作。

配置保存在项目根目录的 `.codex` 中，可以提交到仓库供团队共享。

例如，Node.js 项目的 Setup Script 可以是：

```bash
npm install
npm run build
```

Action 可以定义为：

```bash
npm test
```

平台命令不同时，可以分别配置 macOS、Windows 或 Linux 的脚本。

# 七、开发实践

下面用“修复登录页回归”串起完整流程：

1. 以 Local 或 Worktree 打开代码库。
2. 让 Codex 读取仓库规则、入口和现有测试。
3. 先复现问题并解释根因，不立即修改。
4. 确认最小修复方案和验收标准。
5. 执行修改并运行相关测试。
6. 在 Review Pane 检查每个 Diff。
7. 对不清楚的代码行添加行内评论。
8. 再次运行测试和必要的界面验证。
9. 最后确认 Stage、Commit 或 Push 的实际范围。

Codex 需要操作浏览器或桌面软件验证结果时，结合 [[8、浏览器与计算机操作|浏览器与计算机操作]]；涉及文件和网络权限时，参考 [[12、权限、设置与故障排查|权限、设置与故障排查]]。
