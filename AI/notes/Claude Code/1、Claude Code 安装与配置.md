---
title: Claude Code入门
date: 2026-05-08
tags: [AI, ClaudeCode]
aliases:
  - Claude Code入门
  - ClaudeCode入门
---

# 一、简介

`Claude Code` 是 Anthropic 推出的 AI 代码编程工具。

它能在终端或 IDE 中理解代码库、编辑文件、执行命令，并与开发工具协同工作，帮助开发者用**自然语言**完成代码阅读、开发、调试、重构、测试等任务。

`Claude Code` 的能力建立在 `Claude` 模型之上，但也可以通过配置**接入第三方模型**。

# 二、安装

以`macOS`为例，推荐使用原生安装方式：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

它安装的是 Claude Code 官方原生二进制，不依赖 Node/npm，并且拥有 Claude Code 自己控制的自动更新机制，更适合作为 Agent 工具长期运行环境。。但如果在后续配置文件中设置了`"CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"`，则不会自动更新。

下载完成后，执行：

```bash
claude --version
```

如果看到版本，说明安装成功。

# 三、配置接入第三方模型

本篇配置是手动修改`~/.claude/settings.json`，如果觉得麻烦，可以跳过本章节，使用 CC Switch 应用简化配置，参考[[AI/notes/CC-Switch/1、简介与安装|CC-Switch 安装]]和[[AI/notes/CC-Switch/2、供应商添加与切换|供应商添加与切换]]。

## 1、基本原理

**通过配置接入第三方模型**，需要配置 `BASE_URL + API_KEY + model` 映射。

这里可以把三个配置理解成：

- `BASE_URL`：接口地址，也就是 `Claude Code` 应该把请求发到哪里。默认情况下，请求会发往 Anthropic 官方 API；配置第三方模型时，需要把它改成第三方平台提供的 Anthropic 兼容接口地址。
- `API_KEY`：接口密钥，也就是第三方平台用来识别“是谁在调用 API”的凭证。它类似密码，不应该公开、提交到 Git 仓库或发给别人；如果泄漏，需要在平台后台删除或重新生成。
- `model`：模型名称，也就是告诉接口实际调用哪个模型。因为 `Claude Code` 内部默认会使用 Claude 的模型别名，所以接入第三方模型时，通常还要把 `sonnet`、`opus`、`haiku`、`fable` 等别名映射到第三方平台真实存在的模型 ID。

其中 `API_KEY` 在 `Claude Code` 配置里常见有两种写法：

- `ANTHROPIC_API_KEY`：把密钥作为 `X-Api-Key` 请求头发送。这是 Anthropic 官方 API Key 的常见形式，也适合兼容这种鉴权方式的第三方平台。
- `ANTHROPIC_AUTH_TOKEN`：把密钥作为 `Authorization: Bearer ...` 请求头发送。很多第三方平台或网关更习惯使用 Bearer Token 鉴权，因此会要求填写这个变量。

两者本质上都是“让服务端确认你有调用权限”的密钥，只是发送时使用的 HTTP 请求头不同。实际配置时不要两个随意混用，应以对应平台文档或示例为准：平台示例写 `ANTHROPIC_API_KEY` 就填它，写 `ANTHROPIC_AUTH_TOKEN` 就填它。

下面介绍几种国内模型的接入方法，按照自己需求选择其中一个即可。

## 2、接入MiniMax

