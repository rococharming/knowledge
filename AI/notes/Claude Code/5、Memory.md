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

- 放到Skill中，作为可复用工作流（参考[[6、Skill|Skill]]）。
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

```rust
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

启用后，会从额外目录加载：

- `CLAUDE.md`
- `.claude/CLAUDE.md`
- `.claude/rules/*.md`
- `CLAUDE.local.md`

其中，`CLAUDE.local.md` 是否加载还会受到 `--setting-sources` 的影响。`--settings-sources`用来指定`Claude Code`本次启动时读取哪些配置来源，参数值是一个逗号分隔列表，可选值包括：`user`、`project`、`local`。其中 `local` 对应本地个人配置，例如 `.claude/settings.local.json`，而在记忆文件体系里，`CLAUDE.local.md` 也属于 local 范围。



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
- `#`操作符写入

## 2、/init初始化

如果项目还没有`CLAUDE.md`，可先运行`/init`命令生成。

`Claude Code`会分析代码库，并生成一个初始`CLAUDE.md`，通常包含它发现的构建命令、测试说明和项目约定。

如果 `CLAUDE.md` 已经存在，`/init` 会建议改进，而不是直接覆盖已有文件。

如果要启用新版初始化交互流程，可以指定`CLAUDE_CODE_NEW_INIT`环境变量：

```shell
CLAUDE_CODE_NEW_INIT=1 claude
```

新版 `/init` 会询问需要设置哪些内容，例如 `CLAUDE.md`、`skills` 和 `hooks`，然后探索代码库、补充问题，并在写入文件前给出可审查的方案。

![[Pasted image 20260522111533.png|500]]


## 3、使用`/memory`查看和编辑

`/memory`是管理记忆内容的主要入口。

它可以用于：

- 查看当前会话加载了哪些`CLAUDE.md`
- 查看当前会话加载了哪些 `CLAUDE.local.md`
- 查看`.claude/rules/*md`是否生效
- 启动或关闭自动记忆
- 打开自动记忆目录
- 打开子代理记忆目录
- 在编辑器中打开对应记忆文件

示例：

![[Pasted image 20260522112849.png|500]]


## 4、使用`#`快捷写入记忆

在交互输入中，可以用`#`开头快速添加记忆，例如：

```text
# 在该项目中总是使用 pnpm 而不是 npm 安装
```

`Claude Code` 会提示你选择要把这条内容保存到哪个记忆文件中或自动写入。



# 四、编写规范的CLAUDE.md

## 1、控制文件大小

`CLAUDE.md` 会在会话开始时加载到上下文窗口中，并与对话内容一起消耗 `token`。因此，它不应该无限扩张。

通常建议单个 `CLAUDE.md` 控制在 **200 行以内**。如果内容越来越多，可以考虑：

- 删除不需要每次对话中都出现的内容
- 将重复可执行的多步骤流程做成skill
- 按局部规则放到`.claude/rules/`并使用`paths`限定生效范围
- 使用`@path`导入改善组织结构

需要注意，`@path` 导入只能改善组织方式，不能减少上下文占用。被导入的文件仍然会在启动时展开并加载进上下文。


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

如果是大型 `monorepo`，而上层目录或其他团队目录中的规则与你当前工作无关，可以使用 `claudeMdExcludes` 排除。（详见[[#^claude-md-excludes|排除特定 CLAUDE.md 文件]]）。


# 五、@path导入

## 1、基本语法

`CLAUDE.md` 支持用 `@path/to/import` 导入其他文件。被导入的文件会展开，并在会话启动时与当前 `CLAUDE.md` 一起加载到上下文中。

示例：

```markdown
请参阅 @README 了解项目概况，并参阅 @package.json 查看可用命令。

# 补充说明

- - Git 工作流参考 @docs/git-instructions.md
```

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

## 3、递归导入深度

被导入的文件还可以继续导入其他文件，但最多支持 **5 层**递归导入。


## 4、适合导入的内容

适合通过 `@path` 导入的内容包括：

- README
- package.json
- Git 工作流说明
- 团队开发规范
- 本地个人偏好文件等

例如：

```markdown
# 个人偏好
- @~/.claude/my-project-instructions.md
```

第一次在项目中遇到外部导入时，`Claude Code` 会显示审批对话框，列出相关文件。如果拒绝导入，该导入会保持禁用，审批对话框不会再次出现。


# 六、CLAUDE.local.md

## 1、概念

`CLAUDE.local.md` 是当前项目中的个人本地记忆文件。它适合存放不应该提交到版本控制的内容，例如：

- 个人常用命令
- 本地开发环境差异
- 私有沙盒URL
- 个人偏好的测试数据
- 临时调试说明

通常应将它加入 `.gitignore`：

```gitignore
CLAUDE.local.md
```

## 2、 与git worktree的关系

如果在同一个仓库的多个 `git worktree`工作，需要注意：

被`Git`忽略的`CLAUDE.local.md`只存在于创建它的那个`worktree`，不会自动同步到其他`worktree`。因为`worktree`本质上是一个干净的`checkout`，所以未跟踪文件默认不会存在。

如果希望多个`worktree`共享同一份个人指令，更推荐在`CLAUDE.md`从用户目录导入一个文件，例如：

```markdown
# 个人偏好  
  
- @~/.claude/my-project-instructions.md
```

由于团队其他成员机器没有`~/.claude/my-project-instructions.md`文件，因此不会导入。

不过，`Claude Code`还提供了一种机制，那就是项目根目录下的`.worktreeinclude`文件。该文件用于指定在创建新的`worktree`时，需要复制进去的，被Git忽略的文件。

当`Claude Code`通过以下方式创建 Git worktree 时，会读取这个文件：

- `claude --worktree`
- `EnterWorktree`工具
- 子代理的`isolation: worktree`

`.worktreeinclude` 中的匹配规则使用 `.gitignore` 语法

只要同时满足以下两个条件的文件才被复制：

1. 匹配`.worktreeinclude`中的某条规则
2. 本身也被 Git 忽略

示例：

```
# 本地环境文件
.env
.env.local

# API 凭据
config/secrets.json

# 本地个人记忆文件
CLAUDE.local.json
```


# 七、AGENTS.md

Claude Code 默认读取的是 `CLAUDE.md`，而不是`AGENTS.md`。

如果你的仓库已经为其他编码代理维护了 `AGENTS.md`，不需要重复写一份相同内容。可以创建一个 `CLAUDE.md`，在其中导入 `AGENTS.md`：

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

需要注意，Windows 创建符号链接通常需要管理员权限或开启 Developer Mode，因此在 Windows 上更推荐使用 `@AGENTS.md` 导入。

# 八、使用.claude/rules/整理规则

### （1）rules规则

当项目规模变大时，如果所有规则都堆在一个`CLAUDE.md`中，容易出现几个问题：

- 文件越来越长，不利于阅读和维护
- 不同主题的规则混在一起，不便于团队协作更新。
- 某些只适用于局部目录的规则，也会被每次对话无差别加载

更大的问题是，如果这些内容在会话启动时一次性加载，那么会消耗大量上下文。

`.claude/rules`的作用是**把规则拆分为独立文件，并支持按路径生效**。这样既可以让规则体系更清晰，也可以减少无关谷子额



### （2）基本设置方式

使用 `.claude/rules/` 很简单：只需要把 Markdown 文件放到项目的 `.claude/rules/` 目录中即可。

每个文件最好只覆盖一个主题，并使用清晰、可读的文件名，例如：

- testing.md
- code-style.md
- security.md
- api-design.md

一个典型结构如下：
```shell
your-project/
├── .claude/
│   ├── CLAUDE.md           # 主项目指令
│   └── rules/
│       ├── code-style.md   # 代码风格指南
│       ├── testing.md      # 测试约定
│       └── security.md     # 安全要求
```

`.claude/rules/` 下的所有 `.md` 文件都会被递归发现，因此你也可以继续按领域拆分子目录，例如：
- `frontend/`
- `backend/`

这样更适合大型项目或 monorepo 进行分层管理。

### （3）无条件加载的规则

如果某个规则文件没有写 `paths`的`YAML frontmatter`，那么它会在启动时直接加载，优先级与`CLAUDE.md`相同。

这类规则适合放置对整个项目都成立的全局规范，例如：

- 通用代码风格
- 提交前测试要求
- 安全基线要求
- 全项目统一的命名约定

也就是说，没有 `paths` 的规则，本质上就是拆分版的全局指令文件。

### （3）路径特定规则 ^path-rules

如果某些规则只适用于特定目录或文件类型，可以在规则文件顶部使用`YAML frontmatter`的`paths`字段进行限定。

示例：

```yaml
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规则

- 所有 API 接口都必须包含输入校验
- 使用统一的错误响应格式
- 补充 OpenAPI 文档注释

```

这表示：只有当`Claude Code`处理匹配 `src/api/**/*.ts` 的文件时，这组规则才会生效。

`paths`支持glob模式来匹配文件路径，可以根据目录、扩展名，或者二者组合进行限制。

常见示例如下：

- `**/*.ts`：匹配任意目录下的TypeScript文件
- `src/**/*`：匹配`src/` 目录下的所有文件
- `*.md`：匹配项目根目录中的所有 Markdown 文件

对于`paths`字段，也可以写多个模式，还可以通过花括号展开一次匹配多个扩展名。

示例：

```yaml
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

