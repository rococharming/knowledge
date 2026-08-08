
# 八、使用.claude/rules/整理规则

## 1、rules规则

当项目规模变大时，如果所有规则都堆在一个`CLAUDE.md`中，容易出现几个问题：

- 文件越来越长，不利于阅读和维护
- 不同主题的规则混在一起，不便于团队协作更新。
- 某些只适用于局部目录的规则，也会被每次对话无差别加载
- 这些内容在会话启动时一次性加载，会消耗大量上下文。

`.claude/rules`的作用是**把规则拆分为独立文件，并支持按路径生效**。这样既可以让规则体系更清晰，也可以减少无关上下文的干扰。


## 2、基本目录结构

只需要把`.md`文件放到项目的`.claude/rules`目录即可。

示例：

```shell
your-project/
├── CLAUDE.md                # 主项目指令
├── .claude/
│   └── rules/
│       ├── code-style.md    # 代码风格指南
│       ├── testing.md       # 测试约定
│       └── security.md      # 安全要求
```

每个文件最好只覆盖一个主题，并使用清晰文件名，例如：

- `testing.md`
- `code-style.md`
- `security.md`
- `api-design.md`

`.claude/rules/`下的`.md`文件会被**递归**发现，因此也可以继续按领域拆分：

```shell
.claude/rules/
├── frontend/
│   └── react.md
├── backend/
│   └── api.md
└── testing.md
```


## 3、无条件加载的规则

如果规则文件没有`paths`的`YAML frontmatter`，它会在会话启动时加载。优先级与`CLAUDE.md`相同。

这类规则适合存放全项目都成立的规范，例如：

- 通用代码风格
- 提交前测试要求
- 安全基线要求
- 全项目统一命名约定

换句话说，没有 `paths` 的规则文件，本质上就是拆分版的全局项目指令。

## 4、路径特定规则

如果某些规则只适用于特定目录或文件类型，就可以在规则文件顶部使用`YAML frontmatter`的`paths`字段。

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

这表示：只有当 `Claude Code` 处理匹配 `src/api/**/*.ts` 的文件时，这组规则才会生效。

**需要注意，路径规则不是每次工具调用都会触发，而是在`Claude Code`读取匹配文件时触发**。

`paths`支持`glob`模式来匹配文件路径，可以根据目录、扩展名，或者二者组合进行限制。

常见示例如下：

|模式|含义|
|---|---|
|`**/*.ts`|任意目录下的 TypeScript 文件|
|`src/**/*`|`src/` 目录下的所有文件|
|`*.md`|项目根目录中的 Markdown 文件|
|`src/components/*.tsx`|指定目录下的 React 组件文件|

也可以一次匹配多个扩展名：

```yaml
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

这类写法适合把同一类规则应用到多个相关目录或多种文件类型上。

## 5、使用符号链接共享规则

`.claude/rules/` 支持符号链接，因此可以把一套公共规则维护在统一位置，再链接到多个项目复用。

示例：

```shell
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

第一条表示把一个共享规则目录链接进当前项目。

第二条表示把一个单独规则文件链接进当前项目。

符号链接会被正常解析和加载，并且循环符号链接会被检测和处理。

## 6、用户级规则

除了项目内的 `.claude/rules/`，还可以在用户目录下维护个人规则：

```shell
~/.claude/rules/
├── preferences.md    # 个人编码偏好
└── workflows.md      # 个人工作流习惯
```

这类规则会应用到当前机器上的所有项目，适合保存不依赖具体项目、但你希望 Claude 始终遵循的偏好，例如：

- 个人代码风格
- 默认分析方式
- 常用工作流
- 偏好的修改策略

**加载顺序上，用户级规则会先于项目规则加载，因此项目规则具有更高优先级**。

# 九、大型团队管理CLAUDE.md

## 1、组织级CLAUDE.md

在团队或组织内推广 `Claude Code` 时，可以部署一份集中管理的组织级 `CLAUDE.md`，为所有开发者提供统一行为指引。

组织级 `CLAUDE.md` 需要放置在系统指定的托管策略路径中：

