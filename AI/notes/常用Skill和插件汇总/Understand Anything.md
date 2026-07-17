---
title: Understand Anything
date: 2026-07-01
tags: [AI, Skill]
aliases:
  - Understand Anything
  - UnderstandAnything
---

# 一、简介

`Understand Anything` 是一个代码库理解工具。它会扫描项目中的文件、函数、类和依赖关系，并结合 LLM 将代码架构与业务流程转换成交互式知识图谱。

借助它可以：

- 查看项目架构和模块依赖
- 搜索代码与业务概念
- 生成新人入门指南
- 解释单个文件的用途和上下游关系
- 分析当前代码修改可能产生的影响

项目主页：[Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything)

本文以 **macOS + Codex** 环境为主。


# 二、安装前准备

使用前需要准备：

- 已安装并能正常使用 Codex
- 已安装 Git
- 能访问 GitHub
- 有一个准备分析的代码项目
- 有可用的模型额度或订阅

可以先在终端检查 Git：

```shell
git --version
```

> [!warning] Token 消耗
> 首次分析会扫描整个目标目录，可能消耗较多 Token。大型项目建议先分析核心子目录；后续更新默认只重新分析发生变化的文件，消耗会明显降低。


# 三、安装到 Codex

在终端运行：

```shell
curl -fsSL https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/main/install.sh | bash -s codex
```

安装脚本会：

1. 将项目下载到：

   ```text
   ~/.understand-anything/repo
   ```

2. 将 Understand Anything 的 Skills 链接到 Codex。
3. 让这些能力可用于所有项目。

