---
title: CC Switch Skill 管理
date: 2026-08-09
tags:
  - AI/coding-tool
  - CC-Switch
  - skills-management
aliases:
  - Skills 管理
  - Agent Skill 管理
---

# 一、Skill 管理

Skill 是一组可复用的提示词、工具说明、脚本或参考资料，用于为 AI 工具增加某类任务能力。CC Switch 的 Skills 页面可以集中发现、安装、同步、更新和恢复 Skill，减少为每个 Agent 单独维护一份文件的工作量。

## 1、基本结构

一个 Skill 通常以目录形式存在，入口文件是 `SKILL.md`：

```text
my-skill/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

`SKILL.md` 用于说明 Skill 的用途、触发条件和执行规则；其他目录是否存在，取决于具体 Skill 的实现。

## 2、识别方式

CC Switch 主要通过查找 `SKILL.md` 识别 Skill。因此，一个 GitHub 仓库可以包含一个或多个 Skill，Skill 也可能位于仓库的子目录中。

# 二、存储与同步

## 1、源存储位置

CC Switch 需要先保存 Skill 的源文件，再将其分发给一个或多个受管应用。常见源存储位置如下：

| 位置 | 作用 |
|---|---|
| `~/.cc-switch/skills/` | CC Switch 默认的统一存储目录 |
| `~/.agents/skills/` | 可与其他 Agent 工具共享的目录 |

当前版本可以在 Skills 设置中切换源存储位置：

![[assets/Pasted image 20260809150623.png|600]]

在通用中找到 Skills 存储位置：

![[assets/Pasted image 20260809150721.png|600]]

## 2、应用目录

各工具通常有自己的 Skill 目录，例如：

| 应用 | 常见目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| Hermes | `~/.hermes/skills/` |

## 3、同步方式

CC Switch 可以通过符号链接或复制，将源存储中的 Skill 分发到应用目录。符号链接避免维护多份副本；复制方式则更独立，但更新时可能需要重新同步。

上面的 设置 -> 通用 -> Skills 同步方式即可切换不同方式。

# 三、发现与安装

## 1、打开 Skills 页面

当当前选中的应用支持 Skills 时，点击顶部导航栏的 **Skills** 按钮进入管理页面：

![[assets/Pasted image 20260809122644.png|600]]

页面通常提供发现、安装、导入、更新、卸载和恢复等入口。

## 2、选择发现来源

「发现技能」通常包含两类来源：

- **已配置仓库**：从 CC Switch 中维护的 GitHub 仓库搜索 Skill；
- **`skills.sh`**：从公共 Skill 注册表中搜索和发现社区 Skill。

两者的区别在于发现来源，最终安装后的 Skill 仍由 CC Switch 统一管理。

![[assets/Pasted image 20260809143705.png|600]]

## 3、管理 Skill 仓库

在仓库来源，点击「仓库管理」：

![[assets/Pasted image 20260809144117.png|600]]

可以查看预置仓库：

![[assets/Pasted image 20260809144220.png|600]]

也可以添加自定义仓库：

仓库 URL 可以写成：

```text
owner/name
```

也可以写：

```text
https://github.com/owner/name
```


## 4、搜索并安装

选择仓库或 `skills.sh` 后，可以按名称、描述或目录搜索：

![[assets/Pasted image 20260809143736.png|600]]

找到目标 Skill 后，点击「安装」即可。部分版本也支持从本地 ZIP 文件安装；安装前应确认压缩包内能够找到有效的 `SKILL.md`。

例如在`skill.sh`中搜索 `mattpocock`，可以看到来自公共注册表或 GitHub 仓库的匹配结果：

![[assets/Pasted image 20260809144620.png|600]]

# 四、导入与维护

## 1、导入已有 Skill

如果之前已经手动为 Claude Code、Codex 等工具安装过 Skill，可以使用「导入已有」，将本地 Skill 纳入 CC Switch 管理，而不必重新下载：

![[assets/Pasted image 20260809141858.png|600]]

## 2、检查与更新

点击「刷新」重新扫描仓库。CC Switch 可以通过内容哈希检测远端 Skill 是否发生变化，并提供单项更新或批量更新功能。

更新前应确认来源仓库和分支仍然可信；Skill 的更新可能改变提示词、脚本或工具行为。

## 3、卸载与恢复

卸载 Skill 前，CC Switch 通常会将其备份到：

```text
~/.cc-switch/skill-backups/
```

之后可以在「从备份恢复」中选择 Skill 和备份时间进行恢复：

![[assets/Pasted image 20260809142906.png|600]]

![[assets/Pasted image 20260809143020.png|600]]

删除备份是不可逆操作；如果只是暂时停用，优先关闭对应应用的同步开关，不要直接删除源文件。