- **macOS**：`/Library/Application Support/ClaudeCode/CLAUDE.md`
- **Linux / WSL**：`/etc/claude-code/CLAUDE.md`
- **Windows**：`C:\Program Files\ClaudeCode\CLAUDE.md`

组织级 `CLAUDE.md` 不能被个人设置排除。这样可以确保组织统一下发的行为指引始终生效。


## 2、排除特定 CLAUDE.md  ^claude-md-excludes

在大型`monorepo`中，仓库上层目录或其他团队目录中可能也存在`CLAUDE.md`或`.claude/rules/`。这些指令不一定和当前工作相关，甚至可能造成干扰。

这时可以使用`claudeMdExcludes`设置，按路径或glob模式排除特定的`CLAUDE.md`文件或规则目录，避免它们被加载进上下文。

一般放在`.claude/settings.local.json`中：

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

`claudeMdExcludes` 使用 **glob 语法**，并且是针对**绝对文件路径**进行匹配的。

它可以在 user、project、local 或托管策略等设置层中配置，数组会跨层合并。托管策略中的 `CLAUDE.md` 不能被排除。


# 十、auto memory

## 1、概念

`auto memory` 可以让 `Claude Code` 在不需要用户手动维护的情况下，跨会话积累项目相关知识。

它会在工作过程中，根据内容是否值得长期保留，自动决定是否记录一些信息，例如：

- 构建命令
- 调试经验
- 架构说明
- 代码风格偏好
- 工作流习惯
- 用户反复纠正过的行为模式

`Claude Code`不会在每次对话后都写入记忆，而是只保存它判断对未来会帮助的内容。


## 2、启用和禁用

自动记忆默认是**开启**的。

可以通过三种方式控制它：

1. 在会话中运行`/memory`，然后在界面中切换自动记忆开关。
![[assets/Pasted image 20260526001218.png|500]]


2. 在项目设置中设置`autoMemoryEnabled`配置

例如，关闭自动记忆：

```json
{
  "autoMemoryEnabled": false
}
```


3. 环境变量禁用

```shell
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```


## 3、存储位置

每个项目都有独立的自动记忆目录，默认位置是：

```shell
~/.claude/projects/<project>/memory/
```

其中 `<project>` 通常根据 Git 仓库路径推导得到，因此同一个仓库中的所有工作树和子目录都共享同一个存储目录。

如果项目没有纳入 Git 版本控制，则使用项目的根目录作为存储目录。

如果希望把自动记忆保存到其他位置，可以配置 `autoMemoryDirectory`：