这类写法适合把同一类规则应用到多个相关目录或多种文件类型上。


### （4）使用符号链接共享规则

`.claude/rules`目录支持符号链接，因此可以把一套公共规则维护在统一位置，再链接到多个项目复用。

示例：

```shell
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

上面两种方式分别表示：

- 将一个共享规则目录链接进项目
- 将某个单独规则文件链接进项目

### （5）项目级规则

除了项目内的 `.claude/rules/`，你还可以在用户主目录下维护一套个人规则：

```shell
~/.claude/rules/
├── preferences.md    # 个人编码偏好
└── workflows.md      # 个人工作流习惯
```

这类规则会应用到你机器上的所有项目中，适合保存那些**不依赖具体项目**、但你希望 Claude 始终遵循的偏好，例如：

- 你偏好的代码风格
- 你习惯的工作流
- 你默认采用的分析或修改方式

加载顺序上，**用户级规则会先于项目规则加载**，因此如果二者发生冲突，通常以**项目规则优先**。这也符合实际场景：个人偏好可以通用，但项目规范应优先于个人习惯。



# 四、大型团队管理CLAUDE.md

## 1、部署组织级CLAUDE.md

在团队或组织内推广`Claude Code`时，可以通过部署一份集中管理的 `CLAUDE.md`，为所有开发者提供统一的行为指引。这样做的目的，是让`Claude Code`在不同成员的机器上都遵循一致的团队规范，例如代码风格、质量要求、合规提醒和通用协作约定。

组织级 `CLAUDE.md` 需要放置在系统指定的托管策略路径中：

- **macOS**：`/Library/Application Support/ClaudeCode/CLAUDE.md`
- **Linux / WSL**：`/etc/claude-code/CLAUDE.md`
- **Windows**：`C:\Program Files\ClaudeCode\CLAUDE.md`

**组织级 `CLAUDE.md` 不能被个人设置排除**。这意味着只要文件被部署到托管策略位置，它就会始终生效，以确保组织级规范不会被用户本地配置绕过。

## 2、排除特定 CLAUDE.md 文件 ^claude-md-excludes

在大型 monorepo 中，仓库上层目录或其他团队维护的目录里，可能也存在 `CLAUDE.md` 或 `.claude/rules/` 文件。这些指令不一定和你当前负责的部分有关，甚至可能对当前工作产生干扰。

这时可以使用`claudeMdExcludes`设置，按路径或glob模式排除特定的`CLAUDE.md`文件或规则目录，避免它们被加载进上下文。

一般在`.claude/settings.local.json`中这样设置：

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

`claudeMdExcludes` 使用 **glob 语法**，并且是针对**绝对文件路径**进行匹配的。

**托管策略中的 `CLAUDE.md` 不能被排除。** 也就是说，`claudeMdExcludes` 只能用于跳过普通项目文件或本地规则，不能绕过组织统一下发的托管指令。


# 五、自动记忆

## 1、概念

自动记忆（`Auto Memory`）可以让 `Claude Code` 在不需要我们手动维护的情况下，**跨会话积累项目相关知识**。它会在工作过程中，根据内容是否值得长期保留，自行决定是否记录一些信息，例如构建命令、调试经验、架构说明、代码风格偏好和工作流习惯。也就是说，`Claude Code`不会在每次会话后都写入记忆，而是只保存那些对未来对话可能有帮助的内容。

## 2、启用和禁用

自动记忆默认是**开启**的。可以通过两种方式控制它：

- 在会话中输入`/memory`，通过界面里的自动记忆开关启用或关闭。
- 在项目设置中设置`autoMemoryEnabled`配置

例如，关闭自动记忆：

```json
{
  "autoMemoryEnabled": false
}
```

如果希望通过环境变量禁用自动记忆，可以设置：

```shell
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```



## 3、存储位置
每个项目都有独立的自动记忆目录，默认位置是：

```bash
~/.claude/projects/<project>/memory/
```

其中 `<project>` 通常根据 Git 仓库路径推导得到，因此：

- 同一个仓库的所有`worktree`
- 同一个仓库的所有子目录

默认共享同一个自动记忆目录。

如果当前目录没有被 Git 纳入版本控制，则`<project>`使用项目根目录来确定记忆位置。

如果你希望把自动记忆改存到其他地方，可以在**用户设置**或**本地设置**中配置 `autoMemoryDirectory`，例如：

```json
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```
`
这个配置可以来自：

