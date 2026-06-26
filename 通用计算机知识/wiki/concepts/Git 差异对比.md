---
title: Git 差异对比
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 差异对比

`git diff` 系列命令比较不同区域、不同提交之间的差异，是提交前检查修改内容的核心工具。`git show` 则查看某次提交的详细改动。

## 提交前检查习惯

提交前推荐固定流程：

```shell
git status          # 哪些文件发生变化
git diff            # 工作区未暂存的修改
git diff --staged   # 暂存区准备提交的修改
git commit          # 确认无误后提交
```

## git diff 的比较范围

`git status` 只显示文件是否变化，不显示具体改动内容。`git diff` 按比较范围分三种：

| 命令 | 比较范围 | 主要用途 |
|------|----------|----------|
| `git diff` | 工作区 vs 暂存区 | 查看还没有暂存的修改 |
| `git diff --staged` | 暂存区 vs 最近一次提交 | 查看准备提交的修改 |
| `git diff HEAD` | 工作区 + 暂存区 vs HEAD | 查看当前所有未提交修改 |

`git diff --staged` 与 `git diff --cached` 等价。

## diff 输出格式

```
diff --git a/c.txt b/c.txt
index ce01362..5e073a9 100644
--- a/c.txt
+++ b/c.txt
@@ -1 +1,2 @@
hello
+new line
```

| 内容 | 含义 |
|------|------|
| `diff --git a/c.txt b/c.txt` | Git 正在比较 `c.txt` 的两个版本 |
| `index ce01362..5e073a9 100644` | 文件内容对象哈希变化，文件模式 `100644` |
| `--- a/c.txt` / `+++ b/c.txt` | 旧版本 / 新版本 |
| `@@ -1 +1,2 @@` | 变更块行号范围 |
| `+` / `-` | 新增 / 删除的行 |

`@@ -1 +1,2 @@` 中 `-1` 表示旧版本从第 1 行开始显示 1 行，`+1,2` 表示新版本从第 1 行开始显示 2 行。

指定单个文件的未暂存修改：

```shell
git diff -- c.txt   # -- 明确分隔参数与文件路径
```

`--` 用于避免文件名与分支名、参数名混淆。

> `git diff` 主要适合文本文件；图片、压缩包、音视频等二进制文件只能告知文件发生了变化，无法展示具体改动。

## HEAD 的含义

`HEAD` 表示当前所在位置，日常场景可理解为「当前分支上的最新一次提交」。

| 写法 | 含义 |
|------|------|
| `HEAD` | 当前所在的提交 |
| `HEAD~1` | 当前提交的上一次提交 |
| `HEAD~2` | 当前提交的上上一次提交 |

## 比较两次提交

```shell
git diff HEAD~1 HEAD          # 上一次提交到当前提交
git diff 6b3ef19 5714062      # 用提交哈希比较
```

## 修改摘要 --stat

只想快速知道哪些文件改了、各改多少行，用 `--stat`：

```shell
git diff --stat              # 未暂存修改摘要
git diff --staged --stat     # 已暂存修改摘要
git diff HEAD --stat         # 全部未提交修改摘要
```

输出 `c.txt | 1 +` 表示 `c.txt` 有 1 行变化且为新增。

## git show：查看某次提交

`git show` 查看某次提交的提交信息和具体改动，可理解为 `git log` + `git diff` 的结合。

```shell
git show HEAD                # 最新提交的详情与 diff
git show --stat HEAD         # 只看提交摘要
git show HEAD -- c.txt       # 某次提交中某文件的变化
git show 64829c9             # 指定提交哈希
```

## 相关页面

- [[Git 提交]] — 提交前用 git diff --staged 检查
- [[Git 工作区域]] — 三种 diff 对应的区域关系
- [[Git 提交历史查看]] — git log -p / git show 查看历史改动
- [[Git 文件状态]] — 工作区与暂存区的双重修改

## 来源

- [[查看修改内容]]
