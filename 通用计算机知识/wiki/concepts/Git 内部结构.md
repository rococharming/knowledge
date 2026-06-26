---
title: Git 内部结构
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 内部结构

`.git` 目录是 Git 仓库的核心，承载工作区、暂存区、本地仓库三个区域在底层的实现。工作区中的普通文件是项目文件，`.git` 中保存的是 Git 管理这些文件所需的数据。

## 目录结构

```shell
ls -l .git
```

| 内容 | 作用 |
|------|------|
| `config` | 当前仓库的本地配置 |
| `HEAD` | 当前检出位置 |
| `hooks/` | Git 钩子脚本目录 |
| `info/` | 当前仓库的本地辅助信息 |
| `objects/` | Git 对象数据库 |
| `refs/` | 分支、标签等引用 |
| `index` | 暂存区的底层文件 |

## index 与暂存区

`.git/index` 是暂存区的底层表现形式。`git add a.txt` 本质上就是把 `a.txt` 当前内容写入 `index`。`git init` 后仓库中可能还没有该文件，首次 `git add` 后才会出现。

## objects/ 与对象类型

`.git/objects/` 是 Git 的对象数据库，保存四类对象：

| 对象 | 说明 |
|------|------|
| `blob` | 文件内容 |
| `tree` | 目录结构 |
| `commit` | 提交对象 |
| `tag` | 标签对象 |

`git commit` 后，Git 会把暂存区内容组织成一次提交，并把相关对象写入 `objects/`。

## HEAD 与检出位置

`.git/HEAD` 表示当前检出位置，常见内容为：

```
ref: refs/heads/main
```

表示当前位于 `main` 分支。若 `HEAD` 直接指向某个提交哈希而非分支引用，则称为 **detached HEAD**（游离 HEAD）状态。

## refs/ 与引用

`.git/refs/` 保存引用，可理解为「用名字指向某个提交」：

| 路径 | 说明 |
|------|------|
| `refs/heads/` | 本地分支 |
| `refs/tags/` | 标签 |
| `refs/remotes/` | 远程跟踪分支 |

例如 `refs/heads/main` 表示本地 `main` 分支指向的提交。

## config 与 hooks

`.git/config` 是当前仓库的本地配置文件，只对当前仓库生效，区别于全局配置 `~/.gitconfig`。

`.git/hooks/` 存放 Git 钩子脚本（如 `pre-commit`、`commit-msg`、`pre-push`）。默认的 `.sample` 文件只是模板，不会自动生效；启用需去掉 `.sample` 后缀，并在 macOS/Linux 上添加可执行权限。

## info/exclude

`.git/info/exclude` 作用类似 `.gitignore`，也可忽略文件，区别是它只对当前本地仓库生效，通常不提交到远程。详见 [[Gitignore]]。

## 相关页面

- [[Git 工作区域]] — 三个区域的划分对应 .git 中的不同部分
- [[Gitignore]] — .gitignore 与 .git/info/exclude 的差异
- [[Git 提交历史查看]] — 基于对象与引用查看历史

## 来源

- [[工作区域与文件状态]]
