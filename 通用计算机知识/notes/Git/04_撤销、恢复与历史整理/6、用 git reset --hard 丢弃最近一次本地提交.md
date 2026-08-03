---
title: 用 git reset --hard 丢弃最近一次本地提交
date: 2026-08-03
tags: [Git, Git恢复, Git撤销, Git基础]
aliases:
  - git reset --hard
  - hard reset
  - 丢弃最近提交
---

# 一、hard reset

`git reset --hard HEAD~1` 用来把当前分支从最近一次提交退回到它的父提交，并把 index 和 working tree 都覆盖到目标提交。它适合处理一个很窄的场景：最近一次本地提交还没有共享，而且已经确认这次提交里的文件修改也不要了。

核心模型是：

```text
git reset --hard HEAD~1
= 当前分支后退一个提交
+ index 重置到目标提交
+ working tree 覆盖到目标提交
```

它不只是拆提交，还会改变磁盘上的已跟踪文件内容。

![[assets/reset-hard-head-one-generated.png|600]]

# 二、安全边界

## 1、先确认真的要丢

`--hard` 是 `reset` 里最需要谨慎的模式。执行前至少确认这些信息：

| 检查 | 目标 |
|---|---|
| `git status -sb` | 只看到准备丢弃的目标修改，不夹带其他路径 |
| `git diff -- README.md` | 确认 working tree 中没有要保留的内容 |
| `git diff --staged -- README.md` | 确认 index 中没有要保留的内容 |
| `[ahead 1]` | 练习仓库中用于判断最近提交还没 push |

如果还有其他路径、其他重要内容，或者提交已经共享，先停下，不要运行 hard reset。恢复前的总入口仍然是 [[1、撤销前的三问诊断|撤销前的三问诊断]]。

## 2、只处理未共享提交

`reset --hard` 会移动当前分支指针。对已经 push、进入 PR、或可能被别人基于其继续工作的提交，默认不要用它改写历史。

共享历史更适合用追加修复提交或 `git revert`，因为这类方式会保留“曾经发生过什么”和“后来如何撤销”的记录。

# 三、命令拆解

## 1、基本命令

丢弃最近一次本地提交及其文件修改：

```shell
git reset --hard HEAD~1
```

命令拆解：

| 部分 | 含义 |
|---|---|
| `git reset` | 移动当前分支指针到指定提交 |
| `--hard` | 移动分支，重置 index，并覆盖 working tree |
| `HEAD~1` | 当前提交的父提交，也就是往回一步 |

`--hard` 的危险点在于：

```text
它会影响 working tree，也就是磁盘上的文件内容。
```

## 2、状态变化

reset 前，刚做了一个本地提交：

```shell
git status -sb
```

可能看到：

```text
## main...origin/main [ahead 1]
```

确认这次提交和文件内容都不要后，执行：

```shell
git reset --hard HEAD~1
```

Git 通常会输出类似：

```text
HEAD is now at fe8d9c0 Previous commit
```

再看状态：

```shell
git status -sb
```

常见结果：

```text
## main...origin/main
```

含义：

| 输出 | 含义 |
|---|---|
| 没有 `[ahead 1]` | 当前分支已经退回目标提交 |
| 没有 `README.md` 修改 | index 和 working tree 都回到目标提交 |
| `git diff -- README.md` 没输出 | 工作区没有这份修改 |
| `git diff --staged -- README.md` 没输出 | 暂存区没有这份修改 |

# 四、边界区别

## 1、三种 reset

`--soft`、`--mixed`、`--hard` 都会移动当前分支和 `HEAD`，差别在于 index 和 working tree：

| 命令 | 移动 `HEAD` / 分支 | 改 index | 改 working tree | 常见结果 |
|---|---|---|---|---|
| `git reset --soft HEAD~1` | 会 | 不会 | 不会 | `M  README.md` |
| `git reset --mixed HEAD~1` | 会 | 会 | 不会 | ` M README.md` |
| `git reset --hard HEAD~1` | 会 | 会 | 会 | clean |

一句话：

```text
--soft 拆回暂存区。
--mixed 拆回工作区。
--hard 连工作区内容也回到目标提交。
```

`--soft` 见 [[4、用 git reset --soft 拆开最近一次本地提交|soft reset]]；`--mixed` 见 [[5、用 git reset --mixed 拆提交并取消暂存|mixed reset]]。

## 2、不是删除所有文件

`git reset --hard` 主要处理 Git 已跟踪文件的 index 和 working tree 状态。它不会删除普通 untracked files。

如果当前目录里有 `?? temp.txt` 这类未跟踪文件，`reset --hard` 通常不会把它删掉。不要把它当成“清空工作目录”的命令。

## 3、不是更彻底的 mixed

`--hard` 不是“更彻底但语义相同的 mixed”。`--mixed` 保留 working tree；`--hard` 会覆盖 working tree。

> [!warning] 看到 hard 先停一下
> 如果目标只是拆开提交并保留内容，不要使用 `--hard`。只有确认提交和文件修改都不要时，才考虑这个模式。

# 五、操作判断

hard reset 可以按这个顺序判断：

```text
status 看范围
diff 看内容
log 确认最近提交
reset --hard 回到目标提交
status + diff 验证 clean
```

对应命令：

```shell
git status -sb
git diff -- README.md
git diff --staged -- README.md
git log --oneline --decorate --max-count=2
git reset --hard HEAD~1
git status -sb
git diff -- README.md
git diff --staged -- README.md
```

目标状态通常是 clean：最近一次本地提交已经不在当前分支顶端，index 和 working tree 都回到目标提交。

如果 `git status -sb` 只剩分支行，`git diff -- README.md` 和 `git diff --staged -- README.md` 都没有输出，就说明 `--hard` 后的状态符合预期。
