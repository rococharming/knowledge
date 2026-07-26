---
title: Superpowers
date: 2026-07-27
tags: [AI, Skill, coding-tool, workflow]
aliases:
  - Superpowers
  - Superpowers 工作流
  - Coding Agent Superpowers
---

# 一、概述

`Superpowers` 是一套面向 Coding Agent 的软件开发方法论 Skill 集合。它不替代 `Claude Code`、`Codex`、`Cursor` 这类 Agent，也不负责让模型本身变聪明；它的作用是给 Agent 加上一套强制性的工程流程。

它的核心判断是：

> Coding Agent 的主要风险不是写不出代码，而是太容易绕过需求澄清、测试反馈、代码审查和收尾决策，然后很快地把错误扩大。

这套 Skills 主要解决四类问题：

- **过早编码**：想法还没变成设计，Agent 已经开始搭架构、写实现。
- **计划缺失**：需求被口头理解后直接开工，没有可复查的施工说明。
- **反馈不足**：代码看起来合理，但没有先失败再通过的测试，也没有完成前的新鲜验证。
- **交付混乱**：任务做完后才讨论分支、提交、合并、推送、保留或丢弃。

可以把 Superpowers 理解成：把 Coding Agent 从“会写代码的聊天框”拉回一条可审计的软件工程流水线。

# 二、安装

## 1、Claude Code

Superpowers 已进入 Claude 官方插件市场，可以直接安装：

```text
/plugin install superpowers@claude-plugins-official
```

也可以运行 `/plugin` 打开插件管理器，在 `Discover` 中搜索。

![[assets/Pasted image 20260714224027.png|600]]

安装完成后，通常需要执行：

```text
/reload-plugins
```

## 2、ChatGPT App

ChatGPT App 可以在侧边栏插件市场中搜索 `Superpowers` 并安装。

![[assets/Pasted image 20260714224235.png|600]]

安装后，Superpowers 会把一组 Skill 注入当前 Agent 环境。日常使用时，不一定需要显式输入某个命令；Agent 会先检查当前任务是否匹配这些 Skill。


# 三、它是怎么生效的

## 1、启动规则

Superpowers 的入口不是某一个“开发命令”，而是 `using-superpowers` 这条启动规则。

它要求 Agent 在任何任务开始前先判断：当前请求有没有适用 Skill。如果有，就必须先读取对应 Skill 的当前说明，再按里面的流程执行。

也就是说，它把“直接写代码”的默认路径，改成“先检查 Skill、再按流程推进”的受控路径：

![[assets/Superpowers-path-comparison-handdrawn.png|600]]

这也是 Superpowers 和普通提示词最不一样的地方：它强调 **强制调用当前 Skill 文件**，而不是让 Agent 凭记忆复述一套工程原则。

## 2、自动触发和显式点名

Superpowers 的 Skill 可以自动触发，也可以由用户显式点名。

例如：

- 你说“给项目加一个登录功能”，应先进入 `brainstorming`，而不是立刻写代码。
- 你说“这个测试为什么失败”，应先进入 `systematic-debugging`，而不是猜一个修复。
- 你说“请按这个计划执行”，应进入 `subagent-driven-development` 或 `executing-plans`。
- 你说“做完前再检查一遍”，应进入 `verification-before-completion`。

显式点名的价值在于降低流程歧义。例如你可以直接说“请先用 systematic-debugging，不要先猜修复”，这样 Agent 更不容易把 Bug 修复当成普通代码改动。

## 3、流程强度

Superpowers 是强流程，但不是所有任务都要变成重流程。

小任务可以很轻：设计说明可能只有几句话，计划也可以很短。复杂任务则需要完整链路：先澄清，再写设计文档，再写实现计划，再分任务执行、测试、审查、收尾。

判断流程强度时，重点看风险，而不是字数：

| 任务类型            | 流程强度 | 原因                     |
| --------------- | ---- | ---------------------- |
| 只读解释、查找文件、回答概念  | 轻流程  | 通常不改代码，也不需要分支收尾        |
| 单文件文档或配置修改      | 轻到中等 | 需要确认目标和验证渲染，但不一定需要完整计划 |
| 新功能、行为变更、Bug 修复 | 中到重  | 需要需求边界、测试反馈和完成前验证      |
| 多模块功能、架构调整、长期任务 | 重流程  | 需要设计文档、任务拆分、审查和分支决策    |

