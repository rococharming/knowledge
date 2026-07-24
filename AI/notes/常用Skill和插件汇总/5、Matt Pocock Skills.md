---
title: Matt Pocock Skills
date: 2026-07-22
tags: [AI, Skill, coding-tool, workflow]
aliases:
  - Matt Pocock Skills 工作流
  - Skills for Real Engineers
  - Matt Pocock Skills
---

# 一、概述

`mattpocock/skills` 是一套面向 Coding Agent 的工程工作流 Skill。它不负责“让模型更聪明”，而是把真实软件开发中反复需要的需求澄清、规格沉淀、任务拆分、测试反馈、Bug 诊断和代码审查拆成小而可组合的流程。

它的核心判断是：

> Coding Agent 的主要风险不是不会写代码，而是会在需求不清、反馈不足和工程约束缺失时，更快地写出偏离目标的代码。

这套 Skills 主要解决四类问题：

- **需求偏差**：实现前先把目标、边界和决策问清楚。
- **语言混乱**：把项目术语写入 `CONTEXT.md`，把重要技术选择写入 ADR（Architecture Decision Record，架构决策记录）。
- **反馈不足**：通过类型检查、自动测试、可复现脚本和审查循环，让 Agent 能判断自己是否真的做对。
- **架构腐化**：用小规格、垂直切片、模块设计和架构扫描，避免代码库越改越难理解。

垂直切片就是把一个大需求拆成多个“能单独跑通、单独验收”的小功能。例如登录功能可以拆成“正确账号密码能登录”和“密码错误时显示提示”，每个切片都包含它需要的少量页面、接口和数据处理；不要拆成“先做页面、再写接口、最后建表”，因为这些任务单独完成时不能真正验收。

截至 2026-07-22，`mattpocock/skills` 版本为 `1.1.0`。这一版里，`ask-matt` 已补齐对 `tdd`、`diagnosing-bugs`、`domain-modeling`、`codebase-design`、`grilling` 等 Skill 的路由；`review` 已改为 `code-review`；`to-prd` 和 `to-issues` 已进入当前的 `to-spec` / `to-tickets` 工作流；`wayfinder`、`research`、`prototype` 等也成为主集合的一部分。

# 二、安装

## 1、复制到项目

如果希望把 Skill 文件复制到自己的项目里，便于阅读、修改和团队定制，可以使用：

```shell
npx skills@latest add mattpocock/skills
```

安装时至少选择：

```text
setup-matt-pocock-skills
```

日常使用通常还会选择 Engineering 分组里的核心 Skill，例如 `ask-matt`、`grill-with-docs`、`to-spec`、`to-tickets`、`implement`、`triage`、`diagnosing-bugs`、`tdd`、`code-review`、`domain-modeling`、`codebase-design`、`wayfinder` 和 `research`。

![[assets/Pasted image 20260722015709.png|600]]

复制安装的特点是：Skill 进入项目后可以按团队规则修改，但后续版本变化需要自己同步。

## 2、Claude Code 插件

如果只想使用随版本更新的托管包，可以在 Claude Code 中安装插件：

```text
/plugin marketplace add mattpocock/skills
/plugin install mattpocock-skills@mattpocock
```

也可以在 shell 中执行：

```shell
claude plugin marketplace add mattpocock/skills
claude plugin install mattpocock-skills@mattpocock
```

插件安装的特点是：整体 Skill 集保持只读并跟随发布版本更新，适合不想维护本地副本的场景。

# 三、项目初始化

## 1、初始化入口

安装完成后，每个准备使用这套工作流的仓库都要运行一次：

```text
/setup-matt-pocock-skills
```

它做的不是创建某个功能需求，而是先确定项目级约定：

- Issue tracker（任务追踪器）用 GitHub、Linear、GitLab、Local Markdown 还是其他系统。
- Triage（任务分流）使用哪些状态标签。
- 项目长期上下文写在哪里，例如 `CONTEXT.md`、`docs/adr/` 或 monorepo 的多上下文布局。
- Agent 入口文件使用 `AGENTS.md` 还是 `CLAUDE.md`。

## 2、任务追踪器

Issue tracker 是记录需求、Bug、任务状态和依赖的地方。对于个人项目，Local Markdown 通常已经够用：规格和任务可以放在 `.scratch/<feature>/` 下；对于多人协作，则更适合接入 GitHub、GitLab 或 Linear。

![[assets/Pasted image 20260722021516.png|600]]

## 3、Triage 状态

Triage 是对新任务进行分析、补充和分流的过程。它先判断信息是否完整、Agent 能否处理、是否需要人工判断，以及是否决定不处理。

![[assets/Pasted image 20260722021830.png|600]]

默认状态通常可以理解为：

