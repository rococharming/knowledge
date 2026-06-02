# 一、概述

## 1、Skill概念

`Skill`是 Claude Code 的扩展机制。

通过编写`SKILL.md`文件，可以把可复用的指令、流程、参考资料、脚本和辅助资源封装成一个可调用能力，让`Claude Code`在合适的任务中使用。

与每次会话自动加载`CLAUDE.md`不同，`Skill`的正文是**按需加载**的：

- 会话开始时，Claude Code 会看到**可自动调用Skill**的名称和描述
- 当 `Skill`被用户手动调用，或被 Claude 自动判断为相关时，`SKILL.md`正文才会进入上下文
- 如果`Skill`被设置为仅用户手动调用，则连描述也不会进入`Claude`上下文

因此，`Skill`适合存放较长的操作手册、检查清单、团队规范、固定工作流和辅助脚本。长篇参考资料不会像`CLAUDE.md`那样每次对话都占用上下文，只有真正使用时才加载。

`Skill`有两种常见调用方式：

- 用户手动调用：`/skill-name`
- `Claude`自动调用：根据`SKILL.md`的 YAML frontmatter 的`description`/`when_to_use`判断是否相关

当你反复粘贴相同的提示词、相同检查清单或相同操作步骤时，就适合把它们整理成Skill。

可以这样理解：

| 内容类型               | 更适合放在哪里                                |
| ------------------ | -------------------------------------- |
| 项目的长期事实、约定、背景信息    | `CLAUDE.md`                            |
| 可复用的任务流程、检查清单、专项规范 | `Skill`                                |
| 临时一次性说明            | 当前对话                                   |
| 需要隔离执行的专项任务        | `Skill` + `context: fork` 或 `Subagent` |

自定义`Slash Command`已经合并进 Skills 体系，因此，`.claude/commands/deploy.md`和`.claude/skills/deploy/SKILL.md`都可以创建`/deploy`命令。

旧版`.claude/commands/*.md`文件仍然兼容，并支持相同的 frontmatter，但官方更推荐使用 Skills，因为 Skill 支持**独立目录**、**辅助文件**、**自动调用控制**、**子代理执行**和**动态上下文注入**等能力。

Claude Code 的 Skills 遵循 `Agent Skills` 开放标准，一份规范的 `SKILL.md` 可以在多个支持该标准的 AI 工具之间复用。`Claude Code` 在此基础上增加了调用控制、权限控制、动态上下文注入、子代理执行和动态加载等扩展能力。

在 Claude Code 的交互体系中，Skills 与以下机制关系紧密：

- `Slash Command`：Skill 可以通过 `/skill-name` 手动调用
- `Subagent`：Skill 可以通过 `context: fork`在隔离子代理中执行
- `Hooks`：Skill 可以配置限定于自身生命周期的 hooks
- `Permissions`：Skill 可以通过`allowed-tools`预批准工具，可以通过权限规则限制 Skill 调用

## 2、捆绑Skills

Claude Code包含一组在每个会话可用的捆绑Skill，包括`/code-review`、`/batch`、`/debug`、`/loop`、`/claude-api`等。

与大多数会直接执行固定逻辑的内置命令不同，捆绑Skill是基于提示词的：它会向 Claude 提供详细指令，并让 Claude 使用其工具来编排完成工作。

可以像调用其他任何技能一样调用它们，只需输入 `/` 后跟技能名称即可。

这里着重介绍`/run`、`/verify`和`/run-skill-generator`三个捆绑 skill。这三个 skill 可以协同工作，用于启动项目，并根据运行中的项目而不仅仅是测试来确认更改。

