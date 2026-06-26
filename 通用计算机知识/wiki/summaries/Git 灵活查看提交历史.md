---
title: Git 灵活查看提交历史
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 灵活查看提交历史

本文介绍 [[Git]] 中提交变多之后，如何按需灵活回头查看历史：限制条数、查看影响文件、查看具体改动、追踪单文件历史、定位某行作者。

## 核心内容

### 限制条数与影响文件

| 需求 | 命令 |
|------|------|
| 只看最近 N 次 | `git log --oneline -3` |
| 查看每次提交改了哪些文件（文件级统计） | `git log --stat` |
| 查看每次提交具体改了什么（逐行 diff） | `git log -p` |

`--stat` 只显示文件级统计，`-p` 显示完整 diff（与 [[Git 差异对比]] 格式一致）。

详见 [[Git 提交历史查看]]。

### 单文件历史与重命名追踪

- `git log --oneline -- a.txt`：用 `--` 分隔参数与文件路径，只看某文件的提交。
- `git log -p -- a.txt`：看每次提交对该文件的具体改动。
- `git log --follow -- b.txt`：文件被重命名后，尝试沿重命名前后追踪历史（仅适合单文件）。

### 查看单次提交详情

`git show` 聚焦单次提交（区别于 `git log` 列多条）：

```shell
git show HEAD            # 最新提交
git show 64829c9         # 指定哈希
git show --stat HEAD     # 仅统计
git show HEAD -- a.txt   # 某次提交中某文件的变化
```

### 定位某行的最后修改者

`git blame` 显示文件每一行最后一次由哪次提交修改，可用 `-L 1,5` 限定行号范围。看到提交哈希后再用 `git show <commit>` 查看具体改动。

## 来源

- [[灵活查看提交历史]]
