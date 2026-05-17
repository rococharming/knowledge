---
title: HTTP 响应
date: 2026-05-17
tags: [http, api, frontend, backend]
source_count: 1
---

# HTTP 响应

HTTP 响应是服务器对客户端请求的处理结果，包含状态信息和返回内容。

## 报文结构

响应报文由四部分组成：

```text
状态行
响应头
空行
响应体
```

空行用于分隔 Header 和 Body。

## 状态行

状态行位于响应的第一行，格式为：

```text
HTTP协议 状态码 原因短语
```

例如：

```http
HTTP/1.1 200 OK
```

| 部分 | 示例 | 作用 |
|---|---|---|
| HTTP 版本 | `HTTP/1.1` | 表示响应使用的协议版本 |
| 状态码 | `200` | 表示请求处理结果 |
| 原因短语 | `OK` | 对状态码的简短说明 |

在实际开发中，最重要的是状态码。原因短语只是辅助说明。

## 状态码

状态码是三位数字，第一位表示大类：

| 范围 | 类型 | 含义 |
|---|---|---|
| `1xx` | 信息 | 请求已收到，继续处理 |
| `2xx` | 成功 | 请求成功处理 |
| `3xx` | 重定向 | 需要进一步操作 |
| `4xx` | 客户端错误 | 请求有问题 |
| `5xx` | 服务端错误 | 服务器处理出错 |

### 常见状态码

| 状态码 | 含义 |
|---|---|
| `200 OK` | 请求成功 |
| `201 Created` | 资源创建成功 |
| `204 No Content` | 请求成功，但没有响应体 |
| `301 Moved Permanently` | 永久重定向 |
| `302 Found` | 临时重定向 |
| `304 Not Modified` | 资源未修改，可以使用缓存 |
| `400 Bad Request` | 请求格式错误 |
| `401 Unauthorized` | 未认证 |
| `403 Forbidden` | 无权限 |
| `404 Not Found` | 资源不存在 |
| `405 Method Not Allowed` | 请求方法不允许 |
| `500 Internal Server Error` | 服务器内部错误 |
| `502 Bad Gateway` | 网关错误 |
| `503 Service Unavailable` | 服务暂时不可用 |
| `504 Gateway Timeout` | 网关超时 |

`401` 和 `403` 容易混淆：`401` 偏向于**还没有通过认证**，`403` 偏向于**已经知道你是谁，但没有权限**。

## 响应头

响应头用于描述服务器返回内容的附加信息。

| 响应头 | 作用 |
|---|---|
| `Content-Type` | 响应体的数据类型 |
| `Content-Length` | 响应体长度 |
| `Set-Cookie` | 让客户端保存 Cookie |
| `Cache-Control` | 控制缓存策略 |
| `Location` | 重定向目标地址 |
| `ETag` | 资源版本标识 |
| `Last-Modified` | 资源最后修改时间 |
| `Access-Control-Allow-Origin` | 跨域访问控制 |

## 响应体

响应体是服务器返回的实际内容。根据 `Content-Type` 的不同，响应体可以是 HTML、JSON、图片、文件等二进制内容。

不是所有响应都有响应体。例如 `204 No Content` 表示请求成功，但响应中没有主体内容。

## 来源

- [[HTTP请求与响应]]
