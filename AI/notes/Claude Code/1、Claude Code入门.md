# 一、简介

`Claude Code`是Anthropic推出的AI编码代码工具。

它能在终端或IDE中理解代码库、编辑文件、执行命令，并与开发工具协同工作，帮助开发者用**自然语言**完成代码阅读、开发、调试、重试、测试等任务。

`Claude Code`能力建立在`Claude`模型之上，但也可以通过配置接入国内第三方模型。

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

![[image-20260427214629504.png]]

可以执行如下命令手动更新：

```bash
claude update
```

如下图所示：	![[image-20260427214617672.png]]

# 三、配置接入第三方模型

## 1、基本原理

进入自己的项目目录，首次启动`Claude Code`:

```bash
cd path/to/projct
claude 
```

会提示登录，但这里不推荐使用官方接口，原因有两点：

- 需要国外手机号验证，比较麻烦
- 后续使用很有可能被封号

因此，这里更推荐**通过配置接入国内第三方模型**。

在国内，想通过网关转发的方式接入第三方模型，需要配 `base URL + auth + model`映射。本质上就是将`Claude Code`的默认发给Anthropic官方接口的请求，改为发到第三方提供的Anthropic兼容接口。

下面介绍几个国内模型的接入方法，选择其中一个即可。

## 2、接入MiniMax

首先进入`Minimax`官网：https://platform.minimaxi.com/，完成注册并登录。

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

上述的`env`键的本质是给`Claude Code`使用的环境变量，让它对每次会话都生效。

这里涉及到的环境变量解释如下：

- `ANTHROPIC_BASE_URL`：把`Claude Code`默认请求的 API 地址替换为指定的代理或网关。

- `ANTHROPIC_AUTH_TOKEN`：自定义`HTTP`请求里的`Authorization`头，`Claude Code`会自动在前面加上`Bearer`，因此这里就是把MiniMax Key当作Bearer Token发送给MiniMax网关。

- `API_TIMEOUT_MS`：API请求超时，单位是毫秒（ms）。

- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`：配置为`1`表示一键关闭非必要流量。通常是为了让`Claude Code`不去做**自动更**新、反馈、错误上报等额外联网动作，只保留核心请求。

- `ANTHROPIC_MODEL`：当前要使用的模型设置名，这里表示**默认主模型直接指定为`MiniMax-M2.7`**

- `ANTHROPIC_DEFAULT_SONNET_MODEL`：把Claude Code里`sonnet`这个默认档位映射到具体模型名。意思是在`Claude Code`会话下，凡是`Claude Code`选择`Sonnet`档位时，实际请求走的是`MiniMax-M2.7`。

- `ANTHROPIC_DEFAULT_OPUS_MODEL`：同理，把 `opus`档位映射到`MiniMax-M2.7`。

- `ANTHROPIC_DEFAULT_HAIKU_MODEL`：同理，把`haiku` 档位映射到`MiniMax-M2.7`。

## 3、接入Kimi

进入Kimi Code官网购买会员订阅计划： https://www.kimi.com/code。

根据自己的需求选择合适的套餐后，访问 Kimi 会员控制台创建并获取 API Key：https://www.kimi.com/code/console

点击「新建 API Key」，复制以 sk-kimi- 开头的密钥。这个 Key 是后续连接 Kimi k2.6 的凭证，请妥善保管，如果泄漏需要重新生成。

![[image-20260427220833065.png]]	

在本地编辑配置文件`~/.claude/settings.json`，增加：

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-kimi-PILLA70MTAcBM5o7S18hGkG4tiQgqYsN7Wqyq45IcStbVhVpwX5X0eTNKP4NDCBP",
    "ANTHROPIC_BASE_URL": "https://api.kimi.com/coding/",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "kimi-for-coding",
    "ANTHROPIC_MODEL": "kimi-for-coding",
    "ANTHROPIC_REASONING_MODEL": "kimi-for-coding",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

注意：需要将`ANTHROPIC_API_KEY`的值填充为复制的API Key，注意API Key不要给别人，如果泄漏了重新生成一个。

说明：

- `Kimi k2.6`在API层面的内部模型标识符为`kimi-for-coding`，而不是`kimi-k2.6`。也可以不设置这些模型字段，因为Kimi Code后端会对这些`Claude Code`模型名执行自动映射，将其路由到`kimi-for-coding`。

- 这里这里使用的是`ANTHROPIC_API_KEY`而不是`ANTHROPIC_AUTH_TOKEN`

# 四、基本使用

## 1、第一次对话

配置好模型之后。现在就可以进入自己的项目目录，在终端执行：

```bash
claude
```

即可进入`Claude Code`会话，如下图所示：

![[image-20260427221731327.png]]

例如这里我配置的是`Kimi`模型，并询问`Claude Code`它使用了什么模型。

现在，可以在对话框输入一些以/开头的命令，熟悉`Claude Code`的一些常用操作了。

## 2、/usage

`/usage`用于查看当前`Claude Code`会话的用量和成本概览。也可以使用别名是`/cost`。

如下图所示：

![[image-20260427222213715.png]]

这里的输出一些信息解释如下：

- `Total cost`：当前会话的本地估算费用。API按量用户可参考该信息，但实际账单以Console为准；Pro/Max订阅用户可以忽略。

- `Total duration (API)`：`Claude Code`在该会话中API调用的**累计耗时**。

- `Total duration (wall)`：表示会话从开始到当前经过的现实时间。

- ``Total code changes`：它反映`Claude Code`跟踪到的变更行数，不一定等同于最终`Git diff`的全部语义，也不一定只限代码，可能包括配置、文档等文件变更。

