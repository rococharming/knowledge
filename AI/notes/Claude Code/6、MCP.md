# 一、MCP的概念

`MCP`全称`Model Context Protocol`（模型上下文协议），它是一套开发协议，用来让 AI Agent（如`Claude Code`、`Codex`等）以统一方式连接外部工具、数据源、数据库和API。

在`Claude Code`中，可以这样理解：`Claude Code`本身扮演`MCP Client`，`GitHub`、`Notion`、`Sentrt`、数据库、本地脚本等能力，则通过不同的`MCP Server`暴露出来。

```text
Claude Code
  └── 通用 MCP Client
        ├── GitHub MCP Server
        ├── Notion MCP Server
        ├── Sentry MCP Server
        ├── PostgreSQL MCP Server
        ├── 本地脚本 MCP Server
        └── 自定义 MCP Server
```

连接`MCP Server`后，`Claude Code`可以在会话中直接读取或操作外部系统。

`MCP`的核心价值是：**把外部系统的能力结构化地交给模型使用**。

> 需要强调的是，MCP 并不是专门为 Claude Code 设计的私有机制，它是一套开放标准。同一个 MCP Server 理论上也可以被其他支持 MCP 的客户端使用。


# 二、MCP提供的能力

一个`MCP Server`可以向`Claude Code`提供三类能力：

| 能力        | 作用                    | 在 Claude Code 中的表现                    |
| --------- | --------------------- | ------------------------------------- |
| Tools     | 让模型调用外部工具或执行操作        | 查询 issue、创建 PR、查数据库、调用 API            |
| Resources | 让模型读取外部资源             | 用 `@` 引用 issue、commit、文档、数据库 schema 等 |
| Prompts   | 让模型调用 Server 提供的预设工作流 | 通常表现为 `/server:prompt_name` 形式的命令     |

## 1、Tools

`Tools`是MCP最核心的能力。它的作用是：把外部系统中的某个操作能力暴露给模型调用。例如 GitHub MCP Server 可以提供：

```text
list_issues
create_issue
search_repositories
create_pull_request
```

这些工具通常不是给用户手动输入的命令，而是`Claude Code`在对话过程中自动调用的能力。

比如对 `Claude Code` 说：

```text
请查询这个仓库最新的 3 个 open issue
```

Claude Code 会根据任务需要，自动判断是否调用 GitHub MCP Server 暴露的相关 tool。

MCP tools 的内部命名通常类似：

```text
mcp__github__list_issues
mcp__github__search_repositories
```

命名结构大致是：

```text
mcp__{server_name}__{tool__name}
```

需要注意：`mcp__github__list_issues` 这类名字通常是工具的内部标识，不会直接显示在 `/` 命令菜单里。

## 2、Resources

`Resources`是 MCP 提供外部上下文的能力。

它的作用是：让 `Claude Code` 可以读取外部系统的某个资源，并把它作为上下文加入当前会话。在 Claude Code 中，resources 通常可以通过 `@` 引用。

资源格式大致是：

```text
server:protocol://resource/path
```

例如，GitHub MCP Server 提供：

![[Pasted image 20260509114604.png]]

示例，在`Claude Code`会话中提问：

```text
请分析 @github:repo//owner/repo/commit/abc123 的改动
```
``
## 3、Prompts

MCP也可以暴露`Prompts`，`Prompts`是 MCP Server 提供的预设提示词或预设工作流。

它的作用是：把某些常用任务封装成一个可直接调用的命令。

例如 GitHub MCP Server 可能提供：

```
issue_to_fix_workflow
AssignCodingAgent
```

Claude Code 官方文档里写的 MCP prompt 命令格式是：

```text
/mcp__<server>__<prompt>
```

也就是：

```text
/mcp__servername__promptname
```

在某些 Claude Code 版本、某些界面或某些 MCP Server 上，实际补全菜单里也可能显示成slash command，格式为：

```text
/server_name:prompt_name
```

例如，在 `/` 命令菜单里看到的：

![[Pasted image 20260509115221.png]]



# 三、MCP Server的管理

`Claude Code`内置 MCP 管理能力，核心命令是：

```shell
claude mcp
```

常见子命令如下：

