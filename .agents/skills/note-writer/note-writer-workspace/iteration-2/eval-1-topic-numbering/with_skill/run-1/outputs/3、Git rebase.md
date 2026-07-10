---
title: Git rebase
tags: [Git, 版本控制, rebase]
---

# 一、rebase 的基本概念

`git rebase` 是把一系列提交"挪到"另一个基线之上的操作。它的名字来自 re-base——重新设定基线。

假设你在 `feature` 分支上开发，同时 `main` 分支也在前进。此时 `feature` 的起点（基线）已经落后于最新的 `main`。rebase 会把你在 `feature` 上的提交逐个取下，接到最新 `main` 的末端，就好像你一直是基于最新 `main` 开发的一样。

它的核心价值是**保持线性历史**：用 rebase 合并分支，不会产生 merge 那种"汇合提交"，提交图是一条直线，读起来更清晰。这是它与 [[2、Git分支|Git 分支]] 中 merge 工作流最本质的区别。

# 二、基本用法

## 1、rebase 的基本流程

场景：`feature` 分支从 `main` 切出后，`main` 又有了新提交。现在想把 `feature` 的新提交接到最新 `main` 上。

示例：

```bash
git checkout feature
git rebase main
```

这两条命令做的事是：切到 `feature`，把它的基线从"切出时的 main"换成"当前最新的 main"。rebase 会依次重放 `feature` 上每个提交到新基线之上。

重放过程中如果遇到冲突，Git 会暂停并提示。解决冲突后继续：

```bash
git add <冲突文件>
git rebase --continue
```

如果想放弃这次 rebase，回到开始前的状态：

```bash
git rebase --abort
```

> 注意：rebase 会为每个被重放的提交生成**新的 commit hash**，因为提交的父节点变了。这意味着 rebase 之后 `feature` 上的"那些提交"在内容上等价，但已经不是原来那几个提交了。

## 2、rebase 与 merge 的对比

两者都能把一个分支的改动整合到另一个分支，但思路不同：

- **merge**：保留分叉与汇合的历史，新增一个 merge commit，是谁先谁后一目了然。
- **rebase**：把分支提交挪到目标末端，历史变线性，没有 merge commit。

| 方面 | merge | rebase |
|---|---|---|
| 历史形态 | 有分叉和汇合 | 线性 |
| 是否新增提交 | 新增 merge commit | 重放生成新提交，无额外 merge commit |
| 冲突处理 | 一次性解决 | 可能逐个提交都要解决 |
| 提交哈希 | 不变 | 改变 |

简单来说：想保留真实分支拓扑、多人协作留痕，用 merge；想读起来干净、像一条时间线，用 rebase。两者并不互斥，团队常按约定搭配使用。

# 三、进阶用法

## 1、交互式 rebase

`git rebase -i` 在重放前先打开一个编辑器，让你**改写提交计划**——合并、改顺序、改提交信息、甚至删除某个提交。这是 rebase 最强大的形态。

示例：

```bash
git rebase -i HEAD~3
```

这会列出最近 3 个提交，每行一个，让你决定如何处理：

```text
pick a1b2c3d 添加功能 A
pick e4f5g6h 修复拼写
pick i7j8k9l 补充注释
```

把 `pick` 改成别的动作就能改写历史：

- `pick`：保留该提交。
- `squash`：把该提交并入前一个提交，合并提交信息。
- `reword`：保留提交，但修改提交信息。
- `drop`：丢弃该提交。

> 注意：交互式 rebase 经常用来"整理未推送的提交"，把一堆零碎的 WIP 提交合并成几个干净提交后再推送。

## 2、rebase 的风险

rebase 改写了提交历史，这带来一个硬性约束：

> **永远不要 rebase 已经推送到公共分支、且别人可能基于它工作的提交。**

因为 rebase 会生成新哈希，别人 pull 时会发现"本地有旧哈希的提交，远端是新哈希的"，陷入冲突泥潭。这是 rebase 最容易踩的坑。

相比之下，merge 不改写历史，公共分支上用 merge 更安全。常见的安全策略是：在**自己的特性分支**上随便 rebase 整理，推到公共分支前整理好；公共分支只用 merge 或 fast-forward。

# 四、延伸

rebase 的关键是理解"它重写历史，所以能让历史变干净，但也会让历史变假"。在私人分支上整理、在公共分支上保守，是稳妥的实践。

进一步可以学习 [[2、Git分支|Git 分支]] 中更完整的分支模型，理解 rebase 与 merge 在团队协作流中的分工。这些操作都建立在 [[1、Git基础|Git 基础]] 的提交与分支模型之上。
