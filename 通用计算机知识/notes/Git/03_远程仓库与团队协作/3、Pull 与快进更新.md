---
title: Pull 与快进更新
date: 2026-07-28
tags: [Git, Git远程仓库, Git协作, Git合并]
aliases:
  - git pull
  - git pull --ff-only
  - pull fast-forward
---

# 一、Pull

`git pull` 用来从远程仓库取得新状态，并把这些变化整合进当前本地分支。它可以粗略理解为：

```text
pull = fetch + 整合当前分支
```

这里最容易误解的是：pull 不是只读观察。只想取回远程状态、更新 `origin/main`、但不改变当前分支时，应使用 [[2、Fetch 与远程跟踪分支|fetch]]。

## 1、两个阶段

pull 包含两个逻辑阶段：

| 阶段 | 做什么 | 影响 |
|---|---|---|
| fetch | 从 GitHub 取回新提交，更新 `origin/main` | 更新远程跟踪分支 |
| integrate | 把远程变化整合进当前本地分支 | 可能移动当前分支 |

所以 pull 前一定要先确认当前分支。你站在 `main` 上 pull，Git 会尝试更新 `main`；站在其他分支上 pull，影响的就是那个当前分支。

## 2、前置检查

运行 pull 前先看状态：

```shell
git status -sb
```

常见的健康状态类似：

```text
## main...origin/main
```

这表示当前在 `main`，并且本地 `main` 已经跟踪 `origin/main`。如果工作区有未提交修改，先处理干净再 pull，避免把本地未完成修改和远程整合混在一起。

# 二、快进更新

`git pull --ff-only` 是一种更保守的 pull：只有当前分支可以 [[通用计算机知识/notes/Git/02_分支、合并与历史演进/3、Fast-forward 合并|fast-forward]] 时才更新；如果本地和远程已经分叉，它会停止。

## 1、命令含义

示例：

```shell
git pull --ff-only
```

它的意思是：

```text
只有当前分支能直接快进到远程最新提交时，才移动当前分支。
如果需要创建 merge commit 或处理分叉，就停止。
```

这种写法的好处是边界清楚：能快进就更新；不能快进就先读图、诊断历史关系，而不是让 pull 自动进入一个自己还没看懂的整合状态。

## 2、输出读法

GitHub 上有新提交后，运行：

```shell
git pull --ff-only
```

可能看到：

```text
From github.com:YOUR-USER/git-practice-remote
   a42b910..b83d231  main       -> origin/main
Updating a42b910..b83d231
Fast-forward
 github-pull-note.md | 1 +
 1 file changed, 1 insertion(+)
```

这段输出分两层读：

| 输出 | 含义 |
|---|---|
| `main -> origin/main` | fetch 阶段更新了远程跟踪分支 |
| `Updating ...` | 本地当前分支准备移动 |
| `Fast-forward` | 当前分支直接快进到远程最新提交 |

如果 pull 结束后 `main` 和 `origin/main` 指向同一个提交，本地分支就已经跟上远程。

# 三、分叉停止

`--ff-only` 的价值不只是“成功快进”，也包括“该停时停”。当本地和远程各自都有新提交时，历史已经分叉，不能简单快进。

## 1、分叉形状

示例：

```text
main(local):   A -- B -- L
                    \
origin/main:          R
```

这里本地 `main` 有提交 `L`，远程 `origin/main` 有提交 `R`。两边都从共同祖先 `B` 后前进，无法通过移动一个指针完成快进。

## 2、停止提示

运行：

```shell
git pull --ff-only
```

可能看到：

```text
fatal: Not possible to fast-forward, aborting.
```

这不是坏事。它说明 Git 没有替你自动创建 merge commit，也没有改写本地提交，而是把控制权交还给你。此时应先用 `git status -sb` 和 `git log --oneline --decorate --graph --all` 读清楚历史图，再决定 merge、rebase，或先和协作者确认。

# 四、命令对比

## 1、Fetch 与 Pull

| 命令 | 更新 `origin/main` | 改当前分支 | 适合场景 |
|---|---|---|---|
| `git fetch origin` | 会 | 不会 | 只想观察远程变化 |
| `git pull --ff-only` | 会 | 会，但只允许快进 | 本地没有分叉时安全跟进远程 |
| `git pull` | 会 | 会，整合方式取决于配置 | 已理解仓库 pull 策略时使用 |

`git pull` 默认的整合方式可能受配置影响，例如使用 merge 或 rebase。团队仓库里应遵守项目约定；个人练习或不确定时，优先用 `git pull --ff-only` 保持历史关系清楚。

## 2、推荐顺序

日常更稳的顺序是：

```shell
git status -sb
git pull --ff-only
git log --oneline --decorate --graph --all --max-count=8
```

含义如下：

| 步骤 | 目的 |
|---|---|
| `git status -sb` | 确认当前分支和工作区状态 |
| `git pull --ff-only` | 只接受可快进的远程更新 |
| `git log --graph --all` | 确认本地分支和远程跟踪分支位置 |

# 五、本地检查

完成 fetch 练习并让本地 `main` 与 `origin/main` 对齐后，可以在 GitHub 网页新建 `github-pull-note.md`，写入：

```text
Created from GitHub for pull practice.
```

提交到 GitHub 的 `main` 后，在本地运行：

```shell
cd path/to/practice-repo
git status -sb
git pull --ff-only
git status -sb
git log --oneline --decorate --graph --all --max-count=8
```

重点观察：

- pull 前当前分支应为 `main`，工作区应为 clean。
- pull 输出中应先看到 `main -> origin/main`，再看到 `Fast-forward`。
- pull 后 `main` 和 `origin/main` 应指向同一个最新提交。
- 如果出现 `Not possible to fast-forward`，说明历史已经分叉，应停止并读图。

pull 的核心结论是：它会获取远程状态并整合到当前分支；`git pull --ff-only` 只允许快进更新，让历史分叉时先停下来。