首先进入`Minimax`开放平台：[Minimax](https://platform.minimaxi.com)，完成注册并登录。

可以选择订阅 Token Plan 或按量计费，生成对应的 API Key 后，复制备用。在本地编辑配置文件`~/.claude/settings.json`，在文件中增加如下内容：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_API_KEY": "YOUR API Key",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": 1,
    "ANTHROPIC_MODEL": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "MiniMax-M3[1M]",
    "ANTHROPIC_DEFAULT_FABLE_MODEL_NAME": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M3[1M]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M3[1M]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M3",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME": "MiniMax-M3"
  }
}
```

部分字段的含义如下：

| 环境变量                                       | 当前值                                  | 含义                                                                                                                                                                           |
| ------------------------------------------ | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_BASE_URL`                       | `https://api.minimaxi.com/anthropic` | 覆盖 Claude Code 默认的 Anthropic API 地址，让 Claude Code 请求 MiniMax 的 Anthropic 兼容接口。官方说明这个变量用于把请求路由到代理或网关；如果不是 Anthropic 官方 host，MCP tool search 默认会被禁用，部分 Remote Control 行为也会受影响。 |
| `ANTHROPIC_API_KEY`                        | 需要复制的 Key                            | API Key。Claude Code 会把它作为 `X-Api-Key` 请求头发送。设置后，它会优先于 Claude Pro / Max / Team / Enterprise 登录订阅来使用。                                                                          |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | `1`                                  | 关闭 Claude Code 的非必要流量。官方说明它等价于同时设置 `DISABLE_AUTOUPDATER`、`DISABLE_FEEDBACK_COMMAND`、`DISABLE_ERROR_REPORTING`、`DISABLE_TELEMETRY`。                                           |
| `ANTHROPIC_MODEL`                          | `MiniMax-M3`                         | 指定 Claude Code 当前会话启动时默认使用的模型。它会覆盖 `settings.json` 里的 `model` 字段，但 `/model` 命令和 `claude --model ...` 仍可覆盖它。                                                                  |
| `ANTHROPIC_DEFAULT_FABLE_MODEL`            | `MiniMax-M3[1M]`                     | 把 Claude Code 的 `fable` 别名映射到 MiniMax-M3 的 1M 上下文版本。也就是说，当你选择 `/model fable` 时，实际请求这个模型。Fable 相关别名需要 Claude Code 版本支持；官方文档提到 Fable 5 需要 Claude Code v2.1.170 或更高版本。          |
| `ANTHROPIC_DEFAULT_FABLE_MODEL_NAME`       | `MiniMax-M3`                         | 控制 `/model` 模型选择器里 `fable` 这一项的显示名称。它主要影响 UI 展示，不是实际发送给 API 的模型 ID。`_NAME` 后缀变量用于自定义 pinned model 在模型选择器里的显示名。                                                               |

> [!note]
> 注意：需要将`ANTHROPIC_API_KEY`的值填充为刚才复制的 API Key，注意 API Key 不要给别人，如果泄漏了重新生成。

上述的 `env` 键的本质是给 `Claude Code` 使用的环境变量，让它对每次会话都生效。


## 3、接入Kimi

Kimi 有两个平台入口：

- [Kimi API 开放平台](https://platform.kimi.com)
- [Kimi Code](https://www.kimi.com/code)

Kimi API 开放平台是更通用的 API 平台，用来按 API Key 调用模型。Kimi Code 则是订阅制，是 Kimi 专门给编程工具准备的一套 Coding API。

以 Kimi API 开放平台为例，新建 API Key 复制备用。

在本地编辑配置文件`~/.claude/settings.json`，在文件中增加如下内容：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.moonshot.cn/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "YOUR API KEY",
    "ANTHROPIC_MODEL": "kimi-k2.7-code",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "kimi-k2.7-code",
    "ANTHROPIC_DEFAULT_FABLE_MODEL_NAME": "kimi-k2.7-code",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "kimi-k2.7-code",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "kimi-k2.7-code",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "kimi-k2.7-code",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "kimi-k2.7-code",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "kimi-k2.7-code",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME": "kimi-k2.7-code"
  }
}
```

说明：

- `kimi-k2.7-code`不支持 1M 上下文，仅支持 256K 上下文。


## 4、接入DeepSeek

进入 DeepSeek 开放平台：[DeepSeek](https://platform.deepseek.com/)，注册账号并登录。

登录后，在右边侧边栏找到 API Keys，点击「创建 API key」：

![[assets/Pasted image 20260514142220.png|600]]

复制后保留备用。

在本地编辑配置文件`~/.claude/settings.json`，增加：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-d43e8ad30991463693f421c9b6b68f3b",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "deepseek-v4-flash[1M]",
    "ANTHROPIC_DEFAULT_FABLE_MODEL_NAME": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-flash[1M]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-flash[1M]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "deepseek-v4-flash",
    "ANTHROPIC_MODEL": "deepseek-v4-flash[1M]",
    "CLAUDE_CODE_EFFORT_LEVEL": "max"
  }
}
```


## 5、接入智谱GLM

