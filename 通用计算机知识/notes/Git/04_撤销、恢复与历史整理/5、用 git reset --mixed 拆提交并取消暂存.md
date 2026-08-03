---
title: 用 git reset --mixed 拆提交并取消暂存
date: 2026-08-03
tags: [Git, Git恢复, Git撤销, Git基础]
aliases:
  - git reset --mixed
  - mixed reset
  - 拆提交并取消暂存
---

# 一、mixed reset

`git reset --mixed HEAD~1` 用来把当前分支从最近一次提交退回到它的父提交，同时把 index 重置到目标提交，但保留 working tree 里的文件内容。它适合处理“刚做完一个本地提交，但想拆开它，并且不想让内容继续留在暂存区”的场景。

核心模型是：

```text
git reset --mixed HEAD~1
= 当前分支后退一个提交
+ index 重置到目标提交
+ working tree 保留文件内容
```

它拆的是提交，并把原提交内容退回工作区；不是删除文件修改。

![[assets/reset-mixed-head-one-generated.png|600]]

# 二、安全边界

## 1、只处理未共享提交

`reset` 会移动当前分支指针，因此仍然只适合本地、未共享的历史整理。执行前先用 [[1、撤销前的三问诊断|撤销前的三问诊断]] 判断：

| 问题 | 目标状态 |
|---|---|
| 改动在哪里 | 已经进入最近一次本地 commit |
| 提交了吗 | 已提交，而且只处理最近一次 |
| 共享了吗 | 没有 push，没有进入 PR |

如果提交已经 push 或进入 PR，默认不要用 `reset` 改写它。共享历史更适合用追加修复提交或 `git revert`。

## 2、ahead 信号

运行：

```shell
git status -sb
```

如果看到：

```text
## main...origin/main [ahead 1]
```

通常表示当前分支比 upstream 多 1 个本地提交。练习仓库里，这可以作为“最近提交还没 push”的主要信号。

真实协作里还要额外确认这个提交是否已经通过 PR、patch、截图或其他渠道被共享过。

# 三、命令拆解

## 1、基本命令

拆开最近一次本地提交，并让内容退回 working tree：

```shell
git reset --mixed HEAD~1
```

命令拆解：

| 部分 | 含义 |
|---|---|
| `git reset` | 移动当前分支指针到指定提交 |
| `--mixed` | 移动 `HEAD` 和当前分支，并把 index 重置到目标提交 |
| `HEAD~1` | 当前提交的父提交，也就是往回一步 |

`--mixed` 是 `git reset` 的默认模式。也就是说：

```shell
git reset HEAD~1
```

通常等价于：

```shell
git reset --mixed HEAD~1
```

初学阶段建议显式写出 `--mixed`，因为它能提醒你：这条命令会影响 index。

## 2、状态变化

reset 前，刚做了一个本地提交：

```shell
git status -sb
```

可能看到：

```text
## main...origin/main [ahead 1]
```

执行：

```shell
git reset --mixed HEAD~1
```

再看状态：

```shell
git status -sb
```

常见结果：

```text
## main...origin/main
 M README.md
```

含义：

| 输出 | 含义 |
|---|---|
| 没有 `[ahead 1]` | 当前分支已经退回到 upstream 对齐的位置 |
| ` M README.md` | 原提交里的修改还在 working tree，但不在 index |
| `git diff -- README.md` 有输出 | 文件内容仍然保留 |
| `git diff --staged -- README.md` 没输出 | 暂存区没有这份修改 |

# 四、边界区别

## 1、和 soft 的区别

`--soft` 和 `--mixed` 都会移动当前分支和 `HEAD`，差别在于 index：

| 命令 | 移动 `HEAD` / 分支 | 改 index | 改 working tree | 常见结果 |
|---|---|---|---|---|
| `git reset --soft HEAD~1` | 会 | 不会 | 不会 | `M  README.md` |
| `git reset --mixed HEAD~1` | 会 | 会 | 不会 | ` M README.md` |

一句话：

```text
--soft 拆回暂存区。
--mixed 拆回工作区。
```

`--soft` 的完整模型见 [[4、用 git reset --soft 拆开最近一次本地提交|soft reset]]。

## 2、和 restore 的区别

`git restore --staged -- README.md` 和 `git reset --mixed HEAD~1` 都可能让状态变成 ` M README.md`，但入口不同：

| 命令 | 主要处理什么 | 典型场景 |
|---|---|---|
| `git restore --staged -- README.md` | index 里的某个文件 | 取消暂存一个文件 |
| `git reset --mixed HEAD~1` | 当前分支指针和整个 index | 拆开最近一次本地提交 |

`restore --staged` 处理“文件已经暂存”；`reset --mixed` 处理“提交已经做出来”。

## 3、不要混用 hard

`--mixed` 会重置 index，但不会丢弃 working tree 内容。`--hard` 会同时重置 index 和 working tree，风险高得多。

> [!warning] 谨慎使用 `--hard`
> 如果目标只是拆开最近一次本地提交，并保留文件修改，不要使用 `git reset --hard HEAD~1`。

# 五、操作判断

mixed reset 可以按这个顺序判断：

```text
status 看是否 ahead
log 确认最近提交
reset --mixed 拆回 working tree
status + diff 验证内容仍在工作区、暂存区为空
```

对应命令：

```shell
git status -sb
git log --oneline --decorate --max-count=2
git reset --mixed HEAD~1
git status -sb
git diff -- README.md
git diff --staged -- README.md
```

目标状态通常是 ` M README.md`：最近一次本地提交已经不在当前分支顶端，文件修改仍留在 working tree，但已经不在 index。

如果 `git diff -- README.md` 能看到原提交内容，而 `git diff --staged -- README.md` 没有输出，就说明 `--mixed` 后的状态符合预期：提交被拆开，内容退回未暂存状态。
