
## 1、Skill概念

`Skill`是 Claude Code 的扩展机制。

通过编写`SKILL.md`文件，可以把可复用的指令、流程、参考资料、脚本和辅助资源封装成一个可调用能力，让`Claude Code`在合适的任务中使用。

不同，`Skill`的正文是**按需加载**的：

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

- 自动触发：输入`我改动了什么`，让Claude自动判断并调用
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


# 四、Skill内容和编写

## 1、SKILL.md 组成

`SKILL.md` 由两部分组成：顶部的 YAML frontmatter 和后面的 Markdown 正文。

| 部分               | 作用                                                       |
| ---------------- | -------------------------------------------------------- |
| YAML frontmatter | 描述 skill 的元信息，例如名称、描述、适用场景。Claude Code 根据这些信息发现和选择 skill |
| Markdown 正文      | 定义 skill 的具体执行方式，包括工作流程、规则、检查清单、示例和注意事项                  |

## 2、SKILL内容类型

`SKILL.md`可以包含任意内容，但编写时应明确：这个 Skill 是给 Claude Code 自动参考，还是由用户手动调用。不同用途影响内容结构、调用方式和运行位置。

### （1）参考型内容

参考型 Skill 用于为 Claude 提供当前工作所需的背景知识，例如约定、模式、风格指南和领域知识。这类内容通常会以内联方式加载，使 Claude 能在当前对话上下文中直接使用这些信息。

示例：

```markdown
---
name: api-conventions
description: 本代码库的 API 设计规范
---

编写 API 接口时：

- 使用 RESTful 命名规范
- 返回统一的错误格式
- 包含请求参数校验
```

适用场景：希望 Claude 在相关任务中自动参考这些规则，而不是每次都由用户手动调用

### （2）任务型内容

任务型 Skill 用于为 Claude 提供某个具体操作的分步说明，例如部署应用、提交、代码生成等。这类 Skill 通常更适合由用户通过 `/skill-name` 显式调用，而不是让 Claude 自动判断是否触发。

如果不希望 Claude 自动调用该 Skill，可以在`YAML frontmatter`添加：

```YAML
disable-model-invocation: true
```

示例：

```markdown
---
name: deploy
description: 将应用部署到生产环境
context: fork
disable-model-invocation: true
---

部署应用：

1. 运行测试套件
2. 构建应用
3. 推送到部署目标

```

适用场景：希望 Skill 表示一个明确的操作流程，由用户主动执行。


## 3、编写Skill时的判断标准

编写`SKILL.md`时，可以重点考虑以下问题：

|问题|说明|
|---|---|
|谁来调用？|是用户手动调用，还是 Claude 自动调用？|
|内容类型是什么？|是背景知识，还是具体任务步骤？|
|在哪里运行？|是内联运行，还是在 subagent 中运行？|
|是否复杂？|是否需要拆分支持文件来保持主文件简洁？|

对于复杂 Skill，可以添加支持文件，将细节放到额外文件中，避免让主 `SKILL.md` 过长。

`SKILL.md` 的主体应尽量简洁。一旦 Skill 被加载，其内容会在整个会话中保留在上下文里，因此每一行都会带来持续的 token 成本。

## 4、Frontmatter参考

可以通过`SKILL.md`文件顶部`---`之间的 YAML frontmatter配置 skill 行为。

示例：

```yaml
---
name: my-skill
description: 这个 skill 的功能
disable-model-invocation: true
allowed-tools: Read Grep
---

你的 skill 指令 ...
```

所有字段都是可选的，但推荐填写`description`，以便 Claude Code 知道何时调用该skill。

所有YAML frontmatter说明：

