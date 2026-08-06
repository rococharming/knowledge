---
title: 用交互式 rebase 整理本地提交
date: 2026-08-06
tags: [Git, Git恢复, Git提交, git-rebase]
aliases:
  - git rebase -i
  - interactive rebase
  - squash
---

# 一、交互式 rebase

交互式 rebase 是整理未共享本地提交的工具。它会打开一个可编辑的 todo 列表，让你决定一段本地提交要保留、改名、暂停修改、合并还是丢弃。

最常见的入门用法是把几个属于同一件事的小提交压成一个更清楚的提交：

```shell
git rebase -i HEAD~2
```

核心模型是：

```text
选择最近 2 个提交
打开 todo 列表
把后一个提交 squash 进前一个提交
生成一个新的整理后提交
```

![[assets/interactive-rebase-squash-local-commits-generated.png|600]]

这里的 rebase 和 [[通用计算机知识/notes/Git/02_分支、合并与历史演进/6、Rebase：把提交重放到新起点|普通 rebase]] 共享一个底层事实：它会重新创建提交，所以哈希会变化。区别在于，普通 rebase 主要是“换起点并重放”，交互式 rebase 还允许你编辑每个提交的处理方式。

# 二、安全边界

## 1、只改未共享

交互式 rebase 会重写所选提交的历史。适合整理这些提交：

| 场景 | 判断 |
|---|---|
| 还没 push | 通常可以整理 |
| 还没进入 PR | 通常可以整理 |
| 别人没有基于它继续工作 | 通常可以整理 |
| 已经 push 或被 review | 不要随手整理 |

一旦提交已经共享，别人可能已经拿到旧提交哈希。此时再用 `rebase -i` 改写历史，容易让协作关系变复杂。共享历史需要重新回到 [[1、撤销前的三问诊断|撤销前的三问诊断]]。

## 2、区别 amend

[[通用计算机知识/notes/Git/01_本地仓库与提交基础/10、修改最近一次提交|amend]] 适合修正最近一次提交；交互式 rebase 适合整理最近多条本地提交。

| 工具 | 适合处理 |
|---|---|
| `git commit --amend` | 最近一次提交 |
| `git rebase -i HEAD~2` | 最近两次提交 |
| `git rebase -i HEAD~4` | 最近四次提交 |

如果只是刚提交完发现 message 写错或漏了一点内容，`amend` 更简单。如果多个小提交其实属于同一个任务，交互式 rebase 更合适。

# 三、todo 列表

## 1、顺序

交互式 rebase 的 todo 列表通常按“从旧到新”的顺序列出提交。它和常见 `git log` 输出相反：`git log` 往往把最新提交放在最上面。

最近两个提交的 todo 可能类似：

```text
pick 1111111 Add first rebase practice line
pick 2222222 Add second rebase practice line
```

如果想把第二个提交并入第一个提交，改成：

```text
pick   1111111 Add first rebase practice line
squash 2222222 Add second rebase practice line
```

`squash` 总是并入上一行保留下来的提交，所以它不能放在第一行。

## 2、更多提交

假设最近有四个本地小提交：

```text
C1 Add login form
C2 Fix login form typo
C3 Add login docs
C4 Polish login docs
```

想整理成两个提交，可以运行：

```shell
git rebase -i HEAD~4
```

todo 可以改成：

```text
pick   C1 Add login form
squash C2 Fix login form typo
pick   C3 Add login docs
squash C4 Polish login docs
```

结果是：

| 输入 | 输出 |
|---|---|
| `C1 + C2` | 一个新的 login form 提交 |
| `C3 + C4` | 一个新的 login docs 提交 |

如果四个提交都属于同一件事，才写成一个 `pick` 后接多个 `squash`，把它们压成一个提交。

# 四、常见动作

## 1、入门动作

交互式 rebase 的 todo 动作很多，入门阶段先掌握最常见的几个：

