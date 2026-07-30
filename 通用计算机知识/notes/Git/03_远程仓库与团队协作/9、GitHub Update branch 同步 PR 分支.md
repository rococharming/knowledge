---
title: GitHub Update branch 同步 PR 分支
date: 2026-07-29
tags: [Git, GitHub, Pull-Request, Git协作]
aliases:
  - Update branch
  - 同步 PR 分支
---

# 一、Update branch

`Update branch` 是 GitHub Pull Request 页面上的同步入口。它的作用是把 base 分支的新变化带进 PR 的来源分支，让 PR 分支追上 base。

最小模型是：

```text
main 有新提交
PR 分支落后
点击 Update branch
base 的新变化进入 PR 分支
PR 仍然 open
```

这里最容易混淆的是：`Update branch` 不是 `Merge pull request`。它更新的是 PR 的 head/source 分支，例如 `feature/pr-practice`；它不会把 PR 的改动正式合入 `main`。

# 二、分支方向

## 1、base 与 head

一个 PR 至少涉及两个方向：

```text
base: main
head: feature/pr-practice
```

`base` 是准备合入的目标分支，通常是 `main`。`head` 是承载改动的来源分支，也就是 PR 分支。

点击 `Update branch` 的意思是：

```text
把 main 的新变化带进 feature/pr-practice
```

不是：

```text
把 feature/pr-practice 合进 main
```

## 2、按钮区别

| 按钮 | 改变谁 | 含义 |
|---|---|---|
| `Update branch` | PR 的 head/source 分支 | 让 PR 分支包含 base 的新变化 |
| `Merge pull request` | base 分支，通常是 `main` | 把 PR 的改动正式合进主线 |

因此，在同步 PR 分支时要确认自己点的是 `Update branch`，而不是最终合并按钮。

# 三、同步前后

## 1、同步前

如果 `main` 已经有 PR 分支尚未包含的新提交，提交图可以简化成：

```text
main:    M --- C
          \
feature:  A --- B
```

用 [[8、PR 分支是否落后于 main|PR 分支落后判断]] 的命令诊断：

```shell
git rev-list --left-right --count origin/main...origin/feature/pr-practice
```

可能得到：

```text
1       2
```

含义是：`origin/main` 有 1 个 PR 分支还没包含的提交，`origin/feature/pr-practice` 有 2 个自己的提交。

## 2、同步后

如果 GitHub 使用传统 merge 方式更新 PR 分支，点击 `Update branch` 后，PR 分支上会多出一个同步提交：

```text
main:    M --- C
          \     \
feature:  A --- B --- U
```

这里的 `U` 是同步提交，它把 `main` 的新变化带进了 PR 分支。再次诊断时，左边通常会回到 0：

```text
0       3
```

左边为 0，说明 `origin/main` 已经没有 PR 分支缺少的提交。

上述默认其实是`merge`方式。

# 四、页面设置

## 1、按钮条件

GitHub 是否显示 `Update branch` 受多个因素影响：

| 情况 | 说明 |
|---|---|
| PR 分支没有落后 | 没有需要同步的 base 新提交 |
| 仓库设置不主动建议更新 | 页面可能不显示明显按钮 |
| 当前账号权限不足 | 不能更新这个 PR 的 head branch |
| 存在合并冲突 | 需要先进入冲突处理流程 |
| head branch 受保护 | 网页按钮可能无法直接更新 |

如果已经用命令确认左边数字大于 0，但 PR 页面仍然没有 `Update branch`，先检查仓库设置和页面提示，不要直接改用 `force push`。

## 2、建议更新

GitHub 仓库的 Pull Requests 设置里有一个选项：`Always suggest updating pull request branches`。启用后，只要 base 分支有新的可同步变化，PR 页面就会更主动地显示更新分支的提示。

![[assets/github-pr-settings-always-suggest-update-branch.png|700]]

这张图中红框标出的设置位于仓库的 Pull Requests 配置区域。它控制的是“当 base 分支出现新变化时，是否提示用户更新 PR 分支”，不是在自动合并 PR，也不是替用户选择 merge 或 rebase 策略。

# 五、网页操作

## 1、操作顺序

使用 GitHub 页面同步 PR 分支时，顺序可以保持简单：

1. 打开 GitHub 仓库的 Pull requests。
2. 进入目标 PR，确认方向是 `feature/pr-practice` into `main`。
3. 确认 PR 仍然是 open 状态。
4. 看到 `This branch is out-of-date` 或 `Update branch` 时，先读清楚提示。
5. 点击 `Update branch`。
6. 如果有下拉菜单，初学阶段优先选择 merge 方式，不选择 rebase。
7. 等页面刷新后，确认 PR 仍然 open，尚未 merge。

## 2、选择 merge

GitHub 可能允许通过 merge 或 rebase 更新 head branch。merge 方式会在 PR 分支上产生一个同步提交，历史更直观；rebase 会重写 PR 分支上的提交位置，后续本地同步会更复杂。

对入门练习和多数不追求线性历史的小仓库来说，先用 merge 方式更容易理解。团队若要求线性历史，应按仓库规则处理。

# 六、本地跟上

## 1、先 fetch

网页按钮改变的是 GitHub 上的远程分支，本地当前分支不会自动移动。回到终端后，先取得远程最新状态：

```shell
git fetch origin
```

再查看当前分支：

```shell
git status -sb
```

可能看到：

```text
## feature/pr-practice...origin/feature/pr-practice [behind 1]
```

这表示远程的 `feature/pr-practice` 已经多了同步提交，而本地同名分支还停在旧位置。

## 2、再快进

如果本地没有自己的新提交，可以用 fast-forward pull 跟上远程分支：

```shell
git pull --ff-only
```

再次查看状态：

```shell
git status -sb
```

看到类似下面的结果，表示本地分支已经和远程分支对齐：

```text
## feature/pr-practice...origin/feature/pr-practice
```

# 七、常见误区

| 误区 | 更准确的理解 |
|---|---|
| `Update branch` 等于合并 PR | 它只是更新 PR 分支，不会把 PR 合进 `main` |
| 网页更新后本地也自动更新 | 网页改变远程分支，本地仍要 `fetch` 和必要的 `pull --ff-only` |
| 按钮不出现就是 Git 坏了 | 可能是没落后、权限不足、仓库设置、冲突或分支保护导致 |
| 初学阶段随手选 rebase | rebase 会改写提交位置，本地同步和团队协作规则更复杂 |

同步成功后，可以再次运行：

```shell
git rev-list --left-right --count origin/main...origin/feature/pr-practice
```

如果左边回到 0，就说明 `origin/main` 已经没有 PR 分支缺少的提交。这个流程衔接 [[6、PR Review 与检查状态|PR 检查状态]]：同步后通常需要重新观察 Checks、冲突提示和 review 结论。
