---
title: Matt Pocock Skills
date: 2026-07-15
tags: [AI, Skill, coding-tool, workflow]
aliases:
  - Matt Pocock Skills 工作流
  - Skills for Real Engineers
  - Matt Pocock Skills
---

# 一、概述

`mattpocock/skills` 是一组面向 Coding Agent 的工程工作流 Skill。

它不是自动开发框架，也不是几条提示词的合集，而是把需求澄清、规格记录、任务拆分、测试驱动、问题诊断和代码审查固化为可重复执行的流程。

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

注意，安装时会看到技能分为两组：

- Mattpocock Skills
- Other

使用时，大部分情况下使用的是  Mattpocock Skills，Other 下按需要选取。

这里安装选择  Mattpocock Skills 的所有技能。

![[assets/Pasted image 20260722015709.png|600]]

## 2、Claude Code 插件方式

如果不想自行维护 Skill 文件，可将它作为 Claude Code 插件安装：

```text
/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock
```

插件方式安装的是只读、跟随官方更新的完整 Skill 集；`skills.sh` 方式更适合希望针对项目裁剪和修改的团队。

# 三、项目初始化

安装时必须包含 `setup-matt-pocock-skills`，然后在每个准备使用这套工作流的项目中运行一次：

```text
/setup-matt-pocock-skills
```

它本质上是在为 Agent 建立一套**项目级工作约定**，让后续 Skill 明确：

- 规格和任务记录在哪里
- 任务使用哪些 Triage 状态
- 领域术语和架构决策从哪里读取
- 项目的 Agent 入口文件是 `AGENTS.md` 还是 `CLAUDE.md`。

它不会直接开始开发功能，也不会立即创建某个功能的规格和任务，而是先生成一组配置文档，，供 `grill-with-docs`、`to-spec`、`to-tickets`、`implement` 等后续 Skill 使用。

## 1、执行前提

最低前提只有三项：

- 已安装 `setup-matt-pocock-skills`。
- 在准备配置的项目目录中运行
- Agent 有权限读取和修改项目文件

即使当前目录还不是 Git 仓库，Skill 仍然可以执行探查并推荐本地 Markdown 模式。不过对于需要持续开发的代码项目，通常建议先初始化 Git：

```shell
git init
```

Git 是否初始化、是否存在远程仓库，主要影响任务追踪器的推荐结果，并不会决定 Skill 能否运行。

## 2、先探查项目现状

执行后，Skill 不会立即创建文件，而是先检查当前项目，例如：

- 是否配置了 GitHub 或 GitLab remote
- 是否已有 `AGENTS.md` 或 `CLAUDE.md` 是否已有 `CONTEXT.md` 或 `CONTEXT-MAP.md`
- 是否已有 `docs/adr/`、`docs/agents/`、`.scratch/`
- 是否安装了 triage Skill
- 项目是否具有 monorepo 特征

探查后会告诉你当前项目的现状，然后继续向下初始化。

![[assets/Pasted image 20260722021245.png|600]]

## 3、选择任务追踪器

第一项需要确认的是 `Issue Tracker`，也就是项目把规格、Bug 和任务记录在哪里。

> `Issue Tracker` 是用于记录需求、Bug、任务状态和依赖的系统。GitHub Issues、GitLab Issues、Linear 都属于 Issue Tracker。对于不依赖平台的个人项目，也可以直接用本地 Markdown 文件记录。

![[assets/Pasted image 20260722021516.png|600]]

常见选择包括：

|方式|保存位置|
|---|---|
|GitHub|当前仓库的 GitHub Issues|
|GitLab|当前仓库的 GitLab Issues|
|Local Markdown|项目的 `.scratch/` 目录|
|Other|Jira、Linear 或团队自定义系统|

Skill 会根据当前环境给出建议：

- remote 指向 GitHub：优先推荐 GitHub Issues。
- remote 指向 GitLab：优先推荐 GitLab Issues。
- 没有 remote：通常推荐 Local Markdown。
- 已存在 `.scratch/`：会将其视为项目可能已经采用本地任务模式的信号。

这里希望在本地管理相关文档，选择 Local Markdown 后，相关约定会写入：`docs/agents/issue-tracker.md`。

`issue-tracker.md`记录的不是具体任务，而是告诉其他 Skill：

> 当它们需要“发布到任务追踪器”或“读取某个任务”时，应该执行什么操作。