| 动作 | 作用 | 适用建议 |
|---|---|---|
| `pick` | 保留并重放这个提交 | 默认动作 |
| `reword` | 保留提交内容，只改提交信息 | 想改 message |
| `edit` | 重放到这里时暂停，让你改提交内容 | 需要中途修改 |
| `squash` | 合并进上一条提交，并整理最终 message | 小提交合并 |
| `fixup` | 合并进上一条提交，但默认丢掉自己的 message | 熟悉后使用 |
| `drop` | 丢弃这个提交 | 谨慎使用 |

还有 `exec`、`break`、`label`、`reset`、`merge` 等动作，主要用于更复杂的 rebase 流程。初学阶段先不要手写它们。

## 2、pick 与 squash

两条提交压成一条时，最小 todo 是：

```text
pick   C1 First small commit
squash C2 Second small commit
```

读法是：

```text
保留 C1
把 C2 的改动并入 C1
整理最终提交信息
生成一个新提交
```

整理后原来的 `C1`、`C2` 不再是当前分支上的最新提交；当前分支会指向新提交 `S`。

# 五、整理示例

## 1、创建小提交

起点应是干净的 `main`：

```shell
git status -sb
```

期待：

```text
## main...origin/main
```

在 `README.md` 末尾新增：

```text
Interactive rebase first line.
```

提交：

```shell
git add README.md
git commit -m "Add first rebase practice line"
```

再新增：

```text
Interactive rebase second line.
```

再次提交：

```shell
git add README.md
git commit -m "Add second rebase practice line"
```

## 2、确认范围

确认当前只多两条本地提交：

```shell
git status -sb
git log --oneline --decorate origin/main..main
```

期待类似：

```text
## main...origin/main [ahead 2]
2222222 (HEAD -> main) Add second rebase practice line
1111111 Add first rebase practice line
```

如果 `origin/main..main` 里还有其他提交，先不要继续。`HEAD~2` 会选中最近两个提交，选错范围就会整理错历史。

# 六、执行整理

## 1、打开 todo

执行：

```shell
git rebase -i HEAD~2
```

编辑器中会出现类似：

```text
pick 1111111 Add first rebase practice line
pick 2222222 Add second rebase practice line
```

把第二行开头从 `pick` 改成 `squash`：

```text
pick 1111111 Add first rebase practice line
squash 2222222 Add second rebase practice line
```

保存并关闭编辑器。Git 随后会打开提交信息编辑器，让你整理 squash 后的新提交 message。

## 2、整理 message

最终提交信息可以整理为：

```text
Add rebase squash practice
```

保存并关闭后，Git 会继续完成 rebase。成功后，最近两条提交会变成一条新提交。

## 3、检查结果

检查：

```shell
git status -sb
git log --oneline --decorate origin/main..main
git show --stat --oneline HEAD
```

期待类似：

```text
## main...origin/main [ahead 1]
3333333 (HEAD -> main) Add rebase squash practice
 README.md | 2 ++
```

重点是：

| 检查项 | 期待 |
|---|---|
| ahead 数量 | 从 2 变成 1 |
| 最新提交信息 | `Add rebase squash practice` |
| 文件统计 | `README.md` 有两行新增 |
| 工作区 | clean |

# 七、收尾清理

## 1、确认无额外修改

如果整理出来的提交只是本地练习，并且内容也不要保留，可以在练习结尾清掉。先确认没有额外修改：

```shell
git diff --stat
git diff --staged --stat
```

两个命令都没有输出，才说明 working tree 和 index 没有夹带未提交修改。

## 2、回到基线

确认无误后执行：

```shell
git reset --hard HEAD~1
git status -sb
```

目标状态：

```text
## main...origin/main
```

这一步只是清理练习提交。真实项目中，如果整理后的提交值得保留，不要执行这个收尾 reset。

# 八、卡住时

## 1、编辑器

如果停在 todo 或提交信息编辑器里，不确定怎么保存退出，先停下来读屏幕内容，不要乱删 todo 行。交互式 rebase 的 todo 是“操作清单”，删错行可能等同于丢弃提交。

## 2、冲突

如果 Git 在 rebase 过程中提示 conflict，先运行：

```shell
git status
```

如果只是练习且没有其他重要修改，通常可以用：

```shell
git rebase --abort
```

回到 rebase 开始前的状态。若是实际工作，先读冲突文件和目标历史，再决定继续、跳过或中止。
