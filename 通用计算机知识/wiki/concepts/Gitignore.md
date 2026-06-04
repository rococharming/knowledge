---
title: Gitignore
date: 2026-06-05
tags: [git, repository]
source_count: 1
---

# Gitignore

`.gitignore` 文件用于指定 Git **不应跟踪**的文件和目录模式。

## 常见忽略场景

| 文件类型 | 示例 |
|----------|------|
| 编译产物 | `target/`、`dist/`、`build/` |
| 依赖目录 | `node_modules/` |
| 日志文件 | `*.log` |
| 临时文件 | `.DS_Store` |
| 本地环境配置 | `.env` |

## 基本语法

```gitignore
.DS_Store
*.log
target/
node_modules/
.env
```

- `*` 匹配任意字符
- `/` 结尾表示目录
- 以 `#` 开头为注释

## 关键规则：只影响未跟踪文件

`.gitignore` **仅对尚未被 Git 跟踪的文件生效**。已被跟踪的文件即使后续加入 `.gitignore`，Git 仍会继续追踪其变更。

### 流程示例

```
config.json 已被提交过
  ↓
后来把 config.json 写入 .gitignore
  ↓
Git 仍然会继续跟踪 config.json 的修改
```

## 停止跟踪已提交的文件

若想让已跟踪的文件停止被 Git 追踪，需从索引中移除：

```shell
git rm --cached config.json
```

该命令会保留工作区的文件本身，但将其从 Git 的跟踪列表中移除。之后再配合 `.gitignore` 即可彻底忽略。

## 相关页面

- [[Git 仓库]] — 仓库的基本结构与状态
- [[Git 配置]] — 全局与本地配置

## 来源

- [[创建Git仓库]]
