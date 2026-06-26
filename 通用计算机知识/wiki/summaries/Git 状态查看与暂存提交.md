---
title: Git 状态查看与暂存提交
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 状态查看与暂存提交

本文围绕 [[Git]] 本地操作的基本闭环——查看状态、加入暂存区、提交到本地仓库、查看历史——介绍 `git status`、`git add`、`git commit`、`git ls-files`、`git log` 的日常用法。

## 核心内容

### 本地操作闭环

```
查看状态 ──▶ 加入暂存区 ──▶ 提交本地仓库 ──▶ 查看历史
git status    git add         git commit        git log
```

### 管理的文件类型

[[Git]] 最擅长文本文件（可做行级 diff），二进制文件只能判断是否变化。大文件场景可考虑 Git LFS。详见 [[Git 提交]]。

### git status

`git status` 展示当前分支、工作区变化、暂存区变化、未跟踪文件和操作提示。简洁模式 `git status -s` 输出 `XY 文件名` 格式，`X` 为暂存区相对本地仓库的状态，`Y` 为工作区相对暂存区的状态。

| 输出 | 含义 |
|------|------|
| `?? b.txt` | 未跟踪文件 |
| `A  a.txt` | 新文件已暂存 |
| ` M a.txt` | 已跟踪，工作区有修改未暂存 |
| `M  a.txt` | 修改已暂存 |
| `MM a.txt` | 部分修改已暂存，暂存后工作区又修改 |

### git add / git commit

`git add` 把工作区变更（新增/修改/删除）以快照形式加入暂存区，可重复执行。`git commit -m` 提交暂存区内容；不带 `-m` 则打开编辑器；多个 `-m` 可写标题与正文。详见 [[Git 提交]]。

### git ls-files

查看 Git 已跟踪文件、暂存区索引信息、未跟踪且未被忽略的文件，文件模式（如 `100644`）标识文件类型与权限。详见 [[Git 提交]]。

### git log（基础）

`git log` 查看完整历史，`git log --oneline` 压缩为一行。提交哈希日常只需前几位。灵活查看见 [[Git 提交历史查看]]。

### 检查习惯

修改前后看 `git status`，提交前看 `git diff --staged`。

## 来源

- [[查看状态、暂存和提交]]
