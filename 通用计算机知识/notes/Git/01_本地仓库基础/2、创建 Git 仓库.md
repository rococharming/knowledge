---
title: 创建 Git 仓库
date: 2026-07-14
tags: [计算机基础, Git, Git基础, git]
aliases:
  - Git 仓库
  - git init
  - git clone
---

# 一、Git 仓库的基本概念

Git 仓库是被 Git 纳入版本控制的项目目录。一个普通目录执行 `git init` 后，会生成隐藏目录 `.git`；正是这个目录保存了提交历史、分支引用、暂存区和仓库配置。

创建仓库通常有两种方式：

| 方式 | 命令 | 适合场景 |
|---|---|---|
| 本地初始化 | `git init` | 从本地目录开始创建新项目 |
| 克隆远程仓库 | `git clone <url>` | 把已有远程仓库复制到本地 |

> Git 不会把目录中的所有文件自动纳入版本控制。文件需要经过 `git add` 和 `git commit`，才会成为提交历史的一部分。

# 二、本地初始化仓库

## 1、创建目录并初始化

```shell
mkdir learngit
cd learngit
git init
```

执行后，Git 会在当前目录创建 `.git`：

```shell
ls -a
```

输出中能看到：

```text
.git
```

`.git` 是仓库的核心目录，一般不要手动修改其中内容。

## 2、在已有目录中初始化

`git init` 不要求目录为空。可以在已有文件的项目目录中执行：

```shell
git init
```

这不会删除原有文件，只会让当前目录具备 Git 仓库能力。已有文件仍需进入暂存区并提交：

```shell
git add .
git commit -m "initial commit"
```

暂存和提交流程见 [[4、查看状态、暂存和提交|查看状态、暂存和提交]]。

# 三、初始分支名称

## 1、设置默认初始分支

较早的 Git 版本或默认配置可能使用 `master` 作为初始分支。现代项目更常使用 `main`。

可以提前设置全局默认分支名：

```shell
git config --global init.defaultBranch main
```

查看配置：

```shell
git config --global init.defaultBranch
```

相关配置见 [[1、Git 安装与配置|Git 安装与配置]]。

## 2、重命名当前分支

如果仓库已经创建，可以把当前分支重命名为 `main`：

```shell
git branch -m main
```

也可以明确指定旧名和新名：

```shell
git branch -m master main
```

如果仓库已经推送到远程，改名还涉及远程分支、上游分支和托管平台默认分支设置，不能只改本地分支名。

# 四、理解 `.git` 目录

## 1、`.git` 保存什么

`.git` 是 Git 仓库的内部数据库。常见内容包括：

| 内容 | 作用 |
|---|---|
| `objects/` | 保存 Git 对象，包括文件内容、目录树、提交等 |
| `refs/` | 保存分支、标签、远程跟踪分支等引用 |
| `HEAD` | 记录当前检出位置 |
| `index` | 暂存区的底层文件 |
| `config` | 当前仓库的本地配置 |
| `hooks/` | Git 钩子脚本目录 |
| `info/exclude` | 当前仓库本地忽略规则 |

删除 `.git` 后，项目文件本身还在，但 Git 历史和仓库身份会丢失。

## 2、Git 会向上查找 `.git`

在仓库子目录中执行 Git 命令时，Git 会从当前目录向上查找 `.git`：

```text
learngit/
  ├── .git/
  └── src/
      └── main.rs
```

即使当前位于 `src/`，执行 `git status` 仍然属于 `learngit` 这个仓库。

# 五、检查仓库状态

## 1、当前目录是 Git 仓库

```shell
git status
```

如果目录已经是仓库，可能看到：

```text
On branch main
No commits yet
nothing to commit
```

这表示仓库已初始化，但可能还没有提交记录。

## 2、当前目录不是 Git 仓库

如果当前目录及其父目录都找不到 `.git`，会看到：

```text
fatal: not a git repository (or any of the parent directories): .git
```

这通常说明还没有执行 `git init`，或者当前路径不在仓库内部。

# 六、克隆远程仓库

## 1、克隆已有仓库

```shell
git clone https://github.com/user/repo.git
cd repo
git status
```

`git clone` 不只是下载项目文件，它还会复制提交历史、分支和标签，并自动设置远程仓库别名 `origin`。

## 2、自定义本地目录名

默认情况下，本地目录名来自远程仓库名：

```shell
git clone https://github.com/user/repo.git
```

如果要指定目录名：

```shell
git clone https://github.com/user/repo.git my-project
```

## 3、查看远程地址

```shell
git remote -v
```

输出通常类似：

```text
origin  https://github.com/user/repo.git (fetch)
origin  https://github.com/user/repo.git (push)
```

`origin` 是克隆来源的默认远程别名。

# 七、小结

`git init` 把本地目录变成仓库，`git clone` 把已有远程仓库复制成本地仓库。理解 `.git` 目录后，后续的工作区、暂存区和提交历史就更容易串起来。

继续阅读 [[3、工作区域与文件状态|工作区域与文件状态]]，可以理解文件从修改到提交之间经历的状态变化。