| 字段                         | 必须  | 说明                                                                                                                                                                        |
| :------------------------- | :-- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`                     | 否   | skill名称。若省略则使用目录名。仅允许**小写字母、数字和连字符**（最多64字符）。                                                                                                                             |
| `description`              | 推荐  | skill的功能和适用场景。Claude用此判断何时调用该skill。若省略则使用markdown正文的第一段作为描述。                                                                                                              |
| `when_to_use`              | 否   | 补充说明 Claude 什么时候应该调用该 Skill，如触发短语、典型请求、适用场景示例。`when_to_use`的内容会追加在`description`后面，一起显示在 Skill 列表中。与`description`一起计入1536字符上限，超出部分将被截断。                                    |
| `argument-hint`            | 否   | 自动补全时显示的提示，用于说明期望的参数。它主要影响用户调用时看到的提示，例如：`/fix-issue [issue-number]`，`/convert-file [filename] [format]`。                                                                  |
| `arguments`                | 否   | 给slash command后面的位置参数起的命名参数，用于在Skill正文用`$name`引用。接收空格分隔的字符串或YAML列表。例如`argument-hint: [filename] [format]`，`arguments: filename format`，正文可写：请将`$filename`导出为`$format`格式。  |
| `disable-model-invocation` | 否   | 默认`false`。设为`true`时禁止Claude自动加载此skill，只能用户手动调用。适用于想用`/name`触发的工作流。也防止该skill被预加载到子代理上下文。                                                                                   |
| `user-invocable`           | 否   | 默认`true`。设为`false`会从`/`菜单中隐藏。适用于用户不应直接调用的背景知识。                                                                                                                            |
| `allowed-tools`            | 否   | 当此 skill 被触发时，Claude 可以使用而无需请求权限的工具。接受空格分隔的字符串或 YAML 列表。注意，这不是限制可用工具范围，所有工具仍可调用。                                                                                          |
| `disallowed-tools`         | 否   | 当此 skill 被触发时，从 Claude 可用工具池中移除的工具。也就是当这个 Skill 正在运行时，Claude 不能使用哪些工具。**注意，这个限制是临时的，一旦你给 Claude 发送下一条消息，这个工具限制就会清除，Claude 又会恢复正常的工具可用范围**。                                |
| `model`                    | 否   | 当此 skill 被触发时，Claude Code使用的模型。只影响当前这次 Skill 运行，不会永久改变会话设置。接受与 /model 相同的值，或 `inherit` 沿用会话模型                                                                             |
| `effort`                   | 否   | 当此 skill 被触发时模型的推理强度。只影响当前这次 Skill 运行，不会永久改变会话设置。选项：`low`、`medium`、`high`、`xhigh`、`max`；可用级别取决于模型。                                                                       |
| `context`                  | 否   | 设为`fork`时会从当前会话中分出一个相对独立的执行上下文，让 subagent 去处理这个 skill。                                                                                                                    |
| `agent`                    | 否   | 当`context: fork`设置时使用的 subagent 类型                                                                                                                                        |
| `hooks`                    | 否   | 限定于该skill生命周期的钩子，在skill执行过程中的某些时机（开始前、调用工具前、调用工具后、结束时），自动触发一段额外逻辑。                                                                                                        |
| `paths`                    | 否   | skill的适用文件范围，Claude只在处理匹配这些路径模式的文件时才自动加载。接受逗号分隔的字符串和YAML列表。使用与**路径特定规则**相同的格式。                                                                                            |
| `shell`                    | 否   | 决定此 skill 中 `` !`command` ``和`` ```! ``块的shell。接受 `bash`（默认）或 `powershell`。设置 `powershell` 在 Windows 上通过 PowerShell 运行内联 shell 命令。需要 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`。 |

## 5、参数传递

Skill支持多种**占位符替换**，用于接受调用时传入的参数：

| 占位符                    | 说明                                                                                                                            | 示例                                                 |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `ARGUMENTS`            | 调用 skill 时传递的所有参数。如果正文内容中不存在 `$ARGUMENTS`，参数将作为 `ARGUMENTS: <value>` 追加。                                                      | `/fix 123` → `123`                                 |
| `ARGUMENTS[N]`/ `$N`   | 按0-based索引取参数，如`$ARGUMENTS[0]` 表示第一个参数                                                                                        | `$0`, `$1`, `$2`                                   |
| `$name`                | 在 `arguments` frontmatter 列表中声明的命名参数。名称按顺序映射到位置，因此使用 `arguments: [issue, branch]` 时，占位符 `$issue` 扩展为第一个参数，`$branch` 扩展为第二个参数。 | `arguments: [issue, branch]`                       |
| `${CLAUDE_SESSION_ID}` | 当前会话ID                                                                                                                        | 适用于日志记录、创建会话特定文件或将 skill 输出与会话关联。                  |
| `${CLAUDE_EFFORT}`     | 当前effort级别                                                                                                                    | `low` / `medium` / `high` / `xhigh` / `max`        |
| `${CLAUDE_SKILL_DIR}`  | 包含该 Skill 的`SKILL.md`文件所在目录。对于插件型Skill，它指的是插件内部该 Skill 的子目录，而不是插件根目录。                                                         | 在 Bash 注入命令中，可以用它引用与 Skill 一起打包的脚本或文件，而不受当前工作目录影响。 |

示例：

```markdown
---
name: migrate-component
description: 将组件从一个框架迁移到另一个框架
---

