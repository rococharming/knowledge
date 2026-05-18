# 一、简介

`JSON-RPC`是一种基于 JSON 的远程过程调用协议。

其中：

- `JSON`是数据格式
- `RPC`是 Remote Procedure Call，即远程过程调用 

简单来说，`JSON-RPC`就是**用 JSON 表达远程过程调用请求和响应的一套协议格式**。

普通 HTTP API 通常围绕资源设计，例如：

```text
GET /users/1
POST /users
DELETE /users/1
```

而 RPC 更像是在调用一个远程函数，例如：

```
user.get
user.post
user.delete
```

`JSON-RPC`的核心思想是：

> 客户端发送一个JSON请求，说明要调用什么方法，传什么参数；服务端执行后，再返回一个JSON响应。


# 二、JSON-RPC和HTTP的关系

`JSON-RPC`不是 HTTP 本身的一部分。

它只规定**请求和响应的JSON结构**，并不强制必须运行在 HTTP 上。`JSON-RPC`可以通过 HTTP、WebSocket、TCP 等不同传输方式承载。

不过在实际使用中，`JSON-RPC`经常通过 HTTP 传输。

示例：

```http
POST /rpc HTTP/1.1
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "user.get",
  "params": {
    "id": 1
  },
  "id": 100
}
```

注：**这里的 `/rpc`只是服务端提供的一个HTTP路径，用来接收 JSON-RPC 请求。它不是 JSON-RPC 协议固定要求的名字**。

也可以叫：

```text
/api
/jsonrpc
/mcp
```

具体路径由服务端决定。


# 三、JSON-RPC请求对象

一个典型的 JSON-RPC 2.0 请求如下：

```json
{
  "jsonrpc": "2.0",
  "method": "user.get",
  "params": {
    "id": 1
  },
  "id": 100
}
```

它包含几个核心字段：

## 1、jsonrpc

`jsonrpc`用来声明 JSON-RPC 协议版本。在 JSON-RPC 2.0 中，通常固定写成：

```json
"jsonrpc": "2.0"
```

这个字段可以帮助服务端确认客户端使用的是哪个协议版本。


## 2、method

`method`表示要调用的方法名。

示例：

```json
"method": "user.get"
```

方法名本质上是一个字符串，具体命名规则由服务端定义。

常见风格命名：

```text
user.get
user.create
tools/list
resources/read
```

JSON-RPC 并不关心这个方法名背后具体对应哪个函数，它只负责把调用意图表达出来。服务端收到后，会根据`method`字段分发到对应处理逻辑。

## 3、params

`params`表示调用方法时传入的参数。

它可以是对象：

```json
{
  "jsonrpc": "2.0",
  "method": "user.get",
  "params": {
    "id": 1
  },
  "id": 100
}
```

也可以是数组：

```json
{
  "jsonrpc": "2.0",
  "method": "sum",
  "params": [1, 2, 3],
  "id": 101
}
```

对象参数更常见，因为字段含义更清晰，也更容易扩展。

例如：

```json
{
  "id": 1,
  "include_posts": true
}
```

比下面这种数组参数更容易阅读：

```json
[1, true]
```

## 4、id

`id`是请求标识，用于把响应和请求对应起来。

示例：

```json
"id": 100
```

服务端返回响应时，也会带上同样的id：

```json
{
  "jsonrpc": "2.0",
  "result": {
    "id": 1,
    "name": "Alice"
  },
  "id": 100
}
```

这样客户端就知道这个响应对应的是哪一次请求。

**`id` 在单个请求中看起来不太重要，但在并发请求、批量请求或长连接场景中非常重要。因为多个请求可能同时发出，响应也可能不按请求顺序返回**。


# 四、JSON-RPC 响应对象

`JSON-RPC`响应分为成功响应和错误响应。

## 1、成功响应

成功响应通常包含`result`字段。

示例：

```json
{
  "jsonrpc": "2.0",
  "result": {
    "id": 1,
    "name": "Alice"
  },
  "id": 100
}
```

其中：

- `jsonrpc` 表示协议版本
- `result` 表示方法调用成功后的返回值
- `id` 对应请求中的 `id`

`result`可以是对象、数组、字符串、布尔值、数字，也可以是`null`。

示例：

```json
{
  "jsonrpc": "2.0",
  "result": true,
  "id": 101
}
```



## 2、错误响应

如果调用失败，服务端会返回`error`字段。

示例：

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32601,
    "message": "Method not found"
  },
  "id": 100
}
```

其中：

- `code`是错误码
- `message`是错误说明
- `data`可以携带额外错误信息

带`data`的示例：

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "field": "id",
      "reason": "expected number"
    }
  },
  "id": 100
}
```