# 四、工作原理

## 1、整体结构

Superpowers 的主流程不是一串命令清单，而是一组带阶段门的开发路径，每个阶段都在限制一种常见失败：

![[assets/Superpowers-workflow-handdrawn.png|800]]

- `brainstorming` 限制“没想清楚就做”。
- `using-git-worktrees` 限制“把用户当前改动和 Agent 改动混在一起”。
- `writing-plans` 限制“凭聊天记忆施工”。
- `subagent-driven-development` 和 `executing-plans` 限制“长任务上下文漂移”。
- `test-driven-development` 限制“实现先行、测试补票”。
- `requesting-code-review` 限制“自己写自己审”。
- `verification-before-completion` 限制“没有证据就宣布完成”。
- `finishing-a-development-branch` 限制“Agent 擅自合并、推送或清理分支”。

## 2、四层 Skill 地图

从职责上看，Superpowers 可以分成四层：

![[assets/Superpowers-skill-map-handdrawn.png|800]]

| 层级     | 代表 Skill                                                                                                           | 职责                                      |
| ------ | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------- |
| 启动层    | `using-superpowers`                                                                                                | 要求每次任务先检查适用 Skill                       |
| 设计层    | `brainstorming`、`writing-plans`                                                                                    | 把想法变成设计，再把设计变成可执行计划                     |
| 执行与反馈层 | `subagent-driven-development`、`executing-plans`、`test-driven-development`、`systematic-debugging`                   | 选择一种计划执行方式，在实现中建立红绿反馈；遇到 Bug 时从根因调查进入修复 |
| 收尾层    | `requesting-code-review`、`receiving-code-review`、`verification-before-completion`、`finishing-a-development-branch` | 审查、验证、处理反馈、决定分支去向                       |

这四层里，最关键的不是“是否用了很多 Agent”，而是每一步都有明确产物和验证方式。设计要被确认，计划要能被执行，测试要先失败再通过，完成声明要有新鲜证据。

## 3、主流程：idea → ship

最典型的 Superpowers 流程，是把一个想法交付成代码。

`brainstorming` 先把模糊想法变成设计。它要求 Agent 先读项目上下文，再一次只问一个关键问题，随后提出 2～3 个方案和取舍，并在用户确认后写入设计文档。

`writing-plans` 再把设计变成施工计划。这个计划不是普通待办列表，而是写给“没有上下文但能执行任务的人”的详细说明。每个任务都应包含文件路径、接口、测试、执行步骤和验证方式。

进入实现时，如果有子 Agent 能力，优先使用 `subagent-driven-development`：每个任务交给新的实现 Agent，任务完成后再交给审查 Agent 检查规格符合度和代码质量。如果没有子 Agent，使用 `executing-plans` 在同一会话里按计划顺序执行，并在检查点停下来。

实现过程中，行为变更优先走 `test-driven-development`。它要求先写失败测试、确认失败原因正确，再写最少代码让测试通过，最后在测试仍然通过的前提下整理结构。

完成前，`verification-before-completion` 会把“我觉得完成了”换成“刚刚运行了什么，输出证明了什么”。最后，`finishing-a-development-branch` 会把集成决定交还给用户：本地合并、推送创建 PR，或保留分支稍后处理。

## 4、Bug 路径：symptom → root cause → fix

Bug 修复不是主流程的简化版，而是另一条入口。

`systematic-debugging` 的铁律是：没有根因调查，就不提出修复。它通常分四步：

1. 读完整错误信息，确认问题能否稳定复现。
2. 找相似的正常样例，比较正常路径和异常路径。
3. 一次验证一个假设，不叠加多个“也许能修”的改动。
4. 找到根因后写失败测试，再做最小修复。

如果连续多次修复失败，Superpowers 倾向于停下来质疑架构假设，而不是继续堆补丁。这个地方很有价值：它把“修了又坏”识别成设计问题，而不是让 Agent 在局部症状上继续打转。

