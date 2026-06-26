---
title: Git 提交历史查看
date: 2026-06-26
tags: [git, version-control]
source_count: 1
---

# Git 提交历史查看

提交变多后，完整的 [[Git 提交|`git log`]] 不便排查问题。本页整理按需查看历史的高级用法：限制条数、查看影响文件、查看具体改动、追踪单文件历史、定位某行作者。

## 只看最近几次提交

用 `-N` 限制条数，常配合 `--oneline`：

```shell
git log --oneline -3      # 最近 3 次
git log --oneline -1      # 最近 1 次
```

```
64829c9 update a.txt
5714062 add b.txt
6b3ef19 add a.txt
```

## 查看提交影响了哪些文件

`--stat` 在提交信息下显示文件级修改统计，但不显示逐行 diff：

```shell
git log --stat
git log --stat -1         # 仅最近一次
```

```
a.txt | 2 ++
1 file changed, 2 insertions(+)
```

| 输出 | 含义 |
|------|------|
| `a.txt \| 2 ++` | `a.txt` 新增 2 行 |
| `1 file changed` | 共改 1 个文件 |
| `2 insertions(+)` | 共新增 2 行 |

## 查看提交的具体修改

`-p`（patch）把每次提交对应的 diff 一起显示，与 [[Git 差异对比|`git diff`]] 的 diff 格式一致：

```shell
git log -p
git log -p -1
```

```diff
+new line
-old line
```

| 标记 | 含义 |
|------|------|
| `+` | 新增内容 |
| `-` | 删除内容 |

`git log -p` 输出可能很长，适合排查具体问题时使用。

## 查看某个文件的历史

用 `-- <file>` 分隔 Git 参数与文件路径，只看与该文件相关的提交：

```shell
git log --oneline -- a.txt     # 只看 a.txt 的提交
git log -p -- a.txt            # 看每次提交对该文件的具体改动
```

### 追踪重命名前后的历史

若文件被重命名（如 `a.txt` → `b.txt`），`--follow` 尝试沿重命名前后继续追踪历史：

```shell
git log --follow -- b.txt
```

> `--follow` 主要用于单个文件路径，不适合一次跟多个文件。重命名推断的原理见 [[Git 文件删除与重命名]]。

## 查看某次提交详情

`git show` 查看单次提交的提交信息与具体改动（与 `git log` 列出多条不同，`show` 聚焦一次）：

```shell
git show HEAD            # 最新提交
git show 64829c9         # 指定哈希
git show --stat HEAD     # 仅统计
git show HEAD -- a.txt   # 仅某次提交中某文件的变化
```

`--` 同样用于分隔提交参数与文件路径。`git show` 与 [[Git 差异对比]] 的查看场景互补：`show` 看某次提交，`diff` 比较两个状态。

## 查看某一行是谁改的

`git blame` 显示文件每一行最后一次由哪次提交修改：

```shell
git blame a.txt
git blame -L 1,5 a.txt   # 仅第 1-5 行
```

输出通常包含提交哈希、作者、时间、行号、当前行内容。看到某行对应的提交哈希后，可用 `git show <commit>` 继续查看该次提交具体改了什么。

## 命令速查

| 需求 | 命令 |
|------|------|
| 只看最近几次提交 | `git log --oneline -3` |
| 查看提交影响了哪些文件 | `git log --stat` |
| 查看提交具体改了什么 | `git log -p` |
| 只看某个文件的提交历史 | `git log --oneline -- a.txt` |
| 追踪文件重命名前后的历史 | `git log --follow -- b.txt` |
| 查看某次提交详情 | `git show HEAD` |
| 查看某次提交中某文件的变化 | `git show HEAD -- a.txt` |
| 查看某一行是谁改的 | `git blame a.txt` |

## 相关页面

- [[Git 提交]] — 基础 `git log` 与提交机制
- [[Git 差异对比]] — `git diff` / `git show` 的 diff 格式解析
- [[Git 文件删除与重命名]] — `--follow` 追踪重命名所依赖的内容推断原理

## 来源

- [[灵活查看提交历史]]