| 命令                                 | 作用                                     |
| ---------------------------------- | -------------------------------------- |
| `claude mcp add`                   | 添加 MCP Server                          |
| `claude mcp list`                  | 查看已配置的 MCP Server                      |
| `claude mcp get <name>`            | 查看某个 MCP Server 的配置                    |
| `claude mcp remove <name>`         | 删除某个 MCP Server                        |
| `claude mcp reset-project-choices` | 重置 project 作用域 MCP Server 的批准记录        |
| `claude mcp serve`                 | 把 Claude Code 自身作为 MCP Server 提供给其他客户端 |
| `/mcp`                             | 在 Claude Code 会话中查看 MCP 状态、认证状态和可用工具等  |

示例：

```shell
claude mcp list
claude mcp get github
cluade mcp remove github
```

进入`Claude Code`之后，也可以执行 slash command：

```shell
/mcp
```

用来查看某个 MCP Server 是否启动成功，是否需要认证，暴露了哪些能力等。`/mcp` 也常用于触发 OAuth 登录流程。


# 四、MCP  Server接入方式

## 1、三种方式

`Claude Code`支持三种 MCP Server 的接入方式：

|接入方式|含义|适合场景|当前建议|
|---|---|---|---|
|HTTP|远程 HTTP MCP Server|GitHub、Notion、Sentry、Stripe 等云服务|推荐方式|
|SSE|Server-Sent Events|老版本远程 MCP Server|已弃用，主要用于兼容|
|stdio|standard input / standard output|本地脚本、本地数据库、本地工具|本地工具推荐方式|

其中：

- HTTP 是现在连接远程 MCP Server 的推荐方式
- SSE 是旧方式，仍然支持，但新配置优先使用 HTTP
- stdio 是本地进程方式，适合本地脚本、数据库、本地工具

## 2、远程 HTTP Server

HTTP 是现在连接远程 MCP Server 的推荐方式。

添加 HTTP Server 的命令如下：

```shell
claude mcp add --transport http <name> <url>
```

其中：

- name：MCP Server 名称
- url：MCP Server 的远程地址

示例1：连接 Notion

