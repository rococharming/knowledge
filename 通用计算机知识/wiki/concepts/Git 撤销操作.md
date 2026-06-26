---
title: Git 撤销操作
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 撤销操作

`git restore` 是撤销本地修改的核心命令，分两种用法：取消暂存（保留工作区内容）与丢弃工作区修改。执行撤销前需先判断「撤销哪里」与「是否保留文件内容」。

## 两个核心命令

| 命令 | 作用 |
|------|------|
| `git restore --staged <file>` | 取消暂存，但保留工作区内容 |
| `git restore <file>` | 丢弃工作区中的未暂存修改 |

## git restore --staged：取消暂存

`git add` 后若暂时不想提交该文件、但不想丢掉内容：

```shell
git restore --staged d.txt
```

| 区域 | 结果 |
|------|------|
| 暂存区 | 取消暂存 |
| 工作区 | 文件内容继续保留 |

效果是「暂时不提交，但写过的内容保留」。暂存状态下 `git status -s` 显示 `A  d.txt`，取消暂存后变为 `?? d.txt`（未跟踪状态），说明文件只在工作区保留。

> `git restore --staged` 不会删除文件内容，只是把修改从暂存区拿出来。

## git restore：丢弃工作区修改

`git restore <file>` 把工作区文件恢复到暂存区或最近一次提交的状态，即丢弃当前未暂存的修改。

| 场景 | 处理方式 |
|------|----------|
| 新增未跟踪文件想废弃 | 直接 `rm <file>`（restore 无法处理未跟踪文件） |
| 已跟踪文件工作区修改想丢弃 | `git restore <file>` |

`git restore` 操作需谨慎，执行前建议先 `git diff <file>` 确认修改确实不需要。

## MM 状态下的分别撤销

当 `git status -s` 显示 `MM d.txt`（暂存区有第一次修改、工作区有第二次未暂存修改）时：

| 操作 | 命令 | 结果 |
|------|------|------|
| 只丢弃工作区第二次修改 | `git restore d.txt` | 保留暂存区修改，`MM` → `M ` |
| 只取消暂存第一次修改 | `git restore --staged d.txt` | 保留工作区内容，修改仍在文件里 |

## 常用场景对比

| 场景 | 命令 | 是否保留文件内容 |
|------|------|------------------|
| 已暂存但暂时不想提交 | `git restore --staged d.txt` | 保留 |
| 修改错了，想丢弃未暂存修改 | `git restore d.txt` | 不保留 |
| `MM` 状态只丢弃第二次修改 | `git restore d.txt` | 保留暂存区修改 |
| `MM` 状态只取消暂存 | `git restore --staged d.txt` | 保留工作区内容 |

## 相关页面

- [[Git 文件状态]] — Modified / Staged 状态对应可撤销的修改
- [[Git 工作区域]] — 撤销操作作用于工作区与暂存区
- [[Git 文件删除与重命名]] — 误删文件的恢复也使用 git restore

## 来源

- [[撤销修改和取消暂存]]