- policy 设置
- local 设置
- user 设置

但**不能来自项目设置**（也就是 `.claude/settings.json`），这样可以避免共享项目把自动记忆重定向到不安全的位置。

## 4、目录结构

自动记忆目录中通常会包含一个入口文件和若干主题文件，例如：

```shell
~/.claude/projects/<project>/memory/
├── MEMORY.md
├── debugging.md
├── api-conventions.md
└── ...

```

其中：

- `MEMORY.md`是**索引文件**，会记录记忆内容的组织形式
- `debugging.md`、`api-conventions.md`等是按主题拆分的详细笔记
- `Claude Code`会根据需要继续创建其他主题文件


## 5、工作方式

每次对话开始前，`Claude Code`不会把整个记忆目录全部读入上下文，而是只加载`MEMORY.md`的一部分：

- 前 200 行
- 或前 25 KB
- 取两者中较小者

超过这个范围的内容不会在启动时自动加载。为了保持启动上下文精简，`Claude Code`会尽量把详细信息拆到单独的主题文件中，而让 `MEMORY.md` 保持简洁。

像 `debugging.md`、`patterns.md` 这类主题文件不会在会话开始时自动加载。只有当 `Claude Code`认为相关信息有用时，才会按需读取这些文件。

在会话过程中，Claude 也会持续读写这些记忆文件。如果你在界面中看到：

