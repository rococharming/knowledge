---
title: 用 git restore 丢弃工作区修改
date: 2026-08-03
tags: [Git, Git恢复, Git撤销, Git基础]
aliases:
  - git restore
  - 丢弃工作区修改
  - restore working tree
---

# 一、工作区恢复

`git restore -- <path>` 用来把指定路径的 working tree 内容恢复到 index 中记录的版本。它适合处理“文件改错了，还没有暂存、也没有提交，现在确认不要这次修改”的场景。

在执行前，先用 [[通用计算机知识/notes/Git/04_撤销、恢复与历史整理/1、撤销前的三问诊断|撤销前的三问诊断]] 判断改动位置。如果短状态显示的是第二列 `M`，例如：

```text
 M README.md
```

就表示 `README.md` 有 working tree 修改，但还没有进入 index。

> [!warning] 先看再丢
> `git restore -- README.md` 会直接丢弃 `README.md` 当前 working tree 里的未提交修改。它不是放进回收站，也不会自动创建一条可找回的提交。

# 二、安全流程

## 1、查看状态

先确认当前仓库状态：

```shell
git status -sb
```

常见输出：

```text
## main...origin/main
 M README.md
```

这里要读两层信息：

| 位置 | 含义 |
|---|---|
| `main...origin/main` | 当前本地分支与 upstream 的关系 |
| ` M README.md` | `README.md` 只有 working tree 修改 |

如果看到的是 `M  README.md`，说明改动已经暂存；如果看到 `MM README.md`，说明同一个文件在 index 和 working tree 都有修改。这两种状态不能简单当作“只丢弃工作区修改”来处理。

## 2、查看内容

确认丢弃前，先查看会被丢掉的具体内容：

```shell
git diff -- README.md
```

命令拆解：

| 部分 | 作用 |
|---|---|
| `git diff` | 查看 working tree 相对 index 的差异 |
| `--` | 路径分隔符，表示后面是文件路径，不是命令选项 |
| `README.md` | 只查看这个文件 |

`git diff -- README.md` 只观察差异，不修改文件、不提交、不影响远程。确认 diff 中没有要保留的内容后，才进入恢复动作。

# 三、执行 restore

## 1、恢复命令

确认修改不要后，执行：

```shell
git restore -- README.md
```

这条命令只恢复指定路径。它会把 `README.md` 的 working tree 内容恢复到 index 里的版本。

在“改动未暂存，index 与最近一次提交一致”的常见状态下，结果看起来就是 `README.md` 回到最近一次提交中的内容。

## 2、结果验证

恢复后立刻检查：

```shell
git status -sb
git diff -- README.md
```

目标结果：

| 检查 | 期待结果 |
|---|---|
| `git status -sb` | 不再显示 ` M README.md` |
| `git diff -- README.md` | 没有输出 |

这两个结果合在一起，才说明这个文件的 working tree 修改已经被丢弃。

# 四、边界区别

## 1、不会发生的事

`git restore -- README.md` 只处理本地文件内容，不会触碰协作历史：

| 不会做的事 | 原因 |
|---|---|
| 不会创建提交 | 它不是 `commit` |
| 不会影响远程 | 它不访问 GitHub 或 GitLab |
| 不会删除分支 | 它不操作 branch |
| 不会改写历史 | 它只恢复 working tree 文件内容 |
| 不会自动恢复所有文件 | 这里只指定了 `README.md` |

这也是它和 `reset`、`revert` 的关键区别：`restore` 面向文件内容，`reset` 常用于移动本地分支指针，`revert` 常用于撤销共享历史中的提交影响。

## 2、和取消暂存的区别

同样是 `git restore`，是否带 `--staged` 会影响不同区域：

| 命令 | 影响区域 | 文件内容是否保留 |
|---|---|---|
| `git restore -- <path>` | working tree | 不保留这部分未暂存修改 |
| `git restore --staged <path>` | index | 保留工作区当前内容 |

如果目标是“已暂存但暂时不提交”，应使用 [[通用计算机知识/notes/Git/01_本地仓库与提交基础/6、撤销修改和取消暂存|撤销修改和取消暂存]] 中的 `git restore --staged <path>`。

# 五、操作判断

丢弃 working tree 修改可以按这个顺序判断：

```text
status 看位置
diff 看内容
restore 丢弃指定路径
status + diff 验证结果
```

对应命令：

```shell
git status -sb
git diff -- README.md
git restore -- README.md
git status -sb
git diff -- README.md
```

如果 `diff` 里有想保留的内容，先不要执行 `restore`。可以选择手动拆分修改、复制到临时位置、创建提交，或使用 `git stash` 暂存现场。撤销的核心不是记住命令，而是先确认要丢掉的内容确实可以丢。

这篇处理的是未提交、未暂存的 working tree 修改。已经进入提交历史的撤销，应回到 [[1、撤销前的三问诊断|撤销前的三问诊断]] 判断是否需要 `reset`、`reflog` 或协作场景下的 `revert`。
