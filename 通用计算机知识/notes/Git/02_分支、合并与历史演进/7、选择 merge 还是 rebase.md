---
title: 选择 merge 还是 rebase
date: 2026-07-26
tags: [计算机基础, Git, Git分支]
aliases:
  - merge vs rebase
  - Git merge rebase 选择
  - 选择 merge 还是 rebase
---

# 一、选择原则

Merge 和 rebase 都能让一个分支吸收另一处的进展。差别不在谁更高级，而在你想保留历史分叉，还是整理自己的本地提交线。

![[assets/merge-vs-rebase-generated.png|600]]

一个稳妥的初学规则是：

```text
merge 适合保留共享历史；
rebase 适合整理自己的本地分支。
```

这条规则承接前两课：[[4、三方合并与 merge commit|merge commit]] 会保留两条线接回来的事实；[[6、Rebase：把提交重放到新起点|rebase]] 会把当前分支提交重放到新 base 后面。

# 二、历史是否共享

选择前先问一个问题：这段提交有没有被别人基于它继续工作？

## 1、共享历史

如果一段历史已经推给别人，并且别人可能基于它继续开发，就不要随手 rebase。因为 rebase 会改写被重放提交的身份，让别人手里的旧提交和你改写后的新提交对不上。

这种场景更适合 merge：

```shell
git merge feature
```

merge 不改写已有提交，而是保留“这两条历史线在这里接回一起”的结构。

## 2、本地分支

如果只是自己的本地 feature 分支，还没有共享给别人，可以考虑 rebase：

```shell
git switch feature/my-work
git rebase main
```

这表示把当前分支自己的提交重放到最新 `main` 后面。它能让提交线更直，也让后续合回 `main` 时更容易 fast-forward。

# 三、对比表

merge 和 rebase 的区别，核心是历史表达方式不同。

## 1、核心差异

| 问题 | merge | rebase |
|---|---|---|
| 核心动作 | 把两条历史线接回一起 | 把当前分支提交重放到新 base 上 |
| 历史形状 | 保留分叉和合并点 | 更直 |
| 是否改写已有提交 | 不改写 | 会改写被重放提交 |
| 常见产物 | 可能有 merge commit | 通常没有 merge commit |
| 适合场景 | 共享历史、记录集成点 | 本地私有分支整理 |

## 2、决策表

| 场景 | 推荐 | 理由 |
|---|---|---|
| 把已完成的 feature 合进 `main` | `git merge feature` | 保留真实合并点，适合共享历史 |
| 自己的本地 feature 想跟上最新 `main` | `git rebase main` | 把本地提交重放到新起点，历史更直 |
| 分支已经推给别人并被继续使用 | 谨慎 merge，避免随手 rebase | rebase 会改写提交身份 |
| 本地练习分支 rebase 后要收回 `main` | 切回 `main` 后 fast-forward merge | `main` 只需追上整理后的分支 |

# 四、个人流程

一种常见个人工作流是：先在本地 feature 上 rebase 整理，再切回 `main` 用 fast-forward 接收成果。

## 1、流程形状

```text
feature 本地开发
-> 在 feature 上 git rebase main
-> 切回 main
-> git merge feature
```

这不是说 rebase 必须搭配 merge，而是说：rebase 后如果 feature 已经接在 `main` 后面，`main` 通常只需要向前移动即可。

## 2、线性收回

当 `feature/rebase-practice` 已经接在 `main` 后面时，历史可能像这样：

```text
* df306c3 (HEAD -> feature/rebase-practice) Add second rebase practice line
* 758bd87 Add first rebase practice line
*   e1aaa33 (main) Merge branch 'feature/conflict-title'
```

这说明：

| 分支 | 状态 |
|---|---|
| `main` | 停在解决冲突后的 merge commit |
| `feature/rebase-practice` | 在 `main` 后面多两个练习提交 |

把它收回 `main`：

```shell
git switch main
git merge feature/rebase-practice
```

预期输出：

```text
Updating e1aaa33..df306c3
Fast-forward
 rebase-note.txt | 2 ++
 1 file changed, 2 insertions(+)
```

这次合并通常是 [[3、Fast-forward 合并|fast-forward]]：`main` 没有自己的新分叉，只是落后于整理后的 feature 分支。

# 五、三个问题

选择 merge 或 rebase 前，可以用三个问题快速判断。

## 1、是否共享

| 问题 | 倾向 |
|---|---|
| 这段提交已经给别人用了？ | 不要随手 rebase |
| 我只是在整理自己的本地分支？ | 可以考虑 rebase |
| 我想保留这次集成发生过的事实？ | 选择 merge |

## 2、站位检查

merge 和 rebase 都受当前分支影响。操作前先确认站位：

```shell
git status -sb
```

站在 `main` 上运行 `git merge feature`，更新的是 `main`。站在 `feature` 上运行 `git rebase main`，被重放的是当前 `feature`。

# 六、团队约定

团队里常见做法不是单纯“永远 merge”或“永远 rebase”，而是按位置分工。

## 1、个人分支

很多团队会允许个人 feature 分支在提交 PR 前 rebase 到最新 `main`，让 review 时看到更清楚的线性提交。

这种做法的前提是：这段 feature 历史主要由你自己维护，改写它不会打乱别人的工作。

## 2、主分支

合入主分支时，通常由平台或维护者按团队策略选择：

| 策略 | 特点 |
|---|---|
| merge commit | 保留分支结构和集成点 |
| squash merge | 把 feature 压成一个提交 |
| rebase merge | 让 feature 提交线性进入主线 |

真正重要的不是背一个绝对规则，而是知道每个动作对历史做了什么。

# 七、本地练习

起点：继续使用 `practice-repo/`。当前分支应为 `feature/rebase-practice`，它已经接在 `main` 后面，工作区 clean。

## 1、合并前检查

```shell
cd path/to/practice-repo
git status -sb
git log --oneline --decorate --graph --all --max-count=10
```

确认 `feature/rebase-practice` 是否接在 `main` 后面。

## 2、收回 main

切回 `main`：

```shell
git switch main
```

合并整理后的分支：

```shell
git merge feature/rebase-practice
```

检查结果：

```shell
git log --oneline --decorate --graph --all --max-count=10
git status -sb
```

目标状态：

| 检查项 | 期待结果 |
|---|---|
| 当前分支 | `main` |
| 合并类型 | fast-forward |
| `main` 与 `feature/rebase-practice` | 指向同一个最新提交 |
| 工作区 | clean |

# 八、常见误区

## 1、历史越直越好

历史直不一定等于更好。共享历史里的合并点有时很有价值，因为它记录了某次集成确实发生过。

## 2、merge 落后

merge 不是落后做法。它保留真实历史结构，适合团队共享场景，也适合需要追踪集成点的项目。

## 3、不看当前分支

不要在没确认当前分支时运行 merge 或 rebase。先用 `git status -sb` 看清楚站位，再决定动作。

# 九、小结

本篇最重要的一句话：

```text
merge 适合保留共享历史，rebase 适合整理自己的本地分支；选择之前先问这段历史有没有被别人依赖。
```

下一步会收束第二专题：用一套小流程串起分支、合并、冲突和历史观察。