- `Usage by model`：按模型统计`input`、`output`、`cache read`、`cache write`
- `input`：本会话中**按模型累计的、按普通输入价格处理**的`input tokens`，通常包括本轮新输入以及未从缓存读取的上下文、工具/文件内容
- `output`：本会话中**按模型累计生成**的`output tokens`。注意`extended thinking / thinking tokens`通常也按`output token`计费
- `cache read`：从`prompt cache`命中的输入token，它仍属于本次请求使用的上下文，但按`cache hit`价格计费，比`普通 input`更加便宜。
- `cache write`：本地请求中被写入`prompt cache`的token，供后续请求命中读取，写入本身会计费，价格通常高于`普通 input`。

**关于缓存命中：**

每新发起一次请求时（对话），请求的总上下文通常包含**系统提示词**、**工具说明**、**项目文件**、**历史对话**和**本轮新问题**等内容。它们从请求内容上都属于**输入上下文**。但在 token 统计和计费口径上，**未命中缓存、需要按普通方式处理的部分**通常计为`input`，**命中缓存并被复用的部分**计为`cache read`，本次请求中被写入缓存、供后续请求复用的部分计为`cache write`。模型的输出（回答）记为`output`。

## 3、/doctor

`/doctor`命令是`Claude Code`的诊断命令，用于检查当前`Claude Code`的安装、配置和运行环境是否存在明显问题。

如下图所示：

![[image-20260427223553784.png]]

这里还可以看到自动更新是 disable 的，正是因为设置了`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`。



## 4、/status

`status`用于打开`Claude Code`设置界面的`Status`页面，查看当前环境状态，例如版本、当前模型、账号状态、连接状态等信息。**它也可以在`Claude Code`正在响应时使用，不需要等待当前响应结束**。

![[image-20260427223830018.png]]

一些字段解释：

- `Session name`：当前会话名称。默认没有名称，可以通过`/rename`为当前会话取一个别名。之后使用 `/resume` 恢复会话时，可以用会话名来识别，而不必依赖很长的 session ID。
- `Session ID`：当前会话的唯一标识。
- `cwd`：当前工作目录，也就是`Claude Code`运行时所在的项目目录。
- `Setting sources`：当前生效配置的来源。例如 `User settings` 表示用户级配置生效，通常对应 `~/.claude/settings.json`。除此之外，还可能有项目级配置、企业/组织级配置等，后面介绍配置体系时可以展开说明。



## 5、/clear

`/clear` 用于**清空当前上下文**，开始一个新的空上下文对话。它适合在切换到一个完全无关的新任务时使用，避免旧上下文干扰新任务。

**旧会话不会因此被删除，后续仍然可以通过 `/resume` 找回**。

`/clear` 的别名包括 `/reset` 和 `/new`。

