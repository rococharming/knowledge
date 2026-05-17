---
title: 浏览器 Network 面板
date: 2026-05-17
tags: [http, frontend, debugging]
source_count: 1
---

# 浏览器 Network 面板

浏览器开发者工具的 Network 面板可以直接观察页面发出的 HTTP 请求和接收的 HTTP 响应，是学习 HTTP 时非常重要的实践工具。

## 打开 Network 面板

以 Chrome 为例：

- 右键页面空白处或元素，点击**检查**
- macOS 快捷键 `Command + Option + I`
- Windows/Linux 快捷键 `Ctrl + Shift + I`
- 按 `F12`

打开开发者工具后，切换到 **Network** 面板。

## 请求列表

刷新页面后，浏览器发出的请求会显示在请求列表中。列表中通常可以看到：

| 内容 | 说明 |
|---|---|
| Name | 请求的资源名称或接口名称 |
| Status | 响应状态码，如 `200`、`304`、`404`、`500` |
| Type | 资源类型，如 `document`、`stylesheet`、`script`、`font` |
| Initiator | 触发这个请求的来源 |
| Size | 资源传输大小，可能显示 `(memory cache)` 等缓存信息 |
| Time | 请求耗时 |

## 资源类型筛选

请求列表上方有筛选按钮，常用筛选项：

| 筛选项 | 作用 |
|---|---|
| `All` | 显示所有请求 |
| `Fetch/XHR` | 只看接口请求，常用于排查前后端 API |
| `Doc` | 只看文档请求，如页面 HTML |
| `CSS` | 只看样式文件 |
| `JS` | 只看 JavaScript 文件 |
| `Font` | 只看字体文件 |
| `Img` | 只看图片资源 |
| `Media` | 只看音频、视频等媒体资源 |
| `Socket` | 只看 WebSocket 连接 |
| `Wasm` | 只看 WebAssembly 资源 |
| `Other` | 其他类型请求 |

排查接口问题时最常用 `Fetch/XHR`；排查页面加载资源时常看 `Doc`、`CSS`、`JS`、`Img`、`Font`。

## 请求详情标签

点击请求列表中的某个请求后，会显示该请求的详情：

| 标签 | 作用 |
|---|---|
| `Headers` | 查看请求 URL、请求方法、状态码、响应头、请求头 |
| `Preview` | 以更友好的形式预览响应内容，如格式化 JSON 或预览图片 |
| `Response` | 查看服务器返回的原始响应体 |
| `Initiator` | 查看这个请求是由谁触发的 |
| `Timing` | 查看请求耗时细节，如排队、连接、等待响应、下载等阶段 |
| `Cookies` | 查看这次请求和响应涉及的 Cookie |

## 来源

- [[HTTP请求与响应]]
