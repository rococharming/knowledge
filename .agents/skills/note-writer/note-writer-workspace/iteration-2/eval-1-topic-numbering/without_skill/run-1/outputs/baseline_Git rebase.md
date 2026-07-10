---
title: Git rebase
tags: [Git, 版本控制]
---

# 一、基本概念

## 1、什么是 rebase

`git rebase` 是 Git 中用于整理提交历史的命令。它的核心思想是：

> 把一系列提交从一个基准（base）上"摘下来"，重新应用到另一个基准上。

"rebase" 这个名字本身就说明了它的行为：**重新设置提交的 base** 。

假设当前提交历史如下：

```text
      C---D---E  feature
     /
A---B---F---G  main
```

`feature` 分支从 `B` 处切出，之后 `main` 又新增了 `F`、`G`。此时 `feature` 的 base 是 `B`。

执行：

```bash
git checkout feature
git rebase main
```

Git 会把 `feature` 上的 `C`、`D`、`E` 逐个重新应用到 `main` 的最新提交 `G` 之上，效果相当于把 base 从 `B` 移动到 `G`：

```text
A---B---F---G  main
             \
              C'---D'---E'  feature
```

注意 `C'`、`D'`、`E'` 是**新生成的提交**，虽然内容相同，但它们的 commit hash 已经改变。这是 rebase 最关键的性质之一。

## 2、rebase 与 merge 的区别

`rebase` 和 `merge` 都能把一个分支的变更整合到另一个分支，但它们产生的历史形态不同。

| 对比项       | merge                        | rebase                          |
| --------- | ---------------------------- | ------------------------------- |
| 历史形态      | 保留分叉与合并节点，历史完整            | 把提交线性地接在目标分支之后，历史更整洁 |
| 提交 hash | 原有提交不变，新增一个 merge commit | 被重新应用的提交 hash 会改变        |
| 冲突处理      | 一次性解决所有冲突                  | 可能在每个被重放的提交上分别解决冲突    |
| 适用场景      | 合并公共分支、保留协作痕迹             | 整理个人分支、保持线性历史            |

用 `merge` 整合 `feature` 到 `main` 的结果是：

```text
      C---D---E  feature
     /         \
A---B---F---G---M  main
```

`M` 是一个合并提交，保留了 `feature` 分支曾经存在过的痕迹。

用 `rebase` 则是把 `feature` 的提交"搬到" `main` 最新点之后，形成一条直线。从历史看，仿佛 `feature` 一直基于最新的 `main` 开发。

> 关于 merge 的基本概念，可参见 [[1、Git基础]]。

# 二、基本用法

## 1、将分支变基到目标分支

最常见的用法是把当前分支变基到另一个分支之上。

示例：

```bash
git checkout feature
git rebase main
```

这表示：以 `main` 为新基准，把 `feature` 上不在 `main` 中的提交逐个重新应用。

如果中途发生冲突，Git 会暂停并提示。解决冲突后继续：

```bash
git add <已解决的文件>
git rebase --continue
```

如果想放弃这次 rebase，回到开始前的状态：

```bash
git rebase --abort
```

## 2、交互式 rebase

交互式 rebase 允许在重放提交的过程中修改每一个提交，例如修改提交信息、合并提交、调整顺序、删除提交等。

语法：

```bash
git rebase -i <基准点>
```

例如，整理当前分支最近 3 个提交：

```bash
git rebase -i HEAD~3
```

Git 会打开编辑器，列出待处理的提交：

```text
pick   a1b2c3d 第一个提交
pick   e4f5g6h 第二个提交
pick   7i8j9k0 第三个提交
```

每一行开头的命令决定了该提交如何被处理。保存退出后，Git 按照列表从上到下依次重放。

> 注意：列表中**最上面的是最旧的提交** ，最下面的是最新的提交，顺序和 `git log` 默认输出相反。

# 三、交互式 rebase 的常用操作

