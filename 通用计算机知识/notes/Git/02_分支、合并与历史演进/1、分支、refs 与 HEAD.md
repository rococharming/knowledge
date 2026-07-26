---
title: 分支、refs 与 HEAD
date: 2026-07-26
tags: [计算机基础, Git, Git分支]
aliases:
  - Git branch
  - Git ref
  - Git HEAD
---

# 一、最小模型

Git 分支不是项目文件夹的副本，而是一个指向 commit 的名字。理解这一点后，创建分支、切换分支、合并分支和查看历史都会变成“观察指针如何移动”。

![[assets/branches-refs-head-generated.png|600]]

这张图可以读成：`main` 和 `feature/note-title` 都是分支名；每个分支名指向某个 commit；`HEAD` 表示当前工作位置，通常跟着当前分支名。

## 1、三个关键词

| 关键词 | 最小理解 | 示例 |
|---|---|---|
| commit | 一次项目快照，有自己的编号，并指向上一个 commit | `c98a758` |
| branch / ref | 指向 commit 的名字 | `main`、`feature/note-title` |
| HEAD | 当前所在位置，通常指向当前 branch | `HEAD -> main` |

其中，branch 是 ref 的一种。ref 可以理解为“引用某个对象的名字”；分支 ref 通常保存在 `.git/refs/heads/` 下，远程跟踪分支等其他名字也属于 ref 家族。

## 2、读图方式

`git log --decorate` 会把分支名、标签名和 `HEAD` 标在提交旁边。例如：

```text
c98a758 (HEAD -> main) Complete local repository daily loop
```

这行可以读成两句话：

- `main` 指向 `c98a758` 这个 commit。
- `HEAD` 当前跟着 `main`。

如果看到：

```text
c98a758 (HEAD -> main, feature/note-title) Complete local repository daily loop
```

说明 `main` 和 `feature/note-title` 同时指向同一个 commit，但当前仍站在 `main` 上。

# 二、创建与切换

创建分支和切换分支是两个动作。创建分支只是增加一个名字；切换分支才会改变 `HEAD` 跟着谁。

## 1、只创建分支

```shell
git branch feature/note-title
```

这条命令会在当前 commit 上创建一个新分支名，但不会切换过去。

| 变化 | 说明 |
|---|---|
| 新增名字 | `feature/note-title` |
| 指向位置 | 当前 commit |
| HEAD 是否移动 | 不移动 |
| 文件是否复制 | 不复制 |

创建后查看最近历史：

```shell
git log --oneline --decorate --max-count=3
```

示例输出：

```text
c98a758 (HEAD -> main, feature/note-title) Complete local repository daily loop
8c4d05c Clarify practice repository purpose
409755c Record commit hygiene note
```

这里的关键是：`feature/note-title` 已经出现，但 `HEAD -> main` 说明当前仍在 `main`。

## 2、切换分支

```shell
git switch feature/note-title
```

切换后，`HEAD` 改为跟着新分支：

```text
c98a758 (HEAD -> feature/note-title, main) Complete local repository daily loop
```

文件内容不一定会变化。如果两个分支指向同一个 commit，工作目录看起来完全一样；真正变化的是 Git 当前站位。

> [!tip] 心智模型
> `git branch name` 是“贴一个新名字”；`git switch name` 是“站到这个名字上”。

# 三、提交移动

提交时，移动的是 `HEAD` 当前跟着的分支名。其他分支不会自动跟着移动。

![[assets/git-branch-commit-move-handdrawn.png|600]]

读这张图时，只看两个问题：提交前 `HEAD` 跟着哪个分支？提交后哪个分支名指向了新 commit？答案都是 `feature/note-title`，所以只有它向前移动，`main` 留在原来的 commit。

## 1、在分支上提交

假设当前在 `feature/note-title`，并新建了 `branch-note.txt`：

```shell
git add branch-note.txt
git commit -m "Add branch practice note"
```

提交后查看所有分支历史：

```shell
git log --oneline --decorate --graph --all --max-count=5
```

示例输出：

```text
* cc3957a (HEAD -> feature/note-title) Add branch practice note
* c98a758 (main) Complete local repository daily loop
* 8c4d05c Clarify practice repository purpose
* 409755c Record commit hygiene note
```