## 5、并行路径：调查可以并行，改代码要谨慎

`dispatching-parallel-agents` 适合并行调查，不适合让多个 Agent 同时改同一片代码。

适合并行的情况：

- 多个测试文件分别失败。
- 初步判断根因互不相关。
- 每个调查范围清楚。
- 不共享同一个数据库、端口、临时目录或测试夹具。

不适合并行的情况：

- 多个任务会修改同一文件。
- 第二个任务依赖第一个任务的结果。
- 还不知道多个症状是否来自同一根因。
- 所有 Agent 都要操作同一份外部状态。

Superpowers 推崇的并行，不是“越多 Agent 越快”，而是让互不污染的调查各自收集证据。

# 五、Skill 速查表

## 1、启动与设计

| Skill                 | 什么时候用             | 主要产物                             | 注意点                         |
| --------------------- | ----------------- | -------------------------------- | --------------------------- |
| `using-superpowers`   | 每次会话或任务开始时        | Skill 检查规则                       | 它是总开关；如果有适用 Skill，就先读 Skill |
| `brainstorming`       | 新功能、组件、行为修改、创造性工作 | 经过确认的设计文档                        | 设计确认前不写实现代码                 |
| `using-git-worktrees` | 设计确认后、准备执行前       | 隔离工作区和任务分支                       | 不适合只读调查或很小的讨论               |
| `writing-plans`       | 已有设计或规格，需要施工计划    | `docs/superpowers/plans/` 下的实现计划 | 计划要详细到另一个 Agent 能照做         |

## 2、实现与反馈

| Skill | 什么时候用 | 主要产物 | 注意点 |
|---|---|---|---|
| `subagent-driven-development` | 有计划且任务边界较清楚 | 分任务实现、任务审查、最终审查 | 新 Agent 做任务，主会话负责统筹 |
| `executing-plans` | 没有合适子 Agent，或任务强相关 | 同一会话顺序执行计划 | 先审计划，有阻塞就停下来问 |
| `test-driven-development` | 新功能、Bug 修复、重构、行为变更 | 红绿循环中的测试和实现 | 没看过测试失败，就不能证明测试有效 |
| `systematic-debugging` | Bug、测试失败、性能问题、异常行为 | 根因、复现方式、回归测试、最小修复 | 不先猜修复，先找证据 |

## 3、审查与收尾

| Skill | 什么时候用 | 主要产物 | 注意点 |
|---|---|---|---|
| `requesting-code-review` | 每个任务后、重大功能后、合并前 | 按严重程度排列的审查意见 | Critical 和 Important 不应被忽略 |
| `receiving-code-review` | 收到 PR 评论、审查 Agent 反馈或用户反馈 | 已验证的接受、修改或反驳结论 | 先验证反馈是否成立，再决定处理方式 |
| `verification-before-completion` | 宣称完成、修好、测试通过、提交或 PR 前 | 新鲜验证证据 | 不能用“应该”“看起来”替代命令输出 |
| `finishing-a-development-branch` | 实现完成且测试通过后 | 合并、PR 或保留分支的用户决策 | 丢弃工作只能由用户明确要求并确认 |

## 4、辅助与元能力

| Skill | 什么时候用 | 主要产物 | 注意点 |
|---|---|---|---|
| `dispatching-parallel-agents` | 多个独立问题可并行调查 | 多路调查结果 | 并行调查可以，冲突性改代码不适合 |
| `writing-skills` | 创建或修改 Skill 本身 | Skill 文件和测试方法 | 面向 Skill 作者，不是普通开发流程 |

## 5、选择口诀

- 不确定有没有 Skill：先看 `using-superpowers`。
- 新功能还没想清楚：`brainstorming`。
- 设计已经确认：`writing-plans`。
- 有计划且可拆任务：`subagent-driven-development`。
- 有计划但要在当前会话顺序做：`executing-plans`。
- 行为变更或修 Bug：`test-driven-development`。
- 问题坏在哪里还不清楚：`systematic-debugging`。
- 做完前要证明结果：`verification-before-completion`。
- 准备合并、推送或保留：`finishing-a-development-branch`。