将 $0 组件从 $1 迁移到 $2。
保留所有现有行为和测试。
```

调用：`/migrate-component SearchBar React Vue`，Skill 正文被替换为：将SearchBar组件从React迁移到Vue。保留所有现有行为和测试。


## 6、注入动态上下文

使用`` !`<command>` ``语法可以在 Skill 内容发送给Claude之前执行shell命令，将命令输出替换到占位符。这样 Claude 接收到的是实际数据而非命令本身。

示例：

```YAML
---
name: pr-summary
description: 概述拉取请求的变更
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## 拉取请求上下文
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## 你的任务
概述此拉取请求...
```

此 skill 通过使用 GitHub CLI 获取实时 PR 数据来总结拉取请求。

当此 skill 运行时：

- 每个 `` !`<command>` `` 立即执行（在 Claude 看到任何内容之前）
- 输出替换 skill 内容中的占位符
- Claude 接收带有实际 PR 数据的完全呈现的提示

这是预处理，不是 Claude 执行的内容。Claude 只看到最终结果。

> 内联形式仅在 `!` 出现在行首或紧跟在空白之后时被识别。如果 `!` 跟在另一个字符之后，占位符将保留为字面文本，命令不会运行。

对于多行命令，使用以 ` ```! ` 开头的围栏代码块而不是内联形式：

````
## 环境

```!
node --version
npm --version
```
````

`disableSkillShellExecution: true` 用于在设置中禁止来自用户目录、项目目录、插件目录或其他目录来源的 skills 和自定义命令执行 shell 命令。启用后，这些命令不会真正运行，而是会被替换为 `[shell command execution disabled by policy]`。不过，捆绑 skills 和托管 skills 不受该设置影响。这个配置最适合用于组织级的托管设置，因为用户通常无法覆盖它，可以用来统一限制不受信任来源的 shell 执行行为。


## 7、在子代理中运行 skill

当希望 skill 在隔离上下文中运行时，在`SKILL.md`中的 YAML frontmatter中增加`context: fork`。当调用Skill时，Claude Code启动一个子代理执行，Skill内容作为子代理的提示词。子代理只能看到Skill提供的指令和显式传入的信息，无法访问对话历史。

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

当此 skill 运行时：

1. 创建一个新的隔离上下文
2. 子代理接收 Skill 正文内容作为其提示词
3. `agent`字段确定执行环境（模型、工具和权限）
4. 结果被总结并返回主对话

`agent` 字段指定要使用的 subagent 配置。选项包括内置代理（`Explore`、`Plan`、`general-purpose`）或来自 `.claude/agents/` 的任何自定义 subagent。如果省略，使用 `general-purpose`。

skill 与 subagent 有两种协作模式：

| 方式                      | 系统提示                  | 任务来源          | 额外加载                            |
| ----------------------- | --------------------- | ------------- | ------------------------------- |
| 带有`context: fork`的Skill | 来自代理类型                | `SKILL.md`内容  | `CLAUDE.md`，除非代理是Explore 或 Plan |
| 带有`skills`字段的Subagent   | Subagent 的 markdown正文 | Claude 的 委派消息 | 预加载Skills + `CLAUDE.md`         |
使用 `context: fork`，你在你的 skill 中编写任务并选择一个代理类型来执行它。内置的 Explore 和 Plan 代理会**跳过CLAUDE.md和git状态**以保持其上下文较小，因此使用 `agent: Explore` 的分叉 skill 仅看到 SKILL.md 内容和代理自己的系统提示。

# 五、调用与权限控制

## 1、调用方式

Skill 默认支持两种调用：

- 用户手动输入`/skill-name`
- Claude在相关场景中自动加载。

两个 YAML frontmatter 字段让你限制这一点：

| 配置                               | 用户可`/name`调用 | Claude可自动调用 | 加载方式                        |
| -------------------------------- | ------------ | ----------- | --------------------------- |
| `disable-model-invocation: true` | Yes          | No          | Description不加载，用户调用时加载完整内容  |
| `user-invocable: false`          | No           | Yes         | Description常驻上下文，Claude自动触发 |
> 默认情况下，skill 描述被加载进上下文，以便 Claude 知道何时可用，但完整 skill 内容仅在调用时加载。但预加载 skills 的 subagent的工作方式不同，完整skill内容在启动时注入。

`disable-model-invocation: true`常用于有副作用的工作流或你想控制时间的工作流，如 `/commit`、`/deploy` 等。你不希望 Claude 因为你的代码看起来准备好了就决定部署。
`user-invocable: false`常用于不可作为命令操作的背景知识。

示例：