例如，GitHub 模式可能要求使用 `gh issue create`；本地模式则要求在 `.scratch/` 下创建 Markdown 文件。

本地 Markdown 结构：

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

其中：

- `.scratch/<feature>/spec.md` 保存该功能的规格。
- `.scratch/<feature>/issues/` 保存拆分后的实现任务。
- - 每个任务单独使用一个 Markdown 文件。
- 文件从 `01` 开始编号，并按照依赖顺序排列。
- 讨论和补充信息追加在文件末尾的 `## Comments` 下。

> [!note]
> `spec` 是 specification 的缩写，表示规格文档，重点描述“要实现什么、边界是什么、如何验收”。PRD 是 Product Requirements Document，即产品需求文档。在这套 Skills 中，两者有时会被作为接近的概念使用，但 `spec` 通常更贴近具体功能的可实现、可验收描述。

如果以后将项目关联到 GitHub 或 GitLab，可以修改：`docs/agents/issue-tracker.md`。也可以重新运行初始化流程，将任务追踪方式切换到远程 Issues。

一个普通任务（Issue）可能如下：

```markdown
# Validate preview app directory

What to build: 验证传入目录是否存在，并检查 manifest.json。

Blocked by: None — can start immediately

Status: ready-for-agent

## Acceptance criteria

- 目录不存在时返回明确错误。
- 缺少 manifest.json 时拒绝注册。
```

如果任务依赖其他任务，可以写成：

```markdown
Blocked by: 01, 02
```

表示当前任务需要等 `01` 和 `02` 完成后才能开始。

普通任务的 Triage 状态通常使用：

- needs-triage
- needs-info
- ready-for-agent
- ready-for-human
- wontfix

其中，由`to-tickets`拆分并确认可以交给 Agent 实现的任务，默认使用：

```markdown
Status: ready-for-agent
```

## 4、配置 Triage 状态

Triage 是对新任务进行分析、补充和分流的过程，也就是先判断：

- 信息是否完整
- Agent 是否可以直接完成
- 是否需要人工判断
- 是否决定不处理

只有安装了 `triage` Skill，初始化流程才会配置这一部分。如果没有安装，Skill 会跳过该步骤，也不会创建`docs/agents/triage-labels.md`。

![[assets/Pasted image 20260722021830.png|600]]

这里选择保持默认，默认有五种状态角色：

|状态|含义|
|---|---|
|`needs-triage`|新任务，尚未分析和分类|
|`needs-info`|信息不足，需要继续补充|
|`ready-for-agent`|信息完整，可以交给 Agent|
|`ready-for-human`|需要人工判断或处理|
|`wontfix`|决定不处理|

典型流程过程是：

![[assets/Pasted image 20260717145925.png|600]]



## 5、配置领域文档布局

接下来，Skill 会根据项目规模选择领域文档布局。

![[assets/Pasted image 20260722022141.png]]

由于当前没有`monorepo`信号，自动识别为单项目上下文`single-context`，因此需要在根目录创建：

```
CONTEXT.md 
docs/adr/
```

>[!notes]
> single-context 表示整个项目共享一套领域上下文。
> 项目术语和长期规则统一记录在根目录的 `CONTEXT.md` 中，架构决策统一保存在 `docs/adr/` 下。它适合大多数单体项目和中小型仓库。

对于大型`monorepo`，才可能使用多个上下文：

```
CONTEXT-MAP.md
packages/
├── ordering/
│   ├── CONTEXT.md
│   └── docs/adr/
└── billing/
    ├── CONTEXT.md
    └── docs/adr/
```

如果项目没有 workspace、多包目录或多个独立领域等 monorepo 信号，Skill 通常会直接采用 single-context，不再要求额外选择。

相关读取规则会写入`docs/agents/domain.md`。

这里需要注意：初始化流程创建的是**领域文档约定**，通常不会立即创建空的 `CONTEXT.md` 或 ADR。

`docs/agents/domain.md` 会告诉后续 Skill：

```
优先读取根目录 CONTEXT.md
优先读取 docs/adr/
这些文件不存在时静默继续，不将其视为错误
```

等项目真正形成稳定的领域术语或重要架构决策后，再按需创建和更新这些文档。

>[!note]
>ADR 是 Architecture Decision Record，即架构决策记录。它不描述“准备实现什么功能”，而是记录“做出了什么技术选择、为什么这样选择、考虑过哪些替代方案”。


