---
title: Matt Pocock Skills
date: 2026-07-15
tags: [coding-tool, workflow, agent, skill]
aliases:
  - Matt Pocock Skills 工作流
  - Skills for Real Engineers
---

# 一、概述

`mattpocock/skills` 是一组面向 Coding Agent 的工程工作流 Skill。它不是“自动开发框架”，也不是几条提示词的合集，而是把需求澄清、规格记录、任务拆分、测试驱动、问题诊断和代码审查固化为可重复执行的流程。

> [!summary] 核心价值
> 它解决的不是“Agent 不会写代码”，而是“Agent 在需求未对齐、反馈不足和缺少工程约束时，会更快地把项目带偏”。

这套 Skills 重点修复四类常见问题：

- **需求偏差**：实现前让 Agent 反向追问，把模糊决策说清楚。
- **上下文丢失**：将领域术语和重要决策写入 `CONTEXT.md` 与 ADR，供后续会话复用。
- **反馈链太弱**：通过类型检查、自动测试和稳定复现，让 Agent 能快速判断对错。
- **架构腐化**：用垂直切片限制单次改动，并定期检查模块责任和接口。


# 二、安装

## 1、通用安装方式

如果希望安装到 Claude Code、Codex 或其他兼容 Agent Skills 标准的工具，使用：

```shell
npx skills@latest add mattpocock/skills
```

安装器会让你选择需要的 Skill、目标 Agent 以及安装范围。这种方式会把 Skill 复制到项目中，便于阅读和按团队规则修改。

如果已安装 [[2、find-skills|find-skills]]，也可先用它搜索、筛选需要的 Skill。

> [!tip]
> 第一次不必全部安装。可先选 `setup-matt-pocock-skills`、`grill-with-docs`、`to-spec`、`to-tickets`、`implement` 和 `diagnosing-bugs`，覆盖从规划到实现、调试的主干。

## 2、Claude Code 插件方式

如果不想自行维护 Skill 文件，可将它作为 Claude Code 插件安装：

```text
/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock
```

插件方式安装的是只读、由上游更新的完整 Skill 集；`skills.sh` 方式更适合希望针对项目裁剪和修改的团队。

## 3、每个项目先初始化

安装时必须包含 `setup-matt-pocock-skills`，然后在每个项目中执行一次：

```text
/setup-matt-pocock-skills
```

它会确认三类项目约定：

- 使用 GitHub、Linear 还是本地文件管理任务。
- Triage 流程使用哪些标签。
- 规格、领域文档和 ADR 保存在哪里。

# 三、工作原理

## 1、Skill 是流程，不是一次性提示词

普通提示词只约束当前一次交互；Skill 则用 `SKILL.md` 记录稳定的触发条件、执行步骤、分支判断和产物。

简单来说，提示词是“这次请这样做”，Skill 是“遇到这类任务时都按这套流程做”。

## 2、显式调用与自动调用

当前官方仓库将 Skill 分为两类：

| 类型 | 如何触发 | 作用 |
|---|---|---|
| 用户调用 | 用户输入 `/grill-with-docs` 等命令 | 编排一段完整流程，保留用户控制权 |
| 模型调用 | 用户显式点名，或 Agent 根据任务自动匹配 | 提供 TDD、调试、审查等可复用工程纪律 |

用户调用的 Skill 主要负责“选流程”，模型调用的 Skill 主要负责“按规则做事”。两者组合后，用户不需要把所有细节都塞进每次提示词。

## 3、三个关键反馈环

- **认知反馈环**：`grill-with-docs` 每次只解决一个问题，能从代码库查到的事实不再询问用户，重要术语与决策同步写入文档。
- **实现反馈环**：`tdd` 先确认要测试的公共边界，然后以“一个失败测试 → 最小实现 → 保持通过后重构”循环推进。
- **诊断反馈环**：`diagnosing-bugs` 按“复现 → 缩小范围 → 提出假设 → 插桩验证 → 修复 → 回归测试”推进，避免读几个文件就猜根因。

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

1. **澄清**：说明目标、已知约束和明确不做的事，让 `grill-with-docs` 对照现有代码、领域语言和 ADR 逐个挑战假设。
2. **固化**：用 `to-spec` 把已经聊清楚的内容整理为规格，不追加未讨论的功能。
3. **拆分**：用 `to-tickets` 拆成可独立验收的 tracer-bullet 垂直切片，并标出阻塞关系。
4. **实现**：用 `implement` 按规格或 tickets 推进；它在事先确认的测试边界上调用 `tdd`，并在结束前运行类型检查、单测与完整测试。
5. **审查**：`code-review` 从固定比较点同时检查代码是否符合项目规范，以及是否真正实现了原始规格。

### （1）什么是垂直切片

垂直切片按“用户可观察的行为”拆任务，而不是按技术层拆。例如，“用户能用正确账密登录并跳转首页”是一个可验收切片；“新增数据表”、“新增 API”、“新增 UI”只是水平分层，单独完成时往往无法验收。

## 2、Bug 修复

不要以“帮我修这个 Bug”开始猜解决方案，而是先提供观察到的行为、期望行为和现有复现步骤，让 Agent 调用 `diagnosing-bugs`。

成功标准是：

- 得到最小且稳定的复现方式。
- 通过日志、断言或小实验验证根因，而不是只凭阅读代码推测。
- 修复后增加能捕获原问题的回归测试。

## 3、旧资料中的命名变化

这组 Skills 更新很快。2026-07-15 核对官方主分支时，部分二手文章的名称已不再是当前主线名称：

| 旧资料名称 | 当前名称 | 用途 |
|---|---|---|
| `/to-prd` | `/to-spec` | 把当前对话和代码上下文整理成规格 |
| `/to-issues` | `/to-tickets` | 拆分垂直切片并记录依赖 |
| `/diagnose` | `/diagnosing-bugs` | 建立可复现、可验证的调试闭环 |
| `/review` | `/code-review` | 从项目规范与实现规格两条轴审查差异 |

> [!warning]
> 命令名和 Skill 列表可能继续变化。实际使用前应先查看当前安装的 Skill 目录或官方 README，不要完全照搬旧文章的命令。

## 4、使用边界

- **小任务不必走全流程**：一次性脚本或小文档修改可直接完成，否则流程成本可能高于实现成本。
- **不代替人的决策**：Skill 负责追问、记录和验证，产品取舍、架构边界和风险接受仍由人决定。
- **先适配再执行**：仓库源自 TypeScript/Node 工作流，其他技术栈、GitLab 或特殊测试体系可以复用原则，但应先调整命令、追踪器和测试边界。
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
