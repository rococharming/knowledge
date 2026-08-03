---
title: 合并 PR 并同步本地 main
date: 2026-08-03
tags: [Git, GitHub, Pull-Request, Git协作]
aliases:
  - Merge pull request
  - 同步本地 main
---

# 一、合并与同步

`Merge pull request` 是把 PR 的改动合进 base 分支的动作。常见情况下，base 是 GitHub 上的 `main`，所以网页合并成功后，远程 `main` 会前进。

完整链路是：

```text
GitHub 上点击 Merge pull request
远程 main 前进
本地 main 还停在旧位置
切回 main
git fetch origin
git pull --ff-only
本地 main 跟上 origin/main
```

这一步和 [[9、同步 PR 分支|同步 PR 分支]] 的方向相反：同步 PR 分支是把 base 的新变化带进 PR 分支；合并 PR 是把 PR 的最终改动带进 base。

# 二、改变位置

## 1、网页合并

合并 PR 改变的是 GitHub 上的 base 分支，通常是远程 `main`。它不会自动改变终端里的本地分支。

| 动作 | 改变哪里 |
|---|---|
| GitHub 页面点击 `Merge pull request` | GitHub 上的 `main` |
| `git fetch origin` | 本地的 `origin/main` 远程跟踪分支 |
| `git pull --ff-only` | 当前本地分支，例如本地 `main` |

因此，网页上看到 PR 已经 merged，不代表本地 `main` 已经包含这些提交。

## 2、提交图

合并前：

```text
origin/main:               M
                            \
origin/feature/pr-practice:  A --- B
```

点击 GitHub 的 `Merge pull request` 后，如果选择普通 merge commit：

```text
origin/main:               M -------- P
                            \       /
origin/feature/pr-practice:  A --- B
```

`P` 是 GitHub 在 `main` 上创建的 PR 合并提交。PR 会变成 merged 状态。

如果仓库选择 squash merge 或 rebase merge，历史图会不同。入门阶段先用普通 merge commit 理解，因为它最容易看清分支关系。

# 三、网页操作

## 1、合并前确认

真正合并前，先确认 [[12、PR 合并前检查清单|合并前检查]] 已经完成，尤其是这些项目：

| 检查项 | 期待状态 |
|---|---|
| base | `main` |
| compare | `feature/pr-practice` |
| conflicts | 没有冲突提示 |
| out-of-date | 没有落后提示，或已处理 |
| Checks | 通过，或确认练习仓库没有配置 CI |
| Files changed | 都属于当前改动目标 |

这些检查通过后，才进入合并动作。

## 2、合并步骤

在 GitHub PR 页面操作：

1. 确认 base 是 `main`。
2. 确认 compare 是 `feature/pr-practice`。
3. 确认没有 conflicts、out-of-date 或失败 Checks。
4. 点击 `Merge pull request`。
5. 如果有合并方式选项，选择普通 merge commit。
6. 确认合并提交标题和说明可以读懂。
7. 点击确认合并。
8. 确认 PR 状态变成 merged。

GitHub 可能在合并后提示删除远程 feature 分支。删除分支属于合并后的清理动作，可以单独处理；不要把合并和清理混在一起。

# 四、本地同步

## 1、切回 main

网页合并后，本地当前分支可能仍然是 `feature/pr-practice`：

```shell
git status -sb
```

可能看到：

```text
## feature/pr-practice...origin/feature/pr-practice
```

这时不要在 feature 分支上直接 `pull`。`git pull` 会更新当前分支，而现在要更新的是本地 `main`：

```shell
git switch main
```

## 2、刷新远程

切到 `main` 后，先获取 GitHub 最新状态：

```shell
git fetch origin
```

查看状态：

```shell
git status -sb
```

可能看到：

```text
## main...origin/main [behind 1]
```

`[behind 1]` 表示本地 `main` 比 GitHub 上的 `origin/main` 落后 1 个提交。

## 3、快进本地 main

网页合并 PR 后，本地 `main` 通常只是落后远程 `main`，没有自己的新提交。此时用 fast-forward 方式跟上：

```shell
git pull --ff-only
```

完成后再次查看：

```shell
git status -sb
```

期待看到：

```text
## main...origin/main
```

这表示本地 `main` 已经与 `origin/main` 对齐。

# 五、练习流程

## 1、合并 PR

打开 GitHub PR 页面，按顺序操作：

1. 确认 base 是 `main`，compare 是 `feature/pr-practice`。
2. 确认没有 conflicts 或 out-of-date 提示。
3. 点击 `Merge pull request`。
4. 如果有合并方式，选择普通 merge commit。
5. 确认合并。
6. 观察 PR 状态变成 merged。
7. 暂时不要删除远程 feature 分支。

完成后，GitHub 上的 `main` 已经包含 PR 改动。

## 2、本地 main 跟上

回到本地终端：

```shell
cd path/to/practice-repo
git status -sb
git switch main
git fetch origin
git status -sb
git pull --ff-only
git status -sb
git log --oneline --decorate --graph --all --max-count=12
```

期待状态：

| 检查项 | 期待结果 |
|---|---|
| GitHub PR | merged |
| 当前本地分支 | `main` |
| 工作区 | clean |
| 本地 `main` | 与 `origin/main` 对齐 |
| 历史图 | 能看到 PR 合并进入 `main` |
| 远程 feature 分支 | 暂时不要求删除 |

# 六、异常处理

## 1、快进失败

如果 `git pull --ff-only` 失败，并看到类似：

```text
fatal: Not possible to fast-forward, aborting.
```

说明本地 `main` 和远程 `main` 不是简单的“本地落后”关系，可能本地 `main` 上也有远程没有的提交。此时先停下，不要随手 merge 或 force push。

可以先查看状态和历史图：

```shell
git status -sb
git log --oneline --decorate --graph --all --max-count=12
```

确认清楚为什么分叉后，再决定如何处理。

## 2、常见误区

| 误区 | 更准确的理解 |
|---|---|
| 网页合并后本地 `main` 自动更新 | 不会，本地仓库需要自己 `fetch` 和 `pull` |
| 还站在 feature 分支上就 `pull` | `pull` 更新当前分支，要同步本地 `main` 应先 `git switch main` |
| 合并 PR 后立刻删除所有分支 | 合并和清理是两个动作，可以分开处理 |
| `pull --ff-only` 失败后继续乱试 | 失败说明历史不是简单快进，应先诊断 |

合并 PR 的关键是分清远程和本地：GitHub 上的 `main` 先前进，本地再通过 `fetch` 和 `pull --ff-only` 跟上。这个流程和 [[3、Pull 与快进更新|pull 的快进更新]] 直接相关。