## 6、选择 Agent 入口文件

完成前面的配置后，Skill 需要把这些约定链接到项目的 Agent 入口文件。

选择规则通常是：

1. 已存在 `CLAUDE.md`：更新 `CLAUDE.md`。
2. 没有 `CLAUDE.md`，但存在 `AGENTS.md`：更新 `AGENTS.md`。
3. 两者都不存在：询问用户创建哪一个。
4. 两者都存在：通常优先更新 `CLAUDE.md`。
5. 已存在 `## Agent skills`：更新原有章节，不重复追加。
6. 不覆盖文件中其他人工编写的内容。

如果项目同时需要兼容不同 Agent，可以要求 Agent 创建 `AGENTS.md`，再让 `CLAUDE.md` 指向它：

```
AGENTS.md
CLAUDE.md -> AGENTS.md
```

入口文件的内容通常如下：

```markdown
## Agent skills

### Issue tracker

Issue 使用 `.scratch/<feature-slug>/` 下的本地 Markdown 文件管理。详见 `docs/agents/issue-tracker.md`。


### Triage labels

Triage 使用默认五个标准标签。详见 `docs/agents/triage-labels.md`。


### Domain docs

本仓库使用 single-context 领域文档布局。详见 `docs/agents/domain.md`。
```

## 7、初始化完成后的文件

最后，Agent 会给出完整的配置草稿，供你审阅。

![[assets/Pasted image 20260722022550.png|600]]

例如这里采用 Local Markdown、默认 Triage 标签和 single-context 后，项目中通常会新增：

```
project/
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
└── docs/
    └── agents/
        ├── issue-tracker.md
        ├── triage-labels.md
        └── domain.md
```

此时可能还没有：

```
.scratch/
CONTEXT.md
docs/adr/
```

这是正常现象：

- `.scratch/` 会在真正创建第一个本地规格或任务时出现。
- `CONTEXT.md` 会在形成需要长期保存的领域知识时出现。
- `docs/adr/` 会在产生需要记录的架构决策时出现。

因此，初始化的重点不是提前创建所有空目录，而是先确定后续 Skill 应该遵守什么规则。

# 四、Skills 的整体结构

## 1、用户调用与模型调用

这套 Skills 可以按照触发方式分为两类：

| 类型    | 如何触发                 | 主要作用               |
| ----- | -------------------- | ------------------ |
| 用户调用型 | 用户主动输入 `/skill-name` | 选择并组织完整工作流         |
| 模型调用型 | Agent 自动匹配，或用户显式点名   | 提供测试、诊断、建模和审查等工程纪律 |

用户调用型 Skill 只能由用户主动启动。例如：

```
/grill-with-docs
/to-spec
/to-tickets
/implement
```

模型调用型 Skill 既可以由用户显式点名，也可以在任务符合条件时由 Agent 自动使用。例如：

```
tdd
diagnosing-bugs 
code-review 
domain-modeling 
codebase-design
```

用户调用型 Skill 主要负责**编排流程**，模型调用型 Skill 主要负责**在流程内部按特定工程方法做事**。

例如，用户执行：

```
/implement
```

`implement` 在实现过程中可以进一步使用：

```
tdd
code-review
codebase-design
```

注意：

- 用户调用型 Skill 可以在内部使用模型调用型 Skill
- 用户调用型 Skill 之间通常不会相互直接调用
- 不需要记住所有 Skill，可以通过`/ask-matt`判断该从哪里开始

因此，不必把每个 Skill 都理解成一条彼此独立的命令。更准确的理解是：

> 用户调用型 Skill 负责选择和推进工作流，模型调用型 Skill 负责为工作流提供可复用的工程纪律。

需要注意，用户调用型 Skill 可以调用模型调用型 Skill，但不会继续调用另一个用户调用型 Skill。这样可以确保流程中的关键切换仍然由用户控制。

## 2、/ask-matt：工作流路由器

当不知道当前应该使用哪个 Skill 时，可以执行：

```
/ask-matt
```

然后描述自己当前遇到的情况，例如：

```
我现在有个新功能想法，但需求还比较模糊
```

```
我收到一个描述不完整的 GitHub Issue。
```

```
这个 Bug 偶尔出现，目前还无法稳定复现。
```

```
我要规划一个跨越多个模块的大型功能。
```

`ask-matt` 本身不会编写代码，也不会直接生成规格。它主要负责判断：

