# 一、简介

`Claude Code`是Anthropic推出的AI代码工具。

它能在终端或IDE中理解代码库、编辑文件、执行命令，并与开发工具协同工作，帮助开发者用**自然语言**完成代码阅读、开发、调试、重构、测试等任务。

`Claude Code`能力建立在`Claude`模型之上，但也可以通过配置**接入国内第三方模型**。

# 二、安装

以`macOS`为例，在终端执行：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

这是原生安装方式，支持后台自带更新`Claude Code`，但如果在后续配置文件中设置了`"CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"`，则不会自动更新。

下载完成后，执行：

```bash
claude --version
```

如果看到版本，说明安装成功：

![[image-20260427214629504.png|400]]

可以执行如下命令手动更新：

```bash
claude update
```

如下图所示：

![[image-20260427214617672.png|400]]

# 三、配置接入第三方模型

## 1、基本原理

进入自己的项目目录，首次启动`Claude Code`:

```bash
cd path/to/project
claude 
```

会提示登录，但这里不推荐使用官方接口，原因有两点：

- 需要国外手机号验证，比较麻烦
- 后续使用很有可能被封号

因此，这里更推荐**通过配置接入国内第三方模型**。

在国内，想通过网关转发的方式接入第三方模型，需要配置 `base URL + auth + model` 映射。本质上是将 `Claude Code` 默认发给 Anthropic 官方接口的请求，改为发到第三方提供的 Anthropic 兼容接口。

下面介绍几种国内模型的接入方法，按照自己的需要选择其中一个即可。

## 2、接入MiniMax

首先进入`Minimax`开放平台：[Minimax](https://platform.minimaxi.com)，完成注册并登录。

购买适合自己的Token Plan后，将对应的API Key复制备用，然后在本地编辑配置文件`~/.claude/settings.json`，在文件中增加如下内容：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "Your MINIMAX KEY",
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_MODEL": "MiniMax-M2.7",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  },
}
```

注意：需要将`**ANTHROPIC_AUTH_TOKEN**`的值填充为刚才复制的**API Key**，注意**API Key**不要给别人，如果泄漏了重新生成一个。

上述的 `env` 键的本质是给 `Claude Code` 使用的环境变量，让它对每次会话都生效。

这里涉及到的环境变量解释如下：

- `ANTHROPIC_BASE_URL`：把 `Claude Code` 默认请求的 API 地址替换为指定的代理或网关。

- `ANTHROPIC_AUTH_TOKEN`：自定义 `HTTP` 请求里的 `Authorization` 头，`Claude Code` 会自动在前面加上 `Bearer`，因此这里就是把 MiniMax Key 当作 Bearer Token 发送给 MiniMax 网关。

- `API_TIMEOUT_MS`：API 请求超时，单位是毫秒（ms）。

- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`：配置为`1`表示一键关闭非必要流量。通常是为了让`Claude Code`不去做**自动更新**、反馈、错误上报等额外联网动作，只保留核心请求。

- `ANTHROPIC_MODEL`：当前要使用的模型设置名，这里表示**默认主模型直接指定为`MiniMax-M2.7`**

- `ANTHROPIC_DEFAULT_SONNET_MODEL`：把 Claude Code 里 `sonnet` 这个默认档位映射到具体模型名。意思是在 `Claude Code` 会话下，凡是 `Claude Code` 选择 `Sonnet` 档位时，实际请求走的是 `MiniMax-M2.7`。

- `ANTHROPIC_DEFAULT_OPUS_MODEL`：同理，把 `opus` 档位映射到 `MiniMax-M2.7`。

- `ANTHROPIC_DEFAULT_HAIKU_MODEL`：同理，把 `haiku` 档位映射到 `MiniMax-M2.7`。

## 3、接入Kimi

进入 Kimi Code 官网购买会员订阅计划： https://www.kimi.com/code。

根据自己的需求选择合适的套餐后，访问 Kimi 会员控制台创建并获取 API Key：

点击「新建 API Key」，复制以 sk-kimi- 开头的密钥。这个 Key 是后续连接 Kimi k2.6 的凭证，请妥善保管，如果泄漏需要重新生成。

![[image-20260427220833065.png|600]]

在本地编辑配置文件`~/.claude/settings.json`，增加：

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "Your Kimi Code KEY",
    "ANTHROPIC_BASE_URL": "https://api.kimi.com/coding/",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "kimi-for-coding",
    "ANTHROPIC_MODEL": "kimi-for-coding",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

