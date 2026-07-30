---
title: Fetch 与远程跟踪分支
date: 2026-07-28
tags: [Git, Git远程仓库, Git协作, Git分支]
aliases:
  - git fetch
  - 远程跟踪分支
  - origin/main
---

# 一、Fetch

`git fetch` 是从远程仓库取回新状态的命令。它会下载本地还没有的提交，并更新 `origin/main` 这类远程跟踪分支，但不会自动移动当前工作的本地分支。

可以把 fetch 理解成一个安全的观察动作：

```text
先从 GitHub 拿回消息 -> 更新 origin/main -> 再决定是否整合到本地 main
```

## 1、更新内容

`git fetch origin` 主要做两件事：

| 动作 | 说明 |
|---|---|
| 下载远程新对象 | 把 GitHub 上本地没有的 commit、tree、blob 等对象拿回来 |
| 更新远程跟踪分支 | 例如把 `origin/main` 更新到 GitHub `main` 的新位置 |

这里的 `origin` 是远程仓库别名，模型见 [[1、远程仓库与第一次推送|远程仓库与第一次推送]]。如果本地 `main` 已经跟踪 `origin/main`，fetch 后就能比较本地分支和远程跟踪分支之间的差异。

## 2、不改内容

fetch 不会自动改变本地 `main` 的文件内容，也不会替你完成合并。它只是让本地知道“远程现在在哪里”。

这点很重要：远程有新提交时，fetch 先更新 `origin/main`；本地 `main` 是否跟进，需要再用 `merge`、`rebase` 或 `pull` 等方式决定。

# 二、三种状态

理解 fetch 的关键，是分清 GitHub 上的真实远程分支、本地记录的远程跟踪分支，以及你正在工作的本地分支。

## 1、名称区分

| 名字 | 含义 | fetch 是否会直接更新 |
|---|---|---|
| GitHub 上的 `main` | 远程仓库里的真实 `main` | 不是本地对象，由远程仓库维护 |
| `origin/main` | 本地记录的 GitHub `main` 状态 | 会 |
| 本地 `main` | 当前工作的本地分支 | 不会 |

`origin/main` 不是 GitHub 本体，而是本地仓库中一条远程跟踪分支。它像一枚书签：记录上一次从 `origin` 观察到的远程 `main` 位置。

## 2、状态变化

假设 GitHub 网页上新增了一个提交，本地还没有运行 fetch，此时三者关系是：

```text
GitHub main 已经前进
origin/main 还停在旧位置
本地 main 也还停在旧位置
```

运行：

```shell
git fetch origin
```

fetch 后变成：

```text
GitHub main 在新位置
origin/main 更新到新位置
本地 main 仍停在旧位置
```

这就是为什么 fetch 后可能看到本地分支 `behind`：远程跟踪分支已经知道远程前进了，但本地工作分支还没有整合这些提交。

# 三、观察远程

fetch 的价值在于把“取回远程状态”和“改动本地分支”拆开。拆开之后，就可以先看清楚远程多了什么，再决定下一步动作。

## 1、运行 fetch

示例：

```shell
git fetch origin
```

可能看到：

```text
From github.com:YOUR-USER/git-practice-remote
   df306c3..a42b910  main       -> origin/main
```

最后一行的 `main -> origin/main` 表示：GitHub 上的 `main` 有了新位置，本地的 `origin/main` 已经更新过去。

## 2、读取状态

fetch 后查看简短状态：

```shell
git status -sb
```

可能看到：

```text
## main...origin/main [behind 1]
```

含义如下：

| 片段 | 说明 |
|---|---|
| `main...origin/main` | 本地 `main` 跟踪 `origin/main` |
| `behind 1` | 本地 `main` 落后 `origin/main` 一个提交 |

`behind` 不是错误，只是提示远程跟踪分支领先于本地分支。此时本地文件还没有自动变化。

## 3、查看差异

看远程比本地多了哪些提交：

```shell
git log --oneline --decorate main..origin/main
```

可能看到：

```text
a42b910 (origin/main) Add note from GitHub
```

看具体文件差异：

```shell
git diff main..origin/main
```

`main..origin/main` 可以读作：从本地 `main` 到 `origin/main` 之间，远程跟踪分支多出来了什么。

# 四、整合本地

确认远程变化没问题后，可以把本地 `main` 跟上 `origin/main`。如果本地 `main` 没有自己的新提交，通常会形成 fast-forward。

## 1、手动合并

示例：

```shell
git merge origin/main
```

可能看到：

```text
Updating df306c3..a42b910
Fast-forward
 github-note.md | 1 +
 1 file changed, 1 insertion(+)
```

这表示本地 `main` 没有分叉，只是落后于 `origin/main`，所以 Git 直接把本地 `main` 指针向前移动。

## 2、再次检查

整合后再次查看：

```shell
git status -sb
```

理想状态是：

```text
## main...origin/main
```

如果不再显示 `[behind 1]`，说明本地 `main` 已经跟上远程跟踪分支。

# 五、Fetch 与 Pull

`fetch` 和 `pull` 都会接触远程仓库，但它们的风险边界不同。学习阶段先练 fetch，有助于把“拿消息”和“改当前分支”分成两步看。

## 1、命令差别

| 命令 | 做什么 | 是否自动整合进当前分支 |
|---|---|---|
| `git fetch origin` | 获取远程状态，更新 `origin/main` | 否 |
| `git pull` | 先 fetch，再整合到当前分支 | 是 |

`pull` 可以粗略理解为：

```text
pull = fetch + 整合
```

这里的“整合”可能是 merge，也可能按配置使用 rebase。正因为 pull 会继续改当前分支，所以在不确定远程多了什么时，先 fetch 再观察会更稳。

## 2、常见误区

| 误区 | 更准确的理解 |
|---|---|
| fetch 会自动改本地文件 | fetch 只更新远程跟踪分支 |
| `origin/main` 就是 GitHub 本体 | `origin/main` 是本地记录的远程状态 |
| 看到 `behind` 就出错了 | `behind` 只是说明本地分支还没整合远程提交 |
| pull 只是 fetch 的别名 | pull 比 fetch 多了整合当前分支这一步 |

# 六、本地检查

完成第一次推送并建立 upstream 后，可以用 GitHub 网页创建一个远程提交，再在本地观察 fetch 的效果。

在 GitHub 网页上新建 `github-note.md`，写入：

```text
Created from GitHub for fetch practice.
```

提交到 GitHub 的 `main` 后，在本地运行：

```shell
cd path/to/practice-repo
git status -sb
git fetch origin
git status -sb
git log --oneline --decorate main..origin/main
git diff main..origin/main
git merge origin/main
git status -sb
```

重点观察：

- fetch 前，本地可能还不知道 GitHub 网页上的新提交。
- fetch 后，`origin/main` 更新，本地 `main` 可能显示 `[behind 1]`。
- `git log main..origin/main` 能看到远程多出来的提交。
- `git diff main..origin/main` 能看到远程提交带来的文件变化。
- `git merge origin/main` 后，本地 `main` 跟上远程状态。

fetch 的核心结论是：它从远程仓库拿回新状态并更新 `origin/main`，但不会自动改本地 `main`。先 fetch、再观察、再整合，是理解远程协作最稳的一步。