如果只是想释放或压缩上下文空间、但仍然延续当前任务，更适合使用 `/compact`，而不是 `/clear`。



## 6、/model

`/model`用于选择或切换当前会话使用的模型。

不带参数时，会打开模型选择器，例如：

![[image-20260427224621077.png]]

带模型名称时，可以直接切换到指定模型。对于支持`effort level`的模型，还可以**调整推理强度**。

这里需要特别强调：如果前面已经配置为接入第三方模型或兼容 Anthropic API 的网关，那么 Claude Code 界面里显示的 `Sonnet`、`Opus`、`Haiku` 等名称，可能只是路由名或模型别名。比如你这里的配置中，`Sonnet`、`Opus`、`Haiku` 都被映射到了`kimi-for-coding`，实际调用的并不是 Anthropic 官方对应模型。



## 7、/resume

`/resume` 用于恢复或切换到之前的会话。可以通过会话 ID、会话名称恢复，也可以不带参数打开会话选择器。 `/continue` 是它的别名。

示例：

```bash
/resume
/resume my-session-name
/resume <session-id>
```

下面时之间执行`/resume`打开的会话选择器：

![[image-20260427225053266.png]]

选择想要的会话进行恢复。



## 8、/compact

`/compact` 用于压缩当前会话上下文，把前面的对话整理成较短摘要，从而给后续对话腾出上下文空间。它适合在长任务还没结束、但上下文已经比较长时使用。压缩会尽量保留关键信息，但细节仍可能丢失，所以在重要节点可以主动指定保留重点。**可以使用 `/compact [instructions]` 支持附带压缩说明**。

示例：

```bash
/compact
/compact Focus on the API changes
/compact 保留数据库结构、接口变更和未完成 TODO
```

`Claude Code`在需要时也可能自动进行`compact`。

如下图所示：

![[image-20260427225456532.png]]

由于这里对话的上下文比较小，所以压缩并不明显，毕竟这里只发了一句：你好，你是什么模型。

也可以看到这里提示了使用`ctrl + o`查看压缩的具体情况。

## 9、/exit

`/exit` 用于退出当前 Claude Code CLI 会话，返回 shell。它的别名是 `/quit`。



# 五、权限模式

## 1、三种核心权限模式

**权限模式用于控制`Claude Code`在编辑文件、执行命令或发起网络请求之前，是否需要向用户确认**。不同模式对应不同的自主程度：监督越多，越安全；确认越少，效率越高，但风险也更大。

日常使用中，`Claude Code`的三个核心权限模式是：

- `default`：默认模式

`default`是最保守，最适合日常使用的模式。在该模式下，`Claude Code`通常可以读取文件，但执行文件编辑、运行命令或其他可能产生影响的操作前，会先向你确认。

可以简单理解为：边做边问你。

该模式适合新手、敏感项目、生产相关代码，或者你希望逐步审查`Claude Code`每一步操作的场景。

- acceptEdits：自动编辑模式

`acceptEdits`会自动批准`Claude Code`在**工作目录内**进行文件创建和编辑，不需要每次改文件都向你确认。除了文件编辑外，它会自动批准一些常见文件系统命令，例如`mkdir`、`touch`、`rm`、`mv`、`cp`等。

但它并不是完全放开。如果操作超出工作目录，涉及受保护路径，或者涉及更敏感的`Bash`命令，`Claude Code`仍然要求你确认。

可以简单理解为：直接改，但危险操作仍会问。

该模式适合你已经比较信任当前任务方向，希望提高迭代效率，之后再通过编辑器或`git diff`统一审查改动的场景。

- plan：规划模式

`plan`是规划模式。`Claude Code`会阅读和分析代码，探索项目结构，并给出修改方案，但不会直接修改源代码。

需要注意的是，`plan`并不等于“完全不执行命令”，`Claude Code`仍然可能运行`shell`命令进行探索，只是不会编辑代码和文件。权限提示仍按默认模式处理。

可以简单理解为：先看、先分析、先出方案，不直接动代码。

适合大型改造前的方案设计、陌生项目梳理、代码评审、重构计划制定等。

## 2、会话中切换权限模式

进入`Claude Code`会话后，默认情况如下：

![[image-20260427231651146.png]]

此时默认就是`default`模式。

