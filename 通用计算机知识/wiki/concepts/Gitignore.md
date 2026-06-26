---
title: Gitignore
date: 2026-06-26
tags: [git, repository]
source_count: 2
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
- `!` 取反，取消忽略（如 `*.log` 后用 `!important.log` 保留该文件）

### 常见规则示例

| 规则 | 含义 |
|------|------|
| `*.log` | 忽略所有 `.log` 结尾的文件 |
| `dist/` | 忽略 `dist` 目录（编译产物、依赖目录同理） |
| `.env` | 忽略 `.env` 文件（含敏感配置，可提交 `.env.example` 作示例） |
| `!important.log` | 取消忽略，保留 `important.log` |

## 查看忽略是否生效

默认情况下 `git status` 不显示被忽略的文件。两个命令用于排查忽略规则：

| 命令 | 作用 |
|------|------|
| `git status --ignored` | 列出当前被忽略的文件 |
| `git check-ignore -v <file>` | 查看某文件**为什么**被忽略 |

`git check-ignore -v app.log` 输出示例：

```
.gitignore:1:*.log    app.log
```

表示忽略来自 `.gitignore` 第 1 行的 `*.log` 规则，作用于 `app.log`。

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

### 停止跟踪的完整流程

```
echo "config.json" >> .gitignore   # 1. 写入忽略规则
git rm --cached config.json        # 2. 让 Git 不再跟踪（保留本地文件）
git add .gitignore                 # 3. 暂存 .gitignore
git commit -m "stop tracking..."   # 4. 提交
```

`git rm --cached` 不删除电脑上的文件，只是让 Git 以后不再跟踪它。

## .git/info/exclude：本地忽略文件

除 `.gitignore` 外，Git 还有只对本机生效的忽略文件 `.git/info/exclude`，写法与 `.gitignore` 相同。

| 文件 | 适合放什么规则 | 是否提交到仓库 |
|------|----------------|----------------|
| `.gitignore` | 项目通用忽略规则（团队共享） | 通常提交 |
| `.git/info/exclude` | 只与自己电脑有关的本地规则（如临时测试文件） | 不会提交 |

只想在当前仓库忽略某文件、不想影响团队时，把规则写到 `.git/info/exclude`。

## 相关页面

- [[Git 仓库]] — 仓库的基本结构与状态
- [[Git 配置]] — 全局与本地配置
- [[Git 文件删除与重命名]] — `git rm --cached` 的语义与删除操作的关联

## 来源

- [[创建Git仓库]]
- [[忽略规则文件]]
