---
title: Git 撤销与取消暂存
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 撤销与取消暂存

本文介绍 [[Git]] 中如何撤销本地修改——区分工作区与暂存区，区分保留与丢弃文件内容，使用 `git restore` 完成取消暂存和丢弃修改。

## 核心内容

### 撤销前的两个判断

| 问题 | 说明 |
|------|------|
| 撤销哪里 | 工作区，还是暂存区 |
| 是否保留文件内容 | 保留已写的内容，还是直接丢弃修改 |

### 两个核心命令

| 命令 | 作用 |
|------|------|
| `git restore --staged <file>` | 取消暂存，保留工作区内容 |
| `git restore <file>` | 丢弃工作区未暂存修改 |

详见 [[Git 撤销操作]]。

### MM 状态的分别撤销

`git status -s` 显示 `MM` 时，同一文件暂存区和工作区各有一部分修改，可分别用 `git restore` 丢弃工作区修改、`git restore --staged` 取消暂存。

### 注意事项

- 未跟踪文件无法用 `git restore` 废弃，需直接 `rm`。
- `git restore` 丢弃工作区修改不可逆，执行前建议 `git diff <file>` 确认。

## 来源

- [[撤销修改和取消暂存]]