注意：需要将 `ANTHROPIC_API_KEY` 的值填充为复制的 API Key，注意 API Key 不要给别人，如果泄漏了重新生成一个。

说明：

- `Kimi k2.6` 在 API 层面的内部模型标识符为`kimi-for-coding`，而不是`kimi-k2.6`。也可以不设置这些模型字段，因为 Kimi Code 后端会对这些 `Claude Code` 模型名执行自动映射，将其路由到 `kimi-for-coding`。

- 这里使用的是 `ANTHROPIC_API_KEY` 而不是 `ANTHROPIC_AUTH_TOKEN`

## 4、接入DeepSeek

进入 DeepSeek 开放平台：[DeepSeek](https://platform.deepseek.com/)，注册账号并登录。

登录后，在右边侧边栏找到 API Keys，点击「创建 API key」：

![[Pasted image 20260514142220.png|600]]

复制后保留备用。

在本地编辑配置文件`~/.claude/settings.json`，增加：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "Your DeepSeek KEY",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro",
    "ANTHROPIC_MODEL": "deepseek-v4-pro",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```



# 四、基本使用

## 1、第一次对话

配置好模型之后，现在就可以进入自己的项目目录，在终端执行：

```bash
claude
```

即可进入`Claude Code`会话，如下图所示：

![[image-20260427221731327.png|500]]

例如这里我配置的是`Kimi`模型，并询问`Claude Code`它使用了什么模型。

现在，可以在对话框输入一些以`/`开头（Slash Command）的命令，熟悉`Claude Code`的一些常用操作了。

## 2、/usage

`/usage` 用于查看当前 `Claude Code` 会话的成本和用量概览，也可以使用别名 `/cost`。

如图所示：

![[image-20260427222213715.png|500]]

输出信息解释如下：

- `Total cost`：当前会话的本地估算费用。API 按量用户可参考该信息，但实际账单以 Console 为准；Pro/Max 订阅用户可以忽略。（这里也提示如果是接入第三方模型，估算费用是不准确的。）

- `Total duration (API)`：当前会话 API 调用的累计耗时。
- `Total duration (wall)`：当前会话从开始到现在经过的现实时间。
- `Total code changes`：它反映会话跟踪到的变更行数，不一定等同于`git diff`的全部语义，也不一定只限代码，可能包括配置、文档等文件变更。
- `Usage by model`：按模型统计`input`、`output`、`cache read`、`cache write`
	- `input`：本会话中按模型累积的普通输入 token。它通常包括：当前新输入、没有命中缓存的上下文、没有被写入缓存的工具结果、文件内容等。
	- `output`：模型生成的输出 token。包括普通回答，也通常包括 extended thinking / thinking tokens 这类模型内部推理输出相关 token。
	- `cache write`：本次请求中被写入 prompt cache 的输入 token。它相比普通 input token 更贵。因为后续如果命中，就可以通过`cache read`便宜地复用。
	- `cache read`：本次请求中从 prompt cache 命中的输入 token。cache read 通常是普通 input 价格的 0.1 倍，也就是约 10%。

> 关于命中缓存 ：本次请求中，有一部分输入上下文没有按普通 input token 计费，而是从 prompt cache 里读出来，显示为 cache read。
> 
> 平时和`Claude Code`对话时，`Claude Code`不只是把你当前这一句话发给模型，而是将很多上下文一起发送，比如 系统提示词、CLAUDE.md、Skill描述、历史对话等。这些内容中有一部分是重复出现的稳定上下文，如果你在同一个项目中重复提问，CLAUDE.md、之前读过的大文件、项目结构、系统提示等可能多轮都不变。如果按普通 input token 计费，就会很贵。
> 
> Prompt caching 的作用就是：把这些稳定上下文写入缓存，后续请求如果还能复用，就从缓存读取。

例如，当我首次打开会话，向模型发送了一句“你好”后，调用`/usage`查看情况：

![[Pasted image 20260514145827.png|500]]

在本次的请求里，输入上下文更接近：4.4k + 41.7k + 0 = 46.1k。

## 3、/doctor

`/doctor` 命令是 `Claude Code` 的诊断命令，用于检查当前 `Claude Code` 的安装、配置和运行环境是否存在明显问题。

如下图所示：

![[image-20260427223553784.png|500]]

这里还可以看到自动更新是 disabled 的，因为设置了 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`。如果希望打开自动更新，移除原先配置中的 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`。

## 4、/status

`/status` 用于打开 `Claude Code` 设置界面的 Status 页面，查看当前环境状态，例如版本、当前模型、账号状态、连接状态等信息。

![[image-20260427223830018.png|500]]

相关字段解释：

- `Session name`：当前会话名称。默认没有名称，可以通过`/rename`为当前会话取一个别名。之后使用 `/resume` 恢复会话时，可以用会话名来识别，而不必依赖很长的 session ID。
- `Session ID`：当前会话的唯一标识。
- `cwd`：当前这个`Claude Code`会话启动时所在的工作目录
- `Setting sources`：当前生效配置的来源。例如 `User settings` 表示用户级配置生效，通常对应 `~/.claude/settings.json`。除此之外，还可能有项目级配置、企业/组织级配置等。这些配置详见[[Settings|Settings]]。


## 5、/clear

`/clear` 用于清空当前上下文，开始一个新的上下文对话。别名：`new`和`reset`。它比较适合在任务边界使用：

- 准备开始另一个完全无关的任务
- 会话开始混淆旧问题和新问题
- 上下文太长，回答开始变慢、变贵、变乱
- 前面尝试方向错了，想让它重新开始

> 注意，clear 不会删除旧会话的上下文，后续仍然可以通过 `/resume` 在历史上下文记录中找到。

如果当前上下文太长，但模型回答效果仍然不错，想延续当前任务，则可以使用`/compact`命令。

## 6、/compact

`/compact` 用于压缩当前会话上下文，把历史会话整理成较短摘要，从而给后续对话腾出上下文空间。

它适合在长任务还没结束、但上下文已经比较长时使用。

压缩会尽量保留关键信息，但细节仍可能丢失，所以可以主动指定保留重点。使用 `/compact [instructions]`附带重点压缩说明。

示例：

```text
/compact
/compact Focus on the API changes
/compact 保留数据库结构、接口变更和未完成 TODO
```

如图所示：

![[image-20260427225456532.png|400]]

由于这里对话的上下文比较小，所以压缩并不明显，毕竟这里只发了一句：你好，你是什么模型。可以看到这里提示了使用`ctrl + o`查看压缩的具体情况。

除了手动压缩，`Claude Code`在需要时也可能**自动进行上下文压缩**。


## 7、/model和/effort

`/model` 用于切换当前会话使用的模型。

`/model` 后不带模型名称时，会打开模型选择器（这里 Kimi 都是同一个模型），例如：

![[image-20260427224621077.png|500]]

`/model` 后带模型名称时，则可以直接切换到指定模型。

示例：

```text
/model [模型名]
```

对于支持 `effort level` 的模型，还可以执行 `/effort`：

![[Pasted image 20260514155326.png|500]]

> 注意：如果 Claude Code 已经配置为接入第三方模型，或接入兼容 Anthropic API 的模型网关，那么界面中显示的 `Sonnet`、`Opus`、`Haiku` 等名称，不一定代表实际调用的是 Anthropic 官方对应模型。
> 例如在当前配置中，`Sonnet`、`Opus`、`Haiku` 都被映射到了 `kimi-for-coding`。因此，虽然 Claude Code 界面上仍然显示这些模型名称，但实际请求会被转发到 `kimi-for-coding`，而不是 Anthropic 官方的 Sonnet、Opus 或 Haiku。



## 8、/resume

`/resume` 用于恢复或切换到之前的会话。可以通过会话 ID、会话名称恢复，也可以不带参数打开会话选择器。 `/continue` 是它的别名。

示例：

```bash
/resume
/resume my-session-name
/resume <session-id>
```

执行`/resume`会打开会话选择器：

![[image-20260427225053266.png|500]]

选择指定会话进行恢复。

## 9、/exit

`/exit` 用于退出当前`Claude Code`会话，返回 shell。它的别名是 `/quit`。


# 五、权限模式

权限模式（Permission Mode）用于控制`Claude Code`会话在编辑文件、执行命令或发起网络请求前，是否需要向用户确认。不同模式对应不同的自主程度：监督越多，越安全；确认越少，效率越高，但风险也更大。

选择什么权限模式，依据具体的实际情况来定。

有关权限模式的更详细介绍参考[[2、Permission Mode|权限模式]]。

日常使用中，`Claude Code`会话打开默认有三种权限模式：

- `default`：默认模式，它是最保守，最适合日常使用的模式。**在该模式下，`Claude Code` 可以读取文件，但进行文件编辑、运行命令或其他可能产生影响的操作前，会先向你确认**。简单来说就是**边做边问**，该模式适合新手、敏感项目、生产相关代码，或者希望逐步审查 `Claude Code` 每一步操作的场景。
- `acceptEdits`：自动编辑模式，它可以读取文件，自动批准 `Claude Code` 在**工作目录内**进行文件创建和编辑。它会自动批准一些常见文件系统命令，例如 `mkdir`、`touch`、`rm`、`mv`、`cp` 等。但它并不是完全放开，如果操作超出工作目录、涉及[[2、Permission Mode#^protected-path|受保护路径]]，或者涉及更敏感的 Bash 命令，`Claude Code` 仍然会和你确认。简单来说就是**直接改，但危险操作仍会问**。该模式适合你已经比较信任当前任务方向，希望提高迭代效率，之后再通过编辑器或 `git diff` 统一审查改动的场景。
- `plan`：规模模式，它也是只读模式。在该模式下，`Claude Code` 会阅读和分析代码，探索项目结构，并给出修改方案，但不会直接修改源代码。`plan` 并不是完全不执行命令，`Claude Code` 仍然可能运行相关命令进行探索，只是不会编辑代码和文件。简单来说就是**先看、先分析、先出方案，不直接动代码**。适合大型改造前的方案设计、陌生项目梳理、代码评审、重构计划制定等。

进入`Claude Code`会话后，默认是`default`模式：

![[image-20260427231651146.png|500]]

按`Shift + Tab`键在权限模式之间循环切换。

```text
default -> acceptEdits -> plan
```

当前模式会显示在状态栏中，如下：
![[image-20260427232015230.png|500]]

![[image-20260427232042012.png|500]]


`Claude Code`还有**Yolo 模式**：`bypassPermissions`，也就是跳过权限检查的模式。

`bypassPermissions`会禁用权限提示和安全检查，工具调用会立即执行，包括受保护路径。可以简单理解为：**基本不问，直接执行**。

它的自主性最高，但风险也最大。适合非常确定环境安全、任务边界清晰，并且你愿意承担误操作风险的场景。不建议在真实工作目录、生产项目、重要代码仓库或包含敏感凭据的环境中随便使用。

启动`Claude Code`时，如果增加`--dangerously-skip-permissions`，就会进入`bypassPermissions`。

```bash
claude --dangerously-skip-permissions
```

此时`bypassPermissions`也加入了`Shift + Tab`的模式循环中。

也可以指定 `--permission-mode` 为 `bypassPermissions` 进入：

```bash
claude --permission-mode bypassPermissions
```

如图所示：

![[image-20260427233202841.png|500]]


# 六、简单实战

下面进行一个简单实战：让`Claude Code`实现一个网页版的TodoList应用：

这里先计划方案，创建项目目录进入会话后，先切换到`plan mode`，在对话框输入：

```text
设计一个 todo 应用，通过 HTML + CSS + JavaScript 实现，请你规划下需求和技术方案
```

如图所示：

![[image-20260427234137834.png|600]]

在整个过程中，`Claude Code`会和你确认一些功能需求。确认完成后，它会生成一份较完整的实现计划。

如果计划符合你的预期，可以让`Claude Code`直接按计划自动执行；

如果对当前计划还不满意，也可以继续补充需求，再让它重新调整方案。

示例：

**沟通需求**：

![[image-20260427234331376.png|600]]

![[image-20260427234350263.png|600]]

![[image-20260427234413903.png|600]]

**生成方案**：

![[image-20260427234632965.png|600]]

**执行计划**：

![[image-20260427234715436.png|600]]

最终的效果如下：

![[image-20260427234915059.png|600]]

# 七、补充

1. 在`Claude Code`会话中，按下`!`可进入Bash执行命令
2. macOS下，在对话框输入内容，换行需要按`Option + Shift`。如果使用的终端是`Terminal`，还需要在`Terminal`设置勾选如下选项才能生效

![[image-20260427235238808.png|500]]

3. 如果觉得在对话框输入内容不方便，按下`Ctrl + G`可以打开默认编辑器来编辑对话内容，比如默认打开`VS Code`。
4. 对话框支持图片输入，可以直接将图片拖到对话框。
