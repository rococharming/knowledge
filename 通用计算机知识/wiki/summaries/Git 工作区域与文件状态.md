---
title: Git 工作区域与文件状态
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 工作区域与文件状态

本文梳理 [[Git]] 本地仓库的核心操作模型——文件如何从工作区经暂存区最终进入本地仓库，以及文件在不同区域间流转时的状态变化。

## 核心内容

### 本地提交模型

Git 本地操作的关键在于「暂存区」这个中间区域，而非直接提交：

```
工作区 ──git add──▶ 暂存区 ──git commit──▶ 本地仓库
```

| 命令 | 作用 |
|------|------|
| `git add` | 把工作区文件内容加入暂存区 |
| `git commit` | 把暂存区内容保存为一次提交 |
| `git status` | 查看工作区和暂存区状态 |

详见 [[Git 工作区域]]。

### 三个工作区域

| 区域 | 英文 | 作用 |
|------|------|------|
| 工作区 | Working Tree | 实际编辑的项目目录 |
| 暂存区 | Staging Area / Index | 保存下次提交要包含的内容 |
| 本地仓库 | Local Repository | 保存已提交的历史记录 |

### 文件状态流转

文件状态分为 `Untracked`（未跟踪）与 `Tracked`（已跟踪，含 `Unmodified` / `Modified` / `Staged` 三种），随 `git add` / `git commit` / 修改文件等操作流转。详见 [[Git 文件状态]]。

### .git 目录内部结构

`.git` 目录承载三个区域的底层实现：`index` 对应暂存区，`objects/` 保存四类对象（blob/tree/commit/tag），`HEAD` 记录检出位置，`refs/` 保存分支与标签引用。详见 [[Git 内部结构]]。

## 来源

- [[工作区域与文件状态]]
