---
title: Git 文件删除与重命名
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 文件删除与重命名

Git 中删除和重命名文件都有「系统命令」与「Git 命令」两种方式：`rm`/`mv` 只操作工作区，需后续 `git add`；`git rm`/`git mv` 同时操作工作区并自动加入暂存区。

## 两种方式对比

| 命令 | 作用 |
|------|------|
| `rm` / `mv` | 只操作工作区，后面还需 `git add` |
| `git rm` / `git mv` | 操作工作区，并自动把变化加入暂存区 |

## 删除文件

### rm 删除

`rm` 是操作系统命令。删除已跟踪文件后，`git status -s` 显示 ` D e.txt`（`D` 在第二列，表示工作区删除但未暂存）。需 `git add e.txt` 把删除记录加入暂存区，之后变为 `D  e.txt`。

```
rm e.txt        →  只是删除工作区文件
git add e.txt   →  把删除记录加入暂存区
git commit      →  提交删除记录
```

### git rm 删除

`git rm` 同时删除工作区文件并把删除记录加入暂存区，等价于 `rm e.txt && git add e.txt`。

```shell
git rm e.txt
```

注意事项：

1. `git rm` 只能删除已被 Git 跟踪的文件。
2. 文件有未提交修改时，Git 可能拒绝删除以防误删。
3. 只想让 Git 不再跟踪、但保留工作区文件，用 `git rm --cached <file>`。

`git rm --cached` 把文件从 Git 跟踪中移出但不删除工作区文件，常配合 [[Gitignore]] 使用。

### 恢复误删文件

| 误删方式 | 恢复步骤 |
|----------|----------|
| `rm` 删除（未暂存） | `git restore e.txt` 直接恢复 |
| `git rm` 删除（已暂存） | 先 `git restore --staged e.txt` 取消暂存，再 `git restore e.txt` 恢复 |

## 重命名文件

### mv 重命名

`mv` 是操作系统命令。重命名后 Git 识别为两个操作：删除旧文件 + 新增未跟踪文件：

```
 D f.txt       # 工作区删除原 f.txt
?? e.txt       # 工作区出现新未跟踪文件
```

`git add f.txt e.txt` 暂存后，Git 识别为重命名 `renamed: f.txt -> e.txt`，简洁状态显示 `R  f.txt -> e.txt`。

> Git 本质上不保存「重命名动作」，而是在比较内容时推断新文件很像旧文件改名而来。若改名同时内容大幅修改，Git 可能识别为删除旧文件 + 增加新文件。

### git mv 重命名

`git mv` 同时完成工作区重命名和暂存，等价于 `mv f.txt e.txt && git add f.txt e.txt`：

```shell
git mv f.txt e.txt
```

执行后状态显示 `R  f.txt -> e.txt`。

### 恢复 mv 重命名

| 状态 | 恢复步骤 |
|------|----------|
| 未暂存 | 直接 `mv e.txt f.txt` 改回 |
| 已暂存 | `git restore --staged f.txt e.txt` → `rm e.txt` → `git restore f.txt` |

## 相关页面

- [[Git 提交]] — 删除/重命名需经 add/commit 进入历史
- [[Git 文件状态]] — D / R 状态码的含义
- [[Git 撤销操作]] — 误删/误重命名的恢复
- [[Gitignore]] — git rm --cached 配合忽略规则

## 来源

- [[删除和重命名文件]]
