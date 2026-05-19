# 一、概述

`Skill`是`Claude Code`的扩展机制，通过编写`SKILL.md`文件定义可复用的指令集，让`Claude Code`获得新能力。与每次对话自动加载的`CLAUDE.md`不同，`Skill`**按需加载**——`SKILL.md`的正文只在调用时才进入上下文，因此长篇参考资料几乎不占用上下文，直到你真正需要它。

`Claude Code`会在任务描述相关时自动触发`Skill`（加载`SKILL.md`正文），也可以通过`/skill-name`手动调用。

之前的自定义命令已合并入`Skill`体系。`.claude/commands/deploy.md`和`.claude/skills/deploy/SKILL.md`都会创建`/deploy`命令，效果相同。旧版命令仍兼容，但同名时`Skill`优先。`Skill`新增的特性包括：

- 每个skill对应独立目录，除`SKILL.md`外可存放辅助文件
- 让`Claude Code`在任务相关时自动加载
- 通过frontmatter控制调用方式（手动/自动/禁用）

`Claude Code`的`Skill`遵循[Agent Skills](https://agentskills.io/)开放标准，一份规范的`SKILL.md`可在多个支持该标准的AI工具间复用。`Claude Code`在此基础上增加了[[#六、调用与权限控制|^调用控制]]、[[#七-1-动态上下文注入|^动态上下文注入]]和[[#七-2-子代理执行|^子代理执行]]。

在`Claude Code`的交互体系中，Skills与以下机制紧密相关：

- **Slash命令**：`/`菜单中既有内置固定逻辑命令，也有`Skill`命令（详见[[3、Slash Command]]）
- **Subagent**：`Skill`可通过`context: fork`在隔离子代理中执行（详见[[9、Subagent]]）

> **何时创建Skill**：当你反复粘贴相同的操作手册、检查清单或多步骤流程时；当`CLAUDE.md`中的某部分内容从"事实陈述"演变为"操作流程"时；当需要封装副作用操作（如部署）并严格控制触发时机时。

# 二、创建第一个Skill

本示例创建一个项目级`summarize-changes` skill，用来总结当前Git仓库中尚未提交的更改并标记潜在风险。它会在Claude读取指令**之前**，自动将实时的`git diff`注入到提示词中，让回答基于真实的工作区变更而非猜测。

当询问"我改了什么"、"帮我写提交信息"、"帮我review这次改动"等问题时，Claude可自动加载该skill，也可通过`/summarize-changes`手动调用。

1. 创建skill目录

在项目目录的`.claude/skills/`下创建目录，目录名即为命令名：

```bash
mkdir -p .claude/skills/summarize-changes
```

2. 编写SKILL.md

每个skill需要一个`SKILL.md`文件，包含两部分：YAML frontmatter（描述用途和适用场景）和Markdown指令内容（告诉Claude如何处理输入和组织回答）。

保存以下内容到`.claude/skills/summarize-changes/SKILL.md`：

```markdown
---
description: 总结当前 Git 仓库中尚未提交的更改，并标记潜在风险。适用于用户询问改动内容、请求生成提交信息，或希望审查当前 diff 的场景。
---

## 当前更改

!\`git diff HEAD\`

## 指令

请根据上方的更改内容，用两到三个要点总结本次改动。

然后列出你发现的潜在风险，例如：

- 是否缺少错误处理
- 是否存在硬编码内容
- 是否需要更新测试
- 是否可能影响已有功能
- 是否存在不清晰但难以维护的实现

如果当前 diff 为空，请直接说明：当前没有尚未提交的更改。
```

3. 测试skill

进入任意Git项目，修改一个文件后启动Claude Code：

```bash
claude
```

两种测试方式：

- 自动触发：输入`我改动了什么`，让Claude判断是否调用
- 手动调用：输入`/summarize-changes`

配置正确时，Claude会返回未提交更改的简要总结和潜在风险提示。

# 三、Skill的存储与结构

## 1、存储作用域

Skill存放位置决定生效范围，支持四级作用域：

| 级别  |                 路径                 |   适用范围    | 覆盖优先级  |
| :-: | :--------------------------------: | :-------: | :----: |
| 企业级 |   参考[[Settings]]的**managed settings**    |  组织内所有用户  |   最高   |
| 个人级 | `~/.claude/skills/<name>/SKILL.md` | 当前用户的所有项目 |   中高   |
| 项目级 |  `.claude/skills/<name>/SKILL.md`  |   仅当前项目   |   中    |
| 插件级 | `<plugin>/skills/<name>/SKILL.md`  |   插件启用处   | 独立命名空间 |

同名Skill的覆盖规则：**企业级 > 个人级 > 项目级**。插件Skill使用`plugin-name:skill-name`命名空间，不与其他级别冲突。

## 2、目录结构

每个Skill是一个独立目录，`SKILL.md`是入口文件（必须），可附带辅助文件：

```text
my-skill/
├── SKILL.md           # 主指令（必须，概览与导航）
├── template.md        # 供 Claude Code 填写的模板（可选）
├── examples/
│   └── sample.md      # 预期输出格式示例（可选）
└── scripts/
    └── validate.sh    # Claude Code 可执行的脚本
```

在`SKILL.md`中引用辅助文件，让Claude知晓各文件的内容和加载时机：

```markdown
## 附加资源

- 完整 API 详情见 [reference.md](reference.md)
- 使用示例见 [example.md](example.md)
```

> 建议`SKILL.md`保持在**500行以内**，详细参考材料放独立文件，通过相对路径引用。

## 3、来自额外目录的skill

`--add-dir`标志主要用于授予文件访问权限，而非配置发现，但Skill是例外：额外目录中的`.claude/skills/`会自动加载。其他`.claude`配置（子代理、命令、输出样式）不从额外目录加载。

来自`--add-dir`目录的`CLAUDE.md`文件默认不加载，需设置`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`（[[4、记忆机制#^566a05|详见记忆机制]]）。

## 4、实时变更检测

- `Claude Code`**实时监控** skills 目录的文件变更（增/删/改），当前会话即时生效
- `--add-dir`附加目录的 skills 目录也会被加载
- 若会话启动时某个顶层 skills 目录不存在，创建后需重启`Claude Code`会话
- 在对话中操作子目录文件时，`Claude Code`会查找该子目录下的`.claude/skills/`并加载（支持 monorepo 场景）

# 四、Frontmatter参考

通过`SKILL.md`文件顶部`---`之间的YAML frontmatter配置skill行为：

```yaml
---
name: my-skill
description: 这个 skill 的功能
disable-model-invocation: true
allowed-tools: Read Grep
---

你的 skill 指令 ...
```

推荐填写`description`，以便`Claude Code`知道何时调用该skill。各字段说明：

|             字段             | 必须 |                                                                                                                  说明                                                                                                                  |
| :------------------------: | :--: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|           `name`           |  否  |                                                                                         skill的显示名称。若省略则使用目录名。仅允许**小写字母、数字和连字符**（最多64字符）。                                                                                         |
|       `description`        | 推荐  |                                                                                     skill的功能和适用场景。Claude用此判断何时应用该skill。若省略则使用markdown内容的第一段。                                                                                     |
|       `when_to_use`        |  否  |                                                         Claude何时调用该skill的额外上下文，如触发短语或示例请求。附加在`description`之后作为Claude在选择skill时看到的元数据。受1,536字符上限约束。                                                         |
|      `argument-hint`       |  否  |                                                              输入slash command时，自动补全提示里显示该命令后面应跟的参数。例如`argument-hint: [issue-number] [priority]`。                                                               |
|        `arguments`         |  否  |                  给slash command后面的位置参数起的命名参数，正文可用`$name`引用。接收空格分隔的字符串或YAML列表。例如`argument-hint: [filename] [format]`，`arguments: filename format`，正文可写：请将`$filename`导出为`$format`格式。                   |
| `disable-model-invocation` |  否  |                                                       默认`false`，设为`true`时禁止Claude自动加载此skill，只能手动调用。适用于想用`/name`触发的工作流。此设置也会阻止skill被预加载到子代理。                                                       |
|      `user-invocable`      |  否  |                                                                                           默认`true`，设为`false`会从`/`菜单中隐藏。适用于用户不应直接调用的背景知识。                                                                                            |
|      `allowed-tools`       |  否  |                                                                              skill触发时Claude可免确认使用的工具。接受空格分隔的字符串或YAML列表。注意，这不是限制可用工具范围，所有工具仍可调用。                                                                              |
|          `model`           |  否  |                                                 skill触发时使用的模型。覆盖仅在当前轮次生效，不保存到设置；下个提示词恢复会话模型。接受与[/model](https://code.claude.com/docs/en/model-config)相同的值，或`inherit`保持当前模型。                                                 |
|          `effort`          |  否  |                                                                 skill触发时的模型推理强度。覆盖仅在当前轮次生效。选项：`low`、`medium`、`high`、`xhigh`、`max`；可用级别取决于模型。                                                                 |
|         `context`          |  否  |                                                                                                    设为`fork`时该skill在分叉的子代理上下文中运行                                                                                                    |
|          `agent`           |  否  |                                                                                                     当`context: fork`设置时使用的子代理类型                                                                                                      |
|          `hooks`           |  否  |                                                                                                          限定于该skill生命周期的钩子                                                                                                          |
|          `paths`           |  否  |                                                          skill的适用文件范围，Claude只在处理匹配这些路径模式的文件时才自动加载。接受逗号分隔的字符串和YAML列表。格式同[[3、记忆机制#^path-rules|路径特定规则]]                                                           |
|          `shell`           |  否  | 决定skill中内联shell命令的解释器。默认`shell: bash`，也可设为`shell: powershell`。影响`!\`command\``及围栏` ```! command ``` `的执行。设置`powershell`在Windows上通过PowerShell运行内联命令，需`CLAUDE_CODE_USE_POWERSHELL_TOOL=1`。 |

# 五、内容类型与选择

`SKILL.md`可以包含任意形式的指令，但编写前建议明确该skill的调用方式——它是供Claude自动参考的背景知识，还是需要用户手动触发的操作流程？应该内联执行还是交给子代理？调用方式直接影响内容组织。

## 1、参考资料型

参考资料型Skill向Claude提供可在当前工作中直接应用的知识，如项目约定、代码风格、设计模式、领域知识或团队规范。适合内联运行，让Claude结合当前上下文直接使用，不一定需要用户显式调用。

```yaml
---
name: api-conventions
description: 本代码库的 API 设计模式
---

编写 API 端点时：
- 使用 RESTful 命名惯例
- 返回统一的错误格式
- 包含请求验证
```

适合参考资料型Skill的内容：API设计规范、代码风格指南、团队写作规范、产品术语表、领域知识说明、常见模式与反模式。

## 2、任务型

任务型Skill定义一组明确的操作步骤，如部署、提交、代码生成、运行检查、发布文档等。通常适合用户显式调用（通过`/skill-name`），而非让Claude自动判断。可添加`disable-model-invocation: true`避免自动触发。

```yaml
---
name: deploy
description: 将应用部署到生产环境
disable-model-invocation: true
---

部署应用
1. 运行测试套件
2. 构建应用
3. 推送到部署目标
```

适合任务型Skill的内容：部署流程、发布流程、提交前检查、代码生成步骤、数据处理流程、固定格式的报告生成。

## 3、选择建议

编写`SKILL.md`前，考虑三个问题：

1. **调用方式**：该skill该由Claude自动调用，还是由用户手动调用？
2. **运行位置**：适合内联执行，还是放到子代理中运行？
3. **内容复杂度**：全部内容是否适合放在`SKILL.md`中，还是需要拆分到辅助文件？

内容较短、规则清晰时，直接写在`SKILL.md`中。涉及较多背景资料、模板、示例或分支流程时，保持主文件简洁，通过辅助文件组织复杂内容。

# 六、调用与权限控制

## 1、调用方式 ^invocation-control

Skill默认支持两种调用：用户手动输入`/skill-name`，以及Claude在相关场景中自动加载。通过frontmatter可精细控制：

| 配置                               | 用户可`/name` | Claude可自动调用 | 加载方式                          |
| -------------------------------- | ----------- | ------------ | ----------------------------- |
| （默认）                             | Yes         | Yes          | Description常驻上下文，完整内容调用时加载   |
| `disable-model-invocation: true` | Yes         | No           | Description不加载，用户调用时加载完整内容   |
| `user-invocable: false`          | No          | Yes          | Description常驻上下文，Claude自动触发 |

> 有副作用的操作（如`/deploy`、发送消息）设置`disable-model-invocation: true`；纯背景知识（如旧系统说明）设置`user-invocable: false`。

## 2、参数传递

Skill支持多种占位符替换，用于接受调用时传入的参数：

| 占位符                    | 说明                  | 示例                           |
| ---------------------- | ------------------- | ---------------------------- |
| `ARGUMENTS`            | 全部参数原样传入            | `/fix 123` → `123`           |
| `ARGUMENTS[N]`/ `$N`   | 按0-based索引取参数     | `$0`, `$1`, `$2`             |
| `$name`                | frontmatter声明的命名参数 | `arguments: [issue, branch]` |
| `${CLAUDE_SESSION_ID}` | 当前会话ID             | 用于日志命名                       |
| `${CLAUDE_EFFORT}`     | 当前effort级别        | `low` / `medium` / `high`    |
| `${CLAUDE_SKILL_DIR}`  | Skill目录路径          | 引用捆绑脚本                       |

示例：

```yaml
---
name: migrate-component
description: 将组件从一个框架迁移到另一个框架
---

将 $0 组件从 $1 迁移到 $2。
保留所有现有行为和测试。
```

调用：`/migrate-component SearchBar React Vue`，效果为"将SearchBar组件从React迁移到Vue。保留所有现有行为和测试。"

## 3、限制Claude的Skill访问

默认情况下，Claude可调用任何未设置`disable-model-invocation`的skill。如果skill定义了`allowed-tools`，激活时Claude会获得这些工具的免确认使用权限，其他工具仍受全局权限控制。因此，涉及敏感操作（`deploy`、`delete`、`rm`等）的skill建议额外限制。

三种限制方式：

1. 通过`/permissions`禁用所有Skill

添加拒绝规则`Skill`，相当于关闭总开关，Claude无法调用任何skill。

2. 通过权限规则允许或拒绝特定skill

- 只允许某个skill：`Skill(commit)` — 仅允许调用名为`commit`的skill
- 允许某一类skill：`Skill(review-pr *)` — 允许以`review-pr`开头且可带参数的skill
- 拒绝某一类skill：`Skill(deploy *)` — 拒绝以`deploy`开头且可带参数的skill，适合限制高风险操作

3. 在Skill中禁用模型调用

在`SKILL.md` frontmatter中添加`disable-model-invocation: true`，该skill不会被Claude自动发现或调用。

少数内置命令也可通过Skill工具调用（如`/init`、`/review`、`/security-review`），但并非所有内置命令都支持（如`/compact`不可以）。

# 七、高级特性

## 1、动态上下文注入 ^inject-dynamic-context

使用`` !`command` ``语法可以在Skill内容发送给Claude**之前**执行shell命令，将命令输出替换到占位符。Claude接收到的是实际数据而非命令本身。

示例——通过GitHub CLI获取实时PR数据来摘要拉取请求：

```markdown
---
name: pr-summary
description: 概述拉取请求的变更
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## 拉取请求上下文
- PR diff: !\`gh pr diff\`
- PR comments: !\`gh pr view --comments\`
- Changed files: !\`gh pr diff --name-only\`

## 你的任务
概述此拉取请求...
```

运行时：每个`` !`<command>` ``立即执行（Claude看到内容之前），输出替换占位符，Claude接收包含实际PR数据的完整提示词。

对于多行命令，使用以` ```! `开头的围栏代码块：

```markdown
## 环境

\`\`\`!
node --version
npm --version
\`\`\`
```

> 这是**预处理**，不是Claude执行。Claude只收到渲染后的内容。管理员可在settings中设置`"disableSkillShellExecution": true`禁用此行为。

## 2、子代理执行 ^run-skill-in-subagent

当希望Skill在隔离环境中独立执行时，在frontmatter中添加`context: fork`。启用后，Skill启动一个子代理执行，正文内容作为子代理的提示词。子代理只能看到Skill提供的指令和显式传入的信息，无法访问完整对话历史。

`context: fork`更适合任务型Skill——具有明确目标、输入和输出的Skill。

示例：

```yaml
---
name: deep-research
description: 深入研究某个主题
context: fork
agent: Explore
---

深入研究 $ARGUMENTS:
1. 使用 Glob 和 Grep 查找相关文件
2. 阅读并分析代码
3. 总结发现，附带具体文件引用
```

运行时：创建新的隔离上下文，子代理接收skill内容作为提示词，`agent`字段决定执行环境（模型、工具和权限），结果被摘要并返回到主对话。

`agent`字段指定子代理配置，选项包括内置代理（`Explore`、`Plan`、`general-purpose`）或`.claude/agents/`中的自定义子代理。若省略则使用`general-purpose`。

**Skill与Subagent的两种协作模式**：

| 方式                      | 系统提示词                          | 任务来源          | 额外加载                     |
| ----------------------- | ------------------------------ | ------------- | ------------------------ |
| Skill带`context: fork` | 由`agent`字段决定（Explore、Plan等） | `SKILL.md`内容 | `CLAUDE.md`              |
| Subagent带`skills`字段  | Subagent的markdown正文         | Claude的委派消息  | 预加载Skills + `CLAUDE.md` |

## 3、Skill内容生命周期

Skill被调用后，渲染后的`SKILL.md`作为**单条消息**进入会话，在整个会话期间保留。`Claude Code`不会在后续轮次中重新读取skill文件。

自动压缩时会保留最近调用的skill。当对话被摘要以释放上下文时，`Claude Code`在摘要后重新附上每个skill前**5000 tokens**，共享**250000 tokens**预算。从最近调用的skill填充此预算，因此一次对话中调用多个skill后，较早的skill可能被完全丢弃。若压缩后skill似乎失效，可**重新调用**以恢复完整内容。

在子代理中预加载的Skill会在子代理启动时**全量注入**。