---
title: Matt Pocock Skills
date: 2026-07-15
tags: [coding-tool, workflow, agent, skill]
aliases:
  - Matt Pocock Skills 工作流
  - Skills for Real Engineers
---

# 一、概述

`mattpocock/skills` 是一组面向 Coding Agent 的工程工作流 Skill。

它不是“自动开发框架”，也不是几条提示词的合集，而是把需求澄清、规格记录、任务拆分、测试驱动、问题诊断和代码审查固化为可重复执行的流程。

> [!summary] 核心价值
> 它解决的不是“Agent 不会写代码”，而是“Agent 在需求未对齐、反馈不足和缺少工程约束时，会更快地把项目带偏”。

这套 Skills 重点修复四类常见问题：

- **需求偏差**：实现前让 Agent 反向追问，把模糊决策说清楚。
- **上下文丢失**：将项目术语写入 `CONTEXT.md`（项目上下文文档），将重要架构选择写入 ADR（Architecture Decision Record，架构决策记录），供后续会话复用。
- **反馈链太弱**：通过类型检查、自动测试和稳定复现，让 Agent 能快速判断对错。
- **架构腐化**：代码随改动增多而变得难以理解和修改。可用垂直切片限制单次改动，并定期检查模块责任。

> [!note] 什么是垂直切片
> 垂直切片就是把一个大需求拆成多个“能单独跑通、单独验收”的小功能。
>
> 例如做登录功能时，可以拆成“正确账号密码能登录”和“密码错误时显示提示”。每个小功能都要同时完成它所需的少量页面、接口和数据处理。不要拆成“先做页面、再写接口、最后建数据表”，因为这些任务单独完成时功能还不能使用，也无法真正验收。

# 二、安装

## 1、通用安装方式

如果希望安装到 Claude Code、Codex 或其他支持 Agent Skills 标准的工具，使用：

```shell
npx skills@latest add mattpocock/skills
```

这套标准让不同 Agent 能识别同一份 `SKILL.md`。安装器会让你选择需要的 Skill、目标 Agent 以及安装范围，并把 Skill 复制到项目中，便于阅读和按团队规则修改。

如果已安装 [[2、find-skills|find-skills]]，也可先用它搜索、筛选需要的 Skill。

> [!tip]
> 第一次不必全部安装。可先选 `setup-matt-pocock-skills`、`grill-with-docs`、`to-spec`、`to-tickets`、`implement` 和 `diagnosing-bugs`，覆盖从规划到实现、调试的主干。

## 2、Claude Code 插件方式

如果不想自行维护 Skill 文件，可将它作为 Claude Code 插件安装：

```text
/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock
```

插件方式安装的是只读、跟随官方更新的完整 Skill 集；`skills.sh` 方式更适合希望针对项目裁剪和修改的团队。

## 3、每个项目先初始化

安装时必须包含 `setup-matt-pocock-skills`，然后在每个项目中执行一次：

```text
/setup-matt-pocock-skills
```

这个技能本质上是在给 Agent 编写一份项目工作说明书。它会把这些约定记录到`docs/agents/`下，并在已有的`CLAUDE.md`或`AGENTS.md`中添加指向这些配置的说明。

它会确认三类项目约定：

- 使用 GitHub、GitLab 还是Markdown文件等作为任务追踪器，也就是用来记录任务状态和依赖的地方。Matt Pocock Skills 当前提供的本地约定，是把任务放在 `.scratch/` 中。一个功能对应一个目录，一个任务对应一个 Markdown 文件。例如：

```
.scratch/
└── preview-app-path/
    ├── spec.md
    └── issues/
        ├── 01-validate-directory.md
        ├── 02-create-symlink.md
        ├── 03-register-preview-app.md
        └── 04-add-tests.md
```

其中一个任务文件可能是：

```
# Validate preview app directory

Type: task
Status: claimed
Blocked by: none

## Description

验证传入目录是否存在，并检查 manifest.json。

## Comments

这里记录讨论和补充信息。
```

完成后可以改成：

```
Status: resolved
```

本地任务之间的依赖也可以记录在文件里：

```
Blocked by: 01, 02
```

表示当前任务需要等 `01` 和 `02` 完成后才能开始。

- Triage（任务分流）流程使用哪些标签，以区分待补充、可交给 Agent、需人工处理等状态。

Triage 原本有“分诊、分流”的意思。在软件项目中，它表示：

> 收到一个新任务后，先判断它是什么、信息是否完整、由谁处理、是否值得处理。

Matt Pocock Skills 默认使用五类角色标签：

|标签|通俗含义|
|---|---|
|`needs-triage`|新任务，还没有分析和分类|
|`needs-info`|信息不足，需要补充|
|`ready-for-agent`|信息完整，可以交给 Agent|
|`ready-for-human`|需要人工判断或处理|
|`wontfix`|决定不处理|

典型流转过程是：

```
needs-triage
      │
      ▼
分析任务
      │
      ├── 信息不足 ──> needs-info
      │
      ├── Agent 可完成 ──> ready-for-agent
      │
      ├── 需要人工处理 ──> ready-for-human
      │
      └── 不准备处理 ──> wontfix
```

 - 规格文档、领域文档和 ADR 保存在哪里。

规格文档通常描述要实现什么、为什么实现、哪些内容属于范围内、哪些内容不做、验收标准是什么、有哪些边界情况。

例如：

```
docs/specs/preview-app-path.md
```

或者使用本地任务模式时：

```
.scratch/preview-app-path/spec.md
```

