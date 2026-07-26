---
title: Fast-forward 合并
date: 2026-07-26
tags: [计算机基础, Git, Git分支]
aliases:
  - fast-forward merge
  - Git 快进合并
  - git merge
---

# 一、Fast-forward

Fast-forward merge 可以理解为“快进合并”：如果当前分支只是落后于另一个分支，且没有自己的新提交，Git 不需要创建新的 merge commit，只要把当前分支名向前移动到目标提交。

![[assets/fast-forward-merge-generated.png|600]]

这仍然是一次合并，只是历史没有真正分叉。它延续了 [[1、分支、refs 与 HEAD|分支指针]] 的模型：分支名本来就是指向 commit 的名字，fast-forward 只是让落后的名字追上去。

## 1、合并条件

fast-forward 的典型前提是：当前分支是目标分支的祖先。

```text
合并前：

main:    A -- B
              \
feature:       C
```

这里 `main` 停在 `B`，`feature` 从 `B` 继续提交到 `C`。如果站在 `main` 上合并 `feature`，Git 可以直接让 `main` 指向 `C`。

## 2、合并结果

```text
合并后：

main:    A -- B -- C
feature:          ^
```

更准确地说，合并后 `main` 和 `feature` 都指向 `C`。没有额外的 merge commit，历史仍是一条直线。

# 二、合并方向

`git merge` 更新的是当前分支。命令参数是“要合进来的分支”，不是“要切过去的分支”。

## 1、先站到接收方

想把 `feature/daily-summary` 合进 `main`，顺序是：

```shell
git switch main
git merge feature/daily-summary
```

第一条命令决定接收方是 `main`；第二条命令把 `feature/daily-summary` 的历史合进当前分支。

## 2、方向对比

| 当前分支 | 命令 | 结果 |
|---|---|---|
| `main` | `git merge feature/daily-summary` | 把 feature 合进 `main` |
| `feature/daily-summary` | `git merge main` | 把 `main` 合进 feature |

> [!warning] 先看当前位置
> merge 前先运行 `git status -sb`。如果站错分支，merge 更新的就不是你以为的那条线。

# 三、输出阅读

fast-forward 合并最重要的信号是输出里的 `Fast-forward`。它说明 Git 没有创建新提交，只是移动了当前分支指针。

## 1、合并前

完成 `feature/daily-summary` 提交后，历史大致像这样：

```shell
git log --oneline --decorate --graph --all --max-count=6
```

示例输出：

```text
* 2e49ca6 (HEAD -> feature/daily-summary) Start daily summary branch
| * cc3957a (feature/note-title) Add branch practice note
|/
* c98a758 (main) Complete local repository daily loop
* 8c4d05c Clarify practice repository purpose
```

这里 `feature/daily-summary` 是从 `main` 开出来的，且 `main` 之后没有自己的新提交，所以可以 fast-forward。开分支流程见 [[2、创建与切换分支|创建与切换分支]]。

## 2、执行合并

站到 `main` 后执行：

```shell
git switch main
git merge feature/daily-summary
```

示例输出：

```text
Updating c98a758..2e49ca6
Fast-forward
 daily-note.txt | 1 +
 1 file changed, 1 insertion(+)
```

| 输出 | 读法 |
|---|---|
| `Updating c98a758..2e49ca6` | 当前分支从旧提交移动到新提交 |
| `Fast-forward` | 没有创建新的 merge commit |
| `daily-note.txt | 1 +` | 这次合并带进来的文件变化 |

## 3、合并后

再次查看历史：

```shell
git log --oneline --decorate --graph --all --max-count=6
```

示例输出：

```text
* 2e49ca6 (HEAD -> main, feature/daily-summary) Start daily summary branch
| * cc3957a (feature/note-title) Add branch practice note
|/
* c98a758 Complete local repository daily loop
* 8c4d05c Clarify practice repository purpose
```

重点看 `HEAD -> main, feature/daily-summary`：当前在 `main`，并且 `main` 和 `feature/daily-summary` 指向同一个提交。这说明 feature 的成果已经进入 `main`。

# 四、不可快进

不是所有合并都能 fast-forward。只要两个分支各自都有新提交，就不能只移动一个指针。

## 1、可以快进

```text
main:    A -- B
              \
feature:       C

main 没有自己的新提交，可以移动到 C。
```

这是“当前分支只是落后”的场景。

## 2、不能快进

```text
main:    A -- B -- D
              \
feature:       C

main 和 feature 都往前走了，需要三方合并。
```

这种情况下，Git 需要把两边的改动合在一起。可能自动成功，也可能出现冲突；后续会进入三方合并和冲突处理。

# 五、常见误区

## 1、把方向读反

`git merge feature/daily-summary` 的意思不是“切到 feature”，而是：

```text
把 feature/daily-summary 合进当前分支
```

所以 merge 前一定先确认当前分支。

## 2、以为不是合并

fast-forward 也是合并。它只是没有新建 merge commit。判断成果是否进入 `main`，看的是 `main` 是否指向了 feature 的最新提交。

## 3、以为自动删除

合并不会自动删除 feature 分支名。`feature/daily-summary` 仍然存在，只是和 `main` 指向同一个 commit。是否删除分支，是后续单独的清理动作。

# 六、本地练习

起点：继续使用 `practice-repo/`。完成 `feature/daily-summary` 提交后，应在 `feature/daily-summary`，工作区 clean。

## 1、合并前检查

```shell
cd /Users/songpengfei/Learn/Git/practice-repo
git status -sb
git log --oneline --decorate --graph --all --max-count=8
```

观察 `feature/daily-summary` 是否比 `main` 多一个提交。

## 2、执行合并

切回接收合并的分支：

```shell
git switch main
```

执行合并：

```shell
git merge feature/daily-summary
```

看到 `Fast-forward` 时，说明这次是快进合并。

## 3、合并后检查

```shell
git log --oneline --decorate --graph --all --max-count=8
git status -sb
```

目标状态：

| 检查项 | 期待结果 |
|---|---|
| 当前分支 | `main` |
| `main` 位置 | 和 `feature/daily-summary` 指向同一个提交 |
| 最新提交 | `Start daily summary branch` |
| 是否出现新 merge commit | 没有 |
| 工作区 | clean |

# 七、小结

本篇最重要的一句话：

```text
fast-forward merge 是当前分支没有分叉时的合并：Git 只把当前分支名向前移动到目标提交。
```

下一步可以学习三方合并：当 `main` 和 feature 都各自前进时，Git 不能只移动指针，而要把两边历史合成一个新的结果。
