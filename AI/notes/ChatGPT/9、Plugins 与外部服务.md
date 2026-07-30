---
title: Plugins 与外部服务
date: 2026-07-30
tags: [AI, ChatGPT, Plugin]
aliases:
  - ChatGPT Plugins
  - ChatGPT插件
---

# 一、Plugins

Plugin 是 ChatGPT 和 Codex 的可安装能力包。它把完成某类工作的指令、工具和外部服务连接组合起来，让 ChatGPT 不只依赖当前消息和本地文件。

Plugin 适合：

- 从 Gmail、Google Drive、Slack 等服务读取资料
- 在外部系统中创建或更新内容
- 执行一套可复用的专业流程
- 为 ChatGPT 增加特定工具

Plugin 可用于桌面 App 的 ChatGPT Work 或 Codex，不用于普通 Chat。安装后通常需要新建 Chat，才能使用新加入的能力。

# 二、组成

一个 Plugin 可以包含下面一种或多种组件：

| 组件 | 作用 |
|---|---|
| Skill | 为特定任务提供可复用的步骤、规则和参考资料 |
| Connector | 连接 GitHub、Slack、Google Drive 等服务 |
| MCP Server | 暴露结构化工具和共享信息，并执行外部动作 |
| Browser Extension | 为工作流提供浏览器能力 |
| Hook | 在指定生命周期节点运行命令 |
| Scheduled Task Template | 提供可复用的定时任务起点 |

## 1、Skill

Skill 主要告诉 ChatGPT **应该怎样完成某类任务**。它可以包含操作步骤、质量要求、参考文件和辅助脚本。

例如：

- 写技术笔记时遵循统一结构
- 创建演示文稿时执行渲染检查
- 代码审查时按仓库标准和需求分别检查

Skill 本身不一定连接外部服务。

## 2、Connector

Connector 让 ChatGPT 访问某个服务中的数据和操作，例如：

- 从 Google Drive 读取文件
- 总结 Slack Channel
- 查询 GitHub Pull Request
- 草拟 Gmail 回复

Connector 使用对应服务自己的登录和权限体系。ChatGPT 能访问什么，取决于当前账号在该服务中原本拥有的权限。

## 3、MCP Server

MCP Server 是 Connector 背后的常见工具接口。它定义 ChatGPT 可以调用哪些工具、接收哪些结构化参数，以及返回什么数据。

普通用户不需要先理解协议细节。使用时更重要的是确认：

- 这个工具来自谁
- 能读取什么
- 能执行什么动作
- 是否需要登录
- 是否会把数据发送到外部服务

# 三、安装

## 1、浏览目录

在桌面 App 中：

1. 选择 ChatGPT 并切换到 Work，或选择 Codex。
2. 打开左侧 **Plugins**。
3. 搜索或浏览 Plugin。
4. 打开详情页，检查提供者和包含的能力。
5. 点击 `+` 安装。
6. 按提示连接需要的外部服务。
7. 新建 Chat 后开始使用。

Plugin Directory 可能包含：

- OpenAI 提供的 Plugin
- 当前 Workspace 提供的 Plugin
- Personal Marketplace 中的个人 Plugin
- 已安装的 Plugin

具体可见内容会受到账号和 Workspace 策略影响。

> [!todo] 待补截图
> 截取 Plugins Directory 和一个 Plugin 详情页，标出提供者、Skills、Connectors、权限说明与安装按钮。

## 2、连接账号

有些 Plugin 安装时要求登录，有些在第一次调用 Connector 时才要求登录。

登录外部服务前，应确认：

- 浏览器地址和授权对象正确
- 请求的权限与任务相符
- 使用的是个人账号还是公司账号
- 是否允许写入、发送或删除

不要因为 Plugin 已安装，就默认批准它请求的所有权限。

# 四、调用

## 1、自动选择

Plugin 安装后，可以直接描述结果，让 ChatGPT 选择合适的工具。

```text
总结今天未读的 Gmail 邮件，按“需要回复”和“仅供了解”分类。
先生成草稿，不要发送任何邮件。
```

这种方式适合只关心任务结果，不要求使用特定工具的情况。

## 2、指定 Plugin

如果必须使用某个 Plugin，可以在输入区键入 `@` 并选择它。

```text
@Google Drive 查找项目目录中最新的发布计划，
整理本周里程碑和仍未解决的问题。
```

指定 Plugin 能减少工具选择歧义，但仍应说明要查找的内容和预期结果。

## 3、组合使用

Work 可以把多个 Plugin 与本地或内置工具组合起来。

示例：

```text
从 Google Drive 获取最新项目计划，
从 Slack 项目频道收集最近七天的决定，
再结合本地模板生成一份状态报告。
把报告保存到本地，发送到 Slack 前必须先让我审阅。
```

# 五、选择能力

| 需求 | 优先选择 |
|---|---|
| 需要一套稳定的操作方法 | Skill |
| 需要读取或操作外部服务 | Connector |
| 需要结构化自定义工具 | MCP Server |
| 需要操作当前登录的网页 | Browser 或 Chrome Extension |
| 没有结构化接口，只能操作桌面 GUI | Computer Use |

能够使用 Connector 时，优先使用 Connector，而不是通过 Computer Use 在网页中逐步点击。结构化工具通常更容易控制输入、输出和权限范围。

# 六、权限与数据

Plugin 的安全边界由多层共同决定：

```text
ChatGPT Permission Mode
        +
Plugin / MCP 工具权限
        +
外部服务账号权限
        +
Workspace 管理策略
```

使用前应检查：

- Plugin 的来源是否可信
- Skill 会指导 ChatGPT 做什么
- Connector 会把哪些数据发送给哪个服务
- MCP Server 是否需要额外认证
- Hook 是否会在本地自动执行命令
- 外部动作是否需要人工确认

通过 Connector 发送到外部服务的数据，还会受到该服务条款和隐私政策约束。

卸载 Plugin 会移除能力包，但其中连接过的 Connector 可能仍保持登录状态。需要彻底撤销访问时，还应在 Connector 管理页或外部服务中断开连接。

有关浏览器和桌面操作的区别，参考 [[8、浏览器与计算机操作|浏览器与计算机操作]]；定时复用 Plugin 的方式参考 [[11、长期任务与自动化|长期任务与自动化]]。