```shell
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

示例2：连接 GitHub

如果需要认证，可以带请求头：

```shell
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
--header "Authorization: Bearer YOUR_GITHUB_PAT"
```

## 3、远程 SSE Server

SSE 是 Server-Sent Events 的缩写。`Claude Code`虽然支持SSE，但它已经属于旧方式。新配置优先使用 HTTP。

添加 SSE Server 的命令如下：

```shell
claude mcp add --transport sse <name> <url>
```

注意：

如果一个 MCP Server 同时支持 HTTP 和 SSE，优先使用 HTTP。


## 4、本地 stdio Server

stdio 是 standard input / standard output 的缩写。这种方式会在本地启动一个 MCP Server 进程，`Claude Code`通过标准输入输出和它通信。

它适合：

- 本地数据库
- 本地文件系统
- 本地脚本
- 自定义工具
- 需要本机环境的 MCP Server

添加 stdio Server 的命令：

```shell
claude mcp add --transport stdio [options] <name> -- <command> [args...]
```

示例：添加 Airtable MCP Server

```shell
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \  
-- npx -y airtable-mcp-server
```

注意参数位置：

- `--transport`
- `--env`
- `--scope`
- `--header`

这些 Claude Code 参数要放在 `name` 前面。

`--` 后面的内容才是 MCP Server 的启动命令。

例如：

```
claude mcp add --transport stdio myserver -- npx server
```

表示添加名为 `myserver` 的 MCP Server，并用下面命令启动它：

```
npx server
```

再例如：

```
claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080
```

表示启动：

```
python server.py --port 8080
```

并给该进程注入环境变量：

```
KEY=value
```

# 五、Claude Code 加载MCP工具

`Claude Code`本地通常保存的是 MCP Server 的连接配置，比如：

```json
"mcpServers": {
	"github": {
		"type": "http",
		"url": "https://api.githubcopilot.com/mcp/",
		"headers": {  
			"Authorization": "Bearer ..."  
	    }
	}
}
```

它不需要在本地预置一份 GitHub MCP 工具说明文档。

**连接 MCP Server 后，Claude Code 会通过 MCP 协议向 Server 获取工具列表**。

MCP 协议是基于 `JSON-RPC 2.0` （详见[[JSON RPC]]）设计的，如果 MCP Server 是 HTTP 类型，例如：

```text
https://api.githubcopilot.com/mcp/
```

那么`Claude Code`会通过 HTTP POST 向 MCP endpoint 发送 JSON-RPC 风格的 MCP 请求。

```json
{
  "jsonrpc": "2.0",
  "metjod": "tools/list",
  "params": {},
  "id": 1
}
```

服务端返回：

```JSON
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {
        "name": "search_issues",
        "description": "Search GitHub issues",
        "inputSchema": {
          "type": "object",
          "properties": {
            "query": {
              "type": "string"
            }
          },
          "required": ["query"]
        }
      }
    ]
  },
  "id": 1
}
```

其中返回的工具字段说明：

| 字段            | 含义                  |
| ------------- | ------------------- |
| `name`        | 工具名                 |
| `description` | 工具描述                |
| `inputSchema` | 工具参数 schema         |
| `properties`  | 参数列表                |
| `required`    | 必填参数                |

`Claude Code`拿到这些工具定义后，会把它们注册成当前会话可用的 MCP tools。

例如，在`/mcp`下可以查看`add_issue_commnet`工具说明：

![[Pasted image 20260509155525.png]]

如果用户说：

```text
帮我给 anthropics/claude-code 的第 123 号 issue 评论：我会看一下这个问题。
```

`Claude Code` 会根据工具描述和参数 schema，选择：

```text
mcp__github__add_issue_comment
```

并从自然语言中提取参数：
```JSON
{
  "owner": "anthropics",
  "repo": "claude-code",
  "issue_number": 123,
  "body": "我会看一下这个问题。"
}
```

随后 Claude Code 会向 MCP Server 发送 `tools/call` 请求。请求体大致类似：

```JSON
{
  "jsonrpc": "2.0",
  "id": 42,
  "method": "tools/call",
  "params": {
    "name": "add_issue_comment",
    "arguments": {
      "owner": "anthropics",
      "repo": "claude-code",
      "issue_number": 123,
      "body": "我会看一下这个问题。"
    }
  }
}
```

这里：

-  "tools/call"：表示调用某个工具
- "params.name"：表示要调用的工具名
- "params.arguments"：表示传给工具的参数

# 六、Claude Code MCP 机制

## 1、MCP Tool Search

MCP Server 暴露的工具越多，工具元信息就越多。如果把所有工具的完整描述和参数 schema 一次性塞进上下文，会消耗大量大量 token。

`Claude Code`支持 **MCP Tool Search** 机制，用于减少这部分上下文占用。MCP Tool Search 默认启用。

其思想是：

> 会话开始时只加载较轻量的信息，而不是加载所有工具的完整定义。任务需要时再搜索相关工具。

如果更喜欢**基于阈值**的加载方式，执行`claude`可以添加：

```shell
ENABLE_TOOL_SEARCH=auto claude
```

基于阈值的意思是：当工具 schema 能放入上下文窗口的一定比例以内时，就预先加载；超过阈值的部分才延迟加载。

还可以设置：

```shell
ENABLE_TOOL_SEARCH=false claude
```

表示禁用 Tool Search，尽量 upfront loading。

另外，如果某个 MCP Server 的工具非常重要，希望它每次都直接加载，可以在配置中使用：

```JSON
{
  "mcpServers": {
    "core-tools": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "alwaysLoad": true
    }
  }
}
```

> `alwaysLoad` 不适合滥用。否则会重新增加上下文占用。

## 2、动态工具更新

Claude Code 支持 MCP 的 `list_changed` 通知。

Server 如果新增、删除或更新了工具列表，可以通知 Claude Code 刷新可用能力。这样就不需要每次都手动断开重连。

## 3、自动重连

HTTP 和 SSE 类型的 MCP Server 如果在会话中断开，Claude Code 会尝试自动重连。

重试过程中，`/mcp` 中可能显示为：

```
pending
```

如果持续失败，则会进入失败状态，需要用户手动处理。

需要注意：

|类型|是否自动重连|
|---|---|
|HTTP|支持自动重连|
|SSE|支持自动重连|
|stdio|不按远程连接方式自动重连|

如果 stdio Server 进程崩溃，通常需要重新启动会话或重新连接。

原因是 stdio Server 本质上是本地子进程，不是远程 HTTP 连接。


# 七、MCP的配置作用域

`Claude Code`的 MCP Server 可以配置在不同作用域。

常见的作用域如下：

| 作用域                  | 生效范围            | 是否团队共享   | 存储位置                      |
| -------------------- | --------------- | -------- | ------------------------- |
| local                | 当前项目            | 否        | `~/.claude.json` 中当前项目路径下 |
| project              | 当前项目            | 是        | 项目根目录 `.mcp.json`         |
| user                 | 当前用户所有项目        | 否        | `~/.claude.json`          |
| plugin-provided      | 插件启用范围          | 取决于插件    | 插件配置                      |

执行 `claude mcp add`增加 MCP Server 时，可以通过`--scope`选择配置作用域，例如：

```shell
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

