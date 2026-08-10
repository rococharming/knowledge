---
title: Memory
date: 2026-05-08
tags: [AI, ClaudeCode]
aliases:
  - Memory
---

# 一、概述

在 `Claude Code` 中，每次会话都会从一个新的上下文窗口开始。想要跨对话保留项目背景、使用偏好和协作经验，主要依赖两类机制：

- `CLAUDE.md`：用户手动编写，用来向`Claude Code`提供稳定、可复用的项目上下文。
- `auto memory`：由`Claude Code`自动维护，用来记录它在协作过程中逐步学习到的偏好、经验和项目模式

这两类内容都会在**新会话开始时加载**。它们本质上都**属于上下文**，而**不是绝对强制执行的配置项**。因此，内容越明确、越具体、越精炼，`Claude Code`的遵循效果通常越稳定。

两者的定位不同：

| 机制            | 谁来维护          | 主要内容            | 适合存放什么                     |
| ------------- | ------------- | --------------- | -------------------------- |
| `CLAUDE.md`   | 用户            | 明确指令、项目规则、工作流约定 | 编码规范、测试命令、目录结构、修改边界        |
| `auto memory` | `Claude Code` | 协作中自动积累的经验和模式   | 调试经验、常见构建命令、偏好、更正后总结出的工作模式 |

> `CLAUDE.md`更适合承载“事先约定”，`auto memory`更适合沉淀“使用中学习”

两者是互补关系。`CLAUDE.md`负责保证基础行为一致，`auto memory`负责让`Claude Code`在持续协作中逐渐适应具体项目和使用者习惯。


# 二、CLAUDE.md

## 1、概念

`CLAUDE.md` 是一个 `Markdown` 文件，用于为 `Claude Code` 提供跨会话的持久指令。

文件内容由用户以纯文本方式编写。`Claude Code`会在会话开始时读取这些内容，并把它们注入上下文，用于理解项目约束、工作流程和预期行为等。

`CLAUDE.md`可以服务于不同范围：

- 单个项目
- 个人工作流
- 团队共享规范
- 组织级统一部署

适合写入 `CLAUDE.md` 的内容包括：

- 构建、测试、发布等常用命令
- 代码风格、命名规则、目录约束
- 项目结构、关键模块职责、重要依赖关系
- “始终执行X”、“不要执行Y”这类长期有效的行为约束

如果某条内容是复杂的多步骤流程，或者是适用于代码库中的某个特定区域，不建议全部堆到`CLAUDE.md`。更适合的方式：

- 放到Skill中，作为可复用工作流（参考[[AI/notes/Claude Code/5、Skill|Skill]]）。
- 放到`.claude/rules/`中，并通过`paths`限定只在特定路径下生效

## 2、适合写入CLAUDE.md的场景

可以将 `CLAUDE.md` 理解为项目的“长期上下文记录”。**它适合存放那些如果不写下来，就需要在每次对话中反复解释的信息**。

当出现以下情况时，可以考虑把相关内容加入`CLAUDE.md`：

1. `Claude Code`第二次犯了同样的错误，需要用固定规则避免重复发生。
2. 审查代码发现，`Claude Code`缺少本应了解的代码库背景
3. 你在本地对话中再次输入和上次相同的纠正、说明和约定
4. 新加入的项目成员也需要掌握同样的上下文，才能高效参与项目

`CLAUDE.md`不适合承载所有内容。它应该保存每次会话都值得加载的信息，而不是临时任务说明、一次性需求和过长的背景材料。

## 3、存放位置

`CLAUDE.md` 可以放在不同位置，对应不同的作用范围。这些位置为 managed policy（托管策略）、用户指令、项目指令和本地指令。

