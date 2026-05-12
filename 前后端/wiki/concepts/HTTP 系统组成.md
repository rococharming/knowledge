---
title: HTTP 系统组成
date: 2026-05-13
tags: [http, architecture, frontend, backend]
source_count: 1
---

# HTTP 系统组成

HTTP 通信链路由客户端、服务器以及两者之间的中间实体组成。

## 客户端

客户端是发起 HTTP 请求的一方。

常见客户端：

- 浏览器（Chrome、Edge、Firefox、Safari）
- 命令行工具（`curl`）
- API 测试工具（Postman）
- 前端 JavaScript 程序（`fetch`、`axios`）
- 后端服务（微服务间调用）
- 爬虫程序、自动化测试脚本

示例：

```shell
curl https://example.com
```

```javascript
fetch('/api/users')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 用户代理（User Agent）

**代表用户发起 HTTP 请求的客户端程序**。

HTTP 请求中的 `User-Agent` 头描述客户端身份：

```http
User-Agent: Mozilla/5.0
```

> `User-Agent` 可被伪造，不应作为严格的安全凭证。

## 服务器

服务器是接收请求并返回响应的一方，负责提供资源或执行业务逻辑。

资源类型：

- **静态文件**：HTML、CSS、JavaScript、图片、字体、视频
- **动态生成结果**：数据库查询结果、Token、JSON 响应、AI 生成结果

实际系统中，服务器可能是一台机器或多台机器组成的集群：

![[Pasted image 20260512222206.png|500]]

请求先到**负载均衡器**，再转发到后端服务器。后端服务器通常连接共享资源（数据库、缓存、消息队列）。

## Web 服务器与应用服务器

| 类型 | 职责 | 示例 |
|------|------|------|
| **Web 服务器** | 处理 HTTP 层面请求和静态资源 | Nginx、Apache、Caddy |
| **应用服务器** | 运行业务代码 | Node.js、Spring Boot、Rust Web 服务 |

![[Pasted image 20260512223046.png]]

## 代理

代理是位于客户端和服务器之间的中间实体，负责转发、处理或控制 HTTP 消息。

### 常见代理类型

- **CDN**：缓存代理，缓存图片等静态资源，命中时直接返回
- **企业代理**：控制员工访问外部网络
- **API 网关、Nginx 反向代理**：后端系统中的中间层

![[Pasted image 20260512233510.png|500]]

### 正向代理与反向代理

| 类型 | 位置 | 代理对象 |
|------|------|---------|
| **正向代理** | 客户端一侧 | 代理客户端请求 |
| **反向代理** | 服务器一侧 | 代理服务器响应 |

正向代理请求路径：

![[Pasted image 20260512234551.png|400]]

反向代理请求路径：

![[Pasted image 20260512234633.png|400]]

反向代理示例：用户访问 `https://api.example.com/users/1`，真实后端可能是 `https://10.0.0.12:8080/users/1`。用户无需知道真实地址。

## 相关页面

- [[HTTP 协议]] — HTTP 概念、模型与性质
- [[HTTP 请求流程]] — 完整访问过程
- [[HTTP 基础概述]] — 素材摘要