- 当前属于哪类任务
- 应该从哪个 Skill 开始
- 后面可能经过哪些步骤
- 哪些步骤可以省略
- 当前任务适合使用哪条工作路径

它相当于整套 Skills 的**工作流路由器**。

## 3、四条主要工作路径

常见的开发任务可以归纳为四条主要路径：

![[assets/Pasted image 20260717153707.png|600]]

### （1）新功能

```
grill-with-docs(澄清需求)
      ↓
to-spec(形成规格)
      ↓
to-tickets(拆分任务)
      ↓
implement(逐个实现)
   ├── tdd
   └── code-review
```

这条路径适合从一个尚未完全明确的新功能想法开始。

各阶段分别解决不同问题：

|阶段|解决的问题|
|---|---|
|`grill-with-docs`|需求究竟是什么|
|`to-spec`|如何将确认结果整理成正式规格|
|`to-tickets`|如何将规格拆成可独立实现的任务|
|`implement`|如何完成其中一个任务|
|`tdd`|如何用快速反馈驱动实现|
|`code-review`|如何检查实现质量和规格完成度|

`grill`即盘问和拷问的意思，如果只是想与 AI 探讨交流，可以选择`grill-me` skill，如果想在澄清需求的同时生成文档，选择`grill-with-docs`。

例如当前项目通过纯前端（HTML + CSS + 原生JS）实现了一个带优先级的待办事项应用。现在想增加一个数据导入和导出的功能：

![[assets/Pasted image 20260722024056.png|600]]

调用`grill-with-docs`，Agent 就开始逐个问题询问并提供一些选项供我们选择。

经过几轮询问后，需求会基本实现。

> `grill-with-docs` 和 superpowers 的`brainstorming`的区别：
> `brainstorming` 倾向于尽快对话完生成文档，`grill-with-docs`倾向于把问题问清楚，可能涉及非常多的轮数，适合需求模糊时深入沟通。
> 实际开发时，可以先使用`grill-with-docs`生成一个详细文档，再使用`brainstorming` 做一个更好地补充。

并非所有新功能都必须完整经过每一个步骤。如果功能很小，Agent 可能经过需求澄清后直接提示开始执行，这里的工作流就简化为：

```
grill-with-docs
      ↓
implement
```

当然，这里为了演示，要求 Agent 生成文档。新版 `mattpocock/skills` 中，旧的 `to-issues` 和 `to-prd` 已被当前工作流里的 `to-tickets` 和 `to-spec` 取代：如果任务比较小，可以直接用 `to-tickets` 拆成可执行任务；如果任务比较复杂，则先用 `to-spec` 生成规格文档，再用 `to-tickets` 拆分任务。

### （2）外部 Issue

```
triage
   ↓
implement
```

这条路径适合处理从外部进入任务追踪器的原始 Issue，例如：

- 用户提交的 Bug
- 团队成员创建的功能请求
- 客服转交的问题
- 临时记录但尚未整理的想法
- 信息不完整的 GitHub Issue
- 尚未分析的 Pull Request

这些 Issue 没有经过当前开发流程的需求澄清，因此不能默认认为它们已经适合交给 Agent。

`triage` 会先判断：

- 问题是否真实存在
- 信息是否足够
- 是否能够稳定复现
- 是否属于当前项目范围
- 是否已有重复 Issue
- 是否可以由 Agent 直接处理
- 是否需要人工作出产品或架构决策

完成分析后，Issue 会进入相应状态：

```
needs-triage
      │
      ├── 信息不足 ──> needs-info
      ├── Agent 可完成 ──> ready-for-agent
      ├── 需要人工处理 ──> ready-for-human
      └── 不准备处理 ──> wontfix
```

只有进入：

```
ready-for-agent
```

之后，才适合交给 `implement`。

> [!note]  
> `to-tickets` 生成的任务不需要再执行 `triage`。
> 
> 因为这些任务已经经过：
> 
> ```
> grill-with-docs
>       ↓
> to-spec
>       ↓
> to-tickets
> ```
> 
> 需求、范围、依赖和验收条件已经确认，所以通常会直接标记为：
> 
> ```
> Status: ready-for-agent
> ```

### （3）疑难 Bug

```
diagnosing-bugs
       ↓
implement / 架构改进
```

这条路径适合难以直接定位的问题，例如：

