---
title: 用 git revert 安全撤销共享历史
date: 2026-08-03
tags: [Git, Git恢复, Git撤销, git-revert]
aliases:
  - git revert
  - 共享历史撤销
  - revert commit
---

# 一、revert

`git revert` 用来追加一个新的反向提交，以抵消某个旧提交带来的文件修改。它适合处理已经 push、进入 PR，或者已经合入共享分支的错误提交。

核心模型是：

```text
git revert HEAD
= 不删除旧提交
+ 追加一个新提交
+ 新提交反向抵消 HEAD 的修改
```

`revert` 的关键价值是保留历史：错误提交仍然留在记录里，撤销动作也用新的提交明确记录下来。

![[assets/revert-shared-history-generated.png|600]]

# 二、共享历史

## 1、何时选择 revert

如果错误提交已经被别人看见，默认不要用 `reset` 改写它：

| 情况 | 含义 |
|---|---|
| 已 push 到远程 | 别人可能已经拉取 |
| 已进入 PR 或 MR | reviewer 可能已经看过并评论 |
| 已合入共享分支 | 团队主线历史已经包含它 |

这些场景里，更安全的方向通常是：

```shell
git revert HEAD
```

因为它不会让旧提交从历史里“消失”，也不会把团队成员正在使用的分支指针往回挪。

## 2、三问定位

选择撤销方式前，仍然先问 [[1、撤销前的三问诊断|撤销前的三问诊断]]：

| 问题 | revert 场景的典型答案 |
|---|---|
| 改动在哪里 | 已经进入 commit |
| 提交了吗 | 已提交 |
| 共享了吗 | 已 push、已进入 PR，或已合入共享分支 |

结论很直接：越接近共享历史，越应该保留可追踪记录，而不是改写别人已经看到的历史。

# 三、最小模型

## 1、错误提交后

假设当前历史是：

```text
A -> B -> C
          ^
       HEAD -> main
```

`C` 是错误提交。如果它已经共享，直接把分支指针移回 `B` 会改变别人已经看到的历史形状。

## 2、revert 之后

执行 revert 后，历史会继续向前：

```text
A -> B -> C -> R
               ^
            HEAD -> main
```

含义：

| 提交 | 含义 |
|---|---|
| `C` | 原来的错误提交，仍然在历史里 |
| `R` | 新的 revert commit，反向抵消 `C` 的文件修改 |

一句话：

```text
reset 是移动分支回去。
revert 是继续往前走，但新增一个反向提交。
```

# 四、命令拆解

## 1、基本命令

撤销最近一次普通提交：

```shell
git revert --no-edit HEAD
```

命令拆解：

| 部分 | 含义 |
|---|---|
| `git revert` | 创建一个新提交，用来反向应用指定提交的修改 |
| `--no-edit` | 使用默认 revert message，不打开编辑器 |
| `HEAD` | 这里指最近一次提交 |

默认提交信息通常类似：

```text
Revert "Add revert practice line"
```

如果不加 `--no-edit`，Git 通常会打开编辑器，让你确认或修改 revert commit 的提交信息。

## 2、状态变化

先有一个错误提交：

```shell
git log --oneline --decorate --max-count=2
```

可能看到：

```text
abc1234 (HEAD -> main) Add revert practice line
fe8d9c0 (origin/main, origin/HEAD) Previous commit
```

执行：

```shell
git revert --no-edit HEAD
```

再看历史：

```shell
git log --oneline --decorate --max-count=3
```

常见结果：

```text
def5678 (HEAD -> main) Revert "Add revert practice line"
abc1234 Add revert practice line
fe8d9c0 (origin/main, origin/HEAD) Previous commit
```

要观察两点：

| 观察 | 含义 |
|---|---|
| 旧提交还在 | 历史没有被删除 |
| 新增 `Revert ...` | Git 用新提交记录撤销动作 |

如果反向修改成功应用，working tree 通常会回到 clean，因为撤销结果已经写进新的提交。

# 五、边界区别

## 1、和 reset

`reset` 和 `revert` 都能表达“我不想要某次提交的效果”，但历史形状完全不同：

| 命令 | 历史形状 | 适合场景 |
|---|---|---|
| `git reset --hard HEAD~1` | 分支指针后退，旧提交不再是分支最新历史 | 未共享、本地确认要丢弃 |
| `git revert HEAD` | 分支继续向前，追加反向提交 | 已共享、需要保留历史记录 |

更短的区别：

```text
reset 改写分支指向。
revert 追加撤销记录。
```

本地确认要丢弃的场景见 [[6、用 git reset --hard 丢弃最近一次本地提交|hard reset]]。

## 2、常见误区

`revert` 不会删除旧提交。它是“追加撤销记录”，不是“回到过去并假装没发生”。

`revert` 也可能冲突。如果目标提交修改过的内容后来又被其他提交改过，反向应用时 Git 可能不知道该如何自动合并。遇到 conflict 时先停下，按冲突处理流程解决。

revert merge commit 还需要额外指定 mainline parent。本篇只讨论普通提交，不展开 merge commit 的撤销。

# 六、操作判断

安全撤销共享提交可以按这个顺序判断：

```text
status 确认当前状态
log 确认目标提交
revert 追加反向提交
status + log 验证历史和工作区
```

对应命令：

```shell
git status -sb
git log --oneline --decorate --max-count=3
git revert --no-edit HEAD
git status -sb
git log --oneline --decorate --max-count=3
```

目标结果是：旧提交仍在历史里，最新提交变成 `Revert "..."`，working tree 通常保持 clean。

如果 `git log` 中能同时看到原提交和新的 revert commit，就说明这次撤销是用“保留历史”的方式完成的。