# 六、重点 Skill 详解

## 1、brainstorming

`brainstorming` 是 Superpowers 的主流程起点。它负责把“我想做一个东西”变成“我们确认要做这个东西，而且知道不做什么”。

它最重要的规则是：

> 设计没有得到用户确认前，不进入实现。

一个完整的 `brainstorming` 通常包括：

- 先读项目结构、文档和最近提交。
- 判断任务是否过大，必要时先拆成多个子项目。
- 每次只问一个关键问题。
- 提出 2～3 个方案，说明取舍和推荐方案。
- 分段展示设计，让用户确认。
- 把确认后的设计写入 `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`。
- 自查设计文档是否有占位符、矛盾、歧义和范围过载。
- 用户确认书面设计后，才进入 `writing-plans`。

这里有两层确认：先确认聊天里的设计方向，再确认保存后的设计文档。前者防止方向错，后者防止写成文档时新增了未确认内容。

## 2、using-git-worktrees

`using-git-worktrees` 用来判断是否需要隔离工作区。可以把它理解为：给这次任务单独开一张工作台。

它通常发生在设计确认之后、真正执行计划之前。这样 Agent 的改动、测试、临时文件和本地提交不容易和用户当前工作混在一起。

通常不需要隔离工作区的情况：

- 只读调查。
- 解释概念。
- 单纯讨论方案。
- 很小的文档或配置修改。

更适合隔离工作区的情况：

- 会修改多个文件。
- 要执行较长计划。
- 当前工作区已有用户改动。
- 后续可能需要提交、审查、推送或丢弃整组改动。

如果平台本身已经提供隔离环境，就不一定表现为项目目录下的 `.worktrees/`。关键不是目录名字，而是改动边界是否清楚。

## 3、writing-plans

`writing-plans` 把设计文档变成实现计划。它的计划面向执行者，而不是面向读者展示愿景。

一个合格计划通常要写清：

- 全局约束：版本、依赖、命名、兼容性、非目标。
- 文件结构：每个文件负责什么，哪些文件会被创建或修改。
- 任务边界：每个任务能否单独测试、单独审查。
- 接口关系：前后任务之间消费和产出的函数、类型、文件或协议。
- 步骤细节：先写什么测试，预期怎么失败，再写什么实现。
- 验证方式：每一步跑什么命令，预期输出是什么。

它反对空泛计划。例如“添加适当错误处理”“写相关测试”“实现这个模块”都不是好任务，因为执行者仍然要自己猜。

好的计划应该像施工说明：另一个 Agent 不需要继承当前聊天上下文，也能按步骤完成。

## 4、subagent-driven-development 和 executing-plans

这两个 Skill 都用于执行计划，区别在于是否依赖子 Agent。

| Skill | 适合场景 | 工作方式 |
|---|---|---|
| `subagent-driven-development` | 任务边界清楚，环境支持子 Agent | 每个任务派发一个新实现 Agent，任务后审查 |
| `executing-plans` | 没有合适子 Agent，或任务上下文强相关 | 当前会话读取计划并顺序执行 |

`subagent-driven-development` 的重点不是并行写代码，而是隔离上下文。每个实现 Agent 只拿到自己的任务简报；主会话负责记录进度、处理问题、发起审查和决定是否继续。

`executing-plans` 更像传统执行模式：当前会话先审计划，再逐项执行。它更慢，但适合任务强相关、拆给多个 Agent 反而容易误解的情况。

## 5、test-driven-development

`test-driven-development` 的核心不是“有测试”，而是“先看到测试失败”。

典型循环是：

```text
RED：写一个最小失败测试
  ↓
确认失败原因正确
  ↓
GREEN：写最少代码让它通过
  ↓
确认测试和相关检查通过
  ↓
REFACTOR：在绿灯下整理结构
```

如果测试一写出来就通过，说明它没有证明新行为；如果测试因为拼写、导入或环境错误失败，也不能算有效红灯。它必须因为目标行为尚未实现而失败。

这个规则尤其适合 Bug 修复。回归测试应该先抓住原始问题，再证明修复后的行为。

