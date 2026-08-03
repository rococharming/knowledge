---
title: 用 git cherry-pick 复制指定提交
date: 2026-08-03
tags: [Git, Git恢复, Git提交, git-cherry-pick]
aliases:
  - git cherry-pick
  - cherry-pick
  - 复制指定提交
---

# 一、cherry-pick

`git cherry-pick` 用来把某个已有提交引入的改动复制到当前分支，并在当前分支上创建一个新提交。它适合处理“我只要某一个提交的改动，不要整条分支历史”的场景。

核心模型是：

```text
git cherry-pick <commit>
= 读取指定提交引入的改动
+ 应用到当前分支
+ 在当前分支创建一个新提交
```

它不是切换分支，也不是合并整条分支。运行前最重要的问题是：当前 `HEAD` 站在哪里，以及要复制的提交是哪一个。

![[assets/cherry-pick-from-recovery-branch-generated.png|600]]

# 二、适用场景

## 1、只要一个提交

如果一条分支上有多个提交，而当前分支只需要其中一个提交的改动，就可以考虑 `cherry-pick`。

例如某个恢复分支里有两条提交：

```text
Revert "Add revert practice line"
Add revert practice line
```

现在只想把 `Add revert practice line` 的改动拿回 `main`，不想把整个恢复分支合进来。这时应挑出那个具体提交，而不是 merge 整条线。

## 2、不要整条线

`merge` 和 `cherry-pick` 的边界可以这样理解：

| 动作 | 含义 | 适合场景 |
|---|---|---|
| `git merge branch` | 把一条分支的历史整合进当前分支 | 想要整条分支的结果和历史关系 |
| `git cherry-pick <commit>` | 只复制某个提交引入的改动 | 只需要一个提交，不需要整条分支 |

一句话：

```text
merge 是要这条线。
cherry-pick 是只要这个点的改动。
```

# 三、定位提交

## 1、确认当前分支

`cherry-pick` 会作用在当前分支上，所以先确认自己站在哪里：

```shell
git status -sb
git branch --show-current
```

如果目标是把改动复制到 `main`，期待看到类似：

```text
## main...origin/main
main
```

如果当前站错分支，命令语法即使正确，也会把新提交创建到错误分支上。

## 2、查看来源历史

先观察来源分支或来源引用附近的提交：

```shell
git log --oneline --decorate recover/revert-practice --max-count=3
```

可能看到：

```text
ffa4a31 (recover/revert-practice) Revert "Add revert practice line"
e8e5b34 Add revert practice line
fe8d9c0 (HEAD -> main, origin/main, origin/HEAD) Merge pull request #1 ...
```

这里 `recover/revert-practice` 指向的是 revert 提交；如果要复制它的父提交，可以使用：

```text
recover/revert-practice~1
```

常见写法：

| 写法 | 含义 |
|---|---|
| `recover/revert-practice` | 该分支当前指向的提交 |
| `recover/revert-practice~1` | 该提交的第一个父提交 |
| `<commit-hash>` | 直接用提交哈希指定某个提交 |

## 3、先检查内容

执行前先用只读命令确认候选提交：

```shell
git show --stat --oneline recover/revert-practice~1
```

可能看到：

```text
e8e5b34 Add revert practice line
 README.md | 3 ++-
```

这一步的目标是确认“我要复制的就是这个提交引入的改动”。如果提交信息、文件路径或 diff 统计不符合预期，先停下来重新定位，不要继续 cherry-pick。

# 四、执行复制

## 1、基本命令

确认当前分支和候选提交后，执行：

```shell
git cherry-pick recover/revert-practice~1
```

执行后，Git 会尝试把这个提交引入的改动应用到当前分支，并自动创建一个新提交。

结果通常是：

| 对象 | 结果 |
|---|---|
| 当前分支 | 新增一个提交 |
| 新提交内容 | 来自被挑选提交的改动 |
| 新提交哈希 | 通常和原提交不同 |
| 来源分支 | 不移动 |
| 远程仓库 | 不会自动修改 |

新提交哈希通常不同，因为提交对象不仅包含文件改动，还包含父提交、提交时间、作者/提交者等信息。

## 2、结果检查

完成后检查状态和历史：

```shell
git status -sb
git log --oneline --decorate --all --max-count=5
```

可能看到：

```text
## main...origin/main [ahead 1]
abc1234 (HEAD -> main) Add revert practice line
ffa4a31 (recover/revert-practice) Revert "Add revert practice line"
e8e5b34 Add revert practice line
fe8d9c0 (origin/main, origin/HEAD) Merge pull request #1 ...
```

重点观察：

| 观察点 | 结论 |
|---|---|
| `main` 显示 `[ahead 1]` | 当前分支多了一个本地新提交 |
| `HEAD -> main` 在新的提交上 | 改动已经复制到当前分支 |
| 来源分支还在原位置 | `cherry-pick` 没有移动来源分支 |
| working tree clean | 自动创建提交成功，没有遗留未处理状态 |

# 五、边界误区

## 1、不会切换分支

`cherry-pick` 不会自动切到来源分支。它总是把改动应用到当前分支。

因此执行前必须确认：

```shell
git branch --show-current
```

如果当前分支不是目标分支，先切换或停下来重新判断。

## 2、可能冲突

`cherry-pick` 复制的是改动，而改动要落到当前分支的文件内容上。如果当前分支的同一块内容已经变化，Git 可能无法自动应用，进而进入 conflict 状态。

遇到冲突时先看：

```shell
git status
```

常见处理方向是：读冲突文件，决定最终内容，`git add` 标记解决，然后按提示继续；如果发现挑错提交，可以中止 cherry-pick。

## 3、不是恢复万能键

`cherry-pick` 适合“复制某个提交的改动”。如果你想保留一整条分支的上下文，merge 更合适；如果你只是想找到误 reset 前的位置，先看 [[9、用 git reflog 找回 reset 前的位置|reflog]]；如果分支名写错，改名操作在 [[通用计算机知识/notes/Git/02_分支、合并与历史演进/2、创建与切换分支#六、分支改名|分支改名]] 中处理。

# 六、操作判断

复制指定提交可以按这个顺序：

```text
status 确认当前分支
log 找候选提交
show 检查候选内容
cherry-pick 复制改动
status + log 验证结果
```

对应命令：

```shell
git status -sb
git branch --show-current
git log --oneline --decorate recover/revert-practice --max-count=3
git show --stat --oneline recover/revert-practice~1
git cherry-pick recover/revert-practice~1
git status -sb
git log --oneline --decorate --all --max-count=5
```

关键判断是：`cherry-pick` 复制的是指定提交引入的改动，并在当前分支生成新提交。只有在你明确“只要这个提交，不要整条分支”时，它才是合适工具。
