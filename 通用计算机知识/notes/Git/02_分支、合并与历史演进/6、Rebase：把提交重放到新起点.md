---
title: Rebase：把提交重放到新起点
date: 2026-07-26
tags: [计算机基础, Git, Git分支]
aliases:
  - git rebase
  - rebase
  - Git 变基
---

# 一、Rebase

Rebase 的核心动作是：把当前分支自己的提交拿起来，放到另一个更新的 base 后面重新播放。它不是合并出一个新节点，而是让当前分支看起来像从新的起点继续开发。

![[assets/rebase-replay-generated.png|600]]

merge 的思路是“把两条历史线接起来”，因此三方合并时可能产生 [[4、三方合并与 merge commit|merge commit]]。rebase 的思路是“换起点并重放提交”，结果通常更像一条直线。

# 二、重放模型

rebase 不是把 commit 原封不动搬家，而是重新应用每个提交里的改动。因为 parent 变了，被重放的提交会变成新的 commit，哈希也会改变。

## 1、rebase 前

```text
main:    A -- B -- M
              \
feature:       C -- D
```

这里 `feature` 从旧的 `B` 分出，自己有 `C` 和 `D` 两个提交。后来 `main` 已经前进到 `M`。

## 2、rebase 后

站在 `feature` 上运行：

```shell
git rebase main
```

结果类似：

```text
main:    A -- B -- M
                    \
feature:             C' -- D'
```

`C'` 和 `D'` 的内容可能很像原来的 `C` 和 `D`，但它们是重新创建的提交。commit 身份包含 parent、内容、作者和提交元信息；parent 变了，哈希通常也会变。

# 三、命令读法

`git rebase main` 里的 `main` 是新的 base，不是要被改写的分支。被重放的是当前分支上的提交。

## 1、基本命令

```shell
git switch feature/rebase-practice
git rebase main
```

这两句可以读成：

```text
站到 feature/rebase-practice 上，
把这个分支自己的提交重放到 main 的最新位置后面。
```

| 部分 | 含义 |
|---|---|
| `git switch feature/rebase-practice` | 切到要被重放的分支 |
| `git rebase main` | 把当前分支重放到 `main` 后面 |
| `main` | 新的 base |
| 当前分支 | 被改写、被重放的分支 |

## 2、成功输出

```text
Successfully rebased and updated refs/heads/feature/rebase-practice.
```

这表示当前分支名已经移动到重放后的最新提交上。接下来应使用历史图确认提交位置。

示例：

```shell
git log --oneline --decorate --graph --all --max-count=10
```

```text
* 83c2f41 (HEAD -> feature/rebase-practice) Add second rebase practice line
* 41ad7b0 Add first rebase practice line
*   e1aaa33 (main) Merge branch 'feature/conflict-title'
```

重点不是记住示例哈希，而是看 `feature/rebase-practice` 是否已经接在 `main` 最新提交后面。

# 四、merge 对比

merge 和 rebase 都能让一条分支吸收另一条分支的进展，但它们留下的历史形状不同。

## 1、差异表

| 问题 | merge | rebase |
|---|---|---|
| 历史形状 | 保留分叉和合并点 | 整理成更直的线 |
| merge commit | 三方合并时通常会有 | 通常没有 |
| 是否改写提交 | 不改写已有提交 | 会把提交重放成新提交 |
| 信息保留 | 保留“何时合并”的结构 | 保留线性提交序列 |
| 学习阶段建议 | 更稳，历史真实 | 只在自己的本地练习分支上用 |

## 2、选择思路

如果想保留分支曾经分叉、后来合并的结构，使用 merge 更自然。自动三方合并示例就是这种情况。

如果只是自己的本地 feature 分支落后于 `main`，想在提交前把它整理到最新起点上，rebase 会让历史更直。但这份整洁来自改写提交身份，需要更谨慎。

# 五、安全边界

rebase 最重要的风险是改写历史。初学阶段可以记住一句话：只 rebase 自己的本地分支。

## 1、不要随手改写共享历史

不要随手 rebase 已经推给别人、并且别人可能基于它继续工作的分支。因为 rebase 后旧提交会被新提交替代，别人手里的历史会和你改写后的历史对不上。

适合练习 rebase 的场景：

| 场景 | 是否适合 |
|---|---|
| 自己刚创建的本地练习分支 | 适合 |
| 尚未推送、没人依赖的个人 feature 分支 | 通常适合 |
| 多人正在基于它开发的共享分支 | 不适合随手 rebase |

## 2、中途冲突

rebase 也可能遇到冲突。它会在某个提交重放失败时暂停，等你解决后继续。

| 想做什么 | 命令 |
|---|---|
| 解决后继续 | `git add <path>`，再 `git rebase --continue` |
| 跳过当前提交 | `git rebase --skip` |
| 放弃本次 rebase | `git rebase --abort` |

这和 [[5、解决合并冲突|解决合并冲突]] 的思路类似：先编辑出最终正确文件，再用 `git add` 告诉 Git 当前文件已经处理好。

# 六、本地练习

起点：继续使用 `practice-repo/`。当前应在 `main`，最新提交是解决冲突后的 merge commit，工作区 clean。

## 1、创建练习分支

```shell
cd path/to/practice-repo
git status -sb
git log --oneline --decorate --graph --all --max-count=10
```

从 `main` 的上一个提交创建练习分支：

```shell
git switch -c feature/rebase-practice HEAD~1
```

这样做是为了让练习分支故意落后于 `main` 最新提交，方便观察 rebase 如何把它重放到新起点上。

## 2、创建两个提交

新建 `rebase-note.txt`，写入：

```text
First rebase practice line.
```

提交：

```shell
git add rebase-note.txt
git commit -m "Add first rebase practice line"
```

继续追加：

```text
Second rebase practice line.
```

再次提交：

```shell
git add rebase-note.txt
git commit -m "Add second rebase practice line"
```

## 3、执行 rebase

观察 rebase 前：

```shell
git log --oneline --decorate --graph --all --max-count=10
```

执行 rebase：

```shell
git rebase main
```

观察 rebase 后：

```shell
git log --oneline --decorate --graph --all --max-count=10
git status -sb
```

目标状态：

| 检查项 | 期待结果 |
|---|---|
| 当前分支 | `feature/rebase-practice` |
| 分支位置 | 接在 `main` 最新提交后面 |
| 两个练习提交 | 哈希已经变成新的 |
| 是否出现 merge commit | 没有新的 merge commit |
| 工作区 | clean |

# 七、常见误区

## 1、高级 merge

rebase 不是“更高级的 merge”。merge 的核心是接线，rebase 的核心是重放。它们服务于不同的历史表达方式。

## 2、提交搬家

rebase 不是把原 commit 原地搬过去，而是在新的 parent 后重新创建提交。因此哈希改变是正常现象。

## 3、共享分支

共享分支上的历史可能已经被别人依赖。除非团队有明确流程，否则不要对这种分支随手 rebase。

# 八、小结

本篇最重要的一句话：

```text
rebase 会把当前分支自己的提交重新播放到新的 base 后面，让历史变直，但也会改写这些提交的身份。
```

下一步可以比较 merge 和 rebase：什么时候保留合并历史，什么时候整理本地提交线。
