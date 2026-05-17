---
title: HTTP 请求
date: 2026-05-17
tags: [http, api, frontend, backend]
source_count: 1
---

# HTTP 请求

HTTP 请求是客户端向服务器发送的消息，用于请求资源或触发操作。

## 报文结构

请求报文由四部分组成：

```text
请求行
请求头
空行
请求体
```

空行用于分隔 Header 和 Body。如果没有请求体，Header 结束后仍然需要一个空行（连续的 `\r\n`）。

## 请求行

请求行位于第一行，格式为：

```text
请求方法  请求路径  HTTP版本
```

例如：

```http
GET /articles/1 HTTP/1.1
```

| 部分 | 示例 | 作用 |
|---|---|---|
| 请求方法 | `GET` | 表示客户端想执行的操作 |
| 请求路径 | `/articles/1` | 表示要访问的资源位置 |
| HTTP 版本 | `HTTP/1.1` | 表示使用的协议版本 |

请求路径通常只包含 `path` 和 `query`，不包含协议和域名。目标主机放在 `Host` 请求头中。

## 请求方法

请求方法用于说明客户端希望对资源执行什么操作，是一种语义约定而非强制约束。

| 方法 | 常见含义 |
|---|---|
| `GET` | 获取资源 |
| `POST` | 提交数据，常用于创建资源或触发处理 |
| `PUT` | 使用完整内容替换资源 |
| `PATCH` | 局部修改资源 |
| `DELETE` | 删除资源 |
| `HEAD` | 类似 `GET`，但只返回响应头 |
| `OPTIONS` | 查询服务器或资源支持的通信选项 |

### GET 请求

`GET` 用于获取资源，参数通常放在 URL 查询字符串中。`GET` 请求通常不应该修改服务器上的资源。

```http
GET /search?keyword=rust&page=1 HTTP/1.1
Host: example.com
```

### POST 请求

`POST` 常用于提交数据，如表单、登录、创建资源等。

```http
POST /api/login HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "username": "Tom",
  "password": "123456"
}
```

### PUT 请求

`PUT` 通常用于整体更新资源，请求体包含资源的完整内容。

### PATCH 请求

`PATCH` 通常用于局部更新资源，请求体只包含需要修改的字段。

### DELETE 请求

`DELETE` 用于删除资源。

## 请求头

请求头用于携带请求的附加信息。

| 请求头 | 作用 |
|---|---|
| `Host` | 请求的目标主机 |
| `User-Agent` | 客户端信息 |
| `Accept` | 客户端希望接收的响应类型 |
| `Content-Type` | 请求体的数据类型 |
| `Authorization` | 认证信息 |
| `Cookie` | 客户端携带的 Cookie |
| `Origin` | 请求来源，常用于跨域 |

### 常见 Content-Type

| Content-Type | 常见用途 |
|---|---|
| `application/json` | JSON 数据，常用于前后端接口 |
| `application/x-www-form-urlencoded` | 传统表单提交 |
| `multipart/form-data` | 文件上传，也可同时提交普通字段 |
| `text/plain` | 纯文本 |
| `text/html` | HTML 文档 |
| `application/octet-stream` | 通用二进制数据 |

## 请求体

请求体用于携带客户端提交给服务器的数据。`GET` 请求通常没有请求体，`POST`、`PUT`、`PATCH` 请求常常会携带请求体。

请求体的格式需要使用 `Content-Type` 告诉服务器，否则服务器可能不知道如何解析。

## 来源

- [[HTTP请求与响应]]