- Bug 偶尔出现
- 测试随机失败
- 性能突然下降
- 修复后问题反复出现
- 报错位置和真正原因相距很远
- 只有某些环境或输入能够触发
- 已经尝试多种修改，但都无法确认是否解决根因

面对这类问题，不应该立即猜测原因并修改代码。

正确顺序是：

```
稳定复现
    ↓
缩小问题范围
    ↓
提出可验证的假设
    ↓
增加日志或观测点
    ↓
验证假设
    ↓
定位根因
    ↓
编写回归测试
    ↓
实施修复
```

`diagnosing-bugs` 的重点不是“尽快给出一个看起来合理的修改”，而是先建立稳定反馈循环：

```
问题存在  →  测试失败
问题修复  →  测试通过
```

只有能够稳定判断问题是否存在，Agent 才能可靠地验证修复。

诊断结束后可能有两种结果：

```
定位到局部实现错误
        ↓
implement
```

或者：

```
发现模块边界、接口或职责存在问题
        ↓
架构改进
```

例如，一个 Bug 总是难以测试，可能不是测试工具的问题，而是代码缺少稳定的模块边界。此时需要先改善架构中的测试 seam，再完成修复。

### （4）大型模糊项目

```
wayfinder
    ↓
to-spec
    ↓
to-tickets
    ↓
implement
```

这条路径适合大型、跨模块、单个会话难以规划清楚的项目，例如：

- 从零设计一个大型系统
- 将单体应用拆分成多个服务
- 重写核心渲染架构
- 设计跨越多个业务领域的新功能
- 同时涉及产品、数据模型、接口和迁移策略
- 目标大致明确，但实现路线仍然充满未知

普通的 `grill-with-docs` 适合在一个相对可控的范围内逐步澄清需求。

但对于大型项目，未知问题可能太多：

```
目标
 ├── 领域边界尚未确定
 ├── 数据迁移方案未知
 ├── 技术选型尚未完成
 ├── 部署方式需要调查
 ├── 兼容性边界尚未确认
 └── 多个团队责任不明确
```

如果直接生成一个巨大 Spec，里面往往会包含大量未经验证的假设。

`wayfinder` 会先将这些未知问题整理为多个**决策任务**：

```
大型模糊目标
      ↓
识别关键未知问题
      ↓
创建 Decision Ticket
      ↓
逐个调查和确认
      ↓
形成清晰实施路线
```

例如：

```
Decision 01：确认旧数据迁移策略
Decision 02：验证新存储方案的性能
Decision 03：确定模块责任边界
Decision 04：选择向后兼容方案
```

这些任务主要用于消除不确定性，不一定直接产生正式功能代码。

等关键决策完成后，再进入：

```
to-spec
   ↓
to-tickets
   ↓
implement
```

因此，`wayfinder` 可以理解为：

> 在大型项目正式编写规格之前，先绘制一张从未知状态走向可实施状态的决策地图。

## 4、其他重要 Skill

除了四条主路径，Matt Pocock Skills 里还有一些不一定出现在固定流程图中、但很值得单独掌握的 Skill。它们通常用于回答某个具体工程问题，而不是直接承担“从需求到上线”的完整路径。

### （1）prototype

`prototype` 的定位是：

> 用可丢弃代码回答一个设计问题。

它不是“先做一个简化版产品”，也不是正式实现的第一阶段，而是当讨论已经不足以判断方向时，用一个可运行结果验证关键未知问题。

适合使用 `prototype` 的场景包括：

- 想确认一个状态模型跑起来是否符合直觉
- 想比较几种 UI 或交互布局
- 想验证某个边界流程会不会让用户迷路
- 想观察一个复杂逻辑在多种输入下如何变化
- 想在投入正式实现前确认技术方案是否可行

`prototype` 会先判断问题属于哪一类：

|问题类型|原型形态|
|---|---|
|逻辑、状态机、流程规则是否合理|小型命令行或本地交互原型，重点暴露每一步的完整状态|
|页面、组件、交互视觉应该长什么样|多个 UI 变体，通常用 URL 参数或切换控件快速对比|

使用时，最好把要回答的问题说清楚，而不是只说“做个 prototype”：

```text
用 prototype 验证一下导入/导出任务的状态模型是否合理，重点看失败重试、重复导入和撤销流程。
```

```text
用 prototype 做三个数据导入面板的 UI 变体，我想比较分步向导、单页表单和拖拽上传三种交互。
```

`prototype` 的关键约束：

