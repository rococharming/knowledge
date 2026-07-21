---
title: Git 本地提交流程
date: 2026-07-22
tags: [git, workflow, commit]
source_count: 1
---

# Git 本地提交流程

Git 的本地提交闭环是：先查看状态，选择要进入暂存区的修改，检查暂存区差异，再把暂存区保存为一次提交。这个流程依赖 [[Git 工作区域与文件状态]] 中的工作区、暂存区和本地仓库模型。

![[Pasted image 20260722014745.png|600]]

这张流程图来自原始素材，用来概括 `git status`、`git add`、`git diff --staged`、`git commit` 和 `git log` 在一次本地开发循环中的位置。

## 1. 查看当前状态

```shell
git status
```

`git status` 先回答当前分支、工作区变化、暂存区变化和未跟踪文件等问题。新建文件通常会出现在 `Untracked files`；执行 `git add` 后，同一文件会进入 `Changes to be committed`。

需要更紧凑的状态视图时使用：

```shell
git status -s
```

简洁状态通常采用 `XY path` 格式，其中 `X` 表示暂存区相对最近一次提交的状态，`Y` 表示工作区相对暂存区的状态。常见组合见 [[Git 工作区域与文件状态#简洁状态码]]。

## 2. 选择要暂存的修改

暂存指定文件：

```shell
git add b.txt
```

暂存当前目录及其子目录范围内的修改：

```shell
git add .
```

`git add` 的本质是把指定路径当前内容写入暂存区，因此它既可处理新增文件，也可处理已跟踪文件的修改和删除。若文件暂存后又继续修改，需要再次执行 `git add`，新的工作区内容才会进入下一次提交。

## 3. 提交前检查暂存区

提交前通常做两层检查：

```shell
git status
git diff --staged
```

| 命令 | 检查重点 |
|---|---|
| `git status` | 哪些路径已经暂存，哪些修改仍留在工作区 |
| `git diff --staged` | 暂存区相对最近一次提交的具体内容差异 |

这个检查步骤可以减少漏提交、误提交和把调试改动带入历史的问题。

## 4. 创建一次提交

```shell
git commit -m "add b.txt"
```

`git commit` 会把暂存区内容保存为一次新提交。提交信息第一行适合说明“做了什么”；需要补充背景或原因时，可以添加正文：

```shell
git commit -m "add user login page" -m "Create login form and basic validation."
```

不带 `-m` 时，Git 会打开默认编辑器编写提交信息；编辑器配置见 [[Git 安装与首次配置]]。

## 5. 查看提交历史

完整历史：

```shell
git log
```

简洁历史：

```shell
git log --oneline
```

日常回看最近几次提交时，常用短历史：

```shell
git log --oneline -5
```

提交哈希很长，日常通常使用前几位短哈希，只要它在当前仓库中能唯一识别即可。

## 6. 查看 Git 当前跟踪的路径

列出 Git 索引中记录的文件：

```shell
git ls-files
```

它不同于普通 `ls`：`ls` 查看工作区目录，`git ls-files` 查看 Git 已经纳入索引的路径，通常包括已经提交过或已经暂存的文件。

查看索引底层信息：

```shell
git ls-files --stage
```

常见文件模式包括：

| 模式 | 含义 |
|---|---|
| `100644` | 普通文件，不可执行 |
| `100755` | 普通文件，可执行 |
| `120000` | 符号链接 |
| `160000` | Git 子模块 |

只列出未跟踪且未被标准忽略规则排除的文件：

```shell
git ls-files --others --exclude-standard
```

其中 `--others` 表示列出不在 Git 索引中的路径，`--exclude-standard` 表示应用 `.gitignore`、`.git/info/exclude` 和全局 ignore 配置。

## 日常闭环

```shell
git status
git add <path>
git diff --staged
git commit -m "message"
git log --oneline -5
```

其中最关键的习惯是：提交前先确认“暂存区里到底是什么”。因为 `git commit` 保存的是暂存区快照，而不是工作区里的全部修改。

## 来源

- [[查看状态、暂存和提交]]
