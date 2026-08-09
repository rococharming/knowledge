---
title: Git Worktree
date: 2026-08-09
tags: [计算机基础, Git, git, version-control]
aliases:
  - Git 工作树
  - git worktree
  - Git Worktree
---

# 一、核心模型

Git Worktree 用来让同一个 Git 仓库同时拥有多个工作目录。每个工作目录都连接到同一份仓库历史，但可以检出不同的分支、拥有不同的工作区文件和暂存区。

常见形态如下：

```text
project/          -> main
project-login/    -> feature/login
project-hotfix/   -> hotfix/crash
```

这不是重新 `git clone` 多份仓库，而是在一个仓库上挂出多个工作目录。原始仓库目录称为 main worktree，通过 `git worktree add` 创建的额外目录称为 linked worktree。

```text
Git repository
      |
      |-- main worktree   -> main
      |-- linked worktree -> feature/login
      `-- linked worktree -> hotfix/crash
```

Worktree 适合解决一个实际问题：不想为了处理另一条分支而频繁 `git stash`、`git switch`，也不想重新克隆一份完整仓库。

# 二、共享与独立

多个 Worktree 属于同一个仓库，所以它们共享提交历史、分支引用、远程仓库配置和 Git objects。但每个工作目录都有自己的 `HEAD`、index（暂存区）和工作区文件。

| 内容 | 是否共享 | 说明 |
|---|---|---|
| Commit 历史 | 共享 | 所有 Worktree 都能看到同一套提交对象 |
| Branch / refs | 共享 | 分支名仍然属于同一个仓库 |
| Remote 配置 | 共享 | `origin`、远程跟踪分支等是一套仓库级信息 |
| `HEAD` | 独立 | 每个 Worktree 可以指向不同分支或提交 |
| Index / 暂存区 | 独立 | 一个 Worktree 暂存文件，不影响另一个 Worktree |
| 工作区文件 | 独立 | 未提交修改留在各自目录中 |

例如在 `project-login/` 中修改文件，不会污染 `project/` 的未提交文件。但如果在任意 Worktree 执行：

```shell
git fetch origin
```

其他 Worktree 也能看到更新后的远程跟踪分支，因为远程状态属于共享仓库数据。远程跟踪分支的模型见 [[通用计算机知识/notes/Git/03_远程仓库与团队协作/2、Fetch 与远程跟踪分支|Fetch 与远程跟踪分支]]。

> Worktree 的核心不是“复制一份项目”，而是“让同一套 Git 历史同时服务多个工作目录”。

# 三、忽略文件

创建新 Worktree 时，Git 只会检出目标 commit 中已经被跟踪的文件，不会复制原 Worktree 里的未跟踪文件。被 ignore 规则忽略的目录通常正是未跟踪内容，所以不会自动出现在新 Worktree 中。

常见例子：

```text
node_modules/
target/
dist/
.env
```

这些文件或目录可能被 `.gitignore`、`.git/info/exclude` 或全局 ignore 规则忽略。只要它们没有进入 Git 跟踪，新 Worktree 就不会把它们带过去；需要使用时，要在对应 Worktree 里重新生成。

需要注意的是，`.gitignore` 和 `.git/info/exclude` 的职责不同：

| 规则来源 | 是否跟随提交 | 对 Worktree 的影响 |
|---|---|---|
| `.gitignore` | 通常会，因为它本身常被提交 | 新 Worktree 会检出这份文件，并继续按其中规则忽略未跟踪文件 |
| `.git/info/exclude` | 不会，它是本地仓库配置 | linked Worktree 会读取同一个仓库 common git dir 下的这份本地忽略规则 |
| 全局 ignore | 不会，它来自用户机器配置 | 在同一台机器上继续生效 |

忽略规则只影响未跟踪文件。已经被 Git 跟踪的文件，即使后来写进 `.gitignore` 或 `.git/info/exclude`，新 Worktree 仍然会检出它，因为它是提交内容的一部分。

> 简单判断：Worktree 会带提交里的 tracked 文件；不会带某个工作目录里临时生成、未跟踪、被忽略的本地文件。

# 四、创建 Worktree

创建 Worktree 前，先确认当前仓库状态：

```shell
git status -sb
git branch --show-current
```

`git status`、暂存和提交的基础流程见 [[通用计算机知识/notes/Git/01_本地仓库与提交基础/4、查看状态、暂存和提交|查看状态、暂存和提交]]。

## 1、检出现有分支

如果本地已经存在 `feature/login`：

```shell
git worktree add ../project-login feature/login
```

语法是：

```shell
git worktree add <新目录> <分支或提交>
```

执行后，Git 会在 `../project-login` 创建一个 linked worktree，并在其中检出 `feature/login`。进入新目录后，可以像普通仓库目录一样工作：

```shell
cd ../project-login
git status -sb
git add .
git commit -m "feat: add login page"
```

## 2、创建新分支

开发新功能时，常见写法是创建分支并同时创建 Worktree：

```shell
git worktree add -b feature/login ../project-login
```

这里的含义是：

| 片段 | 含义 |
|---|---|
| `-b feature/login` | 创建新分支 |
| `../project-login` | 创建新的工作目录 |
| 省略起点 | 默认从当前 `HEAD` 创建 |

分支本质是指向 commit 的引用，创建分支后，后续提交会推动该分支向前移动。这个模型见 [[通用计算机知识/notes/Git/02_分支、合并与历史演进/1、分支、refs 与 HEAD|分支、refs 与 HEAD]]。

## 3、指定起点

更稳妥的做法是先更新远程视野，再明确新分支从哪里开始：

```shell
git fetch origin

