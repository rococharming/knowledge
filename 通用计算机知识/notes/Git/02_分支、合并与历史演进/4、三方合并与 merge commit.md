---
title: 三方合并与 merge commit
date: 2026-07-26
tags: [计算机基础, Git, Git分支]
aliases:
  - three-way merge
  - merge commit
  - Git 三方合并
---

# 一、三方合并

三方合并发生在两个分支从共同祖先分开后，又各自都有新提交的场景。此时 Git 不能像 [[3、Fast-forward 合并|fast-forward 合并]] 那样只移动一个分支指针，而要比较共同祖先、当前分支和目标分支，再生成合并结果。

![[assets/three-way-merge-generated.png|600]]

三方合并的重点不是“冲突”，而是“比较三份状态”。如果两边改动能自动组合，Git 会直接创建一个 merge commit；只有改动落在同一块内容且无法自动判断时，才会进入冲突处理。

# 二、三方角色

三方合并里的“三方”不是三个人或三个仓库，而是三个 commit 位置：共同祖先、当前分支、被合进来的分支。

## 1、base

`base` 是两个分支共同的祖先 commit。Git 用它判断两边分别从哪里开始变化。

示意：

```text
          D  main
         /
A -- B
         \
          C  feature/note-title
```

这里 `B` 是共同祖先。`main` 从 `B` 走到 `D`，`feature/note-title` 从 `B` 走到 `C`。

## 2、ours 与 theirs

`ours` 和 `theirs` 取决于你当前站在哪个分支。站在 `main` 上运行：

```shell
git merge feature/note-title
```

对应关系是：

| 角色 | 对应 |
|---|---|
| `base` | 两个分支分开前的共同提交 |
| `ours` | 当前分支，也就是 `main` |
| `theirs` | 被合进来的分支，也就是 `feature/note-title` |

> [!warning] 站位决定命名
> `ours` 不永远是 `main`，`theirs` 也不永远是 feature。它们是合并时的站位概念。

# 三、merge commit

merge commit 是用来记录“两条历史线在这里接回一起”的提交。普通 commit 通常只有一个 parent；merge commit 通常有两个 parent。

## 1、历史形状

合并前：

```text
* 2e49ca6 (HEAD -> main, feature/daily-summary) Start daily summary branch
| * cc3957a (feature/note-title) Add branch practice note
|/
* c98a758 Complete local repository daily loop
```

这表示 `main` 已经包含 daily summary；`feature/note-title` 还停在另一条线上。因为 `main` 和 `feature/note-title` 都从 `c98a758` 之后各自前进了，所以这次不能 fast-forward。

这里的改动位置并不冲突：`main` 上的 `2e49ca6` 修改了 `daily-note.txt`，而 `feature/note-title` 上的 `cc3957a` 新增了 `branch-note.txt`。两边改的是不同文件，所以 Git 应当能自动完成三方合并，并创建 merge commit。

## 2、合并结果

站在 `main` 上合并：

```shell
git switch main
git merge feature/note-title
```

示例输出：

```text
Merge made by the 'ort' strategy.
 branch-note.txt | 1 +
 1 file changed, 1 insertion(+)
```

这里没有出现 `Fast-forward`，而是出现 `Merge made by...`。这通常说明 Git 完成了三方合并，并创建了一个新的 merge commit。

合并后查看历史：

```shell
git log --oneline --decorate --graph --all --max-count=8
```

示例输出：

```text
*   7a14c31 (HEAD -> main) Merge branch 'feature/note-title'
|\
| * cc3957a (feature/note-title) Add branch practice note
* | 2e49ca6 (feature/daily-summary) Start daily summary branch
|/
* c98a758 Complete local repository daily loop
```

`*   7a14c31` 前面的图形连着两条 parent 线，这是 merge commit 在历史图里的典型特征。

# 四、parent

确认一个提交是不是 merge commit，可以查看它的原始头信息。merge commit 通常会有两行 `parent`。

## 1、查看命令

```shell
git show --no-patch --pretty=raw HEAD
```

示例输出：

```text
commit 7a14c31...
tree ...
parent 2e49ca6...
parent cc3957a...
author ...
committer ...

    Merge branch 'feature/note-title'
```

`--no-patch` 表示不显示文件差异；`--pretty=raw` 表示用原始格式显示提交头信息。

## 2、parent 含义

| parent | 通常表示 |
|---|---|
| 第一条 parent | 合并前当前分支的最新提交 |
| 第二条 parent | 被合进来的分支的最新提交 |

在本例里，第一条 parent 是 `main` 合并前的位置 `2e49ca6`，第二条 parent 是 `feature/note-title` 的位置 `cc3957a`。merge commit 把这两条线接回一起。

# 五、命令读法

三方合并时要同时看命令方向、输出提示和历史图形。只看文件内容，很容易漏掉“历史结构已经变了”。

## 1、常用命令

| 命令 | 作用 | 关键读法 |
|---|---|---|
| `git merge feature/note-title` | 把目标分支合进当前分支 | 当前分支会接收合并结果 |
| `Merge made by...` | Git 自动完成三方合并 | 通常已经创建 merge commit |
| `git log --oneline --decorate --graph --all` | 查看历史形状 | merge commit 会连着两条线 |
| `git show --no-patch --pretty=raw HEAD` | 查看当前提交原始头信息 | merge commit 有两行 `parent` |

## 2、常见误区

| 误区 | 更准确的理解 |
|---|---|
| 三方合并一定会冲突 | 三方合并只是合并方式，不一定冲突 |
| merge commit 是多余提交 | 它记录两条历史线在哪里接回一起 |
| `ours` 和 `theirs` 是固定分支 | 它们取决于当前站在哪个分支 |

# 六、本地练习

起点：继续使用 `practice-repo/`。完成 `feature/daily-summary` 的 fast-forward 合并后，当前分支应为 `main`，且 `feature/daily-summary` 已经合进 `main`。

## 1、合并前检查

```shell
cd path/to/practice-repo
git status -sb
git log --oneline --decorate --graph --all --max-count=8
```

确认当前在 `main`，工作区 clean，并观察 `feature/note-title` 是否仍在旁边。

## 2、执行合并

```shell
git merge feature/note-title
```

如果编辑器打开合并信息，保留默认信息并保存退出。默认合并信息通常能说明是哪个分支被合进来。

## 3、合并后检查

```shell
git log --oneline --decorate --graph --all --max-count=8
git show --no-patch --pretty=raw HEAD
git status -sb
```

目标状态：

| 检查项 | 期待结果 |
|---|---|
| 当前分支 | `main` |
| 最新提交 | merge commit |
| parent 数量 | 两个 |
| `feature/note-title` | 仍指向自己的原提交 |
| 工作区 | clean |

# 七、小结

本篇最重要的一句话：

```text
三方合并会比较共同祖先、当前分支和目标分支；当两边都前进过时，Git 通常用一个 merge commit 把两条历史线接回一起。
```

下一步会进入冲突处理：当两边改到同一块内容时，Git 会暂停合并，让人明确选择最终内容。