`result`和`error`不会同时出现。一次调用要么成功返回`result`，要么失败返回`error`。

下面给出了常见的错误码概览：

| 错误码               | message            | 含义               | 常见场景                                                          |
|:-------------------- | ------------------ | ------------------ | ----------------------------------------------------------------- |
| `-32700`             | `Parse error`      | JSON 解析错误      | 请求体不是合法 JSON，例如括号没闭合、字符串引号错误               |
| `-32600`             | `Invalid Request`  | 请求对象不合法     | JSON 是合法的，但不符合 JSON-RPC 请求结构，比如 `method` 类型不对 |
| `-32601`             | `Method not found` | 方法不存在         | 请求的 `method` 没有被服务端注册或不可用                          |
| `-32602`             | `Invalid params`   | 参数不合法         | `params` 类型不对、缺少必要参数、参数值不符合要求                 |
| `-32603`             | `Internal error`   | 内部错误           | 服务端执行方法时发生未预期错误                                    |
| `-32000` 到 `-32099` | `Server error`     | 服务端错误预留区间 | 服务端实现可以在这个范围内定义自己的 server error                 |



# 五、JSON-RPC常见错误码

JSON-RPC 2.0 定义了一些常见错误码。

## 1、Parse error

错误码：

```text
-32700
```

表示服务端收到的 JSON 本身无法解析。

例如请求体不是合法 JSON：

```json
{
  "jsonrpc": "2.0",
  "method": "user.get",
```

这种情况下，问题出在 JSON 语法层面，服务端甚至还没进入具体方法调用逻辑。


## 2、Invalid Request

错误码：

```text
-32600
```

表示 JSON 是合法的，但不是合法的 JSON-RPC 请求对象。

例如缺少必要字段：

```json
{
  "method": "user.get"
}
```

这里缺少 `jsonrpc` 等协议字段，服务端可能认为它不是一个规范的 JSON-RPC 请求。


## 3、Method not found

错误码：

```text
-32601
```

表示请求的方法不存在。

示例：

```json
{
  "jsonrpc": "2.0",
  "method": "user.unknown",
  "id": 100
}
```

服务端没有注册 `user.unknown` 这个方法，就会返回类似错误。


## 4、Invalid params

错误码：

```text
-32602
```

表示方法存在，但参数不合法。

例如服务端期望`id`是数字：

```json
{
  "jsonrpc": "2.0",
  "method": "user.get",
  "params": {
    "id": "abc"
  },
  "id": 100
}
```

这里`id`传了字符串，导致`Invalid params`。


## 5、Internal error

错误码：

```text
-32603
```

表示服务端内部错误。

例如服务端执行方法时发生了数据库异常、运行时错误或其他未预期问题。


# 六、Notification通知请求

`JSON-RPC`中，如果请求不包含`id`，通常表示这是一个`notification`，也就是通知请求。

示例：

```json
{
  "jsonrpc": "2.0",
  "method": "log.write",
  "params": {
    "message": "user login"
  }
}
```

通知请求的特点是：

> 客户端只发送调用，不要求服务端返回响应

因为没有`id`，服务端即使处理完成，也没有必要返回对应响应。

这种模式适合**日志、事件上报、状态通知**等场景。

但如果调用结果很重要，就不应该使用 notification。因为客户端无法知道调用是否成功。


# 七、批量请求

JSON-RPC支持批量请求，也就是一次发送多个请求对象。

示例：

```json
[
  {
    "jsonrpc": "2.0",
    "method": "user.get",
    "params": {
	  "id": 1
    },
    "id": 100
  },
  {
    "jsonrpc": "2.0",
    "method": "user.get",
    "params": {
	  "id": 2
    },
    "id": 101  
  }
]
```

服务端可以返回一个响应数组：

```json
[
  {
    "jsonrpc": "2.0",
    "result": {
	  "id": 1,
	  "name": "Alice"
    },
    "id": 100
  },
  {
    "jsonrpc": "2.0",
    "result": {
	  "id": 2,
	  "name": "Bob"
    },
    "id": 101  
  }
]
```

需要注意的是，批量响应的顺序不一定必须和请求顺序一致。因此，客户端应该通过`id`匹配请求和响应，而不是依赖数组顺序。

# 八、JSON-RPC调用流程

一次典型的 JSON-RPC 调用可以理解为：

![[Pasted image 20260518155917.png|500]]


JSON-RPC 的重点不在于传输层，而在于消息格式。无论底层走 HTTP 还是 WebSocket，只要双方遵守 JSON-RPC 请求和响应结构，就可以完成远程调用。