| 作用范围     | 位置                                                                                                                                                           | 用途                               | 使用场景示例           | 共享对象       |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- | ---------------- | ---------- |
| **托管策略** | macOS：`/Library/Application Support/ClaudeCode/CLAUDE.md`  <br>Linux / WSL：`/etc/claude-code/CLAUDE.md`  <br>Windows：`C:\Program Files\ClaudeCode\CLAUDE.md` | 组织级统一指令                          | 公司编码标准、安全策略、合规要求 | 组织内所有用户    |
| **用户指令** | `~/.claude/CLAUDE.md`                                                                                                                                        | 适用于所有项目的个人全局偏好                   | 代码风格偏好、个人工具      | 仅当前用户      |
| **项目指令** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md`                                                                                                                        | 项目团队共享的指令                        | 项目架构、编码标准、常用工作流  | 通过版本控制共享   |
| **本地指令** | `./CLAUDE.local.md`                                                                                                                                          | 当前项目中的个人偏好（**应加入 `.gitignore`**） | 沙盒 URL、偏好的测试数据   | 仅当前机器、当前项目 |

实践中，**项目级指令通常优先考虑放在仓库根目录的`./CLAUDE.md`**，因为它更明显，团队成员更容易发现。如果项目已经把 Claude 相关配置统一收在 `.claude/` 目录中，也可以使用 `./.claude/CLAUDE.md`。


## 4、CLAUDE.md加载规则

**`Claude Code`会从当前工作目录开始，沿着目录树向上查找`CLAUDE.md`和`CLAUDE.local.md`**。所有发现的文件都会拼接进上下文，而不是互相覆盖。

例如，在下面目录启动`Claude Code`：

```shell
repo/
├── CLAUDE.md
└── crates/
    ├── CLAUDE.md
    └── app/
        └── src/
```

如果当前工作目录是 `repo/crates/app/`，`Claude Code` 会向上查找并加载：

```shell
repo/CLAUDE.md
repo/crates/CLAUDE.md
```

**加载顺序是从文件系统上层目录到当前工作目录**。越靠近当前工作目录的指令越晚出现在上下文中，因此也更容易影响任务。

在同一目录中，如果有`CLAUDE.local.md`会追加到`CLAUDE.md`之后，因此，同一层级下，个人本地指令会被 Claude 更晚读到。


## 5、从额外目录加载记忆文件

`--add-dir`可以让`Claude Code`访问主工作目录之外的额外目录。**但默认情况下，额外工作目录的`CLAUDE.md`不会自动加载**。

如果希望额外目录的记忆文件也被加载，需要设置环境变量`CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`：

```shell
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

启用后，会从额外目录加载：

- `CLAUDE.md`
- `.claude/CLAUDE.md`
- `.claude/rules/*.md`
- `CLAUDE.local.md`

其中，`CLAUDE.local.md` 是否加载还会受到 `--settings-sources` 的影响。`--settings-sources`用来指定`Claude Code`本次启动时读取哪些配置来源，参数值是一个逗号分隔列表，可选值包括：`user`、`project`、`local`。其中 `local` 对应本地个人配置，例如 `.claude/settings.local.json`，而在记忆文件体系里，`CLAUDE.local.md` 也属于 local 范围。



## 6、CLAUDE.md注释

`CLAUDE.md` 中可以使用块级 `HTML` 注释：

```text
<!-- 这是一段给维护者看的注释 -->
```

这些注释在注入到 `Claude Code` 上下文时会被移除，因此不会消耗上下文 `token`。

需要注意：

- 只有 Markdown 正文里的 HTML 注释在注入上下文时被移除，如果这个注释写在 Markdown 代码块里面，则它被当成代码示例的一部分保留
- 如果 `Claude Code` 使用 `Read` 工具直接读取某个 `CLAUDE.md` 文件，注释仍然可见


# 三、创建和修改CLAUDE.md

## 1、创建或修改方式

创建或修改`CLAUDE.md`有三种主要方式：

- `/init`命令初始化
- `/memory`命令打开编辑

## 2、/init初始化

如果项目还没有`CLAUDE.md`，可先运行`/init`命令生成。