这就是分支开始分开的瞬间：`feature/note-title` 向前移动到新提交，`main` 仍停在旧提交。

## 2、谁会移动

| 当前状态 | 执行提交后 | 不会发生什么 |
|---|---|---|
| `HEAD -> main` | `main` 向前移动 | 其他分支不会自动移动 |
| `HEAD -> feature/note-title` | `feature/note-title` 向前移动 | `main` 不会自动移动 |
| detached HEAD | `HEAD` 指向新提交 | 没有分支名自动接住新提交 |

日常开发中，先确认自己在哪个分支，再提交改动。这和 [[通用计算机知识/notes/Git/01_本地仓库与提交基础/13、本地仓库日常循环|本地仓库日常循环]] 的“先观察、再操作、再验证”是一条连续习惯。

# 四、观察命令

分支学习的关键不是背命令，而是能看懂输出里的名字贴在哪个 commit 上。

## 1、常用命令

| 命令 | 作用 | 读图重点 |
|---|---|---|
| `git branch` | 列出本地分支 | `*` 标记当前分支 |
| `git status -sb` | 查看当前分支和简短状态 | `## main` 表示当前在 `main` |
| `git log --oneline --decorate --max-count=3` | 查看最近提交和 ref 位置 | 分支名贴在哪个 commit 上 |
| `git log --oneline --decorate --graph --all` | 查看所有分支的简短历史图 | 历史是否已经分叉 |

其中 `--decorate` 会显示分支名等 ref，`--graph` 会画出历史形状，`--all` 会把所有分支都纳入视图。

## 2、常见标记

| 标记 | 含义 |
|---|---|
| `HEAD -> main` | 当前 `HEAD` 跟着 `main` |
| `(main, feature/x)` | 两个分支名指向同一个 commit |
| `*` | `git log --graph` 里的提交节点，不等于当前分支标记 |
| `--all` | 显示所有分支，而不只显示当前分支能到达的历史 |

如果输出看不懂，先拆成三个问题：当前 `HEAD` 在哪里？每个分支名指向哪个 commit？当前分支是否比另一个分支多了提交？

# 五、本地练习

起点：继续使用 `practice-repo/`。第一专题结束后，仓库应为 clean，最新提交是 `Complete local repository daily loop`。

## 1、创建并观察

```shell
cd /Users/songpengfei/Learn/Git/practice-repo
git status -sb
git log --oneline --decorate --max-count=4
git branch feature/note-title
git log --oneline --decorate --max-count=3
```

检查点：

| 检查项 | 期待结果 |
|---|---|
| 当前分支 | 仍是 `main` |
| 新分支 | `feature/note-title` 已出现 |
| 两个分支位置 | `main` 和 `feature/note-title` 指向同一个 commit |

## 2、切换并提交

```shell
git switch feature/note-title
git status -sb
```

新建 `branch-note.txt`，写入：

```text
Practiced branches, refs, and HEAD.
```

然后提交：

```shell
git status -s
git diff
git add branch-note.txt
git commit -m "Add branch practice note"
git log --oneline --decorate --graph --all --max-count=6
git status -sb
```

目标状态：

| 检查项 | 期待结果 |
|---|---|
| 当前分支 | `feature/note-title` |
| 最新提交 | `Add branch practice note` |
| `main` 的位置 | 仍在 `Complete local repository daily loop` |
| 工作区状态 | clean |

# 六、常见误区

## 1、分支不是副本

创建分支通常很快，因为 Git 只是创建一个新 ref，不会复制整个项目目录。真正的文件内容来自 commit 快照，而不是来自“分支文件夹”。

## 2、创建不等于切换

```shell
git branch feature/note-title
```

只创建分支。

```shell
git switch feature/note-title
```

才切换当前分支。

## 3、只移动当前分支

如果 `HEAD` 跟着 `feature/note-title`，提交后移动的是 `feature/note-title`，不是 `main`。后续合并时，Git 才会把不同分支上的历史重新整理到一起。

# 七、小结

本篇最重要的一句话：

```text
分支是指向 commit 的名字，HEAD 告诉 Git 当前跟着哪个名字；提交时，当前分支名向前移动。
```

掌握这个模型后，后续的 merge、rebase、冲突解决和历史整理都会更容易理解：它们本质上都是在处理多个 commit 和多个 ref 之间的关系。
