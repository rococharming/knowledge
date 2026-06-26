---
title: Git 文件状态
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 文件状态

Git 中文件状态分为两大类：**Untracked**（未跟踪）与 **Tracked**（已跟踪）。已跟踪文件进一步细分四种状态，随工作区与暂存区的操作流转。

## 状态分类

| 状态 | 含义 |
|------|------|
| `Untracked` | 未跟踪，文件尚未被 Git 纳入管理 |
| `Unmodified` | 已跟踪，内容与最近一次提交一致 |
| `Modified` | 已跟踪，但工作区内容发生了修改 |
| `Staged` | 修改已加入暂存区，等待提交 |

## 状态流转

```
新建文件
  │
  ▼
Untracked ──git add──▶ Staged ──git commit──▶ Unmodified
                                                  │
                                              修改文件
                                                  ▼
                       Staged ◀──git add─── Modified
```

## 各状态说明

- **Untracked**：新建文件后未执行过 `git add`，只存在于工作区，Git 尚未将其纳入版本控制。
- **Staged**：`git add` 后文件进入暂存区，此时已成为已跟踪文件——即使还没提交，也不再是 `Untracked`。
- **Modified**：已跟踪文件在工作区被再次修改。此时该文件可能同时存在两份变化：暂存区一版、工作区新修改一版。
- **Unmodified**：暂存区内容被提交后，工作区没有新修改，文件回到未修改状态。

## 同一文件的双重状态

`git add` 后继续修改同一文件时，`git status` 会同时显示两个区域的变化：

| 输出区域 | 含义 |
|----------|------|
| `Changes to be committed` | 暂存区中已有一版内容 |
| `Changes not staged for commit` | 工作区又产生了新修改 |

此时直接 `git commit` 提交的是暂存区那一版，不包含工作区后续修改。要让最新修改进入本次提交，需再次 `git add`。`git add` 可重复执行，每次都会把文件当前内容重新写入暂存区。

## 相关页面

- [[Git 工作区域]] — 工作区、暂存区、本地仓库的划分
- [[Git 差异对比]] — 用 git diff 查看不同区域间的修改
- [[Git 撤销操作]] — 在不同状态间撤销修改

## 来源

- [[工作区域与文件状态]]