`Claude Code`会分析代码库，并生成一个初始`CLAUDE.md`，通常包含它发现的构建命令、测试说明和项目约定。

如果 `CLAUDE.md` 已经存在，`/init` 会建议改进，而不是直接覆盖已有文件。

如果要启用新版初始化交互流程，可以指定`CLAUDE_CODE_NEW_INIT`环境变量：

```shell
CLAUDE_CODE_NEW_INIT=1 claude
```

新版 `/init` 会询问需要设置哪些内容，例如 `CLAUDE.md`、`skills` 和 `hooks`，然后探索代码库、补充问题，并在写入文件前给出可审查的方案。

![[assets/Pasted image 20260522111533.png|500]]


## 3、使用`/memory`查看和编辑

`/memory`是管理记忆内容的主要入口。

它可以用于：

- 查看用户和项目范围内有哪些`CLAUDE.md`
- 查看用户和项目范围内有哪些 `CLAUDE.local.md`
- 查看相关记忆文件的位置，包括尚未创建但可以创建的入口文件
- 启动或关闭自动记忆
- 打开自动记忆目录
- 在编辑器中打开对应记忆文件；如果选择的文件还不存在，会先创建它

如果要确认当前会话中哪些记忆文件已经实际加载，应运行`/context`，并查看其中的 `Memory files` 列表。

示例：

![[assets/Pasted image 20260522112849.png|500]]


# 四、编写规范的CLAUDE.md

## 1、控制文件大小

`CLAUDE.md` 会在会话开始时加载到上下文窗口中，并与对话内容一起消耗 `token`。因此，它不应该无限扩张。

通常建议单个 `CLAUDE.md` 控制在 **200 行以内**。如果内容越来越多，可以考虑：

- 删除不需要每次对话中都出现的内容
- 将重复可执行的多步骤流程做成skill
- 按局部规则放到`.claude/rules/`并使用`paths`限定生效范围
- 使用`@path`导入改善组织结构

需要注意，使用 `@path` 将内容拆分到多个文件，只能改善文件的组织和维护方式，不能减少上下文占用。Claude Code 会展开被导入文件的实际内容，并将其与引用它的 `CLAUDE.md` 一起加载到上下文中。

因此，不要为了缩小 `CLAUDE.md` 而简单地把大量内容移动到其他文件后再通过 `@path` 全部导入。只有删除不必要的内容，或者改用 Skill、带 `paths` 的局部规则等按需加载机制，才能真正减少常驻上下文占用。


## 2、使用清晰结构

建议使用 `Markdown` 标题和项目符号对指令分组。

例如，可以按如下方式组织：

```markdown
# 项目概览

# 构建和测试命令

# 代码风格

# Git 工作流

# 修改边界

# 常见问题

```

结构清晰的文档比密集的大段文字更容易被 `Claude Code` 理解和遵循。

## 3、保持具体、可验证

指令应尽量具体，避免模糊表达。

推荐写法：

```markdown
- 使用 2 个空格缩进
- 提交前运行 npm test
- API handler 放在 src/api/handlers/
```

不推荐写法：

```markdown
- 正确格式化代码
- 测试你的改动
- 保持文件格式良好
```

好的指令应该让 Claude 明确知道“要做什么”，并且结果可以被检查。


## 4、避免规则冲突

如果多个记忆文件中存在相互矛盾的规则，`Claude Code` 可能会任意选择其中一条执行。

因此，应定期检查：

- 根目录下的 `CLAUDE.md`
- 用户级 `~/.claude/CLAUDE.md`
- 子目录中的嵌套 `CLAUDE.md`
- `.claude/rules/` 中的规则文件
- `auto memory` 中自动保存的项目经验