| 状态 | 含义 |
|---|---|
| `needs-triage` | 新任务，尚未分析和分类 |
| `needs-info` | 信息不足，需要继续补充 |
| `ready-for-agent` | 信息完整，可以交给 Agent |
| `ready-for-human` | 需要人工判断或处理 |
| `wontfix` | 决定不处理 |

典型分流过程如下：

![[assets/Pasted image 20260717145925.png|600]]

## 4、领域文档

领域文档决定项目术语、长期上下文和架构决策写在哪里。单项目通常使用根目录 `CONTEXT.md` 和 `docs/adr/`；monorepo 才更可能按包或业务域拆多个上下文。

![[assets/Pasted image 20260722022141.png|600]]

初始化之后，常见项目结构可以长这样：

```text
project/
├── AGENTS.md
├── docs/
│   └── agents/
│       ├── issue-tracker.md
│       ├── triage-labels.md
│       └── domain.md
└── .scratch/
    └── <feature>/
        ├── spec.md
        └── issues/
```

![[assets/Pasted image 20260722022550.png|600]]

`.scratch/`、`CONTEXT.md` 和 `docs/adr/` 不一定会立刻出现。

- `.scratch/` 通常在第一次创建本地规格或任务时出现。
- `CONTEXT.md` 通常在项目形成需要长期保存的领域术语、规则或上下文时出现。
- `docs/adr/` 通常在产生需要记录的重要架构决策时出现。

初始化的重点不是提前创建所有空目录，而是先让后续 Skill 知道这些内容应该写到哪里、按什么规则读写。

# 四、工作原理

## 1、两类 Skill

Matt Pocock Skills 按触发方式分成两类：

| 类型 | 触发方式 | 职责 |
|---|---|---|
| 用户调用型 | 用户输入 `/skill-name` | 编排完整工作流 |
| 模型调用型 | Agent 按任务自动使用，或用户显式点名 | 提供可复用工程纪律 |

用户调用型 Skill 像“流程入口”。常见例子：

- `ask-matt`：不知道该从哪里开始时，用它选择路径。
- `grill-with-docs`：深度澄清需求，同时沉淀项目术语和架构决策。
- `to-spec`：把已讨论清楚的内容整理成规格。
- `to-tickets`：把规格或计划拆成带依赖关系的可执行任务。
- `implement`：按规格或任务实现，并在实现中驱动测试和审查。
- `triage`：处理外部进入的 Issue 或 Pull Request。
- `wayfinder`：面对超出单次会话承载的大型目标时，先把未知问题拆成调查和决策任务。

模型调用型 Skill 像“工程方法”。常见例子：

- `tdd`：用 red → green 的反馈循环实现功能或修 Bug。
- `diagnosing-bugs`：先复现、最小化、提出可证伪假设，再修复。
- `code-review`：从代码标准和规格完成度两个角度审查差异。
- `codebase-design`：围绕模块、接口、深模块和 seam（测试或设计边界）改进设计。

用户调用型 Skill 可以使用模型调用型 Skill，但通常不会继续调用另一个用户调用型 Skill。这样可以避免流程失控：关键阶段切换仍由用户决定。

## 2、主路径

日常开发可以先记住四条路径。图里的 `ask-matt` 没有单独画出来，因为它是路由器：不确定入口时先用它，已经确定场景时可以直接调用对应 Skill。

![[assets/Matt Pocock Skills - four workflows.png|600]]

第一条是新功能：

```text
grill-with-docs
  ↓
to-spec
  ↓
to-tickets
  ↓
implement
  ├── tdd
  └── code-review
```

需求很小时，不一定需要完整走完。例如一个边界清楚的小修复，可能只需要 `grill-with-docs` 后直接 `implement`。`to-spec` 和 `to-tickets` 的价值在于留下可复查的规格与任务边界，不是为了制造流程。

第二条是外部 Issue：

```text
triage
  ↓
implement
```

外部 Issue 往往信息不完整。`triage` 会先判断它是否真实、是否可复现、是否属于当前项目、是否需要人工决策，以及是否能交给 Agent。只有状态进入 `ready-for-agent`，才适合继续实现。

第三条是疑难 Bug：

```text
diagnosing-bugs
  ↓
implement / codebase-design
```

疑难 Bug 的重点不是先猜一个修复，而是先建立反馈循环：

```text
Bug 存在  →  检查失败
Bug 修复  →  检查通过
```

如果问题暴露的是模块边界差、测试面不稳定或职责混乱，就不要只补表层逻辑，而应转入 `codebase-design` 或 `improve-codebase-architecture`。

第四条是大型模糊项目：

```text
wayfinder
  ↓
decision map
  ├── research
  ├── prototype
  └── grilling
  ↓
to-spec / implement
```