交互式 rebase 的强大之处在于可以改写历史。下表列出常用命令：

| 命令       | 缩写 | 作用                       |
| -------- | -- | ------------------------ |
| pick     | p  | 保留该提交，原样应用              |
| reword   | r  | 保留提交内容，修改提交信息         |
| edit     | e  | 应用后暂停，可修改提交内容或拆分提交   |
| squash   | s  | 把该提交合并到上一个提交，保留两条信息 |
| fixup    | f  | 把该提交合并到上一个提交，丢弃该提交信息 |
| drop     | d  | 丢弃该提交                   |
| （调整行顺序） |    | 通过交换行顺序改变提交先后          |

## 1、reword 修改提交信息

把某行改为 `reword`：

```text
pick   a1b2c3d 第一个提交
reword e4f5g6h 第二个提交
pick   7i8j9k0 第三个提交
```

保存后，Git 在重放到 `e4f5g6h` 时会打开编辑器，让你重新输入这条提交信息。提交内容本身不变。

## 2、squash 合并提交

`squash` 会把当前提交合并进它**上面那一行**的提交，并把两条提交信息拼接在一起。

```text
pick   a1b2c3d 添加功能骨架
squash e4f5g6h 补充实现
squash 7i8j9k0 修复小问题
```

保存后，Git 会把三条提交合并成一条，并让你编辑合并后的提交信息。

如果只关心最终内容、不想要中间提交信息，用 `fixup` 更合适：

```text
pick   a1b2c3d 添加功能骨架
fixup  e4f5g6h 补充实现
fixup  7i8j9k0 修复小问题
```

`fixup` 同样合并提交，但会直接丢弃被合并提交的信息，只保留第一条提交的 message。

> 实际开发中，`fixup` 常用于把"补丁式"的小提交并入对应的功能提交，保持历史简洁。

## 3、drop 丢弃提交

把某行改为 `drop`，或直接删除整行，该提交就不会被重放：

```text
pick   a1b2c3d 保留这个提交
drop   e4f5g6h 丢弃这个提交
pick   7i8j9k0 保留这个提交
```

丢弃提交后，后续提交会基于前一个保留的提交重新应用。

## 4、调整提交顺序

交互式列表的行顺序就是重放顺序。直接交换行的位置即可调整提交先后。

```text
pick   7i8j9k0 原本最新的提交
pick   a1b2c3d 原本最旧的提交
pick   e4f5g6h 原本中间的提交
```

调整顺序后，如果提交之间存在依赖，可能会产生冲突，需要手动解决。

# 四、处理冲突

## 1、冲突的产生

rebase 的本质是逐个重新应用提交。当某个被重放的提交与目标分支上的改动修改了同一处代码时，就会产生冲突。

示例：

```bash
git checkout feature
git rebase main
```

如果 `feature` 上的 `C` 与 `main` 上的改动冲突，Git 会暂停并提示：

```text
CONFLICT (content): Merge conflict in src/main.rs
```

与 merge 一次解决所有冲突不同，**rebase 可能在每个被重放的提交上分别产生冲突** 。

## 2、解决冲突并继续

冲突文件的格式与 merge 一致：

```text
<<<<<<< HEAD
当前 base 分支上的内容
=======
正在重放的提交带来的内容
>>>>>>> 提交信息
```

解决步骤：

1. 编辑冲突文件，保留需要的内容，删除冲突标记
2. 用 `git add` 标记已解决
3. 用 `git rebase --continue` 继续

```bash
git add src/main.rs
git rebase --continue
```

如果某个提交的冲突实在难以处理，可以跳过它：

```bash
git rebase --skip
```

任何时候都可以放弃整个 rebase：

```bash
git rebase --abort
```

## 3、冲突处理的选择对照

