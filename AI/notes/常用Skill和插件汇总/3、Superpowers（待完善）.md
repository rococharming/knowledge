
# 一、简介

AI Agent 在处理复杂项目时，如果缺少约束，容易直接进入编码阶段，跳过需求澄清、测试、代码审查和分支隔离，最后产生一个能运行但不稳定、难维护的原型。

`Superpowers`的价值不是提升模型智力，而是把成熟软件工程中的流程约束嵌入 Agent 工作流中。它通过一组可组合的`skills`，强制 Agent 按设计、计划、隔离开发、测试驱动、代码审查和分支收尾的方式完成任务。

简单来说：

>它解决的不是“模型不够聪明”的问题，而是“Agent 缺少工程纪律”的问题。


# 二、安装

`Superpowers` 将一系列技能打包成了插件。

## 1、Claude Code

官方插件市场 `claude-plugins-official` 会在启动 Claude Code 时自动可用。

可以运行 `/plugin` 进入插件管理器：

```text
/plugin
```

在 `Discover` 标签页浏览和安装插件。

或者直接执行：

```
/plugin install superpowers@claude-plugins-official
```

## 2、Codex CLI

`Superpowers` 已经在官方 Codex plugin marketplace 中，可以直接通过插件界面安装：

```text
/plugins
```

搜索：

```text
superpowers
```

选择：

```text
Install Plugin
```


# 三、使用前提

## 1、项目状态

使用 `Superpowers` 前，项目最好满足以下条件：

```shell
git status
```

工作区应尽量保持干净：nothing to commit, working tree clean

项目也应该已经有至少一次 Git 提交：

```shell
git log --oneline -1
```

如果项目只是刚刚 `git init`，但还没有任何提交，后续创建分支、创建 `worktree`、比较变更和最终合并都会变得不稳定。

推荐状态是：

|条件|说明|
|---|---|
|已被 Git 管理|`Superpowers` 的分支隔离、代码审查、最终合并都依赖 Git 状态|
|至少有一次提交|方便创建分支、比较变更、回滚和清理|
|工作区干净|避免 Agent 把你原本未提交的改动和新任务改动混在一起|
|测试基线可通过|避免在原本就失败的项目状态上继续开发|

## 2、团队协作中的启动方式

团队协作项目中，推荐从最新的主干分支启动 `Claude Code`，而不是先手动创建功能分支。

常见流程：

```init
git switch main 
git pull 
git status 
claude
```

然后在 `Claude Code` 会话中提出需求，让 `Superpowers` 自己完成后续的设计、分支隔离和实现流程。

不推荐一开始就手动创建 `feature` 分支再启动 `Claude Code`，除非团队流程明确要求这样做。因为 `Superpowers` 本身就会为任务创建隔离工作区和新分支。如果先手动创建 `feature` 分支，再让 `Superpowers` 创建新的任务分支，容易形成更复杂的分支关系。


# 四、工作原理
## 1、整体机制

`Superpowers` 不是简单的提示词增强，也不是一组零散的操作说明。它更像是一套完整的软件开发工作流。

它通过多个`skills`组织开发过程：

| 阶段      | 使用的 skill                                                                 | 作用                        |
| ------- | ------------------------------------------------------------------------- | ------------------------- |
| 需求澄清与设计 | `superpowers:brainstorming`                                               | 把模糊想法转成明确设计               |
| 工作区隔离   | `superpowers:using-git-worktree`                                          | 创建隔离`worktree`和新分支        |
| 编写实现计划  | `superpowers:writing-plans`                                               | 把设计拆成可执行任务                |
| 执行计划    | `superpowers:subagent-driven-development`或`superpowers:executing-plans` | 按计划完成任务                   |
| 测试驱动开发  | `superpowers:test-driven-development`                                    | 强制执行 `RED-GREEN-REFACTOR` |
| 代码审查    | `superpowers:requesting-code-review`                                     | 按计划审查代码并分类问题              |
| 分支收尾    | `superpowers:finishing-a-development-branch`                              | 测试、合并、PR、保留或丢弃            |
这里的关键词是“强制”。在 `Superpowers` 中，`skills` 不是给 Agent 参考的建议，而是工作流中的必经步骤。Agent 不能随意跳过设计、测试、审查和收尾流程。


