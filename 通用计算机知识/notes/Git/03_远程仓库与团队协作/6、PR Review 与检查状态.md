---
title: PR Review 与检查状态
date: 2026-07-29
tags: [GitHub, PullRequest, Git协作, CodeReview]
aliases:
  - PR Review
  - Pull Request Review
  - Files changed
---

# 一、PR Review

PR Review 是在 GitHub 上围绕一组分支差异做判断：这次改动是否符合目标，风险是否可接受，是否还有必须处理的问题，现在能不能合并。

它不是本地 Git 命令，也不是简单地点一下 approve。Review 的价值是把判断过程留在 PR 页面上，方便作者、reviewer 和后来的维护者追踪。

## 1、判断顺序

一个稳定的 review 顺序是：

```text
先读 PR 方向
再读 Files changed
再看评论与 Checks
最后给出 review 判断
```

这套顺序建立在 [[5、功能分支与 Pull Request|功能分支与 Pull Request]] 的模型上：PR 是从 compare 分支请求合入 base 分支的协作对象。

## 2、核心问题

Review 时不要只问“代码有没有红绿行”，而要问：

- 这次改动是否服务同一个目标？
- 文件差异是否符合 PR 标题和描述？
- 有没有无关改动混进来？
- 有没有影响其他文件、流程或协作者？
- 自动检查和人工讨论是否还有阻塞？

# 二、PR 页面

PR 页面把讨论、提交、文件差异、自动检查和合并状态放在同一个地方。读懂这个页面，比记住某个按钮更重要。

![[assets/github-pr-review-open-merge-ready.png|700]]

这张截图展示了一个打开中的 PR：状态是 `Open`；方向是从 `feature/pr-practice` 合进 `main`；页面上有 Conversation、Commits、Checks、Files changed 四个关键入口；合并区域显示 `No conflicts with base branch`，说明 GitHub 判断当前可以自动合并，并展示了 `Merge pull request` 按钮。

## 1、关键区域

| 区域 | 作用 | 重点 |
|---|---|---|
| base / compare | 表示 PR 方向 | 通常是 `base: main`，`compare: feature/pr-practice` |
| Conversation | 讨论时间线 | 标题、描述、评论、review 结论 |
| Commits | PR 包含的提交 | 是否集中在一个任务 |
| Files changed | 最终文件差异 | review 的核心入口 |
| Checks | 自动检查结果 | 测试、构建、格式检查等是否通过 |
| merge box | 合并状态 | 是否有冲突、是否允许合并 |

方向仍然最重要：

```text
base: main
compare: feature/pr-practice
```

意思是：请求把 `feature/pr-practice` 合进 `main`。如果方向选反，Files changed 里看到的差异含义也会反。

## 2、合并状态

截图里的 `No conflicts with base branch` 表示 GitHub 当前没有发现和目标分支的文本冲突，因此可以自动执行合并。它只说明“能合并”，不等于“应该合并”。

是否应该合并，还要结合 Files changed、评论、Review 结论和 Checks 状态判断。`Merge pull request` 按钮出现时，仍然要先确认改动内容和流程要求。

# 三、Review 结论

GitHub 的 Review 结论通常分三类：Comment、Approve、Request changes。它们表达的是 reviewer 对这次 PR 的判断，而不是本地 Git 历史本身。

## 1、三种结果

| 结论 | 含义 | 使用场景 |
|---|---|---|
| Comment | 留下反馈，不明确批准或阻止 | 一般问题、建议、学习记录 |
| Approve | 认为改动可以合并 | 已读完 diff，风险可接受 |
| Request changes | 要求作者先修改再合并 | 发现必须处理的问题 |

作者自己的 approve 通常不会算作有效批准。真实团队里，review 的价值来自另一个人独立看过。

## 2、评论位置

评论可以放在 Conversation，也可以放在 Files changed 的具体行上：

| 评论位置 | 适合内容 |
|---|---|
| Conversation | 总体反馈、结论、问题汇总 |
| Files changed 行评论 | 针对某一行代码或某个文件差异的问题 |

如果问题和具体文件行强相关，优先在 Files changed 里对行评论。这样作者能直接看到反馈对应哪处改动。

# 四、Files changed

Files changed 是 review 的核心入口。Conversation 告诉你别人怎么说，Files changed 才告诉你最终会合进目标分支的实际变化。

## 1、阅读顺序

推荐顺序：

1. 先读 PR 标题和描述，理解作者声称要做什么。
2. 打开 Files changed，看实际改了什么。
3. 判断新增、删除、修改是否都服务同一个任务。
4. 对不理解或有风险的行留言。
5. 回到 Conversation，确认讨论是否已经解决。
6. 查看 Checks 和 merge box，判断是否还有合并阻塞。

读 diff 时，重点不是红绿行数量，而是每一处变化是否有合理意图。

## 2、风险问题

读 Files changed 时可以反复问：

| 问题 | 目的 |
|---|---|
| 这行变化为什么需要 | 判断改动意图 |
| 有没有影响其他文件 | 判断联动风险 |
| 有没有缺少测试或说明 | 判断验证缺口 |
| 有没有无关改动 | 控制 PR 范围 |
| 是否符合 PR 标题 | 防止内容和目标不一致 |

对于学习仓库，Files changed 可能只有一个小文件；但这个习惯会迁移到真实项目里的大 PR。

# 五、Checks

Checks 是 GitHub 页面上展示的自动检查结果，常见来源包括测试、构建、格式检查和安全扫描。

## 1、状态来源

如果仓库没有配置 CI，PR 页面可能没有 Checks 结果。这不表示 Git 或 GitHub 出错，只说明这个仓库还没有自动检查流程。

人工 review 和自动 Checks 是两类判断：

| 类型 | 能发现什么 | 不能替代什么 |
|---|---|---|
| 人工 review | 意图、设计、可读性、风险边界 | 不能稳定跑遍所有测试 |
| 自动 Checks | 测试失败、构建失败、格式问题 | 不能理解业务意图 |

Checks 通过，不代表代码一定好；Checks 缺失，也不代表 PR 一定不能合并。它们只是合并判断的一部分。

## 2、合并阻塞

合并前至少确认三类状态：

| 状态 | 说明 |
|---|---|
| diff 已读 | Files changed 中的改动符合目标 |
| 讨论已处理 | Conversation 和行评论没有未解决关键问题 |
| 检查状态可接受 | Checks 通过，或确认仓库没有配置自动检查 |

如果 merge box 显示有冲突，合并按钮通常会被阻塞，需要先更新 feature 分支或解决冲突。

# 六、本地检查

Review 主要发生在 GitHub 页面，本地只需要确认当前分支和 upstream 状态。

示例：

```shell
git status -sb
git branch -vv
```

可能看到：

```text
## feature/pr-practice...origin/feature/pr-practice
* feature/pr-practice abc1234 [origin/feature/pr-practice] Add pull request practice note
  main                def5678 [origin/main] Complete remote practice
```

重点观察：

- PR 仍然是 open。
- base 是 `main`。
- compare 是 `feature/pr-practice`。
- Files changed 能看到 `pr-practice-note.md`。
- Conversation 可以留下普通评论，例如 `Review practice: checked the diff and PR direction.`
- Checks 或 merge box 的状态能解释清楚。

PR Review 的核心结论是：先读懂 diff，再把合并判断和讨论留在 GitHub 页面上；看到可以合并的按钮，也要先确认方向、差异、评论和检查状态。
