---
title: Claude Code Skill 系统
date: 2026-06-02
tags: [coding-tool, workflow, agent]
source_count: 1
---

# Claude Code Skill 系统

Claude Code 的 Skill 扩展机制，通过 `SKILL.md` 文件将可复用的指令、流程、参考资料和脚本封装成可调用能力。

## 核心特性

### 按需加载

与每次会话自动加载的 `CLAUDE.md` 不同：

- 会话开始时，Claude Code 只看到可自动调用 Skill 的名称和描述
- Skill 被手动调用或自动判断为相关时，正文才进入上下文
- 设置为仅手动调用的 Skill，连描述也不会进入 Claude 上下文

这使得 Skill 适合存放较长的操作手册、检查清单和团队规范，避免持续占用 token。

### 与相关机制的关系

| 机制 | 关系 |
|---|---|
| `Slash Command` | Skill 可通过 `/skill-name` 手动调用 |
| `Subagent` | Skill 可通过 `context: fork` 在隔离子代理中执行 |
| `Hooks` | Skill 可配置限定于自身生命周期的 hooks |
| `Permissions` | Skill 可通过 `allowed-tools` 预批准工具权限 |

Skills 遵循 `Agent Skills` 开放标准，可在多个支持该标准的 AI 工具间复用。

## 存储作用域

| 级别 | 路径 | 适用范围 | 覆盖优先级 |
| :---: | :--- | :---: | :--- |
| 企业级 | managed settings 配置 | 组织内所有用户 | 最高 |
| 个人级 | `~/.claude/skills/<name>/SKILL.md` | 当前用户所有项目 | 中高 |
| 项目级 | `.claude/skills/<name>/SKILL.md` | 当前项目 | 中 |
| 插件级 | `<plugin>/skills/<name>/SKILL.md` | 插件启用处 | 独立命名空间 |

同名 Skill 覆盖规则：企业级 > 个人级 > 项目级。插件 Skill 使用 `plugin-name:skill-name` 命名空间，不与其他级别冲突。

若在 `.claude/commands/` 有同名 `.md` 文件，则 skill 优先。

### 项目级 Skills 加载规则

项目级 skills 从多个位置加载：
- 起始目录中的 `.claude/skills/`
- 从起始目录向上直到仓库根目录之间各级父目录里的 `.claude/skills/`
- 起始目录下方子目录中的嵌套 skills（按需发现）

适合 monorepo 场景：根目录定义通用 skills，子包定义专用 skills。

### 额外目录中的 Skill

通过 `--add-dir` 参数或 `/add-dir` 命令授予额外目录时，该目录中的 `.claude/skills/` 也会被自动发现和加载（此例外仅适用于 Skills）。

## 目录结构

每个 Skill 是独立目录：

```text
my-skill/
├── SKILL.md           # 主指令，必须存在
├── template.md        # 模板文件，可选
├── reference.md       # 详细参考资料，可选
├── examples/          # 示例输入/输出，可选
└── scripts/           # 辅助脚本，可选
```

辅助文件适合放置：长篇 API 文档、固定输出模板、示例输入输出、校验脚本、图片和静态资源。

`SKILL.md` 应保持简洁，详细资料拆到辅助文件中，减少上下文占用。

## 内容类型

### 参考型 Skill

为 Claude 提供当前工作所需的背景知识（约定、模式、风格指南、领域知识），以内联方式加载，使 Claude 能在当前对话上下文中直接使用。

适用场景：希望 Claude 在相关任务中自动参考这些规则。

### 任务型 Skill

为 Claude 提供某个具体操作的分步说明（部署应用、提交、代码生成等），通常由用户显式调用。

若不希望自动调用，在 frontmatter 添加 `disable-model-invocation: true`。

适用场景：表示明确的操作流程，由用户主动执行。

## 编写判断标准

| 问题 | 说明 |
|---|---|
| 谁来调用？ | 用户手动调用，还是 Claude 自动调用？ |
| 内容类型是什么？ | 背景知识，还是具体任务步骤？ |
| 在哪里运行？ | 内联运行，还是在 subagent 中运行？ |
| 是否复杂？ | 是否需要拆分支持文件来保持主文件简洁？ |

## SKILL.md 组成

由两部分组成：

| 部分 | 作用 |
|---|---|
| YAML frontmatter | 描述 skill 元信息（名称、描述、适用场景），Claude Code 据此发现和选择 skill |
| Markdown 正文 | 定义 skill 的具体执行方式，包括工作流程、规则、检查清单、示例和注意事项 |

## 动态上下文注入

使用 `` !`<command>` `` 语法在 Skill 内容发送给 Claude 之前执行 shell 命令，将输出替换到占位符位置。

```markdown
## 当前更改

!`git diff HEAD`
```