## 6、systematic-debugging

`systematic-debugging` 用于所有技术问题：测试失败、线上 Bug、性能回退、构建失败、集成异常。

它的核心原则是：

> 先找根因，再谈修复。

最容易违反这条规则的时刻，往往是“看起来很简单”的时候。Superpowers 会要求先读完整错误、稳定复现、检查最近变化、比较正常路径和异常路径，再提出单一假设并最小验证。

如果问题跨多个组件，例如 CI、构建脚本、签名、部署或 API、服务、数据库，就应该在组件边界加诊断信息，先看坏值在哪一层出现，而不是直接改最深处的症状。

## 7、requesting-code-review 和 receiving-code-review

`requesting-code-review` 用于主动审查：任务完成后、重大功能完成后、合并前。审查者应拿到精确上下文：做了什么、依据哪个计划或需求、从哪个提交到哪个提交，而不是拿到整段聊天历史。

`receiving-code-review` 用于处理收到的反馈。它强调不要机械接受，也不要本能反驳，而是先验证反馈是否成立：

- 如果反馈指出真实缺陷，就修复并验证。
- 如果反馈是误判，就用代码、测试或需求依据解释为什么不改。
- 如果反馈暴露需求冲突，就回到用户或规格层重新确认。

这两者共同解决一个问题：审查不是仪式，而是让不同上下文的判断互相校验。

## 8、verification-before-completion

`verification-before-completion` 是完成声明前的闸门。

它要求 Agent 在说“完成”“修好了”“测试通过”“可以提交”之前，先回答四个问题：

1. 哪个命令能证明这个结论？
2. 刚刚是否运行了完整命令？
3. 是否读了完整输出和退出状态？
4. 输出是否真的支持这个结论？

这条 Skill 解决的是 Agent 很常见的语言问题：把“我推测应该可以”说成“已经完成”。在 Superpowers 里，没有新鲜验证证据，就不能做成功声明。

## 9、finishing-a-development-branch

`finishing-a-development-branch` 处理最后一步：工作完成后，分支怎么办。

它先要求重新跑完整测试；如果测试失败，不能进入集成菜单。测试通过后，再识别当前是否普通仓库、命名分支 worktree，还是 detached HEAD。

正常情况下，它只提供三个选项：

| 选项 | 含义 |
|---|---|
| 本地合并 | 合并回基线并再次测试 |
| 推送并创建 Pull Request | 保留分支，继续处理远端反馈 |
| 保留现状 | 用户稍后处理 |

丢弃工作不是默认菜单项。只有用户明确要求丢弃时，Agent 才能列出将删除的分支、提交和工作区，并要求用户输入确认词。

# 七、推荐使用模板

## 1、功能开发模板

```text
请使用 Superpowers 完成这个任务。

目标：<希望实现的用户价值>
现状：<相关模块、已有行为、已知问题>
约束：<兼容性、依赖、性能、安全、Git 权限>
非目标：<这次明确不做什么>
验收：<可观察、可执行的成功标准>

先读取项目规则和现有实现；不要重复询问仓库里已有答案。
在任何推送、合并请求、合并、部署或删除操作前获得我的明确确认。
```

## 2、Bug 修复模板

```text
请先使用 systematic-debugging 复现并定位根因，不要先猜修复。

症状：<看到的错误、失败测试或异常行为>
复现：<已知复现步骤；如果不稳定，请说明频率>
最近变化：<可能相关的提交、依赖、配置或环境变化>
验收：<修复后必须通过的测试、命令或用户可见行为>

找到根因后，用失败的回归测试证明问题，再实现最小修复并运行完整验证。
```

# 八、总结

Superpowers 最有价值的地方，是把 Coding Agent 的“能力”变成可控流程。

它不是为了让每个小改动都变慢，而是让风险更高的开发任务有明确的阶段门：需求先确认，计划先写清，测试先变红，审查要独立，完成要有证据，分支去向由用户决定。

最好的使用方式，是让流程强度和任务风险匹配：小事轻一点，大事完整一点；但一旦进入实现、调试、审查或收尾，就让证据说话。