## 2、核心工作流

在`Superpowers`中，一个完整的开发周期通常会经过七个步骤。

### （1）头脑风暴

使用的 skill：`superpowers:brainstorming`

当 Agent 判断你正在创建功能、修改行为或构建组件时，它不会立刻开始写代码，而是先进入头脑风暴阶段。

这个阶段的目标是确认：

- 你真正想实现什么；
- 当前项目上下文是什么；
- 需求有哪些边界条件；
- 有哪些可选方案；
- 哪个方案更适合当前项目。

Agent 会通过类似苏格拉底式问答的方式逐步澄清需求，而不是一次性给出大段方案。等需求和方案明确后，它会生成设计文档。

默认设计文档位置是：

```text
docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md
```

这个设计文档可以理解为后续开发的 `spec`，也就是规格说明。它回答的是：

- 要做什么?
- 为什么这么做?
- 边界是什么?
- 整体设计是什么?

这里的 `spec` 不是测试文件，也不是代码注释，而是经过需求澄清后形成的设计规格文档。

### （2）创建 Git worktree

使用的 skill：`superpowers:using-git-worktrees`。

设计确认后，`Superpowers` 会创建或确认一个隔离的开发工作区。这个工作区通常是一个新的 `Git worktree`，并对应一个新的任务分支。

需要注意：`worktree` 通常不是给每个小任务创建一个，而是给一次完整功能开发创建一个。

`worktree` 的作用是把本次开发和当前主工作区隔离开。这样 Agent 的修改不会污染你原来的目录，也方便后续丢弃、保留、合并或创建 PR。

如果当前平台已经提供原生 worktree 能力，`Superpowers` 会优先使用平台能力。如果没有，才会退回到 `git worktree add` 这类 Git 命令。

创建或进入隔离工作区后，Agent 会进行项目初始化和测试基线检查。

测试基线指的是：在 Agent 正式修改代码之前，项目现有测试是否通过。

例如 Rust 项目中可能运行：

```rust
cargo test
```

如果开发前测试已经失败，那么后续就很难判断失败是由 Agent 新改动引入的，还是项目原本就坏了。因此，`Superpowers` 会在正式开发前检查当前测试基线是否干净。

> 注意，流程可能不会自己创建 Git worktree 时，在执行实施计划前需要确认下，可能需要手动调用skill

### （3）编写实现计划

使用的 skill：`superpowers:writing-plans`

设计文档确认后，`Superpowers` 会把设计拆成一组非常小的实现任务。每个任务通常应该能在两到五分钟内完成。

实现计划会明确写出：

- 当前任务的目标；
- 需要修改的文件路径；
- 预期实现内容；
- 测试要求；
- 验证命令；
- 完成标准。

默认计划文档位置是：

```text
docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md
```

设计文档、实现计划和任务可以这样理解：

- spec：设计规格，说明要做什么、为什么做、边界是什么
- plan：实施计划，说明分几步做，改哪些文件、如何验证
- task：plan 中的一个最小执行单元

例如：

```
spec：
实现一个终端版 2048 游戏，需要支持棋盘、移动、合并、分数、最高分保存和终端渲染。

plan：
Task 1：添加依赖
Task 2：实现 Board 核心逻辑
Task 3：实现 GameState
Task 4：实现 Renderer
Task 5：实现主循环
```

`plan` 是从 `spec` 拆出来的执行说明。后续子 Agent 不应该自由发挥，而应该严格按照 `plan` 中的任务描述执行。

### （4）执行实现计划

使用的 skill：`superpowers:subagent-driven-development`或`superpowers:executing-plans`。

如果当前环境支持子代理，推荐使用：`superpowers:subagent-driven-development`。

两者区别是：

| 执行方式                          | 说明                   | 适合场景                  |
| ----------------------------- | -------------------- | --------------------- |
| `subagent-driven-development` | 每个任务派发一个新的子 Agent 执行 | Claude Code 等支持子代理的平台 |
| `executing-plans`             | 在当前会话中按计划顺序执行        | 不支持子代理，或希望人工逐步检查      |
`Subagent-Driven` 并不是把所有任务并行丢给多个子 Agent 同时执行。它的常见执行方式是：