```json
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

这个值必须是**绝对路径**，或者以 `~/` 开头。

这个配置可以来自用户、项目、本地、托管策略配置，也可以通过启动参数传入。如果写在项目设置或本地设置中，需要先信任当前工作区，避免克隆别人的项目后未经确认就把自动记忆写到意外位置。


## 4、目录结构

自动记忆目录通常包含一个入口文件（`MEMORY.md`）和若干主题文件：

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

每次对话开始时，`Claude Code`不会把整个自动记忆目录全部加载进上下文。它只会加载`MEMORY.md`的一部分：前 200 行或前 25 KB（取先满足者），超出这个范围的内容不会在启动时自动加载。

因此，`MEMORY.md`会尽量短小，作为索引文件记录整个记忆目录中有什么内容，以及详细信息存放在哪些主题文件中。

这个限制只适用于 `MEMORY.md`。`CLAUDE.md` 会完整加载，但文件越短、越具体，通常越容易被稳定遵循。

当 `Claude Code` 写入 `MEMORY.md` 后，会检查它是否接近或超过读取限制。如果接近限制，会提示把索引改短：每条记忆尽量一行，把细节移到主题文件，并合并或删除陈旧条目。如果已经超过限制，写入仍会成功，但会要求重写索引，因为超出部分下次启动时不会被加载。

检查 `MEMORY.md` 大小时，会先移除 `YAML frontmatter` 和块级 `HTML` 注释，只计算真正会加载进上下文的内容。

主题文件如`debugging.md`、`patterns.md`不会在启动时加载，只有当 `Claude Code` 认为相关信息有用时，才会使用普通文件工具按需读取。

主会话的 `auto memory` 默认不会加载到子代理中。子代理如果启用自己的记忆，会使用独立的记忆目录；如果是从当前会话 fork 出来的子代理，则会继承父会话已有上下文。

在会话过程中，如果你看到：

- `Writing memory`
- `Recalled memory`
- `Saved 2 memories`
- `Recalled 2 memories`

说明 `Claude Code` 正在读写自动记忆目录。

如果某个自动记忆文件带有 `YAML frontmatter`，`Claude Code` 后续写入它时，会在 frontmatter 中记录 `modified` 时间，用来表示这条记忆最后被更新的时间。没有 frontmatter 的文件不会因此自动新增 frontmatter。

## 6、审计与编辑

自动记忆文件本质上就是普通的`Markdown`文件，因此可以随时查看、修改、删除、拆分和重命名。

如果不确定 `Claude Code` 记住了什么，可以运行`/memory`，然后打开自动记忆文件夹检查。



# 十一、排查记忆相关问题

## 1、Claude Code没有遵循记忆文件

首先要明确：**`CLAUDE.md` 不是系统提示本身的一部分**，而是在系统提示之后，作为额外用户消息传递给模型。

因此，它会影响`Claude Code`的行为，但不等于强制执行。

排查顺序如下：

1. 运行 `/context`，确认相关 `CLAUDE.md`、`CLAUDE.local.md`、`.claude/rules/*.md` 是否确实出现在 `Memory files` 中。
2. 如果没加载，检查文件是否放在当前会话能加载的位置。
3. 如果加载了，检查是否存在相互冲突的规则
4. 把模糊指令改成具体、可验证的指令

如果只是想打开、创建或编辑这些记忆文件，可以使用 `/memory`。

如果指令必须在特定时间点运行，例如每次提交或每次文件编辑之后，请将其作为 Hook 来编写。Hook 在固定的生命周期事件中作为shell命令执行。

对于希望在系统提示词级别执行的命令，使用`--append-system-prompt`，由于必须每次调用时都传递它，因此它更适合脚本和自动化，而不是交互式使用。

使用 `InstructionsLoaded` Hook 来记录加载的确切指令文件、加载时间以及原因，这对于调试特定路径的规则或子目录中的懒加载文件非常有用。


## 2、不知道自动记忆保存了什么

如果不确定`Claude Code`已经记住了哪些内容，可以直接运行 `/memory`，然后打开自动记忆文件夹查看、编辑或删除。

## 3、CLAUDE.md太大

如果`CLAUDE.md`超过 200 行，通常应该开始整理。

可以采用以下方式：

- 删除不需要每次会话加载的内容。
- 将路径相关规则放到 `.claude/rules/`。
- 将多步骤流程改成 `skill`。
- 将临时说明从 `CLAUDE.md` 中移除。
- 将本地偏好放到 `CLAUDE.local.md` 或用户目录导入文件中。

需要注意的是，把内容拆成 `@path` 导入虽然有助于组织结构更清晰，但**不会减少上下文占用**。因为被导入的文件仍然会在启动时一起加载进上下文，所以导入解决的是“可维护性”问题，而不是“长度”问题。

## 4、/compact之后指令似乎丢失了

执行 `/compact` 之后，并不是所有指令都会以同样方式保留下来。

项目根目录的 `CLAUDE.md` 会在压缩后继续保留，因为 `/compact` 之后，`Claude Code`会重新从磁盘读取它，并再次注入到会话中。

但子目录中的嵌套 `CLAUDE.md` 不会自动重新注入。它们只有在 `Claude Code` 后续再次读取对应子目录中的文件时，才会重新加载。

因此，如果你发现某条指令在 `/compact` 之后消失了，常见原因是：

- 这条指令原本只存在于对话里，没有写入文件
- 这条指令位于嵌套 `CLAUDE.md` 中，而该目录尚未被重新触发读取
- 这条指令来自路径限定规则，但当前还没有读取匹配路径的文件。

如果希望某条规则在压缩后稳定保留，最可靠的方法是写进项目根目录的 `CLAUDE.md`，而不是只留在对话内容中。
