# 一、概述

`find-skills`是 Vercel Labs skills 仓库中的一个 Agent Skill。它的作用是：

> 帮助用户发现、筛选和安装适合当前任务的 Agent Skills。

`find-skills` 适合在这些场景下使用：

- 你想找某个能力对应的 skill
- 你问：“有没有能做 X 的 skill？”
- 你想扩展 Claude Code、Cursor、Codex 等 AI 编程 Agent 的能力
- 你想搜索某个领域的工具、模板或工作流
- 你不确定某个任务是否已经有现成 skill 可用

# 二、安装

想为 `Claude Code` 安装 `find-skills`，可以运行如下命令：

```shell
npx skills add vercel-labs/skills@find-skills 
```

进入如下界面：

![[Pasted image 20260508101609.png]]

这里默认已经选择了几个 Agent （如Codex），因为它们的 skill 都放在`.agents/skills`目录下，skills命令默认就安装在该目录。

为了给`Claude Code`也装上，需要在`Additional agents`里按下*空格*选择`Claude Code`，然后回车确认到下一步：

![[Pasted image 20260508101938.png]]

接下来会让我们选择安装的范围：项目级还是全局？

这里建议全局，因为`find-skills`比较常用。

接下来是选择安装的方式：通过符号链接还是复制？

![[Pasted image 20260508102331.png]]

这里选择符号链接方式，这样方便更新，链接统一指向 .agent/skills 下的 skill，以后更新之需要更新 .agent/skills。

# 三、使用

安装后，当你向 Agent 提出类似问题时，`find-skills` 就可以派上用场：

```
有没有适合 React 性能优化的 skill？
```

```
帮我找一个能做 PR review 的 skill。
```

```
有没有可以生成 changelog 的 skill？
```

```
我想让 Claude Code 更擅长写测试，有没有相关 skill？
```

`find-skills` 背后主要依赖 Skills CLI，也就是：

```
npx skills
```

官方 `find-skills` 文档中列出的几个关键命令包括：

- `npx skills find [query]` 用于按关键词搜索 skill
- `npx skills add <package>` 用于安装 skill
- `npx skills check` 用于检查更新
- `npx skills update` 用于更新已安装 skills。