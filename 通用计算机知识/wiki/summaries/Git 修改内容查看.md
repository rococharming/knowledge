---
title: Git 修改内容查看
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 修改内容查看

本文介绍如何在 [[Git]] 中查看修改的具体内容——从 `git status` 只知「文件变了」到用 `git diff`、`git show` 看清「具体改了什么」。

## 核心内容

### 提交前检查流程

```shell
git status → git diff → git diff --staged → git commit
```

### git diff 的三种比较范围

| 命令 | 比较范围 |
|------|----------|
| `git diff` | 工作区 vs 暂存区（未暂存修改） |
| `git diff --staged` | 暂存区 vs 最近一次提交（准备提交的修改） |
| `git diff HEAD` | 工作区 + 暂存区 vs HEAD（所有未提交修改） |

`--stat` 可只看文件级修改摘要。详见 [[Git 差异对比]]。

### diff 输出格式

`@@ -1 +1,2 @@` 表示旧版本第 1 行起显示 1 行、新版本第 1 行起显示 2 行；`+` 为新增、`-` 为删除。`--` 用于分隔参数与文件路径，避免文件名与分支名/参数名混淆。

### HEAD 的含义

`HEAD` 表示当前所在位置，日常可理解为当前分支最新提交；`HEAD~1`、`HEAD~2` 表示向前若干次提交。可用 `git diff HEAD~1 HEAD` 比较两次提交。

### git show

查看某次提交的详细信息与具体改动（`git log` + `git diff` 的结合），支持 `--stat`、指定文件、提交哈希。详见 [[Git 差异对比]]。

## 来源

- [[查看修改内容]]
