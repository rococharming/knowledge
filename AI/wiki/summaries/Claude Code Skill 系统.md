---
title: Claude Code Skill 系统
date: 2026-06-02
tags: [coding-tool, workflow, agent]
source_count: 1
---

# Claude Code Skill 系统

Claude Code 的 Skill 扩展机制完整指南，涵盖概念、存储结构、内容编写、调用方式与权限控制。

## 核心概念

Skill 是 Claude Code 的可复用扩展机制，通过 `SKILL.md` 文件封装指令、流程、参考资料和脚本。与每次会话自动加载的 `CLAUDE.md` 不同，Skill 正文是**按需加载**的——只有被用户手动调用或被 Claude 判断为相关时，内容才进入上下文。

Skill 适合存放较长的操作手册、检查清单、团队规范、固定工作流和辅助脚本，避免长篇参考资料持续占用上下文。

## 调用方式

- **用户手动调用**：`/skill-name`
- **Claude 自动调用**：根据 `SKILL.md` frontmatter 的 `description`/`when_to_use` 判断

旧版 `.claude/commands/*.md` 已合并进 Skills 体系，官方推荐使用 Skills 目录结构。

## 捆绑 Skills

Claude Code 包含一组每个会话可用的捆绑 Skill，基于提示词而非固定逻辑：

| Skill | 用途 |
|---|---|
| `/run` | 启动应用并观察实际运行效果 |
| `/verify` | 构建并运行应用，按目标验收改动 |
| `/run-skill-generator` | 生成项目专属运行配方，供 `/run` 和 `/verify` 使用 |

## 存储作用域

| 级别 | 路径 | 适用范围 | 覆盖优先级 |
|---|---|---|---|
| 企业级 | managed settings 配置 | 组织内所有用户 | 最高 |
| 个人级 | `~/.claude/skills/<name>/SKILL.md` | 当前用户所有项目 | 中高 |
| 项目级 | `.claude/skills/<name>/SKILL.md` | 当前项目 | 中 |
| 插件级 | `<plugin>/skills/<name>/SKILL.md` | 插件启用处 | 独立命名空间 |

同名 Skill 覆盖规则：企业级 > 个人级 > 项目级。插件 Skill 使用 `plugin-name:skill-name` 命名空间。

## 目录结构

每个 Skill 是独立目录，`SKILL.md` 为入口文件：

```text
my-skill/
├── SKILL.md           # 主指令，必须存在
├── template.md        # 模板文件，可选
├── reference.md       # 详细参考资料，可选
├── examples/          # 示例输出，可选
└── scripts/           # 辅助脚本，可选
```

## 内容类型

- **参考型 Skill**：提供背景知识（约定、模式、风格指南），通常自动加载
- **任务型 Skill**：提供具体操作的分步说明（部署、提交、代码生成），通常手动调用，可设置 `disable-model-invocation: true`

## 核心机制

- **动态上下文注入**：使用 `` !`command` `` 语法在 Skill 加载前执行 shell 命令，将输出替换到内容中
- **参数传递**：支持 `ARGUMENTS`、`$N`、`$name` 等占位符替换
- **子代理执行**：设置 `context: fork` 可在隔离子代理中运行 Skill
- **实时变更检测**：Skills 目录的增删改在当前会话中实时生效（`SKILL.md` 文本级）

## 权限控制

- `allowed-tools`：Skill 运行期间预先批准指定工具，免确认使用
- `disable-model-invocation: true`：禁止 Claude 自动调用，仅用户手动触发
- `user-invocable: false`：从 `/` 菜单中隐藏，仅作为背景知识
- `skillOverrides`：在设置层面覆盖 Skill 可见性（`on`/`name-only`/`user-invocable-only`/`off`）

## 相关页面

- [[Claude Code Skill 创建]] — 创建 Skill 的实操步骤与示例
- [[Claude Code 命令类型]] — Slash Command 五类分类体系，含 Skill 相关分类
- [[Claude Code]] — Claude Code 实体页面
- [[Claude Code 内置命令]] — 内置命令速查，含 `/skills` 命令

## 来源

- [[Skill]]