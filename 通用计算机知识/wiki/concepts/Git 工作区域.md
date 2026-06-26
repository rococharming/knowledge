---
title: Git 工作区域
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 工作区域

Git 本地仓库有三个核心区域，构成了本地提交的数据流模型：

```
工作区 ──git add──▶ 暂存区 ──git commit──▶ 本地仓库
```

| 区域 | 英文 | 作用 |
|------|------|------|
| 工作区 | Working Tree / Working Directory | 实际编辑文件的项目目录 |
| 暂存区 | Staging Area / Index | 保存下一次提交要包含的内容 |
| 本地仓库 | Local Repository | 保存已提交的历史记录 |

文件修改首先发生在工作区，`git add` 后进入暂存区，`git commit` 后生成提交保存到本地仓库。

## 工作区（Working Tree）

工作区即平时直接看到和编辑的项目目录。除 `.git` 目录外，项目中的普通文件和目录都属于工作区：

```
learngit/
  ├── .git/
  ├── README.md
  ├── src/
  └── Cargo.toml
```

工作区中可进行新建、修改、删除、移动、重命名等操作，这些变化会被 Git 检测到，但不会自动进入版本历史。

## 暂存区（Staging Area / Index）

暂存区是 Git 在提交前收集变更的区域，可理解为「下一次 commit 要提交的内容」。

```shell
git add a.txt
```

**关键理解**：`git add` 记录的是执行该命令时文件内容的**快照**，而非「文件名要提交」的标记。`git add` 后若继续修改该文件，暂存区保存的仍是之前那一版内容，新修改停留在工作区。

暂存区底层由 `.git/index` 管理，`git init` 后首次 `git add` 才会生成该文件。

## 本地仓库（Local Repository）

本地仓库是 Git 真正保存历史记录的地方：

```shell
git commit -m "add a.txt"
```

数据保存在 `.git` 目录中，包括提交历史、分支引用、标签引用、对象数据和仓库配置。

## 提交流程要点

`git commit` 提交的是**暂存区**中的内容，不是工作区中的所有内容。同步到远程仓库才使用 `git push`，它属于远程操作，不属于本地提交核心流程。

## 相关页面

- [[Git 文件状态]] — 文件在工作区与暂存区之间的状态流转
- [[Git 内部结构]] — `.git` 目录如何承载三个区域
- [[Git 提交]] — add/commit 的具体用法

## 来源

- [[工作区域与文件状态]]
