---
title: 本地 merge 同步 PR 分支
date: 2026-08-03
tags: [Git, GitHub, Pull-Request, Git协作]
aliases:
  - git merge origin/main
  - 本地同步 PR 分支
---

# 一、本地同步

本地 merge 同步 PR 分支，是指不通过 GitHub 网页按钮，而是在本地 PR 分支上把 `origin/main` 合并进来，再把同步后的 PR 分支推回 GitHub。

核心顺序是：

```text
先 fetch 看见最新 origin/main
站在 PR 分支上 merge origin/main
本地 PR 分支包含 base 新提交
push 更新远程 PR 分支
```

这个动作和 [[9、同步 PR 分支|GitHub Update branch]] 的 merge 方式很像：二者都是把 base 分支的新变化带进 PR 的 head/source 分支。区别在于一个发生在 GitHub 页面，一个发生在本地终端。

# 二、操作对象

## 1、当前分支

本地同步 PR 分支时，当前分支应该是 PR 的来源分支，例如：

```text
feature/pr-practice
```

要改变的是 PR 分支，而不是 `main`。如果站在 `main` 上运行合并命令，方向就错了。

同步前先确认状态：

```shell
git status -sb
```

期待看到类似：

```text
## feature/pr-practice...origin/feature/pr-practice
```

## 2、合并对象

同步命令通常写成：

```shell
git merge origin/main
```

而不是：

```shell
git merge main
```

原因是：要同步的是 GitHub 上 base 分支的最新状态。先运行 `git fetch origin` 后，`origin/main` 才代表本地刚刚拿到的远程 `main` 位置。如果本地 `main` 还落后，直接 merge `main` 可能会把旧状态合进 PR 分支。

# 三、同步过程

## 1、同步前

假设 GitHub 上的 `main` 已经向前走了一步，而 PR 分支还没有包含这个提交：

```text
origin/main:              M --- C
                           \
feature/pr-practice:        A --- B
origin/feature/pr-practice: A --- B
```

用 [[8、PR 分支是否落后于 main|PR 分支落后判断]] 的命令比较：

```shell
git rev-list --left-right --count origin/main...origin/feature/pr-practice
```

可能得到：

```text
1       2
```

左边的 `1` 表示 `origin/main` 有 1 个 PR 分支还没包含的提交。

## 2、本地合并

在 PR 分支上运行：

```shell
git merge origin/main
```

如果没有冲突，会生成一个本地 merge commit：

```text
origin/main:              M --- C
                           \     \
feature/pr-practice:        A --- B --- U
origin/feature/pr-practice: A --- B
```

这里的 `U` 是本地同步提交。此时本地 PR 分支已经包含了 `origin/main` 的新提交，但远程 PR 分支还没有。

## 3、推回远程

本地同步完成后，再把当前 PR 分支推回 GitHub：

```shell
git push
```

推送后，本地 PR 分支和远程 PR 分支都包含同步提交：

```text
origin/main:              M --- C
                           \     \
feature/pr-practice:        A --- B --- U
origin/feature/pr-practice: A --- B --- U
```

这一步更新的是打开 PR 的来源分支。它仍然不是把 PR 合并进 `main`。

# 四、命令顺序

## 1、完整流程

一个完整的本地 merge 同步流程可以写成：

```shell
cd path/to/practice-repo
git status -sb
git fetch origin
git rev-list --left-right --count origin/main...origin/feature/pr-practice
git merge origin/main
git status -sb
git push
```

如果 `git merge origin/main` 成功，`git status -sb` 可能会显示：

```text
## feature/pr-practice...origin/feature/pr-practice [ahead 1]
```

`[ahead 1]` 表示本地 PR 分支已经有了同步提交，但 GitHub 上的远程 PR 分支还没有。此时普通 `git push` 就是把这个同步提交发送出去。

## 2、结果确认

推送后可以再次刷新远程跟踪分支并检查：

```shell
git fetch origin
git rev-list --left-right --count origin/main...origin/feature/pr-practice
git status -sb
```

同步成功后，`git rev-list` 左边通常回到 `0`，表示 `origin/main` 已经没有 PR 分支缺少的提交；`git status -sb` 也应该显示本地分支与 `origin/feature/pr-practice` 对齐。

