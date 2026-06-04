---
title: Git 仓库
date: 2026-06-05
tags: [git, repository]
source_count: 1
---

# Git 仓库

Git 仓库（repository，简称 repo）是 Git 管理项目的基本单位。一个普通目录执行 `git init` 后，会生成 `.git` 隐藏目录，该目录即成为仓库。

## 仓库创建

### 本地初始化

在空目录或已有文件的目录中执行：

```shell
git init
```

已有文件不会自动进入版本控制，需要后续执行 `git add` 和 `git commit`。

### 克隆远程仓库

```shell
git clone <远程仓库URL>
```

详见 [[Git 远程仓库]]。

## .git 目录

`.git` 目录保存仓库的所有内部数据：

| 内容 | 说明 |
|------|------|
| 提交对象 | 保存提交历史相关数据 |
| 分支信息 | 保存分支引用 |
| 标签信息 | 保存标签引用 |
| 暂存区信息 | 保存 `git add` 后的索引状态 |
| HEAD | 记录当前所在分支或提交 |
| 仓库配置 | 保存当前仓库的本地配置 |

**不要手动修改 `.git` 目录中的内容**，否则可能导致仓库状态异常。

删除 `.git` 目录后，当前目录退化为普通文件夹，版本历史丢失但项目文件保留。

## 初始分支

执行 `git init` 时 Git 会创建初始分支。早期默认名为 `master`，现在主流使用 `main`。

可通过全局配置预设默认分支：

```shell
git config --global init.defaultBranch main
```

重命名当前分支：

```shell
git branch -m <新名称>
```

若已推送到远程，改名后还需同步远程分支设置。

## 仓库状态检查

### git status

```shell
git status
```

- 在仓库内：显示当前分支、提交状态、未跟踪文件等
- 非仓库：报错 `fatal: not a git repository`

### 向上查找机制

Git 会向上级目录递归查找 `.git`。例如：

```shell
learngit/
  ├── .git/
  └── src/
      └── main.rs
```

即使当前位于 `src/` 子目录，`git status` 也能正常工作，因为 Git 会找到 `learngit/.git`。

## 相关页面

- [[Git]] — Git 版本控制系统概述
- [[Git 配置]] — 仓库级别的本地配置
- [[Gitignore]] — 文件忽略规则
- [[Git 远程仓库]] — 远程仓库的克隆与管理

## 来源

- [[创建Git仓库]]
