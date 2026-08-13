# 一、项目初始化
## 1、初始化入口

安装完成后，每个准备使用这套工程工作流的仓库都要运行一次：

```text
/setup-matt-pocock-skills
```

它做的不是创建某个功能需求，而是为当前仓库写入一组后续 Skill 会读取的配置。配置重点包括：

- Issue tracker（任务追踪器）用 Local Markdown、GitHub、GitLab，还是其他系统。
- Triage（任务分流）使用哪些状态标签。
- 领域文档写在哪里，例如 `CONTEXT.md`、`docs/adr/` 或 monorepo 的多上下文布局。
- Agent 长期上下文文件使用 `AGENTS.md` 还是 `CLAUDE.md`。

## 2、任务追踪器

第一部分是配置 Issue tracker。它是记录需求、Bug、任务状态和依赖的地方，也是 `triage`、`to-spec`、`to-tickets` 等 Skill 后续读写任务的位置。

对于个人项目，Local Markdown 通常已经够用：规格和任务会放在 `.scratch/<feature>/` 下。对于多人协作，则更适合使用 GitHub Issues、GitLab Issues，或把 Jira、Linear 等其他系统的工作流写成自定义说明。

个人仓库一般选择 Local Markdown。选择后，相关规则会写入 `docs/agents/issue-tracker.md`。

## 3、Triage 状态

第二部分是配置 Triage Labels 状态。

Triage 是对 Issue 或外部 PR 进行分析、补充和分流的过程。它先判断问题是否成立、信息是否完整、能否交给 Agent、是否需要人工判断，以及是否决定不处理。

这五个状态角色不是 Local Markdown 专属，而是 `triage` 的通用状态机。一般情况下，使用默认名称即可：

| 状态                | 含义              |
| ----------------- | --------------- |
| `needs-triage`    | 新任务，尚未分析和分类     |
| `needs-info`      | 信息不足，需要继续补充     |
| `ready-for-agent` | 信息完整，可以交给 Agent |
| `ready-for-human` | 需要人工判断或处理       |
| `wontfix`         | 决定不处理           |

不同 Issue tracker 只是落地位置不同：

- GitHub/GitLab：状态通常体现为平台 Issue Label。
- Local Markdown：状态写在本地 issue 文件顶部附近的 `Status:` 行，例如 `Status: needs-triage`。
- 其他 tracker：按 `docs/agents/issue-tracker.md` 和 `docs/agents/triage-labels.md` 中记录的规则映射。

Local Markdown 模式下同样可以使用这套状态转换。Issue 文件通常位于 `.scratch/<feature-slug>/issues/<NN>-<slug>.md`，状态变化就是修改文件里的 `Status:` 行，并把补充说明追加到 `## Comments` 下。

需要注意的是，`to-tickets` skill 面向的是已经清楚的 spec 或计划，所以它生成的本地 issue 通常天然就是 `ready-for-agent`。`needs-triage`、`needs-info`、`ready-for-human` 和 `wontfix` 更常见于 `/triage` skill 处理尚未澄清的请求时。

这类请求可以来自 GitHub/GitLab Issue，也可以来自本地 Markdown issue。Matt Pocock Skills 没有单独提供一个“把聊天反馈创建成待 triage 本地 issue”的专用 Skill；如果使用 Local Markdown，可以让普通 Agent 按 `docs/agents/issue-tracker.md` 的约定，把反馈或模糊任务记录到 `.scratch/<feature-slug>/issues/`，初始状态设为 `needs-triage`，再交给 `/triage` 分流。

常见转换可以这样理解：

- 新进入的 Issue 通常先进入 `needs-triage`。
- 如果缺少复现步骤、目标描述或关键约束，就转为 `needs-info`。
- 当报告者补充信息后，再回到 `needs-triage` 重新判断。
- 如果任务已经验证清楚、范围明确、可以写成 Agent brief，就转为 `ready-for-agent`。
- 如果任务需要产品判断、人工验收、外部权限或高风险操作，就转为 `ready-for-human`。
- 如果需求已实现、重复、超出范围或决定不做，就转为 `wontfix`。


