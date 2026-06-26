---
title: Git 提交
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 提交

`git add` 与 `git commit` 构成 Git 本地操作闭环的核心：先暂存变更，再提交到本地仓库。日常本地操作的固定闭环为 `git status` → `git add` → `git commit` → `git log`。

## Git 管理的文件类型

Git 同时管理文本文件与二进制文件，但最擅长文本文件：

| 文件类型 | 示例 | Git 处理方式 |
|----------|------|--------------|
| 纯文本 | `.txt`、`.md` | 精细的行级 diff |
| 网页相关 | `.html`、`.css`、`.js`、`.json` | 精细的行级 diff |
| 程序源码 | `.c`、`.cpp`、`.rs`、`.java`、`.py` | 精细的行级 diff |
| 配置文件 | `.xml`、`.toml`、`.yaml`、`.ini` | 精细的行级 diff |
| 图片/音视频/可执行文件/库 | `.png`、`.mp4`、`.exe`、`.dll` | 仅能判断是否变化 |

对文本文件，Git 可精确比较哪一行被修改、删除或新增；对二进制文件，Git 最多只能判断文件是否变化、大小是否变化、内容校验值是否变化，无法展示具体改动。

> 项目中若有大量大文件（静态库、视频、设计稿等），通常使用 **Git LFS**（Large File Storage）管理。

## git add：加入暂存区

`git add` 的核心作用不是「添加文件」，而是把工作区的变更加入暂存区。它记录的是执行命令时文件内容的快照，可重复执行，每次都把当前内容重新写入暂存区。

| 用法 | 作用 |
|------|------|
| `git add <file>` | 暂存指定文件 |
| `git add .` | 暂存当前目录及子目录的变更 |

`git add .` 的作用范围随当前目录而定：在仓库根目录处理整个仓库，在子目录只处理该子目录及其子目录。

`git add` 可处理多种变更类型：新增文件、修改文件、删除文件。

## git commit：提交变更

`git commit` 把暂存区内容提交到本地仓库，形成新的提交记录。**它提交的是暂存区内容**，若暂存区为空则不会创建新提交。

### 基本用法

```shell
git commit -m "commit message"
```

`-m` 直接在命令行写提交说明。提交前建议先检查暂存区：

```shell
git status
git diff --staged
```

### 编辑器编写提交信息

不带 `-m` 直接执行 `git commit` 会打开编辑器。默认编辑器取决于配置和环境（vim、nano、VS Code 等）。可配置默认编辑器：

```shell
git config --global core.editor "code --wait"
```

### 多行提交信息

通过多个 `-m` 编写标题与正文：

```shell
git commit -m "add user login page" -m "Create login form and basic validation."
```

两个 `-m` 之间会自动添加空行，结构为「标题 + 空行 + 正文」。较长的提交说明推荐直接用编辑器编写。

## git ls-files：查看已跟踪文件

`git ls-files` 列出 Git 当前已跟踪的文件（已提交的 + 已暂存的），不等同于 `ls`——后者看工作区目录内容，前者看 Git 索引记录。

| 用法 | 作用 |
|------|------|
| `git ls-files` | 列出已跟踪文件 |
| `git ls-files --stage` | 显示底层索引信息（模式、对象哈希、阶段、文件名） |
| `git ls-files --others --exclude-standard` | 列出未跟踪且未被标准忽略规则排除的文件 |

`--stage` 输出中的文件模式含义：

| 模式 | 含义 |
|------|------|
| `100644` | 普通文件，不可执行 |
| `100755` | 普通文件，可执行 |
| `120000` | 符号链接 |
| `160000` | Git 子模块 |

## git log：查看提交历史（基础）

```shell
git log              # 完整历史
git log --oneline    # 每次提交压缩为一行
```

每次提交包含提交哈希、作者、日期和提交说明。提交哈希很长，日常使用只需前几位（如 `ce55c4b`），只要在仓库中能唯一标识即可。`git log` 默认进入分页显示，按 `q` 退出。

更灵活的历史查看见 [[Git 提交历史查看]]。

## 本地操作检查习惯

- 修改前后看 `git status`
- 提交前看 `git diff --staged`

## 相关页面

- [[Git 工作区域]] — add/commit 在三区域模型中的位置
- [[Git 文件状态]] — add 后文件状态的流转
- [[Git 差异对比]] — 提交前用 git diff 检查
- [[Git 提交历史查看]] — git log 的高级用法

## 来源

- [[查看状态、暂存和提交]]