`wayfinder` 适合一个会话放不下、路线仍然有雾的大目标。它默认是“计划，不是执行”：先命名 destination（目标终点），再把未知问题整理成 decision tickets（决策任务），通过 `research`、`prototype`、`grilling`、`domain-modeling` 等方式逐个消除不确定性。

等关键未知被消除后，才进入普通开发流：如果路线已经足够清楚，可以交给 `to-spec` 形成规格；如果最后发现事情很小，也可能直接实现。它不是固定的 `wayfinder → to-spec → to-tickets → implement` 流水线。

## 3、上下文沉淀

这套 Skills 的一个重点是：不要把关键知识只留在聊天里。

常见沉淀位置包括：

| 文件 | 保存内容 |
|---|---|
| `CONTEXT.md` | 项目术语、领域模型、长期规则 |
| `docs/adr/` | 架构决策、替代方案和取舍 |
| `.scratch/<feature>/spec.md` | 某个功能的规格 |
| `.scratch/<feature>/issues/` | 按依赖拆开的实现任务 |

这样做的收益是：下一次会话、另一个 Agent 或团队成员进入项目时，不必重新从聊天记录里猜“这个词是什么意思”“为什么当时选了这个方案”“这个任务为什么不能并行”。

# 五、实践指南

## 1、先用 ask-matt 找入口

不熟悉这套 Skills 时，不需要背完整命令表。先用：

```text
/ask-matt
```

然后描述当前情况：

```text
我有一个功能想法，但范围还不清楚。
```

```text
我收到一个信息不完整的 Issue。
```

```text
这个 Bug 偶尔出现，暂时无法稳定复现。
```

```text
我要规划一个跨多个模块的大改造。
```

`ask-matt` 的作用是路由，不是替你完成所有工作。它会告诉你该从哪条路径开始，以及哪些步骤可以省略。

## 2、grill-me 和 grill-with-docs

`grill-me` 和 `grill-with-docs` 都用于需求澄清，区别在于是否面向代码项目沉淀长期上下文。

| Skill | 适合场景 | 产物 |
|---|---|---|
| `grill-me` | 非代码计划、想法讨论、个人决策、轻量方案澄清 | 对话中的共同理解 |
| `grill-with-docs` | 代码项目的新功能、架构选择、需求边界不清的问题 | 共同理解 + `CONTEXT.md` / ADR 等项目文档更新建议 |

如果只是想和 Agent 把一个想法聊清楚，用 `grill-me` 更轻。如果是在仓库里准备开发功能，用 `grill-with-docs` 更合适：它会先读项目上下文，再逐个确认关键决策，并在需要时更新 `CONTEXT.md` 或建议记录 ADR。

![[assets/Pasted image 20260722024056.png|600]]

`grill-with-docs` 比普通讨论更适合需求模糊的新功能。它不会一上来就写代码，而是先把“要做什么、边界是什么、哪些决策还没定”问清楚。

## 3、新功能流程

新功能是最能体现这套 Skills 价值的场景。完整链路是：

```text
grill-with-docs
  ↓
to-spec
  ↓
to-tickets
  ↓
implement
  ├── tdd
  └── code-review
```

每个 Skill 解决的问题不同：

| Skill | 解决的问题 | 何时可以省略 |
|---|---|---|
| `grill-with-docs` | 需求、边界、术语和关键决策是否清楚 | 需求已经明确，且不需要沉淀项目上下文 |
| `to-spec` | 把已经确认的讨论整理成可复查的规格 | 改动很小，规格写出来比直接做更重 |
| `to-tickets` | 把规格拆成能独立实现、带依赖关系的任务 | 只有一个很小的实现任务 |
| `implement` | 按规格或任务完成代码改动 | 不涉及实现，只做调查或讨论 |
| `tdd` | 用红绿反馈循环约束行为是否正确 | 真正的一行文案、配置或无逻辑改动 |
| `code-review` | 检查代码标准和规格完成度 | 临时原型或不会进入主线的实验 |

因此，小功能可以压缩为：


```text
grill-with-docs
  ↓
implement
```

中等功能再补上规格和任务拆分：

```text
grill-with-docs
  ↓
to-spec
  ↓
to-tickets
  ↓
implement
```

这里的关键不是“流程越完整越专业”，而是让每一步都有产出：需求澄清产生共同理解，`to-spec` 产生规格，`to-tickets` 产生可执行任务，`implement` 产生实现和验证结果。

## 4、外部 Issue 流程

外部 Issue 不应该直接进入实现，因为它可能信息不完整、不可复现、重复、超出范围，或者需要人工产品判断。

```text
triage
  ↓
implement
```