进入 [智谱 AI 开放平台](https://bigmodel.cn/)，注册账号并登录。

智谱 GLM 也可以选择按用量计费和订阅 Coding Plan。

这里以按用量计费为例，生成 API Key 复制备用。

在本地编辑配置文件`~/.claude/settings.json`，增加：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "ANTHROPIC_API_KEY": "YOUR API KEY",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "glm-5.2[1M]",
    "ANTHROPIC_DEFAULT_FABLE_MODEL_NAME": "glm-5.2",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.7",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL_NAME": "glm-4.7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5.2[1M]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "glm-5.2",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5.2[1M]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "glm-5.2",
    "ANTHROPIC_MODEL": "glm-5.2"
  }
}
```

# 四、基本使用

## 1、第一次对话

配置好模型之后，就可以进入项目目录，在终端执行 `claude`，第一次会进入选择终端样式界面：

![[assets/Pasted image 20260811131827.png|600]]


这里选择默认的 Dark mode，可以在下面看到该样式的效果。

下面进入 Claude Code 的一些使用提示：

![[assets/Pasted image 20260811133017.png|600]]

按提示键入<kbd>Enter</kbd>，这里询问要不要自动优化终端快捷键和提示音设置：

![[assets/Pasted image 20260811133200.png|600]]

它想帮你设置两件事：

- <kbd>Option</kbd> + <kbd>Enter</kbd>：在输入框里换行，而不是发送消息。
- 关闭 audible bell：避免终端发出“叮”的提示音。

这里选`Yes`即可，后续如果想重新设置，可以使用`/terminal-setup`命令。

接下来进入：

![[assets/Pasted image 20260811133549.png|600]]

这是 Claude Code 的**工作区信任确认**。它在问：这个项目是不是你信任的目录。选了信任之后，Claude Code 才会在这个目录里读取、编辑、执行文件。

选择`Yes`后，就可以进入 Claude Code 了：

![[assets/Pasted image 20260811133722.png|600]]

现在可以发送文本验证是否可用：

![[assets/Pasted image 20260811133820.png|600]]

接下来介绍 Claude Code 一些日常开发常用的 Slash Command（斜杠命令）。Slash Command 是指以`/`开头的指令，直接在文本框输入`/`会弹出可用的 Slash Command 列表。

![[assets/Pasted image 20260811133950.png|600]]

## 2、/usage

`/usage` 用于查看当前 Claude Code 会话的成本和用量概览，也可以使用别名 `/cost`。

示例：

![[assets/Pasted image 20260811134055.png|600]]

首先看顶部标签：

```shell
Settings  Status  Config  Usage  Stats
```

这是 Claude Code 的终端 UI 标签页。你当前停在 **Usage** 页。

然后是第二行的`Session`，表示当前这一次 Claude Code 会话。也就是说，这段统计只针对这次打开 Claude Code 后的当前 session。

接下来就是完整的一些用量信息了：

- **Total cost**：表示当前会话的估算费用。这里提示用的是 Claude Code 不认识价格表的模型（deepseek flash），所以费用可能不准确。所以接入第三方模型时，此信息可以忽略。
- **Total duration (API)**：这次会话里，真正发生 API 请求、等待模型返回的累计时间。
- **Total duration (wall)**：从这个会话开始到现在，真实墙钟时间过去了多久。
- **Total code changes**：反映会话跟踪到的变更行数，不一定等同于`git diff`的全部语义，也不一定只限代码，可能包括配置、文档等文件变更。
- **Usage by model**：按模型统计 token 用量。逐项解释：

| 字段                      | 含义            |
| ----------------------- | ------------- |
| `deepseek-v4-flash[1m]` | 本次调用的模型名      |
| `27.1k input`           | 输入给模型的 token  |
| `169 output`            | 模型生成的输出 token |
| `0 cache read`          | 没有读取缓存 token  |
| `0 cache write`         | 没有写入缓存 token  |

Claude Code 的 token 统计类型包括 `input`、`output`、`cacheRead`、`cacheCreation`，也就是输入、输出、缓存读取、缓存创建。

以当前接入的 deepseek flash 为例，此时发送“你好”得到回复后，执行`/usage`查看结果：

![[assets/Pasted image 20260811220459.png|600]]

由于是新的会话首次提问，此时的`cache read`为0。注意这里明明只发了“你好”，但`input`却有`33.2k`，这是因为每次发给模型的上下文除了当前轮次的新问题，还包含系统提示词、CLAUDE.md、项目规则、工具列表、MCP配置、历史对话等。

现在继续第二次提问“你是什么模型”，再调用`/usage`查看结果：

![[assets/Pasted image 20260811220838.png|600]]

本次可以看到`cache read`不再为0，因为本次命中了缓存。第一次请求结束时，DeepSeek 后端已经把可复用的 prompt 前缀缓存起来了。这次实际传给模型的上下文是`input`+`cache read`。`input`是本次新增、需要重新处理的 token，而`cache read`是之前已经计算过，本次直接复用的 token。

## 3、/doctor

`/doctor`用于诊断当前 Claude Code 环境是否正常，包括 Claude Code 安装状态、更新状态、配置文件、MCP 配置、工具依赖、权限与运行环境等。

新版 `/doctor` 命令升级为完整环境检查工具，不仅诊断 Claude Code 安装、配置、MCP、工具环境等问题，还可以辅助修复发现的问题。

![[assets/Pasted image 20260811223926.png|600]]

Claude Code 默认以英文方式回答，这里我们可以先引入`CLAUDE.md`（具体可参考：[[AI/notes/Claude Code/4、Memory|Memory]]），这里理解为长期全局规则，每次新开一个会话都会进入上下文。

打开`~/.claude/CLAUDE.md`，写入：

```markdown
## 沟通偏好

