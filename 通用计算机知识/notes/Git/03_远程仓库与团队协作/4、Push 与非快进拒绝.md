---
title: Push 与非快进拒绝
date: 2026-07-28
tags: [Git, Git远程仓库, Git协作, Git推送]
aliases:
  - git push
  - non-fast-forward
  - non-fast-forward rejection
---

# 一、Push

`git push` 的方向是从本地到远程：把本地已有提交发送到 GitHub，并尝试移动远程分支。最常见的形式是把本地 `main` 推到 `origin` 上的 `main`：

```shell
git push origin main
```

push 的安全边界是：远程分支只能在不丢历史的前提下向前移动。如果远程已经有本地没有的提交，直接 push 会被拒绝。

## 1、方向关系

| 名字 | 含义 |
|---|---|
| 本地 `main` | 当前仓库里的本地分支 |
| `origin/main` | 本地记录的远程 `main` 状态 |
| GitHub `main` | GitHub 仓库里的真实远程分支 |

`push` 会尝试让 GitHub `main` 接收本地 `main` 的提交。远程地址和 `origin/main` 的基础模型见 [[1、远程仓库与第一次推送|远程仓库与第一次推送]]。

## 2、领先状态

当本地有远程还没有的提交时，`git status -sb` 可能显示：

```text
## main...origin/main [ahead 1]
```

含义如下：

| 片段 | 说明 |
|---|---|
| `main...origin/main` | 本地 `main` 跟踪 `origin/main` |
| `ahead 1` | 本地 `main` 比 `origin/main` 多 1 个提交 |

`ahead` 不等于已经发布。它只表示本地领先远程跟踪分支，这些提交还没有到 GitHub 上。

# 二、正常推送

当本地 `main` 只是领先远程，没有分叉时，push 通常会成功。这个过程本质上是远程分支的 fast-forward：GitHub `main` 从旧提交移动到新提交。

## 1、推送输出

示例：

```shell
git push origin main
```

可能看到：

```text
To github.com:YOUR-USER/git-practice-remote.git
   b83d231..c71a120  main -> main
```

最后一行表示：GitHub 上的 `main` 从 `b83d231` 移动到了 `c71a120`。这不会丢历史，因为新提交是在旧提交后面继续前进。

## 2、发布判断

push 成功后再看状态：

```shell
git status -sb
```

如果本地和远程重新对齐，通常会看到：

```text
## main...origin/main
```

此时不再显示 `[ahead 1]`，说明本地新增提交已经发布到远程。

# 三、拒绝原因

non-fast-forward 拒绝是远程仓库对历史的保护。它不是网络错误，也不是认证失败，而是 GitHub 发现“直接接受这次 push 会覆盖远程已有提交”。

## 1、分叉形状

典型分叉如下：

```text
local main:    A -- B -- L
                    \
GitHub main:          R
```

本地有提交 `L`，GitHub 有提交 `R`。如果此时直接 push，本质上是在要求 GitHub 把 `R` 替换成 `L`，这会让远程已有提交失去位置。

## 2、拒绝输出

运行：

```shell
git push origin main
```

可能看到：

```text
To github.com:YOUR-USER/git-practice-remote.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'github.com:YOUR-USER/git-practice-remote.git'
hint: Updates were rejected because the remote contains work that you do not have locally.
```

关键短语是 `non-fast-forward` 和 `remote contains work that you do not have locally`。它们说明远程有本地还没整合的提交。

# 四、修复路径

被拒绝后，优先做的是拿回远程状态、读清历史图，再把远程已有提交整合进本地。整合完成后，再 push 整合后的历史。

## 1、推荐顺序

```shell
git fetch origin
git log --oneline --decorate --graph --all --max-count=10
git merge origin/main
git push origin main
```

每一步的目的如下：

| 步骤 | 目的 |
|---|---|
| `git fetch origin` | 先拿回 GitHub 的新状态，更新 `origin/main` |
| `git log --graph --all` | 看清本地和远程怎么分叉 |
| `git merge origin/main` | 把远程已有提交整合进本地 `main` |
| `git push origin main` | 把整合后的历史推到 GitHub |

这里的 fetch 只是观察远程新状态，机制见 [[2、Fetch 与远程跟踪分支|Fetch 与远程跟踪分支]]；整合时可能出现 fast-forward，也可能产生 merge commit，取决于本地和远程历史形状。

## 2、不同文件

如果本地提交和远程提交改的是不同文件，`git merge origin/main` 通常可以自动合并。例如远程新增 `github-diverge-note.md`，本地新增 `local-diverge-note.md`，Git 可以把两个文件都保留下来。

自动合并成功后再 push，远程会收到一个包含两边历史的新结果。这个结果不覆盖远程已有提交，而是把远程提交也纳入本地历史后再向前发布。

# 五、谨慎 Force

`git push --force` 会强行改写远程分支。它能绕过 non-fast-forward 拒绝，但代价是远程历史会被本地历史替换。

## 1、风险

force push 可能让别人已经基于远程提交做的工作失去位置。对共享分支，尤其是 `main`、`master`、`develop` 这类公共分支，默认不要 force push。

> [!warning] 遇到 non-fast-forward 拒绝时，不要把 `--force` 当作修复捷径。先 fetch、看图、整合，再 push。

## 2、判断边界

| 情况 | 推荐动作 |
|---|---|
| 普通协作分支被拒绝 | `fetch`、看图、整合、再 push |
| 公共主分支被拒绝 | 停下来确认远程新提交来源 |
| 自己的临时分支且确认无人依赖 | 才考虑受控改写历史 |

后续理解团队分支和 Pull Request 后，再讨论更安全的 `--force-with-lease` 等做法会更合适。

# 六、本地检查

完成 pull 快进更新并保持 `main` 与 `origin/main` 对齐后，可以先练一次正常 push，再制造一次 non-fast-forward 拒绝。

## 1、正常 push

在本地新建 `local-push-note.md`，写入：

```text
Created locally for push practice.
```

提交并推送：

```shell
cd path/to/practice-repo
git add local-push-note.md
git commit -m "Add local push practice note"
git status -sb
git push origin main
git status -sb
```

重点观察：提交后应出现 `[ahead 1]`；push 成功后，本地 `main` 与 `origin/main` 重新对齐。

## 2、拒绝修复

在 GitHub 网页新建 `github-diverge-note.md`，写入：

```text
Created on GitHub before local push.
```

提交到 GitHub 的 `main`。随后在本地新建 `local-diverge-note.md`，写入：

```text
Created locally after GitHub changed.
```

提交并尝试 push：

```shell
git add local-diverge-note.md
git commit -m "Add local diverge practice note"
git push origin main
```

预期会被 non-fast-forward 拒绝。然后按下面顺序修复：

```shell
git fetch origin
git log --oneline --decorate --graph --all --max-count=10
git merge origin/main
git push origin main
git status -sb
```

最终应能解释三件事：`ahead` 表示本地提交尚未发布；non-fast-forward 拒绝保护远程已有提交；修复路径是先 fetch、看图、整合，再 push。
