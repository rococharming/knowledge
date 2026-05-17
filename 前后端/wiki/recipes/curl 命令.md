---
title: curl 命令
date: 2026-05-17
tags: [http, api, devops, backend]
source_count: 1
---

# curl 命令

`curl` 是一个常用的命令行 HTTP 客户端工具，可以直接控制请求 URL、请求方法、请求头、请求体、上传文件、是否跟随重定向等内容。

## 基础用法

最简单的用法是直接请求一个 URL：

```shell
curl https://example.com
```

这会发送 `GET` 请求，并把响应体输出到终端。

## 发送 GET 请求

`GET` 是 curl 的默认方法，通常不需要显式写 `-X GET`。

```shell
curl https://httpbin.org/get
```

带查询参数时建议用双引号包裹 URL（`&` 在 Shell 中有特殊含义）：

```shell
curl "https://httpbin.org/get?name=Tom&age=26"
```

## 查看响应头

使用 `-i` 同时查看响应头和响应体：

```shell
curl -i https://example.com
```

使用 `-I` 只查看响应头（发送 `HEAD` 请求）：

```shell
curl -I https://example.com
```

## 指定请求方法

使用 `-X` 指定请求方法：

```shell
curl -X DELETE https://httpbin.org/delete
curl -X PUT https://httpbin.org/put
```

> 很多时候 curl 会根据选项自动选择方法。例如使用 `-d` 提交数据时，curl 默认会使用 `POST`，因此普通 POST 请求不一定需要写 `-X POST`。

## 添加请求头

使用 `-H` 添加请求头：

```shell
curl https://httpbin.org/get \
  -H "Accept: application/json"
```

多个请求头可以写多个 `-H`：

```shell
curl https://httpbin.org/get \
  -H "Accept: application/json" \
  -H "User-Agent: my-curl-client"
```

## 发送请求体

### 传统表单数据

使用 `-d` 发送表单数据：

```shell
curl https://httpbin.org/post \
  -d "username=Tom&password=123456"
```

使用 `-d` 时，curl 默认发送 `POST` 请求，Content-Type 为 `application/x-www-form-urlencoded`。

### JSON 数据

发送 JSON 时需要显式设置 `Content-Type`：

```shell
curl https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name":"Tom","age":25}'
```

JSON 较长时可以放到文件中，使用 `@` 读取：

```shell
curl https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d @user.json
```

### 原始二进制数据

使用 `--data-binary` 发送文件的原始字节：

```shell
curl https://httpbin.org/post \
  -H "Content-Type: application/octet-stream" \
  --data-binary @avatar.png
```

### 上传文件（multipart/form-data）

使用 `-F` 模拟浏览器表单上传文件：

```shell
curl https://httpbin.org/post \
  -F "username=Tom" \
  -F "avatar=@avatar.png"
```

使用 `-F` 时，curl 会自动使用 `multipart/form-data` 并生成 boundary。一般不要手动写 `Content-Type: multipart/form-data`，容易漏掉 boundary 导致服务器无法解析。

## 其他常用选项

| 选项 | 作用 |
|---|---|
| `-v` | 查看详细请求过程，`>` 开头是请求内容，`<` 开头是响应内容 |
| `-L` | 跟随重定向（301、302 等） |
| `-o <文件>` | 将响应保存到指定文件 |
| `-O` | 使用远程文件名保存 |

例如跟随重定向：

```shell
curl -L https://httpbin.org/redirect/1
```

保存响应到文件：

```shell
curl https://example.com -o example.html
curl -O https://example.com/files/report.pdf
```

## 来源

- [[HTTP请求与响应]]