| Skill                  | 用途                                                 |
| ---------------------- | -------------------------------------------------- |
| `/run`                 | 启动应用并观察实际运行效果。看当前程序能不能跑起来、运行后输出/页面/接口是什么           |
| `/verify`              | 构建并运行应用，按目标验收改动是否正确。确认刚才的代码修改是否真的符合需求，而不是只看类型检查或测试 |
| `/run-skill-generator` | 生成项目专属的运行配方，教 `/run` 和 `/verify` 如何构建和启动你的项目       |
`/run` 和 `/verify` 无需设置即可使用。它们会根据你的项目类型（CLI、服务器、TUI、浏览器驱动等），以及 README、`package.json` 或 `Makefile` 中的内容来推断启动方式。

但对于那些需要标准启动流程之外内容的项目，这种推断会变得不可靠，例如需要数据库、env环境变量文件、图形会话或多步骤构建流程的项目。

`/run-skill-generator`则会记录启动配方，它会从一个干净环境开始让应用成功运行，捕获有效的步骤，包括安装命令、环境变量、启动脚本等，然后将其作为项目专属技能提交到`.claude/skills/run-<name>/`。

之后，`/run`、`/verify`以及该仓库中的任何其他Agent都会遵循这个已记录的配方，而不是重新发现启动方式。

每个项目运行一次 `/run-skill-generator` 即可；如果构建或启动流程发生变化，则需要再次运行。

下面给一个简单Rust项目示例：

1. 准备一个Rust CLI项目

```shell
cargo new hello_cli  
cd hello_cli
```

项目结构大概是：

```text
hello_cli/
├── Cargo.toml
└── src/
    └── main.rs
```

初始 `src/main.rs`：

```rust
fn main() {
    println!("Hello, world!");
}
```

2. 第一次让 Claude Code 记录运行方式

在 Claude Code 里输入：

```text
/run-skill-generator 这是一个 Rust CLI 项目。构建用 cargo build，运行用 cargo run。请记录这个项目的运行方式。
```

它的作用是生成项目专属运行配方，后续 `/run` 和 `/verify` 就不需要每次重新猜怎么启动项目。

结果：

![[Pasted image 20260602110117.png|600]]

可以看到生成了`run-hello-cli` skill。

3. 使用`/run`查看程序真实运行结果

![[Pasted image 20260602111517.png|400]]

可以看到 Claude 会自动加载`run-hello-cli` skill 运行项目。

现在让 Claude Code 修改程序：

```text
把程序输出改成 Hello from Rust
```

Claude 修改后，`src/main.rs` 可能变成：

```rust
fn main() {  
	println!("Hello from Rust");  
}
```

结果：

![[Pasted image 20260602111951.png|400]]

会发现 Claude Code 除了更改源码，还会更改之前创建的`run-hello-cli` skill内容来适配当前修改并自动验证结果。

4. 使用`/verify`验收代码改动

继续让 Claude Code 改一个功能：

```text
让程序读取命令行参数 name，如果传入 name，就输出 Hello, name。
```

结果：

![[Pasted image 20260602112252.png|400]]

然后可以输入：

```text
/verify
```

`/verify`更像针对刚才的功能要求做验收，它不仅会构建运行程序，还会围绕你描述的预期行为做确认。


# 二、创建并使用第一个Skill

## 1、简介

本示例创建一个项目级`summarize-changes` skill，用来总结当前仓库中尚未提交的更改，并标记潜在风险。

它会在 Claude 读取`Skill`指令**之前**，自动执行`git diff HEAD`，把实时`diff`注入到提示词中。这样 Claude 的回答基于真实工作区变更，而不是根据上下文猜测。

当询问"我改了什么"、"帮我写提交信息"、"帮我review这次改动"等问题时，Claude可自动加载该skill。也可通过`/summarize-changes`手动调用。

## 2、创建Skill目录

在项目根目录创建目录：

```shell
mkdir -p .claude/skills/summarize-changes
```

`summarize-changes`就是SKILL名。

`.claude/skills/summarize-changes/SKILL.md`对应命令`/summarize-changes`。

也可以把这个 Skill 放到个人目录中，让它对所有项目生效：