- `Writing memory`
- `Recalled memory`

## 6、审计与编辑

自动记忆文件本质上就是普通的`Markdown`文件，因此你可以随时：

- 手动查看
- 直接编辑
- 删除不想保留的内容

如果想在会话中查看这些文件，可以使用 `/memory`。

# 六、排查记忆相关问题

下面整理了使用 `CLAUDE.md` 和`Auto memory`时最常见的几个问题，以及对应的排查思路。

## 1、Claude Code没有遵循CLAUDE.md

**需要明确一点：`CLAUDE.md`的内容并不是系统提示本身的一部分，而是会在系统提示之后，作为一条额外的用户消息传递给模型**。`Claude Code`会读取并尽量遵循这些指令，但这并不等同于硬性强制执行。尤其当指令写得不够具体，或者不同文件之间存在冲突时，遵循效果就可能不稳定。

可以按照如下顺序排查：

1. 运行`/memory`，确认当前会话中确实加载了`CLAUDE.md`和`CLAUDE.local.md`。如果某个文件没有出现在列表中，说明`Claude Code`当前实际看不到它。
2. 检查`CLAUDE.md`是否放在了当前会话能加载的位置
3. 尽量把指令写的具体、明确、可验证。例如，“使用 2 个空格缩进”通常会比“把代码格式化好”更容易被稳定执行。
4. 检查不同的`CLAUDE.md`文件之间是否存在冲突。如果两个文件对同一件事给出了不同要求，`Claude Code`可能会随机选择其中一个来遵循。

如果某条指令必须提升到**更强的优先级**，可以考虑使用 `--append-system-prompt`。这种方式更接近系统提示层级，但需要在每次调用时显式传入，因此更适合脚本或自动化场景，而不是日常交互式使用。

另外，调试这类问题时，`InstructionsLoaded` hook 也很有帮助。它可以准确记录哪些指令文件被加载了、在什么时候加载、以及为什么会被加载，对于排查路径规则或子目录中延迟加载的指令尤其有用。

## 2、不知道自动记忆保存了什么

如果不确定`Claude Cpde`已经记住了哪些内容，可以直接运行 `/memory`，然后打开自动记忆文件夹查看。

## 3、CLAUDE.md太大

`CLAUDE.md` 过长会占用更多上下文空间，也可能降低`Claude Code`对关键指令的遵循效果。通常建议将单个 `CLAUDE.md` 控制在 200 行以内。

如果内容已经变得很多，可以考虑以下做法：

- 使用路径限定规则，让某些指令只在处理特定文件时加载
- 删除那些并不需要在每次会话中都出现的内容
- 把全局规则、局部规则和任务说明拆开管理

需要注意的是，把内容拆成 `@path` 导入虽然有助于组织结构更清晰，但**不会减少上下文占用**。因为被导入的文件仍然会在启动时一起加载进上下文，所以导入解决的是“可维护性”问题，而不是“长度”问题。

## 4、`/compact`之后指令似乎丢失了

执行 `/compact` 之后，并不是所有指令都会以同样方式保留下来。

项目根目录下的 `CLAUDE.md` 会在压缩后继续保留。因为 `/compact` 之后，`Claude Code会重新从磁盘读取它，并再次注入到会话中。

但子目录中的嵌套 `CLAUDE.md` 不会自动重新注入。它们只有在`Claude Code`后续再次读取对应子目录中的文件时，才会重新加载。

因此，如果你发现某条指令在 `/compact` 之后消失了，常见原因通常有两种：

- 这条指令原本只存在于对话里，并没有写入文件
- 这条指令位于某个嵌套的 `CLAUDE.md` 中，而该文件在压缩后还没有被重新触发加载

如果希望某条规则在压缩后依然稳定保留，最可靠的方法是把它写进 `CLAUDE.md`，而不是只停留在对话内容里。