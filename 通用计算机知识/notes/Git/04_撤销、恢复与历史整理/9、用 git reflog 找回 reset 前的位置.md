---
title: 用 git reflog 找回 reset 前的位置
date: 2026-08-03
tags: [Git, Git恢复, Git撤销, Git远程]
aliases:
  - git reflog
  - reflog
  - HEAD 足迹
---

# 一、reflog

`git reflog` 用来查看本地 `HEAD` 或引用最近移动过的位置。它解决的是一个很实际的问题：执行 `reset` 之后，`git log` 可能看不到刚才的提交了，但本地 reflog 通常还记得 `HEAD` 曾经到过哪里。

核心模型是：

```text
git log    看当前分支历史里有什么。
git reflog 看本地 HEAD 或引用最近移动到过哪里。
```

简单说：`log` 看“分支现在能走到哪里”；`reflog` 看“你本地刚才去过哪里”。

![[assets/reflog-recover-reset-position-generated.png|600]]

# 二、reset 场景

## 1、清回基线

本地有明确不要保留、也没有 push 的 ahead 提交时，可以用 [[8、用 git reset --hard origin-main 清理本地练习历史|reset 到 origin/main]] 把当前分支清回远程跟踪基线：

```shell
git reset --hard origin/main
```

这个命令会让当前分支、index 和 working tree 都对齐到本地记录的 `origin/main`：

```text
git reset --hard origin/main
= 当前分支指向 origin/main
+ index 对齐 origin/main
+ working tree 对齐 origin/main
```

![[assets/reset-hard-origin-main-cleanup-generated.png|600]]

## 2、历史消失感

`reset --hard origin/main` 执行后，当前分支已经回到 `origin/main`。再用 `git log` 看当前分支历史时，刚才被清理掉的本地 ahead 提交通常不再出现在分支顶端。

这不是说对象一定立刻从 `.git` 里消失了，而是当前分支不再指向那段历史。此时更稳的恢复入口不是马上再 reset 回去，而是先查 reflog，确认 `HEAD` 在 reset 前的位置。

# 三、本地足迹

## 1、查看 reflog

查看最近几次 `HEAD` 移动记录：

```shell
git reflog --oneline --date=relative --max-count=8
```

可能看到类似：

```text
fe8d9c0 HEAD@{2 minutes ago}: reset: moving to origin/main
ffa4a31 HEAD@{12 minutes ago}: revert: Revert "Add revert practice line"
e8e5b34 HEAD@{13 minutes ago}: commit: Add revert practice line
```

这里有三类信息：

| 项 | 含义 |
|---|---|
| `fe8d9c0` | reflog 条目记录的位置对应的提交 |
| `HEAD@{...}` | 可以临时引用这个历史位置的名字 |
| `reset: ...` / `revert: ...` | 让 `HEAD` 移动到该位置的操作说明 |

`HEAD@{0}` 通常是当前 `HEAD` 位置；`HEAD@{1}` 常是上一个 `HEAD` 位置。但不要死记序号，因为新的 checkout、commit、reset 都可能继续写入 reflog，让序号变化。

## 2、找 reset 前

如果刚执行过：

```shell
git reset --hard origin/main
```

reflog 中常会出现：

```text
HEAD@{0}: reset: moving to origin/main
HEAD@{1}: revert: Revert "Add revert practice line"
```

这表示当前 `HEAD` 在 reset 后的位置，而上一个位置可能就是 reset 前的提交。关键判断不是“看到 `HEAD@{1}` 就用”，而是结合说明文字和提交内容确认它是不是要找的位置。

# 四、确认位置

## 1、先 show

确认候选位置时，先用只读命令查看：

```shell
git show --stat --oneline HEAD@{1}
```

它只展示提交摘要和文件统计，不移动分支、不修改 index、不覆盖 working tree。若输出类似：

```text
ffa4a31 Revert "Add revert practice line"
 README.md | 3 +--
```

说明 `HEAD@{1}` 指向的是 reset 前的那个 revert 练习位置。

## 2、也可看 log

如果想看候选位置附近的历史，可以用：

```shell
git log --oneline --decorate --max-count=3 HEAD@{1}
```

这个命令同样只是观察。它从 `HEAD@{1}` 指向的提交开始往父提交方向列历史，适合确认“这个位置下面接着哪些提交”。

> [!warning] 先观察，再恢复
> 不要一看到 `HEAD@{1}` 就直接执行 `git reset --hard HEAD@{1}`。先用 `show` 或 `log` 确认候选位置，避免把当前分支移动到错误提交。

# 五、恢复分支

## 1、保存位置

确认候选位置后，先创建一个恢复分支保存它：

```shell
git branch recover/revert-practice HEAD@{1}
```

这条命令的效果是：

| 区域 | 结果 |
|---|---|
| 当前 `main` | 不改变 |
| index | 不改变 |
| working tree | 不改变 |
| 新分支 | `recover/revert-practice` 指向 `HEAD@{1}` |

它只是给那个提交起了一个稳定名字。以后即使 reflog 序号变化，只要分支还在，就可以通过 `recover/revert-practice` 找到这个位置。

## 2、检查分支

检查恢复分支是否已经创建：

```shell
git branch --list "recover/*"
```

期待看到：

```text
  recover/revert-practice
```

再看当前状态：

```shell
git status -sb
```

目标是当前分支仍然 clean，例如：

```text
## main...origin/main
```

# 六、边界误区

## 1、本地记录

reflog 是本地记录，不是团队共享记录。别人电脑上的 reflog 不会自动包含你的 `reset`、`checkout`、`commit` 足迹。

因此，reflog 适合处理“我这台机器上刚刚误操作了”的问题，不适合作为团队审计历史。已经共享出去的错误提交，仍然优先考虑 [[7、用 git revert 安全撤销共享历史|revert]] 这类保留历史记录的方式。

## 2、不是永久

reflog 不是永久档案。Git 会按过期策略清理旧 reflog 条目，不可达对象也可能在垃圾回收后消失。

所以发现误 reset、误 checkout、误删分支后，越早查看 reflog 越好。确认位置后，优先用分支、标签或新提交把它固定下来，而不是长期依赖 `HEAD@{n}` 这种会变化的引用。

## 3、不是反悔键

reflog 本身不恢复文件，也不移动分支。它只是帮你找到本地引用曾经到过的位置。

真正保存位置的是：

```shell
git branch recover/revert-practice HEAD@{1}
```

真正移动当前分支的是：

```shell
git reset --hard HEAD@{1}
```

初学和不确定场景里，先创建恢复分支更稳，因为它保存位置但不改当前工作状态。

# 七、操作判断

reflog 找回 reset 前位置，可以按这个顺序：

```text
status 确认当前状态
reflog 找 HEAD 足迹
show/log 检查候选位置
branch 创建恢复分支
status 验证当前分支未被改动
```

对应命令：

```shell
git status -sb
git reflog --oneline --date=relative --max-count=8
git show --stat --oneline HEAD@{1}
git branch recover/revert-practice HEAD@{1}
git branch --list "recover/*"
git status -sb
```

关键判断是：reflog 用来找位置，`show` 用来确认位置，`branch` 用来保存位置。只有确认要移动当前分支时，才考虑再用 `reset`。