每次回答使用中文和我交流
```

这样，每次对话都以中文方式呈现，现在可以看看`/doctor`都看了些什么：

![[assets/Pasted image 20260811225949.png|600]]

可以看到运行`/doctor`，还会建议我将默认权限模式设置为`auto`，这里选择应用，后续权限模式详细介绍该模式。

![[assets/Pasted image 20260811230851.png|700]]


## 4、/status

`/status` 用于查看当前 Claude Code 会话和环境状态，包括 Claude Code 版本、当前会话名称、ID、当前工作目录、Base URL、认证方式、模型、当前加载了哪些来源。

![[assets/Pasted image 20260811231403.png|600]]


## 5、/clear

`/clear` 用于清空当前上下文，开始一个新的上下文对话。别名：`new`和`reset`。它比较适合在如下场景使用：

- 准备开始另一个**完全无关**的任务
- 会话开始混淆旧问题和新问题
- 上下文太长，回答开始变慢、变贵、变乱
- 前面尝试方向错了，想让它重新开始

> 注意，clear 不会删除旧会话的上下文，后续仍然可以通过 `/resume` 在历史上下文记录中找到。


## 6、/compact

`/compact` 用于压缩当前会话上下文（Context Window），将较早的对话、工具调用、结果等信息总结成一份摘要，然后继续基于摘要工作，以释放上下文空间。LLM 有上下文窗口限制，上下文无法一直无限制增长，所以 Agent 需要对上下文进行压缩。

`/compact`不是清空对话，也不是重新开始。

压缩会尽量保留关键信息，但细节仍可能丢失，可以主动指定保留重点。使用 `/compact [instructions]`附带重点压缩说明。

示例：

```text
/compact
/compact 保留当前任务目标、修改方案和未完成事项
```

即使不主动执行`/compact`压缩，Claude Code 也会在上下文临近上限时**自动进行上下文压缩**，以避免超出限制。

## 7、/model

`/model` 用于切换当前会话使用的模型。

`/model` 后不带模型名称时，会打开模型选择器。例如：


![[assets/Pasted image 20260811234533.png|600]]

由于这里模型映射的都是 deepseek-v4-flash，因此这里没必要切换。当有不同模型时，可以根据当前要完成的任务难易程度选择不同模型控制成本。

对于支持 `effort level` 的模型，还可以执行 `/effort`：

![[assets/Pasted image 20260709133217.png|400]]



## 8、/effort

`/effort` 是 Claude Code 控制“模型推理投入程度”的命令，本质是调整 Claude API 的 `effort` 参数。它主要对 Anthropic Claude 模型有效；如果你接入 DeepSeek 等第三方模型，通常没有实际作用，除非第三方兼容层明确实现了该参数。


## 9、/resume

`/resume` 用于恢复或切换到之前的会话。可以通过会话 ID 或会话名称恢复，也可以不带参数打开会话选择器。`/continue` 是它的别名。

示例：

```shell
/resume
/resume my-session-name
/resume <session-id>
```

执行 `/resume` 会打开会话选择器：

![[assets/Pasted image 20260812001952.png|600]]

## 10、/exit

`/exit` 用于退出当前  Claude Code 会话，返回 shell。它的别名是 `/quit`。