# 一、简介

`Claude Code` 是 Anthropic 推出的 AI 代码工具。

它能在终端或 IDE 中理解代码库、编辑文件、执行命令，并与开发工具协同工作，帮助开发者用**自然语言**完成代码阅读、开发、调试、重构、测试等任务。

`Claude Code` 的能力建立在 `Claude` 模型之上，但也可以通过配置**接入第三方模型**。

# 二、安装

以`macOS`为例，在终端执行：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

这是原生安装方式，支持后台自动更新 Claude Code。但如果在后续配置文件中设置了`"CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"`，则不会自动更新。

下载完成后，执行：

```bash
claude --version
```

如果看到版本，说明安装成功：

![[assets/image-20260427214629504.png|400]]

可以执行如下命令手动更新：

```bash
claude update
```

如下图所示：

![[assets/image-20260427214617672.png|400]]

# 三、配置接入第三方模型

## 1、基本原理

进入项目目录，首次启动`Claude Code`：

```bash
cd path/to/project
claude 
```

会提示登录，但这里不推荐使用官方接口，原因有两点：

- 需要国外手机号验证，比较麻烦
- Anthropic 对中国管控较严，后续使用很有可能被封号

因此，推荐**通过配置接入第三方模型**，需要配置 `BASE_URL + API_KEY + model` 映射。

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
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_AUTH_TOKEN": "YOUR API KEY",
    "ANTHROPIC_DEFAULT_FABLE_MODEL": "deepseek-v4-pro[1M]",
    "ANTHROPIC_DEFAULT_FABLE_MODEL_NAME": "deepseek-v4-pro",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1M]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "deepseek-v4-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1M]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "deepseek-v4-pro",
    "ANTHROPIC_MODEL": "deepseek-v4-pro"
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

配置好模型之后，就可以进入项目目录，在终端执行：

```shell
claude
```

即可进入 Claude Code 会话交流了，如下图所示：

![[assets/Pasted image 20260709103931.png|400]]

现在，可以在对话框输入`/`开头（Slash Command）的命令，熟悉 Claude Code 的一些常用操作了。

## 2、/usage

`/usage` 用于查看当前 Claude Code 会话的成本和用量概览，也可以使用别名 `/cost`。

如图所示：

![[assets/Pasted image 20260709112423.png|500]]

输出信息解释如下：

