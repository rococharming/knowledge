---
title: 更新已打开的 Pull Request
date: 2026-07-29
tags: [GitHub, PullRequest, Git协作, Git推送]
aliases:
  - 更新 PR
  - update pull request
  - PR 追加提交
---

# 一、PR 更新

打开的 Pull Request 不是冻结快照。只要 PR 的来源分支不变，继续往这个分支推新提交，GitHub 上的 PR 就会自动刷新。

核心模型是：

```text
本地 feature 分支产生新提交
push 到 origin/feature 分支
GitHub PR 自动显示新提交和新差异
```

## 1、来源分支

PR 追踪的是 compare，也就是来源分支。以 `feature/pr-practice` 为例，PR 的方向通常是：

```text
base: main
compare: feature/pr-practice
```

只要继续更新 `feature/pr-practice`，这个 PR 就会看到新的 commit 和新的 Files changed。PR 的方向、页面区域和 review 读法见 [[6、PR Review 与检查状态|PR Review 与检查状态]]。

## 2、普通更新

回应 review 的普通小改动，常见做法不是重开 PR，也不是直接改 `main`，而是在同一个 feature 分支上继续提交。

示例场景：

| 反馈 | 更新方式 |
|---|---|
| 补一句说明 | 在 feature 分支修改文件，提交并 push |
| 改一个文件名 | 在 feature 分支提交重命名，push |
| 增加测试 | 在 feature 分支新增测试提交，push |

GitHub 会把这些新提交加入同一个 PR，因为 PR 的来源分支没有变。

# 二、两种更新

“更新 PR”有两种含义，必须分清。一个是回应 review，另一个是同步 base 分支。

## 1、场景区分

| 场景 | 目标 | 常用动作 |
|---|---|---|
| 回应 review | 给当前 PR 增加自己的新改动 | 在 feature 分支提交，然后 `git push` |
| 同步 base | 把 `main` 的新变化带进 PR 分支 | GitHub 的 Update branch，或本地 merge/rebase 后 push |

回应 review 时，改的是来源分支自己的内容；同步 base 时，目标是让 PR 分支包含 `main` 的新变化。后者会牵涉 [[3、Pull 与快进更新|pull]]、merge、rebase 和可能的冲突，风险边界更复杂。

## 2、不要混用

GitHub 页面上的 Update branch 主要解决“PR 分支落后于 base”的问题，不是回应 review 小改动的默认入口。

如果 reviewer 只是要求补一行说明，最清楚的做法是：

```text
在同一个 feature 分支修改 -> commit -> git push
```

这样 PR 的 Conversation、Commits、Files changed 都能保留清晰的时间线。

# 三、普通推送

第一次推送 feature 分支时通常用了 `-u`：

```shell
git push -u origin feature/pr-practice
```

这已经建立了 upstream。后续站在同一个 feature 分支上追加提交后，通常直接运行 `git push` 即可。

## 1、upstream

upstream 关系可以理解为：

```text
本地 feature/pr-practice
跟踪
origin/feature/pr-practice
```

因此本地分支知道默认推到哪个远程分支。可以用：

```shell
git branch -vv
```

确认是否看到类似：

```text
* feature/pr-practice abc1234 [origin/feature/pr-practice] Add pull request practice note
```

方括号里的 `[origin/feature/pr-practice]` 就是这个本地 feature 分支的默认远程对应关系。

## 2、追加提交

普通追加提交流程如下：

```shell
git status -sb
git diff
git add pr-practice-note.md
git commit -m "Update pull request practice note"
git push
```

`git diff` 放在 commit 前，是为了确认本次只包含回应 review 所需的改动，不把无关文件混进 PR。

# 四、页面变化

新提交 push 到来源分支后，PR 页面会自动刷新。它不是新建一个 PR，而是在原 PR 上追加新的历史和新的累计差异。

## 1、变化位置

| 位置 | 推送前 | 推送后 |
|---|---|---|
| Conversation | 已有 PR 创建记录和评论 | 出现新提交推送记录 |
| Commits | 只有第一次提交 | 多出 `Update pull request practice note` |
| Files changed | 第一次提交带来的最终差异 | 显示当前 PR 的累计最终差异 |
| Checks | 可能没有结果，或已有结果 | 有 CI 时通常会基于新提交重新运行 |

Files changed 通常展示的是这个 PR 相对 base 的累计最终差异，不是只展示最后一次提交。也就是说，如果 PR 里有两次提交，Files changed 看的是这两次提交合起来对 `main` 的最终影响。

## 2、Review 影响

追加提交后，reviewer 通常会重新查看差异。某些平台或仓库设置中，新的提交可能让已有 approval 失效，需要重新 review。

所以追加提交前要保持提交范围清楚：一个回应 review 的提交应该只解决对应反馈，避免把新任务混入已有 PR。

# 五、谨慎改写

回应 review 的小改动，普通追加提交最清楚。初学阶段不要把 force push 当成默认动作。

## 1、风险命令

先不要默认使用：

```shell
git push --force
git push --force-with-lease
```

这些命令会改写远程分支历史。虽然 `--force-with-lease` 比 `--force` 多一层保护，但它仍然属于历史改写工具，不是普通 PR 更新流程的默认选择。

## 2、选择原则

| 目标 | 优先方式 |
|---|---|
| 回应 review 的小改动 | 普通新提交 + `git push` |
| 保留清楚审查记录 | 普通追加提交 |
| 整理提交历史 | 等理解团队规则后再考虑 squash、rebase 或 force-with-lease |

普通追加提交的优点是可追踪：reviewer 能看到你针对反馈新增了什么，也能在 Conversation 中追溯变化。

# 六、本地检查

假设本地已经在 `feature/pr-practice`，并且 GitHub 上的 PR 仍然 open。先确认状态：

```shell
cd path/to/practice-repo
git status -sb
```

期待看到：

```text
## feature/pr-practice...origin/feature/pr-practice
```

在 `pr-practice-note.md` 新增一行：

```text
Updated after PR review practice.
```

检查差异：

```shell
git diff
```

差异应类似：

```diff
 Created on a feature branch for pull request practice.
+Updated after PR review practice.
```

确认只新增了这一行后，提交并推送：

```shell
git add pr-practice-note.md
git commit -m "Update pull request practice note"
git push
```

回到 GitHub PR 页面观察：

- Conversation 是否出现新提交记录。
- Commits 是否从一次提交变成两次提交。
- Files changed 是否展示更新后的累计差异。
- Checks 是否重新运行，或仍然没有配置检查。
- PR 仍然 open，暂不合并。

更新已打开 PR 的核心结论是：打开的 PR 会跟着来源分支移动；回应 review 时，在同一个 feature 分支继续提交并普通 push，PR 就会自动更新。