领域文档记录项目里的业务概念、专业术语和长期规则。这样 Agent 下次看到一些抓虐术语时，就不会每次重新猜测含义。

默认的单上下文结构通常是：

```
CONTEXT.md
```

对于大型 monorepo，才可能使用多个 `CONTEXT.md`，再由根目录的 `CONTEXT-MAP.md` 指向各模块。

ADR 是 **Architecture Decision Record**，即“架构决策记录”。

它不是描述“要做什么”，而是记录做出了什么技术选择、为什么这样选、考虑过哪些其他方案。

例如：

```
docs/adr/0003-use-symlink-for-preview-app.md
```
# 三、工作原理

## 1、显式调用与自动调用

当前官方仓库将 Skill 分为两类：

| 类型 | 如何触发 | 作用 |
|---|---|---|
| 用户调用 | 用户输入 `/grill-with-docs` 等命令 | 编排一段完整流程，保留用户控制权 |
| 模型调用 | 用户显式点名，或 Agent 根据任务自动匹配 | 提供 TDD（测试驱动开发）、调试、审查等可复用工程纪律 |

用户调用的 Skill 主要负责“选流程”，模型调用的 Skill 主要负责“按规则做事”。两者组合后，用户不需要把所有细节都塞进每次提示词。

## 3、三个关键反馈环

反馈环是“执行一小步，立即用结果决定下一步”的循环，用来及时发现偏差。

- **认知反馈环**：`grill-with-docs` 每次只解决一个问题，能从代码库查到的事实不再询问用户，重要术语与决策同步写入文档。
- **实现反馈环**：`tdd` 先确认公共测试边界，也就是用户或其他模块能直接调用并观察结果的接口；然后以“一个失败测试 → 最小实现 → 保持通过后重构”循环推进。
- **诊断反馈环**：`diagnosing-bugs` 按“复现 → 缩小范围 → 提出假设 → 插桩验证 → 修复 → 回归测试”推进。插桩是临时加入日志、计数器或断言来验证假设；回归测试用于确保同一问题不会再次出现。

> [!important]
> 这套工作流的速度上限取决于反馈速度。能用一条命令快速得到稳定的成功/失败信号，比让 Agent 读更多代码更有价值。

# 四、实践指南

## 1、新功能的推荐主线

```text
/grill-with-docs
        ↓
/to-spec
        ↓
/to-tickets
        ↓
/implement
        ↓
/code-review
```

1. **澄清**：说明目标、已知约束和明确不做的事，让 `grill-with-docs` 对照现有代码、项目术语和 ADR 逐个挑战假设。
2. **固化**：用 `to-spec` 把已经聊清楚的内容整理为规格，不追加未讨论的功能。
3. **拆分**：用 `to-tickets` 拆成上文所说的垂直切片。每个任务都应包含让小功能跑起来所需的页面、接口和数据改动，并标明哪些任务必须先完成。
4. **实现**：用 `implement` 按规格或任务单（tickets）推进；它在事先确认的测试边界上调用 `tdd`，并在结束前运行类型检查、单元测试与完整测试。
5. **审查**：`code-review` 从固定比较点（如 `main` 分支或某个提交）检查代码是否符合项目规范，以及是否真正实现了原始规格。

## 2、Bug 修复

不要以“帮我修这个 Bug”开始猜解决方案，而是先提供观察到的行为、期望行为和现有复现步骤，让 Agent 调用 `diagnosing-bugs`。

成功标准是：

- 得到最小且稳定的复现方式。
- 通过日志、断言或小实验验证根因，而不是只凭阅读代码推测。
- 修复后增加能捕获原问题的回归测试。

## 3、使用边界

- **小任务不必走全流程**：一次性脚本或小文档修改可直接完成，否则流程成本可能高于实现成本。
- **不代替人的决策**：Skill 负责追问、记录和验证，产品取舍、架构边界和风险接受仍由人决定。
- **先适配再执行**：仓库原本主要面向 TypeScript 语言和 Node.js 运行环境。其他语言、运行环境、GitLab 等协作平台或特殊测试体系可以复用原则，但应先调整命令、任务追踪器和测试边界。
- **保持小而可组合**：如果要定制，优先修改与团队现有流程冲突的少量规则，不要把它扩展成另一个笨重框架。如果需要开发自己的 Skill，可参考 [[1、skill-creator|skill-creator]]。

## 5、最小上手方案

对一个会持续迭代的现有项目，可从下面这套最小闭环开始：

1. 安装主干 Skill，运行 `/setup-matt-pocock-skills`。
2. 选一个真实但范围可控的功能，用 `/grill-with-docs` 澄清目标和不做什么。
3. 用 `/to-spec` 和 `/to-tickets` 固化规格，只拆出少量可独立验收的切片。
4. 用 `/implement` 实现第一个切片，检查 Agent 是否真正跑了失败测试、最小实现和最终验证。
5. 根据项目实际情况删改 Skill 规则，而不是因为一次不适配就放弃整套方法。

判断是否真正用起来的标准，不是“安装了多少个 Skill”，而是需求、决策、任务和验证结果能否在不同会话之间稳定传递。

# 五、参考资料

- [[Matt Pocock Skills 怎麼用在 Coding  Planning]]
- [[打造真实项目的 AI 编程环境：Matt Pocock 的 Skill 工作流完整上手攻略]]
- [[How to Use Matt Pocock's Skills for Claude Code A Complete Guide]]
- [mattpocock/skills 官方仓库](https://github.com/mattpocock/skills)