安装完成后，需要 **完全退出并重新启动 Codex**。官方说明见[多平台安装章节](https://github.com/Egonex-AI/Understand-Anything#one-line-install-codex--opencode--openclaw--antigravity--gemini-cli--pi-agent--vibe-cli--vs-code-copilot--hermes--cline--kimi-cli--trae--nanobot--kiro)。

如果不放心直接执行网络脚本，可以先下载并检查脚本内容：

```shell
curl -O https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/main/install.sh
less install.sh
bash install.sh codex
```


# 四、第一次分析代码库

在 Codex 中打开真正需要分析的项目目录，而不是 Understand Anything 自身的仓库。

例如：

```shell
cd ~/Projects/my-project
codex
```

然后在 Codex 对话中输入：

```text
使用 understand 分析当前项目，输出语言使用简体中文。
```

如果当前 Codex 界面支持 Skills 显式调用，也可以输入：

```text
$understand --language zh
```

项目文档采用的通用命令形式是：

```text
/understand --language zh

# 支持的语言：en（默认）、zh、zh-TW、ja、ko、ru
```

不同 Codex 版本的 Skill 入口可能显示为 `$understand`、技能按钮或自然语言调用，三者目标相同。

分析完成后，项目中会出现：

```text
.understand-anything/
├── knowledge-graph.json
├── config.json
└── intermediate/
```

| 文件或目录 | 作用 |
|---|---|
| `knowledge-graph.json` | 核心知识图谱 |
| `config.json` | 语言等配置 |
| `intermediate/` | 分析过程中的临时数据 |


# 五、打开知识图谱

分析完成后输入：

```text
使用 understand-dashboard 打开当前项目的知识图谱。
```

也可以显式调用：

```text
$understand-dashboard
```

官方通用写法是：

```text
/understand-dashboard
```

它通常会启动本地服务并打开浏览器。进入 Dashboard 后，建议按下面的顺序探索：

1. 查看架构层和颜色图例。
2. 使用 Guided Tour 查看推荐学习顺序。
3. 点击核心文件节点，阅读节点摘要。
4. 沿依赖关系查看它调用了什么、又被什么调用。
5. 搜索 `auth`、`payment`、`database` 等业务概念。
6. 切换用户角色，让解释更适合初学者、开发者或产品经理。


# 六、最常用的操作

## 1、询问代码库

```text
使用 understand-chat 回答：这个项目的启动流程是什么？
```

其他常用问题：

```text
用户登录请求从哪里进入？
数据库连接在哪里初始化？
修改订单状态会影响哪些模块？
这个项目最值得先阅读的五个文件是什么？
前端和后端通过什么接口通信？
```

## 2、解释单个文件

```text
使用 understand-explain 解释 src/auth/login.ts。
```

也可以明确指定解释结构：

```text
请按“用途、输入、输出、依赖、调用方、潜在风险”解释 src/auth/login.ts。
```

## 3、生成新人入门指南

```text
使用 understand-onboard 为第一次接触这个项目的开发者生成入门指南。
```

## 4、提取业务流程

```text
使用 understand-domain 提取当前项目的业务领域、流程和关键步骤。
```

这特别适合电商、支付、审批和工单等业务系统。

## 5、分析当前代码改动的影响

先修改代码，但不必提交，然后输入：

```text
使用 understand-diff 分析当前修改会影响哪些模块和流程。
```

它会结合 Git diff 与已有图谱，分析潜在的连锁影响。


# 七、代码变化后如何更新

直接重新执行：

```text
使用 understand 增量更新当前项目的知识图谱，保持简体中文。
```

后续默认只分析发生变化的文件。

如果希望每次 Git commit 后自动更新，可以输入：

```text
使用 understand --auto-update 为项目启用提交后自动更新。
```

> [!warning] Git Hook
> 自动更新会修改项目的 Git Hook。团队项目启用前，应先确认现有 Hook 是否承担测试、格式化或部署等任务，避免覆盖或破坏原有流程。


# 八、大型项目的推荐方式

不要一开始就扫描整个超大型 monorepo，可以先限定目录：

```text
使用 understand 分析 src/frontend，并使用简体中文。
```

或者：

```text
$understand src/frontend --language zh
```

推荐顺序：

1. 先分析核心业务目录。
2. 确认生成效果和 Token 消耗。
3. 再逐步扩大到完整项目。
4. 排除生成文件、缓存、依赖和构建产物。

常见的不需要分析的内容包括：

```text
node_modules/
dist/
build/
coverage/
.venv/
vendor/
*.min.js
```


# 九、与团队共享

官方建议提交 `.understand-anything/` 中的图谱，但排除本地临时数据：

```text
.understand-anything/intermediate/
.understand-anything/diff-overlay.json
```

然后提交其余内容：

```shell
git add .understand-anything .gitignore
git commit -m "docs: add Understand Anything knowledge graph"
```

这样其他成员可以直接打开图谱，不必重新进行完整分析。

图谱超过 10 MB 时，可以使用 Git LFS：

```shell
git lfs install
git lfs track ".understand-anything/*.json"
git add .gitattributes .understand-anything/
```


# 十、更新和卸载

进入安装仓库：

```shell
cd ~/.understand-anything/repo
```

更新：

```shell
./install.sh --update
```

卸载 Codex 集成：

```shell
./install.sh --uninstall codex
```

完成后重新启动 Codex。


# 十一、常见问题

## 1、Codex 找不到 understand

依次检查：

1. 安装后是否完全重启了 Codex。
2. 安装目录是否存在：

   ```shell
   ls ~/.understand-anything/repo
   ```

3. 重新运行安装：

   ```shell
   cd ~/.understand-anything/repo
   ./install.sh codex
   ```

4. 不要拘泥于 `/understand` 语法，可以直接告诉 Codex：

   ```text
   请调用 Understand Anything 的 understand skill 分析当前项目。
   ```

## 2、Dashboard 没有打开

- 查看 Codex 输出的本地网址，手动复制到浏览器。
- 检查 Dashboard 使用的端口是否被占用。
- 关闭已有的 Vite 开发服务器后重试。

## 3、分析时间很长或 Token 消耗太高

- 先限定一个核心子目录。
- 排除依赖、缓存和构建产物。
- 不要反复删除 `.understand-anything/`。
- 初次分析后使用增量更新。
- 超大项目可以考虑使用本地模型。

## 4、图谱内容不准确

> [!important] 重要结论仍需回到代码验证
> LLM 生成的摘要和业务判断不是事实来源。结构关系主要来自 Tree-sitter 静态分析，语义描述则由 LLM 生成，因此后者更容易出现误判。

重要结论应回到以下内容进行验证：

- 实际代码
- 测试
- 配置文件
- 数据库迁移
- API 定义


# 十二、最短上手流程

真正需要记住的只有以下几步。

## 1、安装

```shell
curl -fsSL https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/main/install.sh | bash -s codex
```

## 2、重启 Codex，然后打开目标项目

```shell
cd ~/Projects/my-project
codex
```

## 3、在 Codex 中依次输入

```text
使用 understand 分析当前项目，输出语言使用简体中文。

使用 understand-dashboard 打开知识图谱。

使用 understand-onboard 生成新人学习指南。

使用 understand-chat 回答：我应该按照什么顺序阅读这个项目？
```

这四步完成后，就已经跑通了 Understand Anything 的核心工作流。