可以按`Shift + Tab`键在权限模式之间循环切换。

```bash
default -> acceptEdits -> plan
```

当前模式会显示在状态栏中。

示例：

![[image-20260427232015230.png]]

![[image-20260427232042012.png]]

实际上，`Claude Code`还有`bypassPermissions`或`auto`模式，如果启用了这些可选模式，那么它们也会被加入到`Shift + Tab`的循环切换中。



## 3、启动时制定权限模式

如果希望启动`Claude Code`时直接进入指定模式，可以在命令行中使用 `--permission-mode` 参数：

```bash
claude --permission-mode default
```

```bash
claude --permission-mode acceptEdits
```

```bash
claude --permission-mode plan
```



## 4、设置模式权限模式

如果不想每次启动`Claude Code`时都手动制定`Claude Code`权限模式，可以在`settings.json`中配置默认模式：

```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

这样之后启动 Claude Code 时，就会默认使用 `acceptEdits` 模式。



## 5、Yolo模式

除了上面几个常用模式外，Claude Code 还有一些更特殊的权限模式。这里重点介绍所谓的 **Yolo 模式**。

Yolo 模式指的是：`bypassPermissions`

也就是跳过权限检查的模式。

`bypassPermissions`会禁用权限提示和安全检查，工具调用会立即执行。只有对受保护路径的写入仍然会提示。

可以简单理解为：基本不问，直接执行。

它的自主性最高，但风险也最大。适合非常确定环境安全、任务边界清晰，并且你愿意承担误操作风险的场景。不建议在真实工作目录、生产项目、重要代码仓库或包含敏感凭据的环境中随便使用。

启动`Claude Code`时，如果增加：

```bash
claude --dangerously-skip-permissions
```

就会进入这种高自主模式。这个参数等价于：

```bash
claude --permission-mode bypassPermissions
```

如下图所示：![[image-20260427233202841.png]]



## 6、受保护路径

无论当前使用哪一种权限模式，`Claude Code`都不会无条件自动批准对某些敏感路径的写入操作。这样设计是为了防止`Claude Code`误改仓库元数据、编辑器配置、Git 钩子、Shell 配置，以及`Claude Code`自身配置。

受保护目录包括：

```text
.git
.vscode
.idea
.husky
.claude
```

其中，`.claude` 下面有一些**例外目录**，因为`Claude Code`经常需要在这些位置创建**自定义命令、技能、子代理或工作树相关文件**：

```text
.claude/commands
.claude/skills
.claude/agents
.claude/worktrees
```

也就是说，`.claude` 整体属于受保护目录，但上述子目录是例外。

受保护文件还包括：

```bash
.gitconfig
.gitmodules
.bashrc
.bash_profile
.zshrc
.zprofile
.profile
.ripgreprc
.mcp.json
.claude.json

```

# 六、简单实战

让`Claude Code`实现一个网页版的`todolist`应用。

这里先计划方案，我们先进入切换到`plan mode`，在对话框输入：

```text
设计一个 todo 应用，通过 HTML + CSS + JavaScript 实现，请你规划下需求和技术方案
```

如下图所示：

![[image-20260427234137834.png]]

 在整个过程中，`Claude Code`会和你确认一些功能需求。确认完成后，它会生成一份较完整的实现计划。

如果计划符合你的预期，可以让`Claude Code`直接按计划自动执行。

如果对当前计划还不满意，也可以继续补充需求，再让它重新调整方案。

示例：

![[image-20260427234331376.png]]

![[image-20260427234350263.png]]

![[image-20260427234413903.png]]

![[image-20260427234632965.png]]

![[image-20260427234715436.png]]

最终的效果页面如下：

![[image-20260427234915059.png]]

# 七、补充

1. 在`Claude Code`会话中，按下`!`可进入Bash执行命令
2. macOS下，在对话框输入内容，换行需要按`Option + Shift`。如果使用的是`Terminal`，还需要在`Terminal`设置勾选如下选项才能生效

![[image-20260427235238808.png]]

3. 如果觉得在对话框输入内容不方便，按下`Ctrl + G`可以打开默认的编辑器编辑对话内容，比如默认打开`VS Code`。
4. 对话框支持图片输入，可以直接将图片拖到对话框。