```markdown
---
name: deploy
description: 将应用部署到生产环境
disable-model-invocation: true
---

将 $ARGUMENTS 部署到生产环境：

1. 运行测试套件
2. 构建应用
3. 推送到部署目标
4. 验证部署是否成功
```


## 2、Skill内容生命周期

当你或者Claude调用一个 skill 时，呈现的 `SKILL.md` 内容作为单个消息进入会话，在整个会话期间保留。Claude Code 不会在后续轮次重新读取 skill 文件，因此将应该在整个任务中应用的指导写成常设说明，而不是一次性步骤。

自动压缩会话时，Claude Code 会尽量把最近调用过的 Skill 重新附加到压缩后的上下文里，但每个 Skill 最多保留 5,000 tokens，所有 Skill 合计最多 25,000 tokens；最近调用的优先，较早调用的可能被丢弃。

如果某个 Skill 在第一次响应之后似乎不再影响 Claude 的行为，通常并不是内容已经消失了，而是内容仍然存在，只是模型选择了其他工具或处理方式。可以加强该 Skill 的 `description` 和正文说明，让模型持续倾向于使用它；或者使用 hooks，以确定性的方式强制执行某些行为。

如果这个 Skill 很大，或者你在它之后又调用了多个其他 Skill，那么在自动压缩之后可以重新调用该 Skill，以恢复完整内容。


## 3、为Skill预先批准工具

`allowed-tools` 用于在某个 Skill 运行期间，**预先批准 Claude 使用指定工具**。

它的作用是：

> 让 Claude 在调用该 Skill 时，可以免确认使用列出的工具。

注意，`allowed-tools`不是工具白名单，也不会限制 Claude 只能使用这些工具。

| 情况                       | 行为                      |
| ------------------------ | ----------------------- |
| 工具写在 `allowed-tools` 中   | Claude 可以免批准使用          |
| 工具没有写在 `allowed-tools` 中 | 仍然可以调用，但是否需要批准取决于你的权限设置 |
| 想禁止某些工具                  | 需要在权限设置中配置 `deny rules` |
示例：

```YAML
---
name: commit
description: 暂存并提交当前更改
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

这个 Skill 的意思是：当用户手动调用 `/commit` 时，Claude 可以直接执行 `git add`、`git commit`、`git status` 相关命令，而不需要每次请求批准。

如果 Skill 位于项目目录`.claude/skills/`，那么`allowed-tools`只有在你接受该项目的 **workspace trust**工作区信任之后才会生效。

**因此，在信任别人仓库之前，应先检查其中的 Skills 配置，因为某个 Skill 可能通过 `allowed-tools` 给自己授予较大的工具访问权限**。

## 4、限制Claude的Skill访问

默认情况下，Claude可调用任何未设置`disable-model-invocation`的skill。

控制 Claude 可以调用哪些 skills 有三种方式：

（1）通过在 `/permissions` 中拒绝 Skill 工具来禁用所有 skills

```text
# Add to deny rules: 
Skill
```

添加拒绝规则`Skill`，相当于关闭总开关，Claude无法调用任何skill。

（2）通过权限规则允许或拒绝特定skill

示例：

```text
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

（3）通过在其 frontmatter 中添加 `disable-model-invocation: true` 来隐藏单个 skill。

在`SKILL.md` frontmatter中添加`disable-model-invocation: true`，这会从 Claude 的上下文中完全删除该 skill。该skill不会被Claude自动发现或调用。


## 5、从设置覆盖skill可见性

`skillOverrides`用于在设置层面控制 Skill 的可见性，而不是修改Skill 自身的 frontmatter 来控制。

它适合用于那些你不想直接编辑`SKILL.md`的Skill，例如：

- 已经提交到共享项目仓库中的 Skill
- 由 MCP 服务器提供的 Skill
- 来自外部来源、不方便修改源文件的 Skill

`SkillOverrides` 是一个对象：

- 每个键是一个Skill名称
- 每个值是该Skill的可见性状态

可见性状态取值如下表所示：

|值|列出给 Claude|是否出现在 `/` 菜单中|
|---|---|---|
|`"on"`|名称和描述|是|
|`"name-only"`|仅名称|是|
|`"user-invocable-only"`|隐藏|是|
|`"off"`|隐藏|隐藏|

未出现在 `skillOverrides` 中的 Skill，默认视为 `"on"`。

示例：

```json
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

可以通过 `/skills` 菜单生成该配置：

1. 打开 `/skills` 菜单
2. 选中某个 Skill
3. 按 `Space` 循环切换状态
4. 按 `Enter` 保存配置

保存后，配置会写入`.claude/settings.local.json`。