Claude 最终看到的是实际数据而非命令本身。多行命令使用以 ` ```! ` 开头的围栏代码块。

> 内联形式仅在 `!` 出现在行首或紧跟空白时被识别。

## 参数传递

| 占位符 | 说明 | 示例 |
|---|---|---|
| `ARGUMENTS` | 调用时传递的所有参数 | `/fix 123` → `123` |
| `ARGUMENTS[N]` / `$N` | 按 0-based 索引取参数 | `$0`, `$1`, `$2` |
| `$name` | frontmatter `arguments` 中声明的命名参数 | `arguments: [issue, branch]` |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID | 日志记录、会话特定文件 |
| `${CLAUDE_EFFORT}` | 当前 effort 级别 | `low` / `medium` / `high` / `xhigh` / `max` |
| `${CLAUDE_SKILL_DIR}` | 包含 SKILL.md 的目录 | 引用打包的脚本或文件 |

## 子代理中运行 Skill

在 frontmatter 中设置 `context: fork`，调用时启动隔离子代理执行：

- 子代理仅看到 Skill 提供的指令和显式传入的信息
- 无法访问对话历史
- 适合具有明确目标、输入和输出的任务型 Skill

`agent` 字段指定 subagent 类型：内置（`Explore`、`Plan`、`general-purpose`）或自定义 subagent。

| 方式 | 系统提示来源 | 任务来源 | 额外加载 |
|---|---|---|---|
| `context: fork` 的 Skill | 代理类型 | SKILL.md 内容 | CLAUDE.md（Explore/Plan 除外） |
| `skills` 字段的 Subagent | Subagent 正文 | Claude 的委派消息 | 预加载 Skills + CLAUDE.md |

## 调用方式与权限控制

### 调用方式配置

| 配置 | 用户可 `/name` 调用 | Claude 可自动调用 | 加载方式 |
|---|---|---|---|
| `disable-model-invocation: true` | Yes | No | 用户调用时加载完整内容 |
| `user-invocable: false` | No | Yes | Description 常驻上下文 |

默认：skill 描述被加载进上下文以便 Claude 知道何时可用，完整内容仅在调用时加载。

### Skill 内容生命周期

- 调用时 `SKILL.md` 内容作为单个消息进入会话，在整个会话期间保留
- 自动压缩时，Claude Code 会尽量把最近调用过的 Skill 重新附加到压缩后的上下文
- 每个 Skill 最多保留 5,000 tokens，所有 Skill 合计最多 25,000 tokens
- 若 Skill 在第一次响应后似乎不再影响行为，可重新调用以恢复完整内容

### 预先批准工具

`allowed-tools` 让 Claude 在调用该 Skill 时可以免确认使用列出的工具：

- 写在 `allowed-tools` 中的工具：免批准使用
- 未写的工具：仍可调用，但是否需批准取决于权限设置
- 想禁止工具：需在权限设置中配置 deny rules

项目级 Skill 的 `allowed-tools` 仅在接受 workspace trust 后生效。

### 限制 Skill 访问

三种方式：
1. 在 `/permissions` 中添加拒绝规则 `Skill`（关闭总开关）
2. 通过权限规则允许或拒绝特定 skill（如 `Skill(commit)`、`Skill(deploy *)`）
3. 在 frontmatter 中设置 `disable-model-invocation: true`

### 从设置覆盖可见性

`skillOverrides` 用于在设置层面控制 Skill 可见性，适合不方便编辑 SKILL.md 的场景（共享项目仓库、MCP 服务器提供、外部来源）。

| 值 | 列出给 Claude | 是否出现在 `/` 菜单 |
|---|---|---|
| `"on"` | 名称和描述 | 是 |
| `"name-only"` | 仅名称 | 是 |
| `"user-invocable-only"` | 隐藏 | 是 |
| `"off"` | 隐藏 | 隐藏 |

可通过 `/skills` 菜单交互式生成配置，保存到 `.claude/settings.local.json`。

## Frontmatter 字段参考

| 字段 | 必须 | 说明 |
| :--- | :---: | :--- |
| `name` | 否 | skill 名称。省略则使用目录名。仅小写字母、数字和连字符，最多 64 字符 |
| `description` | 推荐 | skill 功能和适用场景。Claude 据此判断何时调用 |
| `when_to_use` | 否 | 补充说明触发场景，追加在 description 后，一起计入 1536 字符上限 |
| `argument-hint` | 否 | 自动补全时显示的参数提示 |
| `arguments` | 否 | 命名参数列表，正文中用 `$name` 引用 |
| `disable-model-invocation` | 否 | 默认 `false`。`true` 时禁止自动加载，只能手动调用 |
| `user-invocable` | 否 | 默认 `true`。`false` 从 `/` 菜单中隐藏 |
| `allowed-tools` | 否 | 预先批准的工具列表 |
| `disallowed-tools` | 否 | 临时移除的工具（仅 Skill 运行期间，下一条消息后恢复） |
| `model` | 否 | Skill 触发时使用的模型 |
| `effort` | 否 | Skill 触发时的推理强度 |
| `context` | 否 | `fork` 时在隔离子代理中执行 |
| `agent` | 否 | `context: fork` 时使用的 subagent 类型 |
| `hooks` | 否 | 限定于该 skill 生命周期的钩子 |
| `paths` | 否 | 适用文件范围，匹配时才自动加载 |
| `shell` | 否 | `` !`command` `` 的 shell，`bash`（默认）或 `powershell` |

## 实时变更检测

Claude Code 监控 Skills 目录变化。在 `~/.claude/skills/`、项目 `.claude/skills/` 或 `--add-dir` 目录内的 `.claude/skills/` 中增删改 skill 会在当前会话中实时生效，无需重启。

> 实时变更检测仅涵盖 `SKILL.md` 文本。插件型 skill 文件夹中的 `hooks/`、`.mcp.json`、`agents/` 和 `output-styles/` 变更需 `/reload-plugins` 生效。

## 相关页面

- [[Claude Code Skill 创建]] — 创建 Skill 的实操步骤与示例
- [[Claude Code 命令类型]] — Slash Command 五类分类体系
- [[Claude Code 内置命令]] — 内置命令速查
- [[Claude Code]] — Claude Code 实体页面

## 来源

- [[Skill]]