- **Total cost**：当前会话的本地估算费用。API 按量用户可参考该信息，但实际账单以 Console 为准。Pro/Max 订阅用户可以忽略。注意，这里提示如果接入第三方模型，估算费用可能不准确。
- **Total duration (API)**：当前会话 API 调用的累计耗时。
- **Total duration (wall)**：当前会话从开始到现在经过的现实时间。
- **Total code changes**：反映会话跟踪到的变更行数，不一定等同于`git diff`的全部语义，也不一定只限代码，可能包括配置、文档等文件变更。
- **Usage by model**：按模型统计`input`、`output`、`cache read`、`cache write`。具体含义可参考[[1、AI常见概念汇总#二、Token|Token]]。实际 input tokens ≈ input + cache read + cache write。

## 3、/doctor

`/doctor` 命令是 `Claude Code` 的自诊断命令，相当于健康检查，会扫描当前安装并报告几类关键状态：

| 检查项                       | 用途                                                       |
| ------------------------- | -------------------------------------------------------- |
| **Diagnostics**           | 运行环境：版本、提交哈希、平台、路径、安装方式                                  |
| **Updates**               | 更新通道、是否启用自动更新、上次更新结果                                     |
| **Background** **server** | 后台守护进程（用于 IDE 集成、statusline 等）                           |
| **Remote** **Control**    | 是否登录 claude.ai / Anthropic API，能否启用远程控制                  |
| **MCP**                   | 已配置的 MCP 服务器、传输协议（stdio / http / sse）、连接状态、注册工具数、上下文预算占用 |
| **Skills**                | 已加载技能列表，及上下文预算占用情况                                       |
| **Version** **locks**     | 运行中的版本锁（防止多实例冲突）                                         |

示例：

![[assets/Pasted image 20260709132248.png|500]]

这里还可以看到自动更新是 disabled 的，因为设置了 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`。如果希望打开自动更新，移除原先配置中的 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`。

## 4、/status

`/status` 用于打开 `Claude Code` 设置界面的 Status 页面，查看当前环境状态，例如版本、当前模型、账号状态、连接状态等信息。

![[assets/Pasted image 20260709132655.png|500]]

部分字段解释：

- `Session name`：当前会话名称。默认没有名称，可以通过`/rename`为当前会话取一个别名。之后使用 `/resume` 恢复会话时，可以用会话名来识别，而不必依赖很长的 session ID。
- `Session ID`：当前会话的唯一标识。
- `cwd`：当前会话启动时所在的工作目录
- `Setting sources`：当前生效配置的来源。例如 `User settings` 表示用户级配置生效，通常对应 `~/.claude/settings.json`。除此之外，还可能有项目级配置等。这些配置详见[[Settings|Settings]]。


## 5、/clear

`/clear` 用于清空当前上下文，开始一个新的上下文对话。别名：`new`和`reset`。它比较适合在任务边界使用：

- 准备开始另一个**完全无关**的任务
- 会话开始混淆旧问题和新问题
- 上下文太长，回答开始变慢、变贵、变乱
- 前面尝试方向错了，想让它重新开始

> 注意，clear 不会删除旧会话的上下文，后续仍然可以通过 `/resume` 在历史上下文记录中找到。

如果当前上下文太长，但模型回答效果仍然不错，想延续当前任务，则可以使用`/compact`命令。

## 6、/compact

`/compact` 用于主动压缩当前会话上下文，把历史会话整理成较短摘要，从而给后续对话腾出上下文空间。

它适合在长任务还没结束、但上下文已经比较长时使用。

压缩会尽量保留关键信息，但细节仍可能丢失，所以可以主动指定保留重点。使用 `/compact [instructions]`附带重点压缩说明。

示例：

```text
/compact
/compact Focus on the API changes
/compact 保留数据库结构、接口变更和未完成 TODO
```

即使不主动压缩，`Claude Code` 也会在上下文临近上限时**自动进行上下文压缩**。但自己主动压缩上下文是一个良好的习惯。


## 7、/model和/effort

`/model` 用于切换当前会话使用的模型。

`/model` 后不带模型名称时，会打开模型选择器。例如：

![[assets/Pasted image 20260709133121.png|400]]

`/model` 后带模型名称时，则可以直接切换到指定模型。

示例：

```text
/model [模型名]
```

对于支持 `effort level` 的模型，还可以执行 `/effort`：

![[assets/Pasted image 20260709133217.png|400]]



## 8、/resume

`/resume` 用于恢复或切换到之前的会话。可以通过会话 ID 或会话名称恢复，也可以不带参数打开会话选择器。`/continue` 是它的别名。

示例：

```bash
/resume
/resume my-session-name
/resume <session-id>
```

执行 `/resume` 会打开会话选择器：

![[assets/image-20260427225053266.png|500]]

## 9、/exit

`/exit` 用于退出当前 `Claude Code` 会话，返回 shell。它的别名是 `/quit`。

# 五、权限模式

权限模式（Permission Mode）用于控制 Claude Code 会话在编辑文件、执行命令或发起网络请求前，是否需要向用户确认。不同模式对应不同的自主程度：监督越多，越安全；确认越少，效率越高，但风险也更大。

选择什么权限模式，依据具体的实际情况来定。

日常使用中，Claude Code 会话启动后默认有三种权限模式：

- `default`：默认模式。该模式下，Claude Code 可以读取文件，但进行文件编辑、运行命令或其他可能产生影响的操作前，会先向你确认。
- `acceptEdits`：自动编辑模式。不仅可以读取文件，同时自动批准在**工作目录内**进行文件创建和编辑。
- `plan`：计划模式。它也是只读模式。在该模式下，Claude Code 会阅读和分析代码，探索项目结构，并给出修改方案，但不会直接修改源代码。`plan` 并不是完全不执行命令，`Claude Code` 仍然可能运行相关命令进行探索，只是不会编辑代码和文件。

进入 Claude Code 会话后，默认是`default`模式：

![[assets/Pasted image 20260713022422.png|600]]

按 <kbd>Shift</kbd> + <kbd>Tab</kbd> 键在权限模式之间循环切换。

```text
default -> acceptEdits -> plan
```

当前模式会显示在状态栏中，如下：

![[assets/Pasted image 20260713022548.png|600]]


![[assets/Pasted image 20260713022607.png|600]]

此外，Claude Code 还有 **Yolo 模式**：`bypassPermissions`，也就是跳过权限检查。

`bypassPermissions`会禁用权限提示和安全检查，工具调用会立即执行。可以简单理解为：**基本不问，直接执行**。

它的自主性最高，但风险也最大。适合非常确定环境安全、任务边界清晰，并且你愿意承担误操作风险的场景。

启动 Claude Code 时，如果增加`--dangerously-skip-permissions`，就会进入`bypassPermissions`。

```shell
claude --dangerously-skip-permissions
```

此时`bypassPermissions`也加入了 <kbd>Shift</kbd> + <kbd>Tab</kbd> 的模式循环中。

也可以通过指定 `--permission-mode` 为 `bypassPermissions` 进入：

```shell
claude --permission-mode bypassPermissions
```

如图所示：

![[assets/Pasted image 20260713022832.png|600]]


有关权限模式的更详细介绍参考[[AI/notes/Claude Code/2、Permission Mode|权限模式]]。

# 六、快速入门实战

下面进行一个简单实战：让 Claude Code 实现一个网页版的待办事项应用：

这里先指定计划方案，创建项目目录进入会话后，先切换到`plan mode`，在对话框输入：

```text
设计一个 todo 应用，通过 HTML + CSS + JavaScript 实现，请你规划下需求和技术方案
```

如图所示：

![[assets/image-20260427234137834.png|600]]

在整个过程中，Claude Code 会和你确认一些功能需求。确认完成后，它会生成一份较完整的实现计划。

如果计划符合你的预期，可以让 Claude Code 直接按计划开始执行；

如果对当前计划还不满意，也可以继续补充需求，再让它重新调整方案。

示例：

**沟通需求**：

![[assets/image-20260427234331376.png|600]]

![[assets/image-20260427234350263.png|600]]

![[assets/image-20260427234413903.png|600]]

**生成方案**：

![[assets/image-20260427234632965.png|600]]

**执行计划**：

![[assets/image-20260427234715436.png|600]]

任务完成后，最终的效果如下：

![[assets/image-20260427234915059.png|600]]

# 七、Tips

1. 在 Claude Code 会话中，按下 <kbd>!</kbd> 可进入 Bash 执行命令。
2. macOS 下，在对话框输入内容，换行需要按 <kbd>Option</kbd> + <kbd>Enter</kbd>。如果使用的终端是`Terminal`，还需要在`Terminal`设置中勾选「将 <kbd>Option</kbd> 键用作 <kbd>Meta</kbd> 键」才能生效；Windows 下的换行快捷键是 <kbd>Shift</kbd> + <kbd>Enter</kbd>。

![[assets/image-20260427235238808.png|500]]

3. 如果觉得在对话框输入内容不方便，按下 <kbd>Ctrl</kbd> + <kbd>G</kbd> 可以打开默认编辑器来编辑对话内容，比如默认打开 `VS Code`。
4. 对话框支持图片输入，可以直接将图片拖到对话框或按 <kbd>Ctrl</kbd> + <kbd>V</kbd> 粘贴。