```text
Task 1
  ↓
子 Agent 执行
  ↓
Spec Compliance Review
  ↓
Code Quality Review
  ↓
Task 1 完成
  ↓
Task 2
  ↓
子 Agent 执行
  ↓
Spec Compliance Review
  ↓
Code Quality Review
  ↓
Task 2 完成
```

也就是说，同一个 `plan` 内的任务通常是顺序推进的。每个任务使用新的子 Agent，是为了避免长时间上下文污染，而不是为了让多个任务同时修改代码。


### （5）测试驱动开发

使用的 skill：`superpowers:test-driven-development`

`Superpowers` 强制执行 `RED-GREEN-REFACTOR` 流程。

```text
RED：先写一个失败的测试
  ↓
GREEN：写最少量代码让测试通过
  ↓
REFACTOR：在测试保持通过的前提下重构
```

这里的重点不是“最后补几个测试”，而是“先用测试定义行为，再写实现”。

如果 Agent 在没有失败测试的情况下先写实现代码，`Superpowers` 的约束会要求删除这些提前写出的代码，重新按照 `TDD` 流程开始。

这个机制是为了解决 AI 生成代码中常见的问题：代码看起来完整，但缺少可靠测试覆盖。


### （6）两阶段代码审查

使用的 skill：`superpowers:requesting-code-review`

在 `subagent-driven-development` 中，每个任务完成后都会进行两阶段审查：

- 第一阶段：Spec Compliance Review
- 第二阶段：Code Quality Review

这两个审查不是一回事。

#### 1）Spec Compliance Review

`Spec Compliance Review` 即规格符合性审查。它检查的是当前实现是否符合任务要求。

这里的 `spec` 是广义的规格要求，不一定只指 `docs/superpowers/specs/...` 里的设计文档。实际审查依据通常包括：

- 原始设计文档 `spec`；
- 实施计划 `plan`；
- 当前任务 `task`；
- 当前任务的文件路径、测试要求和验证步骤。

它关注的是“做没做对”，而不是“代码写得漂不漂亮”。


#### 2）Code Quality Review

`Code Quality Review` 即代码质量审查。

它检查的是：当前实现是否写得足够好。

它关注的是“做得好不好”，例如：

- 命名是否清晰；
- 文件职责是否单一；
- 是否有重复代码；
- 抽象是否过度；
- 错误处理是否合理；
- 测试是否可靠；
- 代码是否容易维护；
- 是否破坏已有功能。


### （7）分支最终化

使用的 skill：`superpowers:finishing-a-development-branch`。

当所有任务完成后，`Superpowers` 不会直接结束，而是进入分支收尾阶段。

这个阶段通常会先运行完整测试，确认项目最终状态没有被破坏。

例如：

```shell
cargo test
```

测试通过后，Agent 会让你选择如何处理当前分支：

|选项|说明|适合场景|
|---|---|---|
|合并到目标分支|在本地把任务分支合并回 `main` / `develop`|个人项目、本地实验|
|创建 GitHub Pull Request|推送远端分支并创建 PR|团队协作项目|
|保留分支|暂时不合并，稍后继续处理|还需要人工检查|
|丢弃改动|删除本次任务分支和 worktree|方案不满意或实验失败|


# 五、完整技能库

除了主开发流程之外，`Superpowers` 还提供了一组专门化的 `skills`，覆盖测试、调试、协作、评审、Git 工作流、子代理编排和技能编写等场景。它的核心机制是：Agent 在执行任务前先检查是否有适用技能；这些技能是强制工作流，而不是可选建议。

## 1、技能分类

| 类别  | skills                                                                          | 用途                                  |
| --- | ------------------------------------------------------------------------------- | ----------------------------------- |
| 测试  | `test-driven-development`                                                       | 执行 `RED-GREEN-REFACTOR`，防止先写实现、后补测试 |
| 调试  | `systematic-debugging`、`verification-before-completion`                         | 先定位根因，再修复；完成前必须验证结果                 |
| 协作  | `brainstorming`、`writing-plans`、`executing-plans`、`dispatching-parallel-agents` | 需求澄清、计划撰写、计划执行、并行调查                 |
| 评审  | `requesting-code-review`、`receiving-code-review`                                | 请求代码审查，处理审查反馈                       |
| Git | `using-git-worktrees`、`finishing-a-development-branch`                          | 创建隔离工作区，完成分支收尾                      |
| 编排  | `subagent-driven-development`                                                   | 每个任务使用新的子 Agent，并进行两阶段审查            |
| 元技能 | `writing-skills`、`using-superpowers`                                            | 创建新技能，确保 Agent 先检查并调用适用技能           |