git worktree add \
  -b feature/login \
  ../project-login \
  origin/main
```

这表示：

```text
origin/main
    |
    `-- feature/login
            |
            `-- ../project-login
```

这样可以明确知道新功能基于 `origin/main` 创建，而不是意外基于当前所在分支。

## 4、临时实验

如果只是临时测试某个提交，不准备把工作绑定到一个分支，可以创建 detached HEAD 的 Worktree：

```shell
git worktree add --detach ../project-test origin/main
```

这种目录适合跑实验、复现问题或让工具临时分析代码。真正要长期提交时，仍建议创建具名分支，避免提交停留在不容易追踪的位置。创建和切换分支的基础操作见 [[通用计算机知识/notes/Git/02_分支、合并与历史演进/2、创建与切换分支|创建与切换分支]]。

# 五、查看 Worktree

查看当前仓库挂了哪些 Worktree：

```shell
git worktree list
```

输出示例：

```text
/Users/aaa/project        fa8928b [main]
/Users/aaa/project-login  e339fd4 [feature/login]
```

主要看三列：

| 列 | 含义 |
|---|---|
| 路径 | 这个 Worktree 在文件系统中的位置 |
| Commit | 当前 `HEAD` 指向的提交 |
| Branch | 当前检出的分支；没有分支时可能显示 detached HEAD |

需要给脚本解析时，可以使用稳定格式：

```shell
git worktree list --porcelain
```

日常人工查看时，普通 `git worktree list` 通常已经足够。

# 六、分支关系

Worktree 和 Branch 很容易混在一起。简单说：Worktree 是目录，Branch 是提交历史上的名字。

```text
Worktree = 文件系统里的工作目录
Branch   = Git 仓库中的分支引用
```

默认情况下，同一个本地分支不能同时被两个 Worktree 检出。因为两个目录如果同时推进同一个分支，`HEAD`、暂存区和工作区状态会变得很难判断。Git 通常会拒绝这种操作。

例如 `feature/login` 已经在 `../project-login` 中检出，再尝试在另一个目录检出同一分支，Git 会阻止你。日常开发不要用 `--force` 绕过这类保护，应该为并行任务创建不同分支。

删除 Worktree 也不会删除分支：

```shell
git worktree remove ../project-login
git branch
```

如果 `feature/login` 分支不再需要，要单独删除：

```shell
git branch -d feature/login
```

这和普通分支清理是同一件事，只是 Worktree 额外提供了一个目录入口。

# 七、移动与修复

`git worktree move` 用来移动 Git 已登记的 linked worktree。它移动的是工作目录的位置，并同步更新 Git 内部保存的 Worktree 路径；它不会改分支名，也不会改提交历史。

## 1、正常移动

推荐用 Git 命令移动：

```shell
git worktree move ../project-login ../worktrees/project-login
```

语法是：

```shell
git worktree move <旧 Worktree 路径> <新 Worktree 路径>
```

移动前可以先看当前登记路径：

```shell
git worktree list
```

移动后再检查一次：

```shell
git worktree list
git -C ../worktrees/project-login status -sb
```

如果输出里的路径已经变成新目录，并且新目录能正常执行 `git status`，说明目录移动和 Git 内部登记都已经同步。

## 2、不要直接 mv

不要优先使用系统命令：

```shell
mv ../project-login ../worktrees/project-login
```

`mv` 只移动文件系统目录，不会主动更新 Git 仓库中记录的 Worktree 管理信息。结果可能变成：

```text
Git 记录：../project-login
实际目录：../worktrees/project-login
```

这时从主仓库执行 `git worktree list`，可能仍然看到旧路径；从新目录执行 Git 命令，也可能出现找不到主仓库或关联信息过期的问题。

因此，正常搬目录时优先用：

```shell
git worktree move ../project-login ../worktrees/project-login
```

只有已经手动移动过，才进入 `repair` 修复流程。

## 3、手动移动后的 repair

如果已经用 `mv` 或文件管理器移动了 linked worktree，可以用 `repair` 重新建立关联。

在刚移动后的 linked worktree 里执行：

```shell
cd ../worktrees/project-login
git worktree repair
```

或者从任意仍然可用的 Worktree 中，显式传入新路径：

```shell
git worktree repair ../worktrees/project-login
```

# 八、清理与锁定
## 1、remove

开发完成后，用 `remove` 删除 linked worktree：

```shell
git worktree remove ../project-login
```

Git 默认只允许删除干净的 Worktree，也就是没有未跟踪文件、没有已跟踪文件修改。删除前先检查：

```shell
git -C ../project-login status -sb
```

如果还有未提交修改，先决定是提交、转移、丢弃，还是暂时保留该 Worktree。不要把 `git worktree remove -f` 当作日常清理命令。

## 2、prune

如果已经手动删除了 Worktree 目录，Git 内部可能还残留对应记录。先做 dry run：

```shell
git worktree prune --dry-run
```

确认只是清理已经不存在的 Worktree 信息，再执行：

```shell
git worktree prune
```

`prune` 清理的是 `$GIT_DIR/worktrees` 里的管理信息，不是帮你删除某个仍然存在的工作目录。

## 3、lock

如果 linked worktree 放在移动硬盘、网络盘或临时挂载目录上，它可能暂时不可访问，但并不代表应该被清理。可以锁定它：

```shell
git worktree lock --reason "external drive" ../project-login
```

锁定后，Git 不会把它当作可随便清理的失效 Worktree；同时也会阻止移动和删除。

解除锁定：

```shell
git worktree unlock ../project-login
```

锁定适合“目录暂时不在”，不适合掩盖脏工作区或不确定的历史状态。

