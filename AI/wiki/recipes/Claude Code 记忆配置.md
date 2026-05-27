---
title: Claude Code 记忆配置
date: 2026-05-28
tags: [coding-tool, memory, workflow]
source_count: 1
---

# Claude Code 记忆配置

Claude Code 记忆系统的配置步骤与最佳实践。

## 创建 CLAUDE.md

### 方式一：/init 初始化

```bash
claude
# 在会话中执行
/init
```

Claude Code 会分析代码库，生成包含构建命令、测试说明和项目约定的初始 `CLAUDE.md`。

若 `CLAUDE.md` 已存在，`/init` 会建议改进而非直接覆盖。启用新版初始化交互：

```bash
CLAUDE_CODE_NEW_INIT=1 claude
```

### 方式二：/memory 管理

```bash
/memory
```

可查看当前加载的 `CLAUDE.md` 和 `CLAUDE.local.md`、切换自动记忆开关、打开记忆目录或编辑器。

### 方式三：# 快捷写入

在交互输入中以 `#` 开头快速添加记忆：

```text
# 在该项目中总是使用 pnpm 而不是 npm 安装
```

Claude Code 会提示选择保存位置。

## 存放位置与作用范围

| 范围 | 位置 | 用途 |
|---|---|---|
| 托管策略 | `/Library/Application Support/ClaudeCode/CLAUDE.md`（macOS） | 组织统一指令 |
| 用户指令 | `~/.claude/CLAUDE.md` | 个人全局偏好 |
| 项目指令 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 项目团队共享 |
| 本地指令 | `./CLAUDE.local.md` | 个人本地偏好 |

建议：项目级指令优先放在仓库根目录的 `./CLAUDE.md`，更显眼且易于团队发现。

## 使用 @path 导入

在 `CLAUDE.md` 中导入其他文件：

```markdown
请参阅 @README 了解项目概况，并参阅 @package.json 查看可用命令。

# 补充说明

- Git 工作流参考 @docs/git-instructions.md
```

路径解析：相对于包含导入语句的文件所在目录，非当前工作目录。递归导入深度最多 5 层。

## 配置 CLAUDE.local.md

适合存放不应提交到版本控制的内容：

- 个人常用命令
- 本地开发环境差异
- 私有沙盒 URL
- 个人偏好的测试数据

务必加入 `.gitignore`：

```gitignore
CLAUDE.local.md
```

### 多 worktree 共享

`CLAUDE.local.md` 被 Git 忽略，不会自动同步到其他 worktree。推荐在 `CLAUDE.md` 中从用户目录导入：

```markdown
# 个人偏好

- @~/.claude/my-project-instructions.md
```

或使用 `.worktreeinclude` 文件指定创建 worktree 时需要复制的被忽略文件。

## 配置 .claude/rules/

### 基本结构

```shell
your-project/
├── CLAUDE.md
├── .claude/
│   └── rules/
│       ├── code-style.md
│       ├── testing.md
│       └── security.md
```

### 路径特定规则

在规则文件顶部添加 `YAML frontmatter`：

```yaml
---
paths:
  - "src/api/**/*.ts"
---

# API 开发规则

- 所有 API 接口都必须包含输入校验
- 使用统一的错误响应格式
```

路径规则在 Claude Code 读取匹配文件时触发，不是每次工具调用都生效。

## 配置 Auto Memory

### 查看状态

```bash
/memory
```

在界面中切换自动记忆开关。

### 项目设置

```json
{
  "autoMemoryEnabled": false
}
```

### 环境变量

```bash
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

### 自定义存储位置

```json
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

必须是绝对路径或以 `~/` 开头。可配置在 policy 设置或 user 配置中，不能是项目配置或本地配置。

## 排除特定 CLAUDE.md

在大型 monorepo 中，使用 `claudeMdExcludes` 排除不相关的规则文件：

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

一般放在 `.claude/settings.local.json` 中。使用 glob 语法，针对绝对文件路径匹配。

## 编写规范

### 文件大小

控制在 **200 行以内**。内容过多时：
- 删除不需要每次会话加载的内容
- 将路径规则放到 `.claude/rules/`
- 将多步骤流程做成 `skill`
- 将本地偏好放到 `CLAUDE.local.md`

### 结构清晰

按主题分组，使用 Markdown 标题和项目符号：

```markdown
# 项目概览

# 构建和测试命令

# 代码风格

# Git 工作流

# 修改边界

# 常见问题
```

### 具体可验证

推荐写法：
- 使用 2 个空格缩进
- 提交前运行 npm test
- API handler 放在 src/api/handlers/

不推荐写法：
- 正确格式化代码
- 测试你的改动
- 保持文件格式良好

## 来源

- [[Memory]]
