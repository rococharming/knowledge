---
title: PR 分支是否落后于 main
date: 2026-07-29
tags: [Git, GitHub, Pull-Request, Git协作]
aliases:
  - PR 分支落后
  - Pull Request out-of-date
---

# 一、状态判断

打开的 Pull Request 不是静止的：功能分支可能继续追加提交，作为 base 的 `main` 也可能被其他 PR 推进。当 `main` 有一些提交还没有进入 PR 分支时，就可以说这个 PR 分支落后于 `main`。

这里的关键不是立刻同步，而是先读懂状态。通常顺序是：

```text
先 fetch
再比较 origin/main 和 origin/feature
左边大于 0，说明 main 有 PR 分支还没包含的提交
```

这个判断建立在 [[2、Fetch 与远程跟踪分支|远程跟踪分支]] 之上：`origin/main` 和 `origin/feature/pr-practice` 是本地保存的远程状态快照，不是 GitHub 服务器本身。

# 二、先 fetch

`origin/main` 和 `origin/feature/pr-practice` 只有在更新后才可靠。判断 PR 分支是否落后前，先运行：

```shell
git fetch origin
```

`fetch` 只更新本地的远程跟踪分支，不会改当前工作区文件，也不会自动合并提交。它的作用是先把“远程现在走到哪里了”拿回来，再用本地命令比较两边历史。

示例：

```shell
cd path/to/practice-repo
git status -sb
git fetch origin
```

如果工作区原本是干净的，`git fetch origin` 不会让当前分支突然多出一个 merge commit，也不会替你解决分支差异。

# 三、数字比较

## 1、命令结构

可以用 `git rev-list --left-right --count` 数出两边各自独有的提交：

```shell
git rev-list --left-right --count origin/main...origin/feature/pr-practice
```

这里的 `origin/main...origin/feature/pr-practice` 表示比较两个引用从共同祖先之后各自独有的提交。命令输出有两个数字：

```text
0       2
```

读法是：

| 位置 | 含义 |
|---|---|
| 左边数字 | `origin/main` 独有提交数量 |
| 右边数字 | `origin/feature/pr-practice` 独有提交数量 |

## 2、结果含义

常见结果可以这样判断：

| 输出 | 含义 | 判断 |
|---|---|---|
| `0 2` | `main` 没有 PR 分支缺少的提交；PR 分支有 2 个自己的提交 | 当前不需要同步 base |
| `1 2` | `main` 有 1 个 PR 分支还没包含的提交；PR 分支有 2 个自己的提交 | PR 分支落后于 base，需要考虑同步 |
| `3 0` | `main` 有 3 个 PR 分支没有的提交；PR 分支没有自己的独有提交 | 可能当前比较的不是预期 PR 分支 |

> 左边数字大于 0，才说明 `main` 有 PR 分支尚未包含的新提交。

# 四、提交列表

## 1、查看差异

数字适合快速判断；如果要看两边到底各多了哪些提交，可以加上 `git log --left-right`：

```shell
git log --oneline --left-right origin/main...origin/feature/pr-practice
```

输出可能类似：

```text
> ed97680 Update pull request practice note
> 523191c Add pull request practice note
```

`>` 表示右边，也就是 `origin/feature/pr-practice` 独有；`<` 表示左边，也就是 `origin/main` 独有。

## 2、判断落后

如果列表中出现 `<` 开头的提交，说明 `origin/main` 上有 PR 分支还没有包含的提交。例如：

```text
< a1b2c3d Update README on main
> ed97680 Update pull request practice note
> 523191c Add pull request practice note
```

这表示两边都继续向前走了：`main` 有自己的新提交，PR 分支也有自己的新提交。此时同步 base 的方式要结合团队规则选择，不能只凭“落后”两个字立刻操作。

# 五、GitHub 提示

## 1、页面状态

GitHub PR 页面可能显示这些状态：

| GitHub 提示 | 可能含义 | 先做什么 |
|---|---|---|
| 没有 Update branch 提示 | PR 分支可能没有落后，或仓库不要求同步 | 用命令确认 |
| `This branch is out-of-date` | base 分支有新提交，PR 分支还没包含 | 判断是否需要同步 |
| `Update branch` | GitHub 可以把 base 的变化带进 PR 分支 | 先确认团队偏好的同步方式 |
| conflicts 提示 | base 的新变化和 PR 分支改动冲突 | 停下，进入冲突处理流程 |

GitHub 的提示适合快速感知 PR 状态，但命令行比较能把“落后几个提交、两边各有什么提交”讲清楚。

## 2、同步时机

PR 分支落后于 `main` 不一定意味着必须马上同步。常见需要同步的情况有：

| 情况 | 原因 |
|---|---|
| 仓库规则要求 branch up to date | 不同步就不能合并 |
| CI 需要基于最新 `main` 重新跑 | 避免旧基础上测试通过，新基础上失败 |
| `main` 的新变化和当前 PR 相关 | 需要提前发现兼容性问题 |
| GitHub 显示冲突 | 必须处理后才能安全合并 |

如果只是小文档改动，且 `main` 的新提交明显无关，团队也可能允许直接合并，或者由 merge queue、squash merge 等流程统一处理。重点是先判断状态，再决定是否同步。

# 六、命令速查

| 命令 | 作用 | 读法 |
|---|---|---|
| `git fetch origin` | 更新本地远程跟踪分支 | 让 `origin/main` 和 `origin/feature` 接近远程最新状态 |
| `git rev-list --left-right --count A...B` | 数出两边各自独有提交数量 | 左边数字属于 `A`，右边数字属于 `B` |
| `git log --oneline --left-right A...B` | 列出两边各自独有提交 | `<` 属于 `A`，`>` 属于 `B` |

这个判断流程通常接在 [[7、更新已打开的 Pull Request|更新已打开的 PR]] 之后使用：PR 分支已经能继续追加提交，下一步就要能判断它和 base 之间是否已经拉开距离。真正执行同步时，再选择 GitHub 页面更新、本地 merge 或本地 rebase。
