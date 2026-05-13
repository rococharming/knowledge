---
title: HTTP 请求流程
date: 2026-05-13
tags: [http, frontend, backend, devops]
source_count: 1
---

# HTTP 请求流程

一次完整的 HTTP 访问经历 7 个阶段，以访问 `https://www.example.com/articles/1` 为例。

## 1. URL 解析

浏览器解析 URL 的各个组成部分：

```text
https://www.example.com/articles/1
├── 协议: https
├── 主机: www.example.com
├── 端口: 443（HTTPS 默认）
└── 路径: /articles/1
```

默认端口：

- HTTP：80
- HTTPS：443

**URL 是客户端定位资源的重要方式**。

## 2. DNS 解析

将域名解析为 IP 地址：

```text
www.example.com → 93.184.216.34
```

域名是给人看的地址，IP 是给网络通信用的地址。

浏览器或系统缓存命中时直接使用；否则向 DNS 服务器查询。

## 3. 连接建立

| 协议 | 底层连接 |
|------|---------|
| HTTP/1.1、HTTP/2 | TCP 连接 |
| HTTPS | TCP + TLS 握手 |
| HTTP/3 | QUIC（基于 UDP） |

![[Pasted image 20260513003914.png]]

## 4. HTTP 请求发送

连接建立后，浏览器构造并发送请求：

```http
GET /articles/1 HTTP/1.1
Host: www.example.com
Accept: text/html
User-Agent: Mozilla/5.0
```

## 5. 服务器处理请求

服务器根据请求内容处理：

- **静态资源**（如 `/logo.png`、`style.css`）：直接从文件系统或缓存读取
- **动态接口**（如 `/api/users/1`）：执行业务代码，查询数据库，返回 JSON
- **页面请求**（如 `/articles/1`）：查询数据库，生成 HTML 或 JSON

## 6. HTTP 响应返回

服务器返回响应：

```http
HTTP/1.1 200 OK
Content-Type: text/html
Cache-Control: max-age=600

<html>
  <body>文章内容</body>
</html>
```

## 7. 客户端解析响应

浏览器解析响应内容：

- 响应体为 HTML 时，解析页面
- HTML 中引用的其他资源会触发更多请求

```html
<link rel="stylesheet" href="/style.css">
<script src="/main.js"></script>
<img src="/logo.png">
```

浏览器会继续请求这些资源：

```text
浏览器 / 客户端                         Web 服务器
     │                                      │
     │  GET /style.css                      │
     │ ───────────────────────────────────▶ │
     │  返回 CSS 文件                       │
     │ ◀─────────────────────────────────── │
     │                                      │
     │  GET /main.js                        │
     │ ───────────────────────────────────▶ │
     │  返回 JavaScript 文件                │
     │ ◀─────────────────────────────────── │
     │                                      │
     │  GET /logo.png                       │
     │ ───────────────────────────────────▶ │
     │  返回图片资源                        │
     │ ◀─────────────────────────────────── │
```

> 打开一个网页通常不是一次 HTTP 请求完成的，而是**多个请求共同完成**。浏览器 DevTools 的 Network 面板中经常能看到几十个甚至上百个请求。

## 相关页面

- [[HTTP 协议]] — HTTP 概念、模型与性质
- [[HTTP 系统组成]] — 客户端、服务器与代理
- [[HTTP 基础概述]] — 素材摘要

## 来源

- [[HTTP基础概述]]