## 4、领域文档

第三部分是配置 Domain docs，领域文档决定**项目术语**和**架构决策**写在哪里。

项目术语指的是项目里长期稳定的业务概念、实体名称、规则边界和命名约定。例如“用户”“账号”“订阅”“工作区”这些词在产品、代码和文档里最好保持同一含义。

架构决策指的是那些以后可能需要回看的技术选择和取舍，例如为什么使用某个数据库、为什么拆成某个模块、为什么选择 monorepo。ADR 是 Architecture Decision Record（架构决策记录）的缩写，`docs/adr/` 通常用来保存这类记录。

单项目通常使用根目录 `CONTEXT.md` 和 `docs/adr/`。

monorepo项目 才更可能按包或业务域拆多个上下文，例如根目录放 `CONTEXT-MAP.md`，再由它指向各个包或领域自己的 `CONTEXT.md`。

> Monorepo 是把多个相互关联的项目、包或服务放在同一个版本仓库中管理的代码库。它们共享同一套 Git 历史和协作边界，但可以各自拥有独立的源码、构建和发布流程。

`setup-matt-pocock-skills` 不会默认假设当前仓库是 monorepo。它会先查找 monorepo 信号，例如：

- 是否存在 `pnpm-workspace.yaml`。
- `package.json` 中是否有 `workspaces` 字段。
- `packages/*` 下是否有带自己 `src/` 的子包。

只有发现这些信号时，它才会询问是否使用 multi-context 布局。没有这些信号时，默认使用 single-context：根目录一个 `CONTEXT.md`，ADR 放在 `docs/adr/`。




## 5、长期上下文文件

最后一部分会根据项目当前是否已有 `CLAUDE.md` 或 `AGENTS.md` 来写入 `Agent skills` 配置块，用于指导 Agent 怎么使用 Matt Pocock Skills 的工作流。

如果已经有 `CLAUDE.md` 或 `AGENTS.md`，会优先写入已有文件；如果其中已经存在 `Agent skills` 配置块，会更新原有配置块，而不是重复追加。

如果还没有 `CLAUDE.md` 和 `AGENTS.md`，会询问你选择哪个文件来存放规则。

如果仓库里还没有这两个文件，并且希望当前项目未来可以被多个 Agent 管理，可以这样要求：

```text
写入 AGENTS.md，同时创建 CLAUDE.md 软链接，指向 AGENTS.md
```

最终，长期记忆文件会加入如下内容：

```markdown
## Agent skills

### Issue tracker

Issues 以本地 Markdown 文件形式记录在 `.scratch/` 下。详见 `docs/agents/issue-tracker.md`。

### Triage labels

本仓库使用默认的五个 triage 标签：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`。详见 `docs/agents/triage-labels.md`。

### Domain docs
本仓库使用 single-context 领域文档布局：根目录 `CONTEXT.md`，ADR 存放在 `docs/adr/`。详见 `docs/agents/domain.md`。
```


## 6、初始化后的目录结构

初始化之后，单项目结构类似如下：

```text
project/
├── AGENTS.md
├── docs/
    └── agents/
        ├── issue-tracker.md
        ├── triage-labels.md
        └── domain.md
```

`.scratch/`、`CONTEXT.md` 和 `docs/adr/` 不一定会立刻出现。

- `.scratch/` 通常在第一次创建本地规格或任务时出现。
- `CONTEXT.md` 通常在项目形成需要长期保存的领域术语、规则或上下文时出现。
- `docs/adr/` 通常在产生需要记录的重要架构决策时出现。

初始化的重点是先让后续 Skill 知道这些内容应该写到哪里、按什么规则读写。

# 二、工作原理

## 1、整体结构

Matt Pocock Skills 是一套分层工作系统：

```text
setup-matt-pocock-skills
  ↓