| 命令                     | 含义                       |
| ---------------------- | ------------------------ |
| `git rebase --continue` | 解决冲突后继续重放下一个提交      |
| `git rebase --skip`     | 跳过当前提交，继续后续重放          |
| `git rebase --abort`    | 放弃 rebase，回到开始前的状态    |

# 五、常见场景

## 1、合并多个小提交

开发过程中常常产生"补丁式"小提交，例如：

```text
* 添加功能
* 修复 typo
* 补充测试
* 再修复一处
```

希望合并成一条干净的提交：

```bash
git rebase -i HEAD~4
```

把后三行改为 `fixup`：

```text
pick   a1b2c3d 添加功能
fixup  e4f5g6h 修复 typo
fixup  7i8j9k0 补充测试
fixup  l1m2n3o 再修复一处
```

保存后这四条提交合并为一条，历史变得简洁。

## 2、保持分支线性

在 `feature` 分支开发期间，`main` 有了新提交。不希望合并时产生 merge commit，可以定期 rebase：

```bash
git checkout feature
git rebase main
```

这样 `feature` 始终基于最新的 `main`，后续合并到 `main` 时可以走 fast-forward，历史保持线性。

## 3、用 --onto 精确指定新 base

`--onto` 用于更精细地控制变基范围，语法为：

```bash
git rebase --onto <newbase> <oldbase> <分支>
```

含义：把 `<分支>` 上自 `<oldbase>` 之后的提交，重新应用到 `<newbase>` 之上。

典型场景：`feature` 最初基于 `oldbase` 分支开发，现在希望它改为基于 `main`。

```bash
git rebase --onto main oldbase feature
```

这会把 `feature` 上不在 `oldbase` 中的提交搬到 `main` 之上，常用于切换 feature 分支的依赖基准。

# 六、注意事项

## 1、不要 rebase 已推送的提交

rebase 会改写提交历史，生成新的 commit hash。如果某条提交已经推送到远程共享分支，其他人可能已经基于它工作。此时再 rebase 并强制推送，会让别人的本地历史与远程不一致，造成混乱。

> 核心原则： **只对尚未分享的、本地的提交执行 rebase** 。

对已推送的公共提交，应该使用 `merge`，保留历史完整性。

## 2、--force 与 --force-with-lease

rebase 改写历史后，本地分支与远程分支已经分叉，普通 `git push` 会被拒绝。需要强制推送：

```bash
git push --force-with-lease
```

`--force` 会无条件覆盖远程分支，风险较高。推荐使用 `--force-with-lease`，它会在远程分支被他人更新时拒绝推送，避免覆盖别人的工作。

| 选项                    | 行为                              |
| --------------------- | ------------------------------- |
| `--force`           | 无条件覆盖远程分支，可能丢失他人提交         |
| `--force-with-lease` | 远程分支未被他人更新时才推送，更安全        |

## 3、rebase 后找回旧提交

rebase 会生成新提交，但旧提交并没有立即被删除，只是不再被任何分支引用。在 GC 清理之前，可以通过 reflog 找回：

```bash
git reflog
```

reflog 记录了 HEAD 的每一次移动。找到 rebase 之前的状态，可以创建分支指向它：

```bash
git branch recover <旧的 commit hash>
```

因此，即使 rebase 出错，只要 reflog 还在，就有机会恢复。

## 4、rebase 与 merge 的选择建议

| 场景                      | 推荐         | 原因                       |
| ----------------------- | ---------- | ------------------------ |
| 整理本地未推送的提交        | rebase     | 让历史整洁，便于审查            |
| 把 feature 同步到最新 main | rebase     | 避免无意义的 merge commit |
| 合并 feature 到 main       | merge 或 ff | 保留协作记录，便于追溯          |
| 整合已推送的公共分支        | merge      | 不改写公共历史，避免冲突       |

简单判断：

- 提交还没推给别人 → 可以 rebase
- 提交已经推给别人 → 用 merge

> 关于 Git 基本概念，可参见 [[1、Git基础]]。
