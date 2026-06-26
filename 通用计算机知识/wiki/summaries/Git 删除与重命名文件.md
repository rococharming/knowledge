---
title: Git 删除与重命名文件
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 删除与重命名文件

本文介绍 [[Git]] 中删除文件（`rm` / `git rm`）与重命名文件（`mv` / `git mv`）两种方式的差异、暂存流程及误操作恢复。

## 核心内容

### 两种方式

| 命令 | 作用 |
|------|------|
| `rm` / `mv` | 只操作工作区，需后续 `git add` |
| `git rm` / `git mv` | 操作工作区并自动加入暂存区 |

### 删除文件

- `rm` 删除后状态码 ` D`（未暂存），需 `git add` 把删除记录加入暂存区变为 `D `。
- `git rm` 等价于 `rm` + `git add`，一步完成删除与暂存。
- `git rm --cached <file>` 只移除跟踪、保留工作区文件，配合 [[Gitignore]] 使用。
- 误删恢复：`rm` 误删用 `git restore`；`git rm` 误删先 `git restore --staged` 再 `git restore`。

详见 [[Git 文件删除与重命名]]。

### 重命名文件

- `mv` 重命名后 Git 识别为「删除旧文件 + 新增未跟踪文件」，`git add` 后识别为重命名（状态码 `R`）。
- `git mv` 一步完成重命名与暂存。
- Git 不保存「重命名动作」，而是按内容相似度推断；改名同时大幅改内容可能识别为删除+新增。
- 误重命名可 `mv` 改回或经 `git restore --staged` + `rm` + `git restore` 恢复。

详见 [[Git 文件删除与重命名]]。

## 来源

- [[删除和重命名文件]]
