---
title: 用 git restore --staged 取消暂存
date: 2026-08-03
tags: [Git, Git恢复, Git撤销, Git基础]
aliases:
  - git restore --staged
  - 取消暂存
  - restore staged
---

# 一、取消暂存

`git restore --staged -- <path>` 用来把指定路径从 index 中撤出来，同时保留 working tree 里的文件内容。它适合处理“已经 `git add`，但暂时不想让这份修改进入下一次提交”的场景。

核心区别是：

```text
取消暂存 = 修改离开 index，但文件内容仍留在 working tree。
```

这个动作不会创建提交，不会移动分支，也不会影响远程仓库。它只改变“下一次提交草稿”里是否包含这个文件的修改。

![[assets/restore-and-unstage-generated.png|600]]

# 二、适用状态

## 1、已暂存修改

如果已经运行：

```shell
git add README.md
```

再查看状态：

```shell
git status -sb
```

可能看到：

```text
## main...origin/main
M  README.md
```

这里第一列 `M` 表示 `README.md` 的修改已经进入 index，第二列为空表示 working tree 没有额外未暂存修改。也就是说，如果现在直接提交，`README.md` 的这份修改会进入 commit。

## 2、不要误用

如果只是想取消暂存，不要直接运行：

```shell
git restore -- README.md
```

不带 `--staged` 的 `git restore` 默认处理 working tree，可能丢弃磁盘文件里的未暂存内容。取消暂存要明确写：

```shell
git restore --staged -- README.md
```

恢复前仍然应先用 [[1、撤销前的三问诊断|撤销前的三问诊断]] 判断改动所在位置。

# 三、操作流程

## 1、查看暂存区

取消暂存前，先看 index 中准备进入下一次提交的内容：

```shell
git diff --staged -- README.md
```

命令拆解：

| 部分 | 作用 |
|---|---|
| `git diff` | 查看差异 |
| `--staged` | 查看 index 相对 `HEAD` 的差异 |
| `--` | 路径分隔符，表示后面是文件路径 |
| `README.md` | 只查看这个文件 |

这一步回答的是：如果现在提交，`README.md` 会带进去什么？

## 2、取消暂存

确认这份修改暂时不该进入下一次提交后，执行：

```shell
git restore --staged -- README.md
```

结果是：

| 区域 | 结果 |
|---|---|
| index | `README.md` 恢复到 `HEAD` 中的版本 |
| working tree | 保留文件里的修改 |
| commit history | 不创建新提交，不移动分支 |
| remote | 不影响 GitHub 或 GitLab |

如果取消暂存前是：

```text
M  README.md
```

取消暂存后常见状态会变成：

```text
 M README.md
```

含义是：修改已经不在 index，但还留在 working tree。

## 3、确认内容

取消暂存后，再检查普通 diff：

```shell
git diff -- README.md
```

这时应该能看到刚才的修改。这个结果说明：`git restore --staged` 不是删除修改，而是把修改从“下一次提交草稿”退回“普通工作区修改”。

# 四、边界区别

## 1、命令对比

`--staged` 是这个命令的关键边界：

| 想做什么 | 命令 | 影响区域 | 是否保留文件内容 |
|---|---|---|---|
| 取消暂存 | `git restore --staged -- README.md` | index | 保留 |
| 丢弃工作区修改 | `git restore -- README.md` | working tree | 不保留 |

可以记成：

```text
--staged 影响 index。
不带 --staged 默认影响 working tree。
```

更完整的工作区恢复流程见 [[2、用 git restore 丢弃工作区修改|丢弃工作区修改]]。

## 2、常见误区

`git restore --staged -- README.md` 不是“撤销文件内容”，而是“撤销暂存状态”。它让 index 回到 `HEAD`，但保留 working tree 内容。

如果真正想丢弃文件内容，需要在取消暂存后继续运行：

```shell
git diff -- README.md
git restore -- README.md
```

但这一步会丢弃 working tree 修改，执行前必须确认 diff 中没有要保留的内容。

# 五、操作判断

取消暂存可以按这个顺序判断：

```text
status 看是否已暂存
diff --staged 看暂存内容
restore --staged 取消暂存
status + diff 验证内容仍在 working tree
```

对应命令：

```shell
git status -sb
git diff --staged -- README.md
git restore --staged -- README.md
git status -sb
git diff -- README.md
```

目标状态不是 clean，而是让修改离开 index、回到 working tree。之后可以重新拆分修改、重新选择要提交的文件，或者在确认不要内容后再使用 [[2、用 git restore 丢弃工作区修改|工作区恢复]]。

这篇和 [[通用计算机知识/notes/Git/01_本地仓库与提交基础/6、撤销修改和取消暂存|撤销修改和取消暂存]] 讲的是同一个核心边界：`--staged` 处理暂存区，不带 `--staged` 处理工作区。