- 从第一天起就是可丢弃代码，文件名和位置要能看出它不是生产实现。
- 必须提供一个简单命令运行，例如 `pnpm prototype` 或 `python prototype_xxx.py`。
- 默认不做持久化，状态尽量放在内存里。
- 不追求测试、抽象和完整错误处理，只保留让原型能跑起来的最小代码。
- 每次交互后要暴露关键状态，让人能判断设计是否成立。
- 验证完成后，把结论写回 Issue、Spec 或实现任务；主分支只保留被验证后的正式决策，不保留原型代码。

可以把 `prototype` 理解为正式工作流旁边的一次低成本试错：

```
未知问题
   ↓
prototype
   ↓
形成结论
   ↓
回到 to-spec / to-tickets / implement
```

### （2）improve-codebase-architecture

`improve-codebase-architecture` 用来扫描代码库中的架构摩擦，找出可以让模块变得更“深”的重构机会。

这里的“深模块”不是指代码更多，而是指：

> 对外接口简单，内部承担了足够多的复杂性，因此未来修改更集中、更容易测试，也更容易让 Agent 理解。

它关注的问题包括：

- 理解一个概念是否需要在很多小文件之间来回跳转
- 某些模块是否过于浅，接口复杂度几乎等于实现复杂度
- 是否为了测试抽出了很多纯函数，但真正的错误仍藏在调用关系里
- 模块之间的 seam 是否模糊，导致职责互相泄漏
- 哪些区域缺少稳定测试面，导致修改时很难判断是否破坏行为

`improve-codebase-architecture` 的典型流程是：

```
选择扫描范围
   ↓
阅读 CONTEXT.md 和相关 ADR
   ↓
扫描代码热点和架构摩擦
   ↓
生成 HTML 架构报告
   ↓
选择一个候选重构方向
   ↓
进入 grilling / codebase-design 继续追问和细化
```

这个 Skill 不会一上来就直接改代码。它会先生成一个可视化 HTML 报告，每个候选项通常包含：

- 涉及哪些文件和模块
- 当前架构为什么造成摩擦
- 可以如何调整模块责任或接口
- 这样做如何改善 locality、leverage 和测试面
- 重构前后的结构图
- 推荐强度，例如 `Strong`、`Worth exploring`、`Speculative`

它特别适合在以下时机使用：

- 某个区域最近频繁修改，每次改动都牵连很多文件
- Bug 很难测试，怀疑不是测试写得差，而是模块边界不合适
- 代码里存在很多“为了复用而抽象”的薄封装，但没有真正降低复杂度
- 想在做大功能前先识别哪些模块需要加深
- 想让代码库更适合 Agent 长期维护

使用时可以给出范围，让它不要漫无边际扫描：

```text
用 improve-codebase-architecture 看一下订单导入这块有没有模块加深的机会，重点关注测试难、状态分散和接口泄漏。
```

```text
用 improve-codebase-architecture 扫一下最近经常改动的区域，给我一个架构改进候选报告。
```

它和 `codebase-design` 的关系是：

- `improve-codebase-architecture` 更像发现问题和生成候选报告。
- `codebase-design` 更像深入设计某个具体模块接口和 seam。

所以常见组合是：

```
improve-codebase-architecture
      ↓
选择候选项
      ↓
codebase-design / grilling
      ↓
to-spec / to-tickets / implement
```

### （3）diagnosing-bugs

`diagnosing-bugs` 用来处理普通“看代码猜原因”很容易失败的问题，例如难复现 Bug、随机失败、性能回退、环境相关错误、修复后反复出现的问题。

它的核心纪律是：

> 先建立能抓住这个 Bug 的反馈循环，再谈定位和修复。

这里的反馈循环不是“测试能跑”，而是必须满足：

- 能触发用户描述的具体问题
- 能在 Bug 存在时变红，在修复后变绿
- 尽量快速，最好是几秒级
- 尽量确定，随机 Bug 也要把复现率提高到足以调试
- Agent 可以反复运行，不依赖大量人工操作

常见反馈循环包括：

|场景|反馈方式|
|---|---|
|业务逻辑错误|写一个能失败的单元测试或集成测试|
|接口行为异常|用 `curl` 或 HTTP 脚本复现请求|
|命令行工具输出错误|准备 fixture 输入，对比 stdout 或快照|
|前端交互 Bug|用 Playwright 或 Puppeteer 驱动页面并断言 DOM、控制台或网络|
|线上偶发问题|保存真实请求、日志、事件流或 HAR 文件，再离线回放|
|版本间回退|用 bisect 或差分脚本比较新旧版本行为|