```shell
mkdir -p ~/.claude/skills/summarize-changes
```

> 项目级 Skill 适合只服务当前仓库；个人级 Skill 适合多个项目都能复用的通用流程。

## 3、编写SKILL.md

保存以下内容到：

```text
.claude/skills/summarize-changes/SKILL.md
```

`SKILL.md`：

```markdown
---
description: 总结当前 Git 仓库中尚未提交的更改，并标记潜在风险。适用于用户询问改动内容、请求生成提交信息，或希望审查当前 diff 的场景。
---

## 当前更改

!`git diff HEAD`

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

其中`` !`git diff HEAD` ``表示动态上下文注入。Claude Code会在 Skill 内容发送给 Claude 之前先执行这条命令，并把命令输出替换到当前位置。Claude 最终看到的是实际 diff 内容，而不是命令本身。

## 4、测试Skill

进入一个 Git 项目，修改任意文件后启动 Claude Code：

```shell
claude
```

可以用两种方式测试：

- 自动触发：输入`我改动了什么`，让Claude判断自动判断并调用
- 手动调用：输入`/summarize-changes`

配置正确时，Claude 会基于当前 `git diff HEAD` 返回改动摘要和潜在风险。

![[Pasted image 20260602113451.png|400]]

# 三、Skill的存储与结构

## 1、存储作用域

Skill存放位置决定生效范围。常见作用域如下：

| 级别  |                 路径                  |   适用范围   |    说明    | 覆盖优先级  |
| :-: | :---------------------------------: | :------: | :------: | ------ |
| 企业级 | managed settings 配置（参考[[Settings]]） | 组织内所有用户  | 由管理员统一下发 | 最高     |
| 个人级 | `~/.claude/skills/<name>/SKILL.md`  | 当前用户所有项目 | 适合通用工作流  | 中高     |
| 项目级 |  `.claude/skills/<name>/SKILL.md`   |   当前项目   | 适合项目专用规则 | 中      |
| 插件级 |  `<plugin>/skills/<name>/SKILL.md`  |  插件启用处   | 使用插件命名空间 | 独立命名空间 |
同名 Skill 的覆盖规则通常是：

> 企业级 > 个人级 > 项目级

插件Skill使用**插件命名空间**，不直接与普通个人级、项目级 Skill 冲突。

插件Skill使用`plugin-name:skill-name`命名空间，不与其他级别冲突。调用时表现为`/plugin-name:skill-name`。

如果在`.claude/commands/`有和 Skill 同名的 `.md` 文件，则 skill 优先。

如果在 skill 文件夹里加上`.claude-plugin/plugin.json`，Claude 会把这个 skill 文件夹当成一个插件加载。

假设你有一个 skill：

```text
.claude/skills/my-tool/SKILL.md
```

正常情况下，它只是一个普通 skill。但如果在这个 skill 文件夹里再加一个插件配置文件：

```text
.claude/skills/my-tool/.claude-plugin/plugin.json
```

那么 Claude Code 会把整个 `my-tool` 文件夹当成一个**plugin 插件**来加载，而不只是单纯的 skill。

这样一来，这个目录就可以捆绑更多东西，不只是 skill。

Claude Code 加载成插件时，插件名显示成`my-tool@skills-dir`，这里 `@skills-dir` 说明这个插件来自 skills 目录，而不是普通插件目录。

## 2、目录结构

每个Skill是一个**独立目录**，`SKILL.md`是入口文件，必须存在。Skill目录中还可以放辅助文件、模板、示例和脚本。

示例：

```text
my-skill/
├── SKILL.md           # 主指令，必须存在
├── template.md        # 模板文件，可选
├── reference.md       # 详细参考资料，可选
├── examples/
│   └── sample.md      # 示例输出，可选
└── scripts/
    └── validate.sh    # 辅助脚本，可选