`triage` 的价值是先分流：能交给 Agent 的进入 `ready-for-agent`，信息不足的进入 `needs-info`，需要人工判断的进入 `ready-for-human`，不处理的进入 `wontfix`。

## 5、疑难 Bug 流程

疑难 Bug 不应先猜修复。先用 `diagnosing-bugs` 建立稳定反馈循环：

```text
diagnosing-bugs
  ↓
implement / codebase-design
```

如果定位到局部实现错误，就进入 `implement`。如果发现问题来自模块边界、接口职责或测试 seam 不清，就转向 `codebase-design` 或 `improve-codebase-architecture`。

## 6、大型模糊项目流程

大型模糊项目先用 `wayfinder`，但它不是固定的实现流水线，而是先画 decision map。

```text
wayfinder
  ↓
decision map
```

`decision map` 里会放当前能说清的问题和还在雾里的问题。能明确成问题的部分变成 decision tickets；需要查资料的走 `research`，需要试形态的走 `prototype`，需要人工判断的走 `grilling`。

等路线清楚后，再按实际情况进入 `to-spec`、`to-tickets` 或直接 `implement`。

## 7、不要把流程用满

判断是否需要更完整流程，看三个问题：

- 这个决策以后是否需要回看？
- 这个任务是否会拆给多个 Agent 或多人执行？
- 改错后的代价是否明显高于先写清规格的成本？

如果三个答案都是否，就不要强行上完整流程。

# 六、其他 Skill

## 1、prototype

`prototype` 用可丢弃代码回答设计问题。它适合验证状态模型、交互流程、UI 变体或某个技术方向是否可行，不适合直接演变成正式实现。

关键点是：原型从一开始就应该被当作临时材料。验证完成后，把结论写回 spec、ticket 或决策记录，正式实现另起一条干净路径。

## 2、improve-codebase-architecture

`improve-codebase-architecture` 用来扫描代码库中的架构摩擦，找出模块加深、职责重划和测试面改善机会。

它不是直接重构代码的命令，而是先生成候选报告：哪里经常牵连修改、哪里接口太浅、哪里缺少稳定 seam、哪里让 Agent 难以理解。选中某个候选后，再进入设计、规格和实现。

## 3、diagnosing-bugs

`diagnosing-bugs` 面向难复现 Bug、随机失败、性能回退、环境相关错误和修复反复失效的问题。

它的纪律是先建立红绿反馈循环，再定位根因。没有复现和验证方式之前，不急着写修复；如果最终发现无处可测，那本身就是架构信号。

## 4、research

`research` 用于工程决策依赖外部资料时，例如框架选型、API 行为、迁移方案、兼容性边界。

它的产物应是一份可回看的 Markdown 调查记录，包含来源链接、事实、推断和不确定点。这样后续讨论不必重新搜索，也能看清当时为什么做这个判断。

## 5、domain-modeling

`domain-modeling` 用来沉淀项目里的领域语言。它会把关键概念、实体、规则、命名和边界写入 `CONTEXT.md`。

当同一个概念在产品、代码和用户口径里有不同说法时，先做领域建模比直接改代码更稳。统一语言后，Agent 才更容易写出贴合业务含义的文件名、函数名和模块边界。

## 6、handoff

`handoff` 把当前长会话压缩成交接文档，让下一次会话或另一个 Agent 能接着工作。

它适合会话很长、已经做了大量调查或局部修改、但任务还没结束的情况。它不替代 spec、issue 或 ADR，只记录“下一位接手者需要知道什么”。

## 7、teach

`teach` 把当前目录变成长期教学工作区，围绕一个主题持续产出课程、练习、参考材料和学习记录。

它不是普通问答，而是把学习目标、资源、课程、练习和回顾沉淀下来，适合系统学习一个工具、框架或理论。

# 七、自测

1. 为什么 `setup-matt-pocock-skills` 应该先运行，而不是直接从 `to-spec` 开始？
2. `grill-me` 和 `grill-with-docs` 的区别是什么？
3. 新功能流程中，`grill-with-docs`、`to-spec`、`to-tickets`、`implement` 分别负责什么？
4. 为什么外部 Issue 通常要先经过 `triage`？
5. 疑难 Bug 为什么要先建立红绿反馈循环？
6. `wayfinder` 为什么是 decision map，而不是固定实现流水线？
7. `prototype`、`research` 和 `handoff` 分别适合解决什么问题？

# 八、来源

- [mattpocock/skills](https://github.com/mattpocock/skills)
- [CHANGELOG.md](https://github.com/mattpocock/skills/blob/main/CHANGELOG.md)
- [wayfinder/SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md)
- [package.json](https://github.com/mattpocock/skills/blob/main/package.json)
