
# 一、概述

JSON-RPC 是一种**基于JSON 轻量级远程过程调用**（Remote Procedure Call）协议。简单说，它规定了客户端和服务端之间如何调用 JSON 格式表达：

- 我要调用哪个方法
- 传什么参数
- 调用结果是什么
- 如果出错，错误信息怎么返回

它本身不绑定具体传输协议，可以跑在 TCP、HTTP、WebSocket、Unix Domain Socket、stdin/stdout等，例如 MCP、LSP等场景都有 JSON-RPC 的影子。

它本质上解决的问题是：

> 客户端希望像调用本地函数一样，调用远程服务器上的函数。

例如本地函数调用像这样：

```JavaScript
add(1, 2)
```

客户端想调用服务端的 `add` 方法：

```JSON
{
  "method": "add",
  "params": [1, 2]
}
```

服务器执行后返回：

```JSON
{
  "result": 3
}
```

JSON-RPC 就是 RPC 协议的一种 JSON 表达格式。

# 二、JSON-RPC 2.0 的基本格式

## 1、请求格式

JSON-RPC 2.0 中，一个标准请求通常长这样：

```json
{
  "jsonrpc": "2.0",
  "method": "methodName",
  "params": {},
  "id": 1
}
```

字段含义：

| 字段        | 含义                            |
| --------- | ----------------------------- |
| `jsonrpc` | 协议版本，JSON-RPC 2.0 固定是 `"2.0"` |
| `method`  | 要调用的方法名                       |
| `params`  | 方法参数，可以是对象或数组                 |
| `id`      | 请求 ID，用于匹配响应                  |

## 2、响应格式

成功响应：

```json
{
  "jsonrpc": "2.0",
  "result": {
    "name": "Alice"
  }
  "id": 1
}
```

|字段|含义|
|---|---|
|`jsonrpc`|协议版本|
|`result`|成功结果|
|`id`|对应请求中的 `id`|

失败响应：

```json
{  
  "jsonrpc": "2.0",  
  "error": {  
    "code": -32601,  
	"message": "Method not found"  
  },  
  "id": 1  
}
```

> result 和 error 不能同时存在

字段含义：

| 字段              | 含义        |
| --------------- | --------- |
| `error.code`    | 错误码       |
| `error.message` | 错误说明      |
| `error.data`    | 可选，额外错误信息 |
| `id`            | 对应请求 ID   |
JSON-RPC 2.0 定义了一些标准错误码：

| 错误码      | 含义                      |
| -------- | ----------------------- |
| `-32700` | Parse error，JSON 解析失败   |
| `-32600` | Invalid Request，请求格式不合法 |
| `-32601` | Method not found，方法不存在  |
| `-32602` | Invalid params，参数错误     |
| `-32603` | Internal error，服务端内部错误  |

服务端也可以定义业务错误码，例如：

```json
{
  "code": 10001,
  "message": "User not found"
}
```


# 三、无响应请求

如果请求中没有 `id` ，则表示这是一个`notification`。

示例：

```json
{
  "jsonrpc": "2.0",
  "method": "log.event",
  "params": {
    "type": "click",
    "target": "submit"
  }
}
```

服务端收到后执行方法，但不会返回响应。

# 四、批量调用

`JSON-RPC` 支持一次发送多个请求：

```json
[
  {
    "jsonrpc": "2.0",
    "method": "user.get",
    "params": { "id": 1 },
    "id": 1
  },
  {
    "jsonrpc": "2.0",
    "method": "user.get",
    "params": { "id": 2 },
    "id": 2
  }
]
```

响应也是数组：

```
[
  {
    "jsonrpc": "2.0",
    "result": {
      "id": 1,
      "name": "Alice"
    },
    "id": 1
  },
  {
    "jsonrpc": "2.0",
    "result": {
      "id": 2,
      "name": "Bob"
    },
    "id": 2
  }
]
```

> 批量响应的顺序不一定和请求顺序一致，客户端应通过 `id` 匹配。

# 四、JSON-RPC over HTTP

`JSON-RPC`只规定消息格式，不规定消息的传输方式。对于 HTTP，实际经常使用 HTTP POST：

```http
POST /rpc HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "user/get",
  "params": {
    "id": 123
  },
  "id": 1
}
```

> 向 `example.com` 这个服务器的 `/rpc` 路径发送一个 HTTP POST 请求，请求体里是一条 JSON-RPC 消息。