## 2、核心技能说明

### （1）测试类

`test-driven-development` 用于强制执行 `RED-GREEN-REFACTOR`，它的作用是防止 Agent 直接写实现代码，最后再象征性补测试。

### （2）调试类

`systematic-debugging` 用于处理 bug、测试失败和异常行为。它强调先定位根因，再设计修复方案，避免随机改代码或只修补表象。

`verification-before-completion` 用于防止 Agent 过早宣布完成。它要求在提交、创建 PR 或声明“已修复”之前，先运行验证命令并确认真实输出。

### （3）协作类

`brainstorming` 用于需求澄清和方案设计。

`writing-plans` 用于把设计文档拆成可执行任务，要求计划明确到包含文件路径、实现步骤、测试要求和验证命令。

`executing-plans` 用于在当前会话中顺序执行计划。

`dispatching-parallel-agents` 用于并行调查多个相互独立的问题。它适合并行研究或排查，不适合让多个 Agent 同时修改同一批代码。


### （4）评审类

`requesting-code-review` 用于请求代码审查，通常会检查实现是否符合计划、是否遗漏需求、是否引入问题。

`receiving-code-review` 用于处理审查反馈，避免 Agent 机械接受所有建议，或者忽略关键问题。


### （5）Git 类

`using-git-worktrees` 用于创建隔离工作区，避免 Agent 直接污染当前主工作区。

`finishing-a-development-branch` 用于分支收尾。任务完成并测试通过后，Agent 会让用户选择合并、创建 PR、保留分支或丢弃改动。

### （6）编排类

`subagent-driven-development` 用于执行已经写好的计划。它通常不是并行执行所有任务，而是：

```
Task 1 → 子 Agent 执行 → 两阶段审查 → Task 2 → 子 Agent 执行 → 两阶段审查 → Task 3 → 子 Agent 执行 → 两阶段审查
```

它的重点是上下文隔离和任务边界清晰，而不是同时让多个 Agent 改同一个代码库。

### （7）元技能

`using-superpowers` 是 Superpowers 的入口型技能。它要求 Agent 在开始任务前，先检查当前任务是否有适用的 Superpowers skill。如果有，就必须加载并遵守对应技能。

`writing-skills` 用于创建新的 Superpowers 风格技能。这里的 skill 不是一次性提示词，也不是某次问题复盘，而是一份可复用的工作方法，通常写成 SKILL.md，供后续 Agent 在类似任务中加载和执行。



# 六、注意事项

`Superpowers` 会强化 Agent 的开发流程，但它不是一个强制沙箱，也不能保证每一步都完全符合用户预期。实际使用时，建议在项目的 `CLAUDE.md` 中补充明确规则，避免 Agent 自动提交、跳过工作区隔离，或直接在 `main` 分支上实现功能。

## 1、禁止自动提交

如果不希望 Agent 自动提交，需要在项目规则中明确禁止。

建议在 `CLAUDE.md` 中加入：

```markdown
# Git 提交规则  
  
- 禁止自动提交。  
- 提交前必须先展示 `git status`、变更摘要和拟定的 commit message。  
- 只有用户明确确认后，才能执行 `git add` 和 `git commit`。
```


## 2、实施前手动确认 worktree

实际使用中，`Superpowers` 在写完计划后，有时会直接进入 `subagent-driven-development`，不一定自动触发 `using-git-worktrees`。因此，在开始执行计划前，最好手动提醒 Agent：

```text
在开始实施计划前，请先使用 superpowers:using-git-worktrees。  
```

也可以把规则写进 `CLAUDE.md`：

```text
# Worktree 规则  
  
- 执行实现计划前，必须先使用 `superpowers:using-git-worktrees`。  
- 禁止直接在 `main` / `master` 上实现功能。  
- 进入 worktree 后，必须报告 `pwd`、当前分支和 `git status`。  
- 如果仍在主分支，或工作区不干净，必须停止并询问用户。
```