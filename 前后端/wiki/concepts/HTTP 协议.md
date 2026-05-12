---
title: HTTP 协议
date: 2026-05-13
tags: [http, api, frontend, backend, architecture]
source_count: 1
---

# HTTP 协议

## 基本概念

HTTP（Hyper Text Transfer Protocol，超文本传输协议）是一种运行在**应用层**的网络协议，用于客户端与服务器之间传输资源。

传输的资源包括：

| 类型 | 示例 |
|------|------|
| 网页相关 | HTML、CSS、JavaScript |
| 媒体 | 图片、音频、视频 |
| 数据 | JSON、XML、API 接口返回 |
| 文件 | 文档、压缩包、下载文件 |

## 核心模型

### 客户端-服务器模型

**客户端主动发起请求，服务器接收请求、处理请求并返回响应**。

```text
浏览器 / 客户端                         Web 服务器
     │                                      │
     │  发送 HTTP 请求                      │
     │ ───────────────────────────────────▶ │
     │                                      │
     │  返回 HTTP 响应                      │
     │ ◀─────────────────────────────────── │
     │                                      │
     │  浏览器解析响应内容并展示页面          │
```

> 客户端不一定是浏览器，服务器也不一定是传统意义上的网站服务器。

### 请求-响应模型

HTTP 最核心的交互模式是**请求-响应**模型。客户端发出**请求**，服务器返回**响应**。

请求示例：

```http
GET /index.html HTTP/1.1
Host: example.com
```

响应示例：

```http
HTTP/1.1 200 OK
Content-Type: text/html

<html>
  <body>Hello HTTP</body>
</html>
```

### 面向资源设计

HTTP 围绕**资源**设计，而非远程函数调用：

- **URL** 标识资源：`/users/1`、`/articles/100`
- **HTTP 方法** 表示操作：

```text
GET    /users/1       获取用户
POST   /users         创建用户
PUT    /users/1       整体更新用户
PATCH  /users/1       局部更新用户
DELETE /users/1       删除用户
```

- **状态码** 表示结果
- **Header** 表示附加信息
- **Body** 表示具体数据

### 协议栈定位

HTTP 位于应用层，不直接负责底层数据传输：

- HTTP/1.1、HTTP/2 建立在 **TCP** 之上
- HTTPS 在 HTTP 和 TCP 之间增加 **TLS** 层，用于加密、完整性校验和身份验证
- HTTP/3 基于 **QUIC**，QUIC 运行在 UDP 之上但实现了可靠传输、加密和拥塞控制

![[Pasted image 20260512214427.png|200]]
![[Pasted image 20260512215314.png|200]]
![[Pasted image 20260512215555.png|200]]

## 基本性质

### 1. 简单易读

HTTP/1.1 的请求和响应报文具有较强的文本可读性：

```http
GET / HTTP/1.1
Host: example.com
Accept: text/html
```

### 2. 灵活

通过 `Content-Type` 传输各种类型的数据：

| Content-Type | 说明 |
|--------------|------|
| `text/html` | HTML 文档 |
| `application/json` | JSON 数据 |
| `image/png` | PNG 图片 |
| `multipart/form-data` | 表单和文件上传 |

### 3. 可扩展

通过 Header 扩展能力：

```http
Cache-Control: max-age=3600      # 缓存控制
Authorization: Bearer token123   # 认证信息
Set-Cookie: session_id=abc123    # Cookie
```

### 4. 无状态

HTTP 本身不会自动记住前一次请求的信息：

```text
请求 1：POST /login
请求 2：GET /profile
```

协议本身不知道这两个请求是否来自同一用户。Web 应用借助 **Cookie / Session / Token** 建立有状态会话。

### 5. 依赖可靠传输

传统 HTTP 依赖 TCP 的可靠传输。HTTP/3 依赖 QUIC（基于 UDP 但实现可靠传输）。

> 底层传输应能可靠交付 HTTP 消息，或在失败时明确报告错误。

## 应用场景

- **前端**：浏览器加载资源、`fetch`/`axios` 请求接口、处理 Cookie/跨域/缓存、分析 DevTools Network
- **后端**：编写 HTTP API、接收请求参数、返回 JSON、处理状态码、认证鉴权、部署到 Nginx/网关
- **其他**：移动端通信、爬虫、云服务、AI 接口调用

## 相关页面

- [[HTTP 系统组成]] — 客户端、服务器与代理的详细说明
- [[HTTP 请求流程]] — URL 解析到客户端解析的完整过程
- [[HTTP 基础概述]] — 本文素材的原始摘要