# 五、命令拆解

| 命令 | 作用 | 重点 |
|---|---|---|
| `git status -sb` | 查看当前分支和工作区 | 确认站在 PR 分支，工作区干净 |
| `git fetch origin` | 更新远程跟踪分支 | 让 `origin/main` 代表 GitHub 最新 base |
| `git rev-list --left-right --count origin/main...origin/feature/pr-practice` | 比较 base 和 PR 分支 | 左边大于 0 才说明 PR 分支缺少 base 提交 |
| `git merge origin/main` | 把 base 新变化带进当前分支 | 当前分支必须是 PR 分支 |
| `git push` | 把本地同步提交发送到远程 PR 分支 | 让 GitHub PR 页面刷新 |

# 六、练习流程

## 1、准备 main 新提交

为了观察本地 merge 同步的完整过程，可以先让远程 `main` 向前移动一步，模拟“另一个改动已经进入主线”的场景。

在 GitHub 仓库页面操作：

1. 打开仓库主页。
2. 切换到 `main` 分支。
3. 新建文件 `local-merge-sync-note.md`。
4. 写入内容：

```text
Main moved forward for local merge sync practice.
```

5. 将这个文件提交到 `main`。

这个提交代表 base 分支上的新变化。完成后，PR 分支暂时还没有包含它。

## 2、诊断落后状态

回到本地仓库，确认当前站在 PR 分支上，并刷新远程跟踪分支：

```shell
cd path/to/practice-repo
git status -sb
git fetch origin
```

期待当前分支仍然是：

```text
## feature/pr-practice...origin/feature/pr-practice
```

然后比较 `origin/main` 和远程 PR 分支：

```shell
git rev-list --left-right --count origin/main...origin/feature/pr-practice
```

期待左边大于 0，例如：

```text
1       1
```

左边大于 0，说明 `origin/main` 有 PR 分支尚未包含的提交，可以继续做本地 merge 同步。

## 3、执行本地同步

确认当前分支仍然是 `feature/pr-practice` 后，把 `origin/main` 合进当前 PR 分支：

```shell
git merge origin/main
```

如果没有冲突，再查看状态：

```shell
git status -sb
```

可能看到：

```text
## feature/pr-practice...origin/feature/pr-practice [ahead 1]
```

这表示本地已经产生同步提交，但远程 PR 分支还没更新。接着推送当前分支：

```shell
git push
```

## 4、确认结果

推送后再次刷新并确认：

```shell
git fetch origin
git rev-list --left-right --count origin/main...origin/feature/pr-practice
git status -sb
```

期待状态是：

| 检查项 | 期待结果 |
|---|---|
| 当前分支 | `feature/pr-practice` |
| 工作区 | clean |
| PR 分支 | 已包含 `origin/main` 的新提交 |
| 左边数字 | 回到 `0` |
| 远程 PR 分支 | 与本地 feature 分支对齐 |
| PR 状态 | 仍然 open，尚未 merge |

# 七、风险边界

## 1、冲突状态

如果 `git merge origin/main` 提示 conflict，说明 Git 无法自动决定保留哪边内容。此时不要继续 push，也不要随手删除冲突标记；应该先查看冲突文件，明确选择内容，再完成合并。

冲突出现时，仓库通常会停在 merge 进行中的状态，`git status -sb` 会显示哪些文件需要处理。

## 2、常见误区

| 误区 | 更准确的理解 |
|---|---|
| 在 `main` 上运行 `git merge origin/main` | 要更新的是 PR 分支，当前分支应是 `feature/pr-practice` |
| `fetch` 之后以为已经同步 | `fetch` 只更新远程跟踪分支，不会合并进当前分支 |
| merge 后忘记 push | GitHub PR 页面只会在远程 PR 分支更新后刷新 |
| 看到冲突继续硬推 | 冲突状态下没有完成合并，不能把半成品推上去 |

本地 merge 同步的优势是过程可观察：你可以在 push 前检查提交图、运行测试、确认状态。它和 [[4、Push 与非快进拒绝|push]]、[[2、Fetch 与远程跟踪分支|fetch]] 一起构成了本地处理 PR 分支同步的基本路径。