`diagnosing-bugs` 的完整流程可以概括为：

```
建立红绿反馈循环
      ↓
复现并最小化场景
      ↓
提出 3-5 个可证伪假设
      ↓
逐个增加观测点验证
      ↓
写回归测试
      ↓
修复并重新运行原始复现
      ↓
清理调试代码并总结根因
```

使用时，最好把症状、复现条件和已尝试过的修复都说出来：

```text
用 diagnosing-bugs 调试这个导入失败问题。现象是 CSV 有重复行时偶尔卡住，刷新后任务状态停在 processing，没有错误提示。
```

```text
用 diagnosing-bugs 看一下最近的性能回退。列表页从 300ms 变成 2s，怀疑和筛选条件或数据库查询有关。
```

`diagnosing-bugs` 有几个重要习惯：

- 在没有红绿反馈循环之前，不急着改代码。
- 复现后要继续最小化场景，删掉不必要的输入、配置和步骤。
- 不只提出一个原因，而是列出多个可证伪假设，并说明每个假设预期看到什么现象。
- 临时日志要有唯一前缀，例如 `[DEBUG-a4f2]`，方便最后全部清理。
- 性能问题优先建立基线和测量方式，而不是靠日志猜。
- 修复后要重新跑最初的复现场景，确认修的是同一个 Bug。

如果最终发现没有合适位置写回归测试，这本身就是一个架构信号：当前模块可能缺少可测试 seam。此时可以把诊断结论交给 `improve-codebase-architecture`，继续分析是否需要加深模块或调整接口。

### （4）research

`research` 适合在工程决策依赖外部资料时使用，例如框架选型、API 行为、迁移方案、兼容性边界等。

它的重点不是随口搜索答案，而是：

- 优先查高可信来源
- 保留来源链接
- 把结论写成 Markdown 文件
- 明确哪些是事实、哪些是推断、哪些仍然不确定

当一个决策会影响后续架构、依赖或开发计划时，先用 `research` 留下一份可回看的调查记录，比直接在对话里得到一个结论更稳。

### （5）domain-modeling

`domain-modeling` 用来沉淀项目里的领域语言。它会把关键概念、实体、规则和术语写入 `CONTEXT.md`，让后续 Agent 不必每次重新猜测这些词是什么意思。

适合使用它的场景包括：

- 需求讨论中出现了新的核心术语
- 同一个概念在代码、产品和用户口径里有不同叫法
- 某个模块应该用业务概念命名，而不是用技术细节命名
- 架构改进需要先确认领域边界

在 Matt Pocock Skills 里，`domain-modeling` 经常被 `grill-with-docs`、`improve-codebase-architecture` 等流程调用，用来保证项目长期上下文不会只留在一次聊天里。

### （6）handoff

`handoff` 用来把当前会话压缩成一份交接文档，让另一个 Agent 或下一次会话能够接着工作。

它适合处理这种情况：

- 当前对话已经很长，后续工作需要换一个新会话继续
- 已经做了大量调查、讨论或局部修改，需要把上下文交给下一个 Agent
- 想把“接下来该怎么做”整理成清晰的接力说明
- 当前任务中有多个文件、决策、未完成事项，担心后续遗漏

`handoff` 生成的不是项目文档，而是临时交接材料。它会保存到系统临时目录，而不是当前代码仓库，避免把一次会话的中间状态污染到项目里。

一份好的 handoff 通常包含：

- 当前任务目标
- 已经完成了什么
- 关键决策和原因
- 相关文件、Issue、Spec、ADR 或提交链接
- 还没有完成的事项
- 下一位 Agent 建议使用哪些 Skill
- 需要注意的风险或约束

`handoff` 不应该重复复制已经存在于其他正式文档里的内容。如果某个结论已经写进 Spec、ADR、Issue、提交或代码 diff，交接文档只需要引用路径或链接。

使用示例：

```text
用 handoff 总结一下当前会话，下一次主要继续实现导入导出功能的 to-tickets。
```

```text
用 handoff 做一份交接，下一位 Agent 需要继续诊断这个性能回退，并优先使用 diagnosing-bugs。
```

使用 `handoff` 时还要注意：

