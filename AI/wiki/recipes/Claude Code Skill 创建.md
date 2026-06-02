---
title: Claude Code Skill 创建
date: 2026-06-02
tags: [coding-tool, workflow, agent]
source_count: 1
---

# Claude Code Skill 创建

创建 Claude Code Skill 的实操步骤，涵盖项目级/个人级 Skill、动态上下文注入和参数传递。

## 创建项目级 Skill

### 1. 创建 Skill 目录

```bash
mkdir -p .claude/skills/summarize-changes
```

目录名即 Skill 名，对应命令 `/summarize-changes`。

### 2. 编写 SKILL.md

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

其中 `` !`git diff HEAD` `` 是动态上下文注入，Claude 会看到实际 diff 内容。

### 3. 测试 Skill

两种方式：
- **自动触发**：输入"我改动了什么"，让 Claude 自动判断并调用
- **手动调用**：输入 `/summarize-changes`

## 创建个人级 Skill

放到个人目录中对所有项目生效：

```bash
mkdir -p ~/.claude/skills/summarize-changes
```

项目级 Skill 适合只服务当前仓库；个人级 Skill 适合多个项目都能复用的通用流程。

## 常用 Frontmatter 配置

### 禁止自动调用（纯手动触发）

```yaml
---
name: deploy
description: 将应用部署到生产环境
disable-model-invocation: true
---
```

适用于有副作用的工作流（如 `/commit`、`/deploy`），避免 Claude 自动执行。

### 隐藏于菜单（纯背景知识）

```yaml
---
name: api-conventions
description: 本代码库的 API 设计规范
user-invocable: false
---
```

适用于不可作为命令操作的背景知识。

### 预批准工具

```yaml
---
name: commit
description: 暂存并提交当前更改
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

### 子代理执行

```yaml
---
name: deep-research
description: 深入研究某个主题
context: fork
agent: Explore
---
```

`context: fork` 在隔离子代理中运行，`agent: Explore` 仅看到 SKILL.md 内容和代理自己的系统提示。

## 参数传递示例

### 位置参数

```markdown
---
name: migrate-component
description: 将组件从一个框架迁移到另一个框架
---

将 $0 组件从 $1 迁移到 $2。
保留所有现有行为和测试。
```

调用：`/migrate-component SearchBar React Vue`

### 命名参数

```yaml
---
name: convert-file
argument-hint: [filename] [format]
arguments: filename format
---
```

正文：`请将 $filename 导出为 $format 格式。`

## 动态上下文注入实战

### 单命令注入

```markdown
## PR 上下文
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

### 多命令注入

````markdown
## 环境

```!
node --version
npm --version
```
````

### PR 总结 Skill 完整示例

```yaml
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

## 辅助文件组织

Skill 目录中可放置辅助文件：

| 文件类型 | 适合内容 |
|---|---|
| `reference.md` | 长篇 API 文档、规范、背景资料 |
| `template.md` | 固定输出模板 |
| `examples/` | 示例输入、示例输出 |
| `scripts/` | 校验脚本、生成脚本、辅助命令 |
| `assets/` | 图片、表格、静态资源 |

在 `SKILL.md` 中引用：

```markdown
## 附加资源

- 完整 API 规范见 [reference.md](reference.md)
- 输出模板见 [template.md](template.md)
- 示例结果见 [examples/sample.md](examples/sample.md)
```

## 项目运行配方生成

### 使用 `/run-skill-generator`

1. 首次运行让 Claude Code 记录启动方式：
   ```
   /run-skill-generator 这是一个 Rust CLI 项目。构建用 cargo build，运行用 cargo run。请记录这个项目的运行方式。
   ```

2. 生成后，后续使用 `/run` 自动加载该 skill 运行项目

3. 使用 `/verify` 验收代码改动

每个项目运行一次即可；构建或启动流程变化时需再次运行。

## 常见场景模板

### 代码审查 Skill

```markdown
---
description: 审查当前代码变更，标记潜在风险和改进建议
disable-model-invocation: true
---

## 当前变更

!`git diff HEAD`

## 审查清单

- [ ] 是否存在逻辑错误
- [ ] 是否缺少错误处理
- [ ] 是否有性能隐患
- [ ] 是否符合项目编码规范
- [ ] 测试是否充分

请逐条检查并给出改进建议。
```

### 提交信息生成 Skill

```markdown
---
description: 根据当前变更生成规范的提交信息
disable-model-invocation: true
allowed-tools: Bash(git *)
---

## 变更内容

!`git diff --staged`

## 指令

根据上方变更生成符合 Conventional Commits 规范的提交信息。
格式：`<type>(<scope>): <subject>`

如果暂存区为空，请先执行 `git add .`。
```

## 相关页面

- [[Claude Code Skill 系统]] — Skill 机制、存储作用域、权限控制的完整概念说明
- [[Claude Code 命令类型]] — Slash Command 五类分类体系
- [[Claude Code 内置命令]] — 内置命令速查，含 `/skills` 管理命令
- [[Claude Code]] — Claude Code 实体页面

## 来源

- [[Skill]]