如果是大型 `monorepo`，而上层目录或其他团队目录中的规则与你当前工作无关，可以使用 `claudeMdExcludes` 排除（详见[[#^claude-md-excludes|排除特定 CLAUDE.md 文件]]）。


# 五、@path导入

## 1、基本语法

`CLAUDE.md` 支持用 `@path/to/import` 导入其他文件。被导入的文件会展开，并在会话启动时与当前 `CLAUDE.md` 一起加载到上下文中。

示例：

```markdown
请参阅 @README 了解项目概况，并参阅 @package.json 查看可用命令。

# 补充说明

- Git 工作流参考 @docs/git-instructions.md
```

`@path` 可以出现在普通段落、列表等位置，不要求单独占一行。

需要注意，Claude Code 不会解析 Markdown 行内代码和围栏代码块中的导入语句。因此，下面的内容只会被当作普通文本，不会触发导入：

```text
`@README.md`
```

这也可以用于在 `CLAUDE.md` 中直接提到 `@path`，而不导入对应文件。

## 2、路径解析规则

导入路径支持**相对路径**和**绝对路径**。

> 注意：相对路径不是相对当前工作目录解析，而是相对于包含导入语句的文件解析。

例如：

```shell
repo/
├── CLAUDE.md
└── docs/
    └── git-instructions.md
```

如果 `repo/CLAUDE.md` 中写：

```markdown
@docs/git-instructions.md
```

它会相对于 `repo/CLAUDE.md` 所在目录解析。

也可以使用用户主目录路径：

```markdown
@~/repo/docs/git-instructions.md
```

## 3、递归导入深度

被导入的文件还可以继续导入其他文件，但最多支持 **4 层**递
归导入。

例如：

```text
CLAUDE.md 
└── 导入 a.md              第 1 次跳转 
    └── 导入 b.md          第 2 次跳转 
        └── 导入 c.md      第 3 次跳转 
            └── 导入 d.md  第 4 次跳转
```

为了避免层级过深而难以维护，实际使用时应尽量减少递归导入。

## 4、适合导入的内容

`@path` 适合拆分那些需要在每次会话中加载，但不适合全部堆放在主 `CLAUDE.md` 中的内容，例如：

- 简短的项目概况
- Git 工作流说明
- 团队开发规范
- 共享的项目约定
- 个人项目偏好
- `AGENTS.md` 等其他代理规则文件

例如：

```markdown
# 项目信息 

- 项目概况：@docs/project-overview.md 
- Git 工作流：@docs/git-instructions.md 
- 团队规范：@docs/development-rules.md 
- 个人偏好：@~/.claude/my-project-instructions.md
```

虽然也可以导入 `README.md`、`package.json` 等文件，但应注意文件大小。被导入文件的完整内容仍会进入上下文，因此不要导入内容庞大、经常变化或并非每次会话都需要的文件。

`@path` 主要用于改善内容组织，并不能减少上下文占用。如果某项知识只在特定任务中需要，更适合将其做成 Skill；如果规则只适用于部分文件，更适合使用带 `paths` 的 `.claude/rules/`。

## 5、外部导入审批

在项目级 `CLAUDE.md` 中，如果导入路径最终指向当前工作目录之外的文件，该导入会被视为外部导入。

例如：

```markdown
@~/.claude/my-project-instructions.md
```

Claude Code 第一次在该项目中遇到外部导入时，会显示审批对话框，并列出准备导入的文件。

如果拒绝审批：

- 这些外部导入会保持禁用
- 对应文件不会进入上下文
- 该项目之后不会再次显示相同的审批对话框

该机制用于防止共享项目中的 `CLAUDE.md` 在未经同意的情况下导入工作目录之外的文件。

用户级记忆文件中的导入不需要该审批，例如：

```
~/.claude/CLAUDE.md
~/.claude/rules/*.md
```

因为这些文件属于用户自己的个人配置，会被视为与其他用户级配置具有相同的信任级别。


## 6、AGENTS.md

Claude Code 比较特殊，长期记忆文件默认读取的是 `CLAUDE.md`，而不是`AGENTS.md`。

如果你的仓库已经为其他编码代理（如 Codex）维护了 `AGENTS.md`，不需要重复写一份相同内容。可以创建一个 `CLAUDE.md`，在其中导入 `AGENTS.md`：

示例：

```markdown
@AGENTS.md

## Claude Code

Use plan mode for changes under `src/billing/`.
```

如果不需要额外补充，也可以使用符号链接：

```shell
ln -s AGENTS.md CLAUDE.md
```

> 需要注意，Windows 创建符号链接通常需要管理员权限或开启 Developer Mode，因此在 Windows 上更推荐使用 `@AGENTS.md` 导入。


# 六、CLAUDE.local.md

## 1、概念

`CLAUDE.local.md` 是当前项目中的个人本地记忆文件，适合存放只与个人环境或工作习惯有关、不应该提交到版本控制的内容，例如：

- 个人常用命令
- 本地开发环境差异
- 私有沙盒URL
- 个人偏好的测试数据
- 临时调试说明

它会与项目中的`CLAUDE.md`一起加载。同一目录中，`CLAUDE.local.md`的内容会排在`CLAUDE.md`后面进入上下文。

但两者仍然属于提供给 Claude 的自然语言指令，不是具有严格覆盖机制的配置文件。因此，应尽量避免在两个文件中编写互相冲突的规则。

通常应将它**加入 `.gitignore`**：

```gitignore
CLAUDE.local.md
```

## 2、与 Git worktree 的关系

如果在同一个仓库的多个 Git worktree 中工作，需要注意：被Git 忽略的 `CLAUDE.local.md` 只存在于创建它的那个 worktree 中，不会自动出现在其他 worktree。

这是因为新建的 worktree 是一个独立的 checkout。主 worktree 中未被跟踪的文件，例如：

```text
CLAUDE.local.md
.env
```

默认不会被复制到新 worktree。

如果希望多个 `worktree` 共享同一份个人指令，可以在项目级记忆文件中导入用户目录下的文件：

```markdown
# 个人偏好  
  
- @~/.claude/my-project-instructions.md
```

这份文件存放在用户目录中，因此多个 worktree 都可以引用同一个文件。由于团队其他成员的机器没有 `~/.claude/my-project-instructions.md` 文件，因此不会导入。

Claude Code 还提供了另外一种机制，可以在项目根目录创建`.worktreeinclude`文件，用于在创建新 `worktree`时复制指定的 Git 忽略文件。

`.worktreeinclude` 使用 `.gitignore` 风格的匹配语法。文件只有同时满足以下两个条件才会被复制：

1. 匹配`.worktreeinclude`中的某条规则
2. 本身也被 Git 忽略

例如：

```
# 本地环境文件
.env
.env.local

# 本地配置
config/secrets.json

# 本地个人记忆文件
CLAUDE.local.md
```

上述配置会在 Claude Code 创建新 worktree 时，把这些文件从原工作目录复制到新 worktree。

该机制适用于 Claude Code 通过内置 Git worktree 逻辑创建的工作目录，包括：

- `claude --worktree`
- 子代理使用的隔离 worktree
- Claude Code 桌面应用创建的并行会话 worktree

需要区分“创建”和“进入”：

- 创建新 worktree 时会处理 `.worktreeinclude`
- 进入已经存在的 worktree 时，不会重新复制这些文件
- 使用普通的 `git worktree add` 手动创建 worktree 时，Claude Code 不会参与创建过程，因此不会处理 `.worktreeinclude`

例如，worktree 创建完成后再修改原目录中的：

```text
CLAUDE.local.md
```

其他已经存在的 worktree 不会自动更新，需要手动复制或重新创建。

如果配置了自定义 `WorktreeCreate` Hook，它会完全替换 Claude Code 默认的 worktree 创建逻辑，此时 `.worktreeinclude` 不会被自动处理。需要复制本地文件时，应在 Hook 脚本中自行实现。