- 不写入仓库，只生成临时交接文档。
- 不记录 API key、密码、个人隐私等敏感信息。
- 如果用户说明了下一次会话的重点，交接文档会围绕这个重点组织。
- 它适合会话切换，不适合替代正式 Spec、Issue 或 ADR。

### （7）teach

`teach` 用来把当前目录变成一个长期教学工作区，让 Agent 围绕某个主题持续教用户学习。

它不是普通问答，也不是一次性解释概念，而是把学习过程拆成多个可积累的材料：

- `MISSION.md`：记录为什么要学这个主题
- `RESOURCES.md`：记录可继续阅读或观看的高质量资源
- `lessons/`：保存一节节短小、可交互的 HTML 课程
- `reference/`：保存速查表、术语表、算法图、流程卡片等参考材料
- `learning-records/`：记录用户已经学到的关键经验和认知变化
- `assets/`：保存课程共用的样式、组件、测验控件或图表工具
- `NOTES.md`：记录用户的学习偏好和临时教学笔记

`teach` 的重点是让知识真正留下来。它会关注两件事：

- Fluency strength：当下能不能顺利想起来和用出来。
- Storage strength：过一段时间后还能不能保留和迁移。

因此，`teach` 不只是讲解，还会设计练习、回忆、测验和反馈循环，避免用户产生“刚听懂就以为掌握了”的错觉。

适合使用 `teach` 的场景包括：

- 想系统学习一个技术、工具、框架或理论
- 想让 Agent 持续按自己的目标安排课程
- 想把学习过程沉淀成可回看的 HTML 课程和参考文档
- 想通过测验、练习和反馈来建立长期记忆
- 想让后续会话知道自己已经学到哪里

使用示例：

```text
用 teach 教我 TypeScript 类型体操，我的目标是能读懂复杂泛型库的类型定义。
```

```text
用 teach 带我学习 Matt Pocock Skills，重点是我能在真实项目里判断什么时候用哪个 skill。
```

`teach` 的工作方式通常是：

```
确认学习使命
   ↓
收集高可信资源
   ↓
生成短小 lesson
   ↓
加入练习和反馈
   ↓
沉淀 reference 与 learning-records
   ↓
根据学习记录安排下一课
```

使用 `teach` 时，最重要的是先说明为什么要学。学习目标越贴近真实任务，课程越容易控制难度，也越容易落到能用的技能上。

## 5、主流程与入口流程

四条路径不是四套完全独立的开发体系，可以理解为：

![[assets/Pasted image 20260717155653.png|600]]

`grill-with-docs` 是“带文档沉淀的需求拷问/澄清流程”，适合在有代码库的前提下，把一个想法从模糊状态压到足够明确，后续可进入 `/to-spec`、`/to-tickets` 或 `/implement`。

它会做三件事：

- 用 `/grilling` 的方式一轮只问一个关键问题，逐步逼近共同理解
- 用 `/domain-modeling` 维护领域语言：如果出现关键术语，会及时沉淀到 `CONTEXT.md`；如果出现重要且难回退的架构决策，才建议写 ADR。
- 不会直接动手实现。只有你确认“我们已经达成共同理解”后，才进入后续实现或拆票流程。



## 6、底层工程纪律

除了上层工作流，这套 Skills 还提供了一些可以被其他流程复用的底层能力：

| Skill             | 作用               |
| ----------------- | ---------------- |
| `grilling`        | 逐个追问尚未解决的关键决策    |
| `domain-modeling` | 提取领域概念、术语、实体和规则  |
| `codebase-design` | 分析模块、接口、责任和 seam |
| `tdd`             | 用测试驱动一个垂直切片的实现   |
| `diagnosing-bugs` | 建立稳定复现和根因诊断流程    |
| `code-review`     | 检查代码标准和规格完成度     |
| `research`        | 调查外部资料并保留来源      |
| `prototype`       | 通过可丢弃实现验证未知问题    |
| `improve-codebase-architecture` | 发现模块加深和架构改进机会 |
| `handoff`         | 生成下一次会话可接手的交接文档 |
| `teach`           | 建立长期教学工作区并持续产出课程 |

这些 Skill 通常不会决定“整个项目下一步做什么”，而是负责回答更具体的问题：

- 需求还不清楚  ->  `grilling`
- 领域概念混乱 -> `domain-modeling`
- 不知道在哪里测试 -> `codebase-design`
- 行为已经明确，需要实现 -> `tdd`
