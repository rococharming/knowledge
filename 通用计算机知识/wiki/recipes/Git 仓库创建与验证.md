---
title: Git 仓库创建与验证
date: 2026-07-22
tags: [git, repository, workflow]
source_count: 2
---

# Git 仓库创建与验证

Git 仓库是纳入 Git 版本控制的项目目录。创建仓库有两种起点：从本地目录初始化，或克隆已有远程仓库。Git 的定位与基础能力见 [[Git 版本控制系统]]；首次安装和身份配置见 [[Git 安装与首次配置]]；提交前的工作区、暂存区和文件状态见 [[Git 工作区域与文件状态]]。

## 1. 从新目录初始化

现代项目通常使用 `main` 作为初始分支。创建目录并初始化：

```shell
mkdir learngit
cd learngit
git init -b main
```

若已经设置 `init.defaultBranch`，也可直接运行 `git init`。初始化会创建 `.git` 元数据目录，但不会自动把工作区文件写入提交历史。

## 2. 将已有项目纳入版本控制

`git init` 不要求目录为空；在已有项目根目录执行它不会删除或改写现有文件。要把当前文件保存为首个提交：

```shell
git init -b main
git add .
git commit -m "initial commit"
```

`git add` 将文件放入暂存区，`git commit` 才会创建快照。提交前应已完成身份配置。

## 3. 克隆已有远程仓库

项目已有远程仓库时，使用 `git clone` 获取工作区与提交历史：

```shell
git clone https://github.com/user/repo.git
cd repo
```

克隆会把来源记录为默认远程别名 `origin`，并检出远程默认分支对应的本地分支。需要指定本地目录名时，在命令末尾追加目标目录：

```shell
git clone https://github.com/user/repo.git my-project
```

检查远程地址：

```shell
git remote -v
```

## 4. 验证仓库状态

在项目目录或其子目录中，确认 Git 识别出的仓库根目录：

```shell
git rev-parse --show-toplevel
```

初始化后，检查当前分支：

```shell
git branch --show-current
```

也可使用 `git status` 查看工作区状态。若当前目录及其父目录均不属于 Git 仓库，Git 会报告不是仓库的错误。

## 5. 理解 `.git` 目录

普通仓库的 `.git` 是内部元数据目录，其中包括：

| 路径或文件 | 用途 |
|---|---|
| `objects/` | 保存对象数据，例如文件内容、目录树和提交 |
| `refs/` | 保存分支、标签与远程跟踪分支等引用 |
| `HEAD` | 记录当前检出位置 |
| `index` | 保存暂存区的底层数据 |
| `config` | 保存当前仓库的本地配置 |
| `hooks/` | 存放 Git 钩子脚本 |
| `info/exclude` | 保存仅对当前仓库有效的本地忽略规则 |

不要删除或手动修改 `.git`：项目文件可能仍在，但提交历史和仓库配置会丢失。对于 linked worktree 或 submodule 等进阶场景，`.git` 可能是指向实际 Git 目录的文件，而非目录。

## 来源

- [[创建 Git 仓库]]
- [[工作区域与文件状态]]
