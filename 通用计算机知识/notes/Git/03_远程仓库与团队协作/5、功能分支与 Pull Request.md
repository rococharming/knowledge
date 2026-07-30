---
title: 功能分支与 Pull Request
date: 2026-07-28
tags: [Git, GitHub, Git协作, PullRequest]
aliases:
  - feature branch
  - Pull Request
  - PR
---

# 一、功能分支

功能分支是为一个独立任务临时创建的分支。它把正在开发的改动和稳定主线隔离开，让 `main` 尽量保持可运行、可发布、可协作。

团队协作里，常见工作模型是：

```text
main 保持稳定
每个任务开 feature branch
把 feature branch 推到 GitHub
用 Pull Request 请求合进 main
```

## 1、分支职责

| 分支 | 职责 | 常见操作 |
|---|---|---|
| `main` | 稳定主线，保存已经确认的结果 | 同步、发布、接收合并 |
| `feature/pr-practice` | 单个任务的工作线 | 提交任务改动、推送到 GitHub、发起 PR |

功能分支延续了 [[通用计算机知识/notes/Git/02_分支、合并与历史演进/2、创建与切换分支|创建与切换分支]] 的模型：分支名只是指向 commit 的引用。开任务分支，就是从当前提交拉出一条独立工作线。

## 2、开始位置

创建功能分支前，通常先让本地 `main` 跟上远程：

```shell
git switch main
git pull --ff-only
git switch -c feature/pr-practice
```

这样做的目的是从最新主线开始工作，减少后续合并时的分叉和冲突。`git pull --ff-only` 的边界见 [[3、Pull 与快进更新|Pull 与快进更新]]。

# 二、Pull Request

Pull Request 不是 Git 本地命令，而是 GitHub 上的协作对象。它表达的是一个合并提议：

```text
请把这个来源分支的改动合进目标分支。
```

PR 给代码审查、讨论、自动检查和最终合并提供了一个固定位置。它让团队不必只靠聊天消息或裸 push 来决定哪些改动进入主线。

![[assets/Pasted image 20260728234633.png|600]]

## 1、对象关系

| 对象 | 含义 |
|---|---|
| feature branch | 任务改动所在分支 |
| Pull Request | 围绕分支差异创建的合并请求 |
| review | 人工审查、评论、请求修改或批准 |
| checks | 自动测试、构建、格式检查等状态 |
| merge | PR 通过后把改动合进目标分支 |

创建 PR 不会自动改变 `main`。只有后续点击 merge，或者维护者按团队流程完成合并后，目标分支才会改变。

![[assets/Pasted image 20260728234709.png|600]]

## 2、方向选择

PR 页面里最关键的是 base 和 compare：

| 区域 | 含义 | 示例 |
|---|---|---|
| base | 目标分支，改动要合进去的地方 | `main` |
| compare | 来源分支，改动从哪里来 | `feature/pr-practice` |

方向应读成：

```text
base: main
compare: feature/pr-practice
```

也就是：请求把 `feature/pr-practice` 合进 `main`。方向选反时，PR 的含义也会反，容易把主线改动误当成功能分支改动。

# 三、发布分支

本地功能分支只有推送到 GitHub 后，GitHub 才能围绕它创建 Pull Request。第一次推送新分支时，通常使用 `-u` 建立 upstream。

## 1、首次推送

示例：

```shell
git push -u origin feature/pr-practice
```

可能看到：

```text
To github.com:YOUR-USER/git-practice-remote.git
 * [new branch]      feature/pr-practice -> feature/pr-practice
branch 'feature/pr-practice' set up to track 'origin/feature/pr-practice'.
```

这里的 `-u` 会让本地 `feature/pr-practice` 跟踪 GitHub 上的 `origin/feature/pr-practice`。后续站在这个分支上时，可以更方便地使用简短的 `git push` 或 `git pull`。

## 2、状态确认

查看本地分支和 upstream：

```shell
git branch -vv
```

可能看到：

```text
* feature/pr-practice  7c1d8a2 [origin/feature/pr-practice] Add pull request practice note
  main                 c71a120 [origin/main] Add local push practice note
```

方括号里的 `[origin/feature/pr-practice]` 表示本地功能分支已经和 GitHub 上的同名远程跟踪分支建立默认对应关系。

# 四、PR 页面

PR 页面不是只看标题。创建前至少确认方向、提交、文件差异和检查状态，避免把错误内容提交给审查者。

## 1、检查区域

| 区域 | 检查点 |
|---|---|
| base | 目标分支，通常是 `main` |
| compare | 来源分支，例如 `feature/pr-practice` |
| Commits | 这次 PR 包含哪些提交 |
| Files changed | 最终会合进 `main` 的文件差异 |
| Checks | 自动检查是否通过 |
| Review | 是否有人批准、评论或请求修改 |

`Files changed` 是最值得认真看的区域之一。它回答的问题是：如果这个 PR 被合并，目标分支到底会得到哪些文件变化。

## 2、合并边界

PR 创建后，它只是一个合并请求。此时：

| 状态 | 是否已经发生 |
|---|---|
| GitHub 上有功能分支 | 是 |
| GitHub 上有 PR 页面 | 是 |
| `main` 已经包含功能分支改动 | 否 |

只有完成 merge 后，`main` 才会包含功能分支里的提交。这个边界很重要，因为“提出请求”和“主线改变”是两个不同动作。

# 五、流程清单

## 1、命令顺序

一个最小功能分支流程如下：

```shell
cd path/to/practice-repo
git status -sb
git switch main
git pull --ff-only
git switch -c feature/pr-practice
```

新建 `pr-practice-note.md`，写入：

```text
Created on a feature branch for pull request practice.
```

提交并推送：

```shell
git add pr-practice-note.md
git commit -m "Add pull request practice note"
git push -u origin feature/pr-practice
git branch -vv
```

## 2、GitHub 操作

推送功能分支后，在 GitHub 仓库页面创建 Pull Request：

| 步骤 | 检查点 |
|---|---|
| 点击 Compare & pull request | 确认来源是刚推送的 feature 分支 |
| 检查 base | 应是 `main` |
| 检查 compare | 应是 `feature/pr-practice` |
| 填写标题 | 例如 `Add pull request practice note` |
| 查看 Files changed | 确认只包含预期改动 |
| 创建 PR | 先创建，不等于已经合并 |

目标状态是：本地停在功能分支，工作区 clean；GitHub 上有 `feature/pr-practice` 远程分支；PR 从 `feature/pr-practice` 指向 `main`，暂时还未合并。

# 六、常见误区

## 1、直接推主线

所有任务都直接推 `main`，会让主线承受未审查、未讨论、未通过检查的改动。功能分支把任务隔离出来，PR 再决定何时进入主线。

## 2、方向选反

PR 的正确读法是“compare 合进 base”。从功能分支进主线时，通常是 `base: main`、`compare: feature/pr-practice`。

## 3、创建即合并

创建 PR 只是提出请求。审查、检查和 merge 是后续动作。只有 merge 完成后，`main` 才包含功能分支改动。

功能分支的核心结论是：任务改动先放在独立分支里，Pull Request 再把这个分支变成一个可讨论、可审查、可合并的 GitHub 提议。