由于`local`是**默认作用域**，因此不加`--scope`默认就是`local`。

注意事项：

- 出于安全考虑，Claude Code 使用 `.mcp.json` 中的 project-scoped Server 前，会要求用户批准。需要重置批准记录，可执行：

```shell
claude mcp reset-project-choices
```

- 团队共享配置时，不要把密钥直接写进 `.mcp.json`。

可以使用环境变量：

```JSON
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```


# 八、插件提供的MCP Server

`Claude Code`的插件可以打包`MCP Server`。插件启用后，对应的 MCP Server 会随插件一起提供能力。有关插件可参考：[[8、Plugin|Plugin]]。

插件系统本身支持：

- skills
- agents
- hooks
- MCP servers
- slash commands

插件提供的 MCP Server 和手动添加的 MCP Server 在使用上类似，都会出现在 Claude Code 的 MCP 能力中。

注意事项：

- 插件可以内置 MCP Server 配置。
- 插件启用后，相关 MCP 能力自动加载。
- 插件 MCP 工具会和手动配置的 MCP 工具一起出现。
- 插件 Server 通常通过插件机制管理，而不是像普通 MCP Server 一样单独管理。
- 如果在会话中启用或禁用插件，可能需要执行 `/reload-plugins` 让 Claude Code 重新加载插件能力。



# 九、MCP 认证方式

远程 MCP Server 通常需要认证。`Claude Code`中常见的认证方式主要有三类：

|类型|典型场景|配置方式|
|---|---|---|
|静态 Header|GitHub PAT、API Key、Bearer Token|`--header` 或 `headers`|
|OAuth 2.0|Sentry、Notion、部分 SaaS 服务|`/mcp` 浏览器授权|
|动态 Header|企业 SSO、短期 Token、Kerberos、内部认证网关|`headersHelper`|

## 1、静态 Header 认证

最常见的方式是通过 HTTP Header 传递认证信息。

例如 Bearer Token：

```shell
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

GitHub 的远程 MCP Server 就是通过 Header 携带 GitHub PAT 进行认证的。

也可以使用其他 Header，例如 API Key：

```shell
claude mcp add --transport http private-api https://api.company.com/mcp \
  --header "X-API-Key: your-key-here"

```

如果要在配置文件中配置，可以写成：

```JSON
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

但如果配置文件可能提交到 Git，**不要直接写入真实 token**。例如上述配置是项目级别的`.mcp.json`配置文件，则更推荐用环境变量：

```shell
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

## 2、OAuth 认证

一些远程 MCP Server 支持`OAuth 2.0`。有关 OAuth 的介绍参考[[OAuth|OAuth]]。

典型流程是先添加 Server：

```shell
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

然后进入 Claude Code：

```shell
claude
```

输入：

```shell
/mcp
```

按提示在浏览器中完成授权。

Claude Code 会保存认证 token，并在需要时自动刷新。之后再次进入项目，通常不需要重新登录；如果需要撤销授权，可以在 `/mcp` 菜单中选择清除认证。

## 3、动态Header认证

如果认证信息不是固定值，而是需要在连接时动态生成，可以使用 `headersHelper`。

例如：

```json
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

`headersHelper`是一个本地脚本文件。当 Claude Code 准备连接这个 HTTP 类型的 MCP Server 时，它会先执行这个脚本，让脚本输出认证 Header，然后 Claude Code 把这些 Header 带到后续请求里。