```

`SKILL.md`应该负责说明：

- 这个 Skill 用来做什么
- 什么时候使用
- Claude 应该如何执行任务
- 辅助文件放在哪里
- 哪些内容需要按需读取

例如，对于辅助文件：

```markdown
## 附加资源

- 完整 API 规范见 [reference.md](reference.md)
- 输出模板见 [template.md](template.md)
- 示例结果见 [examples/sample.md](examples/sample.md)
```

建议 `SKILL.md` 保持简洁，把详细参考资料拆到辅助文件中。这样 Skill 被加载时，Claude 先看到核心指令，需要时再读取具体文件。

## 3、辅助文件使用原则

辅助文件适合放置以下内容：

| 文件类型           | 适合内容              |
| -------------- | ----------------- |
| `reference.md` | 长篇 API 文档、规范、背景资料 |
| `template.md`  | 固定输出模板            |
| `examples/`    | 示例输入、示例输出         |
| `scripts/`     | 校验脚本、生成脚本、辅助命令    |
| `assets/`      | 图片、表格、静态资源        |
`SKILL.md`不宜塞入全部内容，如果内容较多，推荐结构是：

- **SKILL.md**：入口、规则、导航、执行步骤
- **辅助文件**：详细资料、模板、示例、脚本

这样既能减少上下文占用，也便于维护。

## 4、来自额外目录的Skill

Claude Code 支持通过`--add-dir`参数或`/add-dir`命令来授予额外目录的文件访问权限而不是配置发现。

但对于 Skills，有一个特殊行为：**额外目录中的`.claude/skills/`也会被发现和加载**。此例外仅适用于 `--add-dir` 和 `/add-dir`。`settings.json` 中的 `permissions.additionalDirectories` 设置仅授予文件访问权限，不加载 skills。

例如：

```shell
claude --add-dir ../shared-tools
```

如果额外目录中存在`../shared-tools/.claude/skills/my-skill/SKILL.md`，这个Skill也会被当前会话发现。

其他 `.claude/` 配置（如 subagents、命令和输出样式）不会从其他目录加载。

例如前面学习的额外目录中的`CLAUDE.md`默认不自动加载，需要设置`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`才加载。

## 5、实时变更检测

`Claude Code`会监控 Skills 目录的变化。在 `~/.claude/skills/`、项目 `.claude/skills/` 或 `--add-dir` 目录内的 `.claude/skills/` 中添加、编辑或删除 skill 会在当前会话中生效，无需重新启动。创建在会话启动时不存在的顶级 skills 目录需要重新启动 Claude Code，以便可以监视新目录。

> 实时变更检测仅涵盖 `SKILL.md` 文本。对于也是插件的 skill 文件夹，对 `hooks/`、`.mcp.json`、`agents/` 和 `output-styles/` 的更改需要 `/reload-plugins` 才能生效。


## 6、项目级skills加载

项目级 skills 会从多个位置加载：Claude Code 会读取起始目录中的 `.claude/skills/`，以及从起始目录向上直到仓库根目录之间各级父目录里的 `.claude/skills/`。因此，即使你在某个子目录中启动 Claude，也仍然可以使用仓库根目录定义的 skills。

当你在起始目录下方的子目录中处理文件时，Claude Code 还会按需发现该子目录中的嵌套 skills。

这适合 monorepo 场景：仓库根目录可以定义通用 skills，每个子包也可以定义自己的专用 skills。


# 四、配置Skills

## 1、SKILL.md 组成

`SKILL.md` 由两部分组成：顶部的 YAML frontmatter 和后面的 Markdown 正文。

| 部分               | 作用                                                       |
| ---------------- | -------------------------------------------------------- |
| YAML frontmatter | 描述 skill 的元信息，例如名称、描述、适用场景。Claude Code 根据这些信息发现和选择 skill |
| Markdown 正文      | 定义 skill 的具体执行方式，包括工作流程、规则、检查清单、示例和注意事项                  |

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