ask-matt 选择入口
  ↓
主流程：idea → ship
  ↑
on-ramp：triage / diagnosing-bugs / wayfinder
  ↓
底层纪律：tdd / code-review / domain-modeling / codebase-design
  ↓
跨会话与辅助：handoff / prototype / research
```

`setup-matt-pocock-skills` 是前置配置，`ask-matt` 是路由器，真正的工作会落到具体流程里。大多数工程任务最终都会汇入同一条主流程：先把问题说清楚，再形成规格或任务，最后实现、测试、审查。

## 2、两类 Skill

这套 Skills 按触发方式分成两类：

| 类型 | 触发方式 | 职责 |
|---|---|---|
| 用户调用型 | 用户输入 `/skill-name` | 编排一个阶段或一条流程 |
| 模型调用型 | Agent 按任务自动使用，或用户显式点名 | 提供可复用工程纪律 |

用户调用型 Skill 像流程入口，例如 `ask-matt`、`grill-with-docs`、`to-spec`、`to-tickets`、`implement`、`triage`、`wayfinder`、`improve-codebase-architecture` 和 `setup-matt-pocock-skills`。

模型调用型 Skill 像底层方法，例如 `tdd`、`diagnosing-bugs`、`research`、`prototype`、`domain-modeling`、`codebase-design`、`code-review` 和 `resolving-merge-conflicts`。

用户调用型 Skill 可以调用模型调用型 Skill，但一般不会继续调用另一个用户调用型 Skill。这样可以让阶段切换保持可控：什么时候从澄清进入规格、什么时候从规划进入实现，仍然由用户决定。

## 3、主流程：idea → ship

主流程处理的是最常见的情况：你有一个想法，希望把它变成可交付代码。

`grill-with-docs` 负责先把想法问清楚，并把项目术语和关键决策沉淀到 `CONTEXT.md` 或 ADR 中。它适合有代码仓库的工程任务；如果没有代码仓库，只是讨论一个普通计划，则用 `grill-me`。

`prototype` （原型设计）是主流程里的临时岔路：当问题很难靠文字决定，可以先做一个不准备上线的小原型，用它回答设计问题。

例如要设计登录和注册页面，讨论时可能会卡在“登录和注册是两个页面，还是同一个页面里切换”“错误提示放在输入框下方，还是放在表单顶部”“移动端布局是否拥挤”等问题上。与其在聊天里反复想象，不如先做一个粗糙可点的 prototype：包含登录表单、注册表单、切换入口、错误提示和移动端布局。实际点过之后，再把结论写回 `to-spec`，例如“登录和注册共用一个 Auth 页面，通过 Tab 切换；字段错误贴近输入框展示；移动端使用单列布局”。原型代码可以丢掉，留下的是被验证过的设计判断。

任务很小时，可以在同一个上下文中直接进入 `implement`。任务较大、需要跨会话或拆给多个 Agent 时，应先用 `to-spec` 把当前讨论整理成规格，再用 `to-tickets` 拆成带阻塞关系的垂直切片。`to-tickets` 生成的 ticket 默认就是 `ready-for-agent`，不需要再经过 `triage`。

`implement` 负责真正实现规格或 ticket。它会尽量在预先约定的测试 seam 上使用 `tdd`，过程中持续运行类型检查和局部测试，结束前再用 `code-review` 从代码标准和规格完成度两个角度审查差异。

## 4、三个 on-ramp

on-ramp 是非主流程起点：任务不是从“我有一个清楚想法”开始，但最后可能汇入主流程或实现阶段。

| 起点 | 使用 Skill | 作用 | 下一步 |
|---|---|---|---|
| 外部请求堆积 | `triage` | 分流 GitHub/GitLab/Local Markdown 中的 Issue 或外部 PR | 进入 `ready-for-agent` 后再交给 `implement` |
| 疑难 Bug | `diagnosing-bugs` | 先复现、最小化、建立红绿反馈，再修复 | 局部错误进入实现；架构问题转向设计或架构改善 |
| 大型模糊项目 | `wayfinder` | 把超过单会话承载的大目标拆成 decision map 和 decision tickets | 决策清楚后回到 `to-spec` / `to-tickets` |

`triage` 只适合处理“外部进入、尚未成熟”的请求，例如用户提交的 Issue、外部 PR、或本地 Markdown tracker 里的待分流任务。它不应该处理 `to-tickets` 生成的 ticket，因为那些 ticket 已经是 agent-ready。

`diagnosing-bugs` 的重点不是马上修，而是先建立一个能证明 Bug 存在的失败检查。只有当“Bug 存在 → 检查失败，Bug 修复 → 检查通过”成立，修复才有可靠反馈。

`wayfinder` 默认是规划工具，不是执行工具。它产出的是决策地图：哪些问题已经决定、哪些问题还在雾里、下一张可处理的 decision ticket 是什么。地图清楚后，才把结论压缩成 spec 或 ticket。

## 5、代码库健康

`improve-codebase-architecture` 不属于某个功能需求，而是代码库保养工具。它扫描最近变化频繁或理解成本高的区域，找出 shallow module、测试 seam 不清、职责分散等问题，并生成架构改善候选。选中某个候选后，再通过 `grilling`、`domain-modeling` 和 `codebase-design` 继续澄清，必要时进入主流程。

它和 `wayfinder` 的区别是：`wayfinder` 面向“大目标还不清楚”的规划问题，`improve-codebase-architecture` 面向“代码库已经有摩擦”的健康问题。前者是在找路线，后者是在找结构改进机会。

## 6、底层纪律

底层纪律不是完整流程，而是其他流程会反复借用的工程方法。它们主要提供两类东西：稳定词汇和反馈循环。

| Skill | 作用 |
|---|---|
| `domain-modeling` | 统一项目术语、领域模型和 ADR 记录 |
| `codebase-design` | 使用 deep module、interface、seam 等词汇设计模块边界 |
| `tdd` | 用 red-green-refactor 建立行为反馈 |
| `code-review` | 从 Standards 和 Spec 两个维度审查 diff |

`domain-modeling` 和 `codebase-design` 解决“怎么命名、怎么划边界”的问题；`tdd` 和 `code-review` 解决“怎么知道改动真的正确”的问题。它们会被 `grill-with-docs`、`implement`、`diagnosing-bugs`、`wayfinder`、`improve-codebase-architecture` 等流程反复调用。

`research` 和 `prototype` 更像辅助能力：前者把外部资料调查沉淀成带引用的 Markdown，后者用一次性原型回答设计问题。它们可以服务主流程，也可以服务 `wayfinder` 的 decision ticket。

## 7、上下文与产物沉淀

这套 Skills 的核心不是“多跑几个命令”，而是把关键知识放到后续 Agent 能读取的位置。

| 文件或目录 | 保存内容 |
|---|---|
| `docs/agents/` | issue tracker、triage labels、domain docs 等工程 Skill 配置 |
| `CONTEXT.md` | 项目术语、领域模型、长期规则 |
| `docs/adr/` | Architecture Decision Record，记录重要架构决策 |
| `.scratch/<feature>/spec.md` | Local Markdown 模式下的规格 |
| `.scratch/<feature>/issues/` | Local Markdown 模式下的实现 ticket |
| `CONTEXT-MAP.md` | monorepo multi-context 布局下的上下文索引 |

跨会话时，`handoff` 用来把当前讨论压缩成交接文件，然后在新会话中继续。它和普通压缩上下文不同：`handoff` 更像跨线程桥梁，适合从主线临时分支去做 `prototype` 或在会话快满时保留关键上下文。


# 三、Skill 速查表

## 1、工程流程入口

这些 Skill 需要用户显式调用，负责启动或推进一个工作阶段。

| Skill                           | 什么时候用                         | 主要产物                                  | 注意点                                              |
| ------------------------------- | ----------------------------- | ------------------------------------- | ------------------------------------------------ |
| `setup-matt-pocock-skills`      | 每个仓库第一次使用工程 Skills 前          | `docs/agents/` 配置和 `Agent skills` 配置块 | 只需一次；切换 tracker 或重做配置时再运行                        |
| `ask-matt`                      | 不确定该用哪个 Skill 或流程             | 入口建议                                  | 它是路由器，不直接替代后续流程                                  |
| `grill-with-docs`               | 有代码仓库，需求、设计或边界还不清楚            | 澄清后的共同理解，必要时更新 `CONTEXT.md` / ADR     | 适合主流程起点；没有代码仓库时用 `grill-me`                      |
| `to-spec`                       | 已经讨论清楚，需要整理成规格                | spec / PRD，并发布到配置好的 tracker           | 不再访谈用户，只综合现有上下文                                  |
| `to-tickets`                    | 需要把 spec、计划或对话拆成可执行任务         | 带阻塞关系的 tracer-bullet tickets          | Local Markdown 下是一票一文件；生成后通常就是 `ready-for-agent` |
| `implement`                     | 按 spec 或 ticket 做实现           | 代码改动、测试结果、结束前的 review                 | 内部会尽量使用 `tdd`，完成前运行 `code-review`                |
| `triage`                        | 处理外部 Issue、外部 PR 或待分流本地 issue | triage 状态、补充问题、agent-ready brief      | 不处理 `to-tickets` 生成的 ticket                      |
| `wayfinder`                     | 目标太大、太模糊，单会话装不下               | decision map 和 decision tickets       | 默认产出决策，不直接执行项目                                   |
| `improve-codebase-architecture` | 想主动检查代码库结构健康                  | 架构改善候选报告                              | 它找候选，不是直接重构命令                                    |

## 2、工程纪律

这些 Skill 更像方法和词汇层。它们可以被流程自动调用，也可以在明确场景下单独使用。

| Skill                       | 什么时候用                          | 主要产物                    | 注意点                                |
| --------------------------- | ------------------------------ | ----------------------- | ---------------------------------- |
| `tdd`                       | 想 test-first 实现功能或修 Bug        | 先失败再通过的测试和实现            | 重点是外部行为，不是测试实现细节                   |
| `diagnosing-bugs`           | Bug 难复现、随机失败、性能回退或修了又坏         | 可复现反馈、根因、回归测试           | 没有能变红的检查前，不急着修                     |
| `code-review`               | 想审查分支、PR 或某个 fixed point 之后的改动 | Standards 和 Spec 两轴审查结果 | 它是审查，不是分流；PR 是否值得处理先用 `triage`     |
| `domain-modeling`           | 项目术语混乱、概念边界不清、需要记录架构决策         | `CONTEXT.md` 更新或 ADR    | 解决“我们说的这个词到底是什么意思”                 |
| `codebase-design`           | 需要设计模块边界、接口、seam 或让代码更可测       | 深模块设计建议                 | 关注 module、interface、depth、seam 等词汇 |
| `resolving-merge-conflicts` | 正在处理 merge / rebase 冲突         | 按意图解决后的冲突               | 逐块判断来源意图，不默认放弃合并                   |

## 3、调查、原型与跨会话

这些 Skill 经常服务于主流程或 `wayfinder`，但本身不一定意味着正式实现。

| Skill       | 什么时候用                      | 主要产物               | 注意点                          |
| ----------- | -------------------------- | ------------------ | ---------------------------- |
| `prototype` | 设计问题靠文字难判断，例如状态模型、交互、UI 形态 | 可丢弃原型和设计结论         | 原型代码不直接变成正式实现；结论写回 spec      |
| `research`  | 需要查官方文档、API 行为、迁移方案或外部事实   | 带引用的 Markdown 调查记录 | 优先 primary sources，可作为后台任务   |
| `handoff`   | 会话很长、要换新会话或分支去做原型/调查       | 交接文档               | 它保留当前讨论，不替代 spec、issue 或 ADR |

## 4、生产力 Skill

这些 Skill 不一定面向代码实现，但可以支撑更大的工作过程。

| Skill                  | 什么时候用                 | 主要产物             | 注意点                                              |
| ---------------------- | --------------------- | ---------------- | ------------------------------------------------ |
| `grill-me`             | 没有代码仓库，只想把计划、设计或决策想清楚 | 对话中的清晰判断         | 不写 `CONTEXT.md`，不沉淀仓库文档                          |
| `grilling`             | 其他 Skill 需要追问和压力测试时   | 一轮逐步澄清的问题链       | 通常由 `grill-me`、`grill-with-docs`、`wayfinder` 等调用 |
| `teach`                | 想围绕一个主题长期学习           | 教学工作区、课程、练习和学习记录 | 适合系统学习，不是普通问答                                    |
| `writing-great-skills` | 想创建或修改 Skill 本身       | 写 Skill 的原则和词汇   | 面向 Skill 作者，不是日常开发主流程                            |

## 5、选择口诀

- 不知道用哪个：先 `ask-matt`。
- 新功能还模糊：`grill-with-docs`。
- 已经聊清楚但需要规格：`to-spec`。
- 规格太大需要拆任务：`to-tickets`。
- 已有 ticket 要实现：`implement`。
- 外部 Issue / PR 先分流：`triage`。
- Bug 难定位：`diagnosing-bugs`。
- 项目太大还看不清路线：`wayfinder`。
- 代码库本身开始难改：`improve-codebase-architecture`。
- 需要外部事实：`research`。
- 需要先看一个可点可跑的小模型：`prototype`。
- 会话太长或要换线程：`handoff`。

# 四、重点 Skill 详解

## 1、grill-with-docs 和 grill-me

`grill-with-docs` 和 `grill-me` 都是“先问清楚再行动”的 Skill。它们的共同点是通过连续追问，把一个模糊想法变成可判断、可执行的共同理解。

区别在于是否绑定代码仓库：

| Skill | 适合场景 | 是否写入项目文档 |
|---|---|---|
| `grill-with-docs` | 代码项目里的功能、架构选择、需求边界澄清 | 会结合 `domain-modeling`，必要时更新 `CONTEXT.md` 或 ADR |
| `grill-me` | 非代码计划、个人决策、产品想法、普通方案讨论 | 不写项目文档，只在会话中澄清 |

例如你要做“登录和注册页面”，但还不确定是否支持第三方登录、注册后是否自动登录、错误提示怎么展示，就适合用 `grill-with-docs`。它会先问清楚业务规则和交互边界，再把稳定术语或关键决策沉淀下来。

如果你只是想讨论“我要不要做一个会员体系”这种还没有进入代码仓库的想法，用 `grill-me` 更轻。它不会创建 spec，也不会更新 `CONTEXT.md`，只负责把你的判断问清楚。

## 2、wayfinder

`wayfinder` 用于一个会话装不下的大型模糊项目。它不是“开始执行”的命令，而是“先把路找出来”的命令。

它会先命名 destination（目标终点），再把未知问题整理成 decision map（决策地图）。地图里会有多个 decision tickets，每个 ticket 解决一个问题，例如：

- 需要先查资料的 ticket，交给 `research`。
- 需要看形态或交互的 ticket，交给 `prototype`。
- 需要人工判断的 ticket，通过 `grilling` 继续追问。
- 需要先完成某个准备动作的 ticket，记录成 task。

`wayfinder` 的产物是“决策”，不是正式功能代码。等关键问题都清楚后，再把地图里的结论汇入 `to-spec`，形成真正可实现的规格。

适合它的例子是：“我要重做整个权限系统”“我要把单体应用拆成多个包”“我要规划一个新产品的 MVP”。如果只是一个边界清楚的小功能，用 `grill-with-docs` 或直接 `implement` 更合适。

## 3、improve-codebase-architecture

`improve-codebase-architecture` 是代码库健康检查工具。它不从某个新功能出发，而是主动扫描代码库哪里已经变得难懂、难测、难改。

它关注的不是“这里代码丑不丑”，而是结构性摩擦：

- 理解一个业务概念需要跳很多文件。
- 模块接口很浅，调用者仍然要知道太多实现细节。
- 为了测试拆出很多小函数，但真正的 Bug 发生在组合处。
- 缺少稳定 seam，导致测试只能绕很远。
- 最近经常修改的区域越来越难维护。

它的产物通常是一个 HTML 架构报告，列出多个 deepening opportunities（模块加深机会）。每个候选会说明涉及文件、问题、建议方向、收益，以及推荐强度。

选中某个候选后，才进入后续澄清和设计：用 `grilling` 问清约束，用 `domain-modeling` 更新术语，用 `codebase-design` 设计模块边界，必要时再回到 `to-spec` / `to-tickets` / `implement`。

## 4、prototype

`prototype` 用来回答“光靠文字很难判断”的设计问题。它产出的是一次性原型，不是正式实现。

本地 Skill 把 prototype 分成两类：

| 类型 | 适合问题 | 原型形态 |
|---|---|---|
| 逻辑 / 状态模型 | 状态流转、业务规则、边界场景是否合理 | 小型可运行终端程序 |
| UI / 交互 | 页面布局、交互方式、视觉变体是否顺手 | 多个 UI 变体，可切换查看 |

比如设计登录和注册页面时，可能不确定“登录和注册是否共用一个页面”“错误提示放在哪里”“移动端是否拥挤”。这时可以让 `prototype` 做一个粗糙可点的页面，把登录表单、注册表单、切换入口和错误提示都放进去。你实际试过后，再把结论写回 `to-spec`。

关键点是：原型从第一天起就是临时材料。正式实现应该吸收原型验证出的结论，而不是把原型代码直接一路改到生产环境。

## 5、research

`research` 用于需要外部事实支撑的工程问题，例如框架选型、API 行为、迁移方案、兼容性边界、官方文档细节。

它的特点是：优先查 primary sources，也就是官方文档、源码、规范、第一方 API，而不是二手博客总结。它会把调查结果写成一个带引用的 Markdown 文件，并保存在仓库合适的位置。

适合使用 `research` 的问题包括：

- “Next.js 当前推荐的缓存策略是什么？”
- “某个 API 在最新版本里是否废弃？”
- “从库 A 迁移到库 B 有哪些官方限制？”
- “这个浏览器能力的兼容性到底如何？”

`research` 不直接替你做产品判断。它提供事实材料，让 `grill-with-docs`、`wayfinder`、`to-spec` 或人工决策有可靠依据。

## 6、handoff

`handoff` 用于跨会话交接。它会把当前对话压缩成一个交接文档，让新的 Agent 或新的会话能接着工作。

它适合三种情况：

- 当前会话太长，继续下去容易丢重点。
- 需要从主线分支出去做 `prototype` 或 `research`。
- 当前任务没做完，但已经积累了很多上下文、决策和待办。

`handoff` 默认把交接文档保存到系统临时目录，而不是当前仓库。它不会重复复制已经写进 spec、issue、ADR、commit 或 diff 的内容，而是用路径或链接引用它们。

它和普通上下文压缩的区别是：普通压缩是在同一个会话里继续，`handoff` 更像把当前线程打包给另一个新会话。需要保留关键上下文、但又想换一个干净工作空间时，用 `handoff` 更稳。
