# 一、HTTP消息概述

## 1、请求与响应

HTTP 通信是通过请求与响应完成的。

客户端发送的消息叫**请求**，服务端发送的消息叫**响应**。

![[Pasted image 20260512210519.png|300]]

一次最基本的HTTP通信可以理解为：

1. 客户端向服务器发送一个HTTP请求
2. 服务器接收请求并进行处理
3. 服务器返回一个HTTP响应
4. 客户端读取响应内容并继续处理

例如浏览器访问一个网页，本质上就是浏览器向服务器发送 HTTP 请求，服务器再返回 HTML、CSS、JavaScript、图片或接口数据等响应内容。

##  2、HTTP消息的基本组成

HTTP 请求和响应都属于 HTTP 消息。

它们结构不同，但整体思路类似：前面是描述信息，后面是实际内容。

一个HTTP请求通常包含：

- 请求行
- 请求头
- 空行
- 请求体

一个HTTP响应通常包含：

- 状态行
- 响应头
- 空行
- 响应体

其中，**空行用于分隔 Header 和 Body**。空行之前是元信息，空行之后才是实际传输的主体内容。


## 3、HTTP/1.1报文与HTTP/2、HTTP/3语义

学习 HTTP 请求与响应时，通常会先从 HTTP/1.1 的文本报文开始。

例如：

```http
GET /index.html HTTP/1.1
Host: example.com
```

这种格式比较直观，适合用来理解 HTTP 的基本结构。

到了 HTTP/2 和 HTTP/3，底层传输格式不再是这种简单的文本报文，而是使用二进制帧等机制传输数据。但是 HTTP 的核心语义没有变，仍然有请求方法、路径、状态码、Header、Body 等概念。

因此，用 HTTP/1.1 的报文结构理解请求和响应，是学习 HTTP 的合适入口。

# 二、HTTP请求

## 1、请求报文结构

HTTP请求报文通常由四部分组成：

```text
请求行
请求头
空行
请求体
```

例如：

```http
POST /api/login HTTP/1.1
Host: example.com
Content-Type: application/json
Authorization: Bearer token123

{
  "username": "Tom",
  "password": "123456"
}
```

其中：

- `POST /api/login HTTP/1.1`是请求行；
- `Host`、`Content-Type`、`Authorization` 是请求头；
- Header 和 Body 之间有一个空行；
- JSON 数据是请求体。

请求行说明“要做什么”，请求头补充说明“如何处理这个请求”，请求体则携带提交给服务器的数据。

如果没有请求体，那么Header结束后仍然需要一个空行，也就是连续的CRLF：

```text
请求行\r\n
请求头\r\n
请求头\r\n
\r\n
```


## 2、请求行

请求行位于 HTTP 请求的第一行。

它通常包含三部分：

```text
请求方法  请求路径  HTTP版本
```

例如：

```http
GET /articles/1 HTTP/1.1
```

表示客户端希望使用`GET`方法，请求服务器上的`/article/1`资源，使用的协议版本是 `HTTP/1.1`。

请求行中三部分各有作用：

|部分|示例|作用|
|---|---|---|
|请求方法|`GET`|表示客户端想执行的操作|
|请求路径|`/articles/1`|表示要访问的资源位置|
|HTTP 版本|`HTTP/1.1`|表示使用的 HTTP 协议版本|
请求路径通常只包含`path`和`query`，不包含协议和域名。

例如访问：

```text
https://example.com/articles/1?page=2
```

请求行中通常是：

```http
GET articles/1?page=2 HTTP/1.1
```

目标主机 `example.com` 会放在 `Host` 请求头中。

## 3、请求方法

### （1）常见请求方法

请求方法用于说明客户端希望对资源执行什么操作。

常见方法如下：

| 方法        | 常见含义              |
| --------- | ----------------- |
| `GET`     | 获取资源              |
| `POST`    | 提交数据，常用于创建资源或触发处理 |
| `PUT`     | 使用完整内容替换资源        |
| `PATCH`   | 局部修改资源            |
| `DELETE`  | 删除资源              |
| `HEAD`    | 类似`GET`，但只返回响应头   |
| `OPTIONS` | 查询服务器或资源支持的通信选项   |

例如一个用户资源接口可以设计成：

```text
GET /users/1         获取用户
POST /users          创建用户
PUT /users/1         整体更新用户
PATCH /users/1       局部更新用户
DELETE /users/1      删除用户
```

请求方法不是强制服务器必须怎么做，而是一种语义约定。服务器最终如何处理请求，取决于后端代码的实现，但合理使用方法可以让接口语义更清晰。

### （2）GET请求

`GET`用于获取资源。

例如：

```http
GET /articles/1 HTTP/1.1  
Host: example.com
```

`GET`请求通常用于查询数据。**它的参数通常放在 URL 查询字符串中**。

例如：

```http
GET /search?keyword=rust&page=1 HTTP/1.1  
Host: example.com
```

这里的 `keyword=rust&page=1` 就是查询参数。

`GET` 请求通常不应该修改服务器上的资源。比如获取文章列表、查看用户信息、加载图片、访问网页，都适合使用 GET。

### （3）POST请求

`POST`常用于提交数据。

例如提交JSON数据：

```http
POST /api/login HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "username": "Tom",
  "password": "123456"
}
```

`POST`请求常见于：

- 提交表单
- 用户登录
- 创建资源
- 上传数据
- 调用需要请求体的接口                  

### （4）PUT请求

`PUT`通常用于整体更新资源。

例如：

```http
PUT /users/1 HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "name": "Alice",  
  "age": 20,  
  "email": "alice@example.com"
}
```

### （5）PATCH请求

`PATCH`通常用于局部更新资源。

例如：

```http
PATCH /users/1 HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "age": 21
}
```

### （6）DELETE请求

`DELETE`用于删除资源。

```http
DELETE /users/1 HTTP/1.1  
Host: example.com
```

## 4、请求头

请求头（Header）用于携带请求的附加信息。

例如：

```http
Host: example.com
Accept: application/json
Content-Type: application/json
Authorization: Bearer token123
```

常见请求头包括：

| 请求头             | 作用            |
| --------------- | ------------- |
| `Host`          | 请求的目标主机       |
| `User-Agent`    | 客户端信息         |
| `Accept`        | 客户端希望接收的响应类型  |
| `Content-Type`  | 请求体的数据类型      |
| `Authorization` | 认证信息          |
| `Cookie`        | 客户端携带的 Cookie |
| `Origin`        | 请求来源，常用于跨域    |

例如：

```http
Accept: application/json
```

表示客户端希望服务器返回 JSON。

```http
Content-Type: application/json
```

表示请求体是 JSON。

```http
Authorization: Bearer token123
```

表示客户端携带了认证令牌。

常见的`Content-Type`：

|Content-Type|常见用途|
|---|---|
|`application/json`|JSON 数据，常用于前后端接口|
|`application/x-www-form-urlencoded`|传统表单提交|
|`multipart/form-data`|文件上传，也可同时提交普通字段|
|`text/plain`|纯文本|
|`text/html`|HTML 文档|
|`application/octet-stream`|通用二进制数据|

## 5、请求体

请求体用于携带客户端提交给服务器的数据。

不是所有的请求都有请求体。`GET`请求通常没有请求体，`POST`、`PUT`、`PATCH`请求常常会携带请求体。

提交 JSON 数据时，请求体可能是：

```json
{  
  "name": "Alice",  
  "age": 18  
}
```

提交传统表单时，请求体可能是：

```text
username=tom&password=123456
```

上传文件时，请求体通常会使用 `multipart/form-data` 格式。

请求体的格式需要使用`Content-Type`告诉服务器，否则服务器可能不知道应该如何解析这段数据。

# 三、HTTP响应

## 1、响应报文结构

HTTP响应报文通常由四部分组成：

```text
状态行
响应头
空行
响应体
```

例如：

```http
HTTP/1.1 200 OK
Content-Type: application/json  
Set-Cookie: session_id=abc123

{  
  "message": "login success"  
}
```

其中：

- `HTTP/1.1 200 OK` 是状态行；
- `Content-Type` 和 `Set-Cookie` 是响应头；
- Header 和 Body 之间有一个空行；
- JSON 数据是响应体。

状态行说明“处理结果”，响应头补充说明“如何理解这个响应”，响应体则是服务器返回的实际内容。

## 2、状态行

状态行位于HTTP响应的第一行。

它通常包含三部分：

```text
HTTP协议 状态码 原因短语
```

例如：

```http
HTTP/1.1 200 OK
```

表示服务器使用 `HTTP/1.1` 返回响应，状态码是 `200`，原因短语是 `OK`。

| 部分      | 示例         | 作用          |
| ------- | ---------- | ----------- |
| HTTP 版本 | `HTTP/1.1` | 表示响应使用的协议版本 |
| 状态码     | `200`      | 表示请求处理结果    |
| 原因短语    | `OK`       | 对状态码的简短说明   |
在实际开发中，最重要的是状态码。原因短语只是辅助说明。

## 3、状态码

状态码用于表示服务器对请求的处理结果。

状态码是三位数字，第一位表示大类。

| 状态码范围 | 类型    | 含义         |
| ----- | ----- | ---------- |
| `1xx` | 信息    | 请求已收到，继续处理 |
| `2xx` | 成功    | 请求成功处理     |
| `3xx` | 重定向   | 需要进一步操作    |
| `4xx` | 客户端错误 | 请求有问题      |
| `5xx` | 服务端错误 | 服务器处理出错    |
日常开发中最常见的是 `2xx`、`3xx`、`4xx`、`5xx`。

常见状态码如下：

| 状态码                         | 含义           |
| --------------------------- | ------------ |
| `200 OK`                    | 请求成功         |
| `201 Created`               | 资源创建成功       |
| `204 No Content`            | 请求成功，但没有响应体  |
| `301 Moved Permanently`     | 永久重定向        |
| `302 Found`                 | 临时重定向        |
| `304 Not Modified`          | 资源未修改，可以使用缓存 |
| `400 Bad Request`           | 请求格式错误       |
| `401 Unauthorized`          | 未认证          |
| `403 Forbidden`             | 无权限          |
| `404 Not Found`             | 资源不存在        |
| `405 Method Not Allowed`    | 请求方法不允许      |
| `500 Internal Server Error` | 服务器内部错误      |
| `502 Bad Gateway`           | 网关错误         |
| `503 Service Unavailable`   | 服务暂时不可用      |
| `504 Gateway Timeout`       | 网关超时         |
其中，`401`和`403`和容易混淆。`401`更偏向于**还没有通过认证**，`403`更偏向于**已经知道你是谁，但没有权限**。

## 4、响应头

响应头用于描述服务器返回内容的附加信息。

例如：

```http
Content-Type: application/json
Cache-Control: max-age=3600
Set-Cookie: session_id=abc123
```

常见响应头包括：

|响应头|作用|
|---|---|
|`Content-Type`|响应体的数据类型|
|`Content-Length`|响应体长度|
|`Set-Cookie`|让客户端保存 Cookie|
|`Cache-Control`|控制缓存策略|
|`Location`|重定向目标地址|
|`ETag`|资源版本标识|
|`Last-Modified`|资源最后修改时间|
|`Access-Control-Allow-Origin`|跨域访问控制|
例如：

```http
Content-Type: application/json
```

表示响应体是 JSON。

```http
Location: /login
```

常用于重定向，表示客户端应该跳转到 `/login`。

```http
Set-Cookie: session_id=abc123
```

表示服务器要求浏览器保存 Cookie。

## 5、响应体

响应体是服务器返回的实际内容。

例如返回 HTML：

```http
HTTP/1.1 200 OK
Content-Type: text/html

<html>
  <body>Hello HTTP</body>
</html>
```

返回 JSON：

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "name": "Alice"
}
```

返回图片、文件、音视频时，响应体就是对应的二进制内容。

不是所有响应都有响应体。例如 `204 No Content` 表示请求成功，但响应中没有主体内容。


# 四、请求与响应示例

## 1、获取网页资源

浏览器访问：

```text
https://example.com/index.html
```

可能发送请求：

```http
GET /index.html HTTP/1.1
Host: example.com
Accept: text/html

```

服务器返回响应：

```http
HTTP/1.1 200 OK  
Content-Type: text/html

<html>  
<body>Hello HTTP</body>  
</html>
```

这表示客户端请求 HTML 页面，服务器成功返回 HTML 内容。

## 2、获取 JSON 数据

前端请求用户信息：

```http
GET /api/users/1 HTTP/1.1
Host: example.com
Accept: application/json

```

服务器返回：

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "name": "Alice"
}
```


## 3、提交JSON数据

客户端创建用户：

```http
POST /api/users HTTP/1.1
Host: example.com  
Content-Type: application/json

{
  "name": "Alice",  
  "email": "alice@example.com"
}
```

服务器返回：

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 1,
  "name": "Alice",  
  "email": "alice@example.com"
}
```

这里的 `201 Created` 表示资源创建成功。

## 4、登录请求

客户端提交登录信息：

```http
POST /api/login HTTP/1.1
Host: example.com  
Content-Type: application/json

{
  "username": "tom",  
  "password": "123456"
}
```

服务器验证成功后可能返回：

```http
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: session_id=abc123; HttpOnly; Path=/

{
  "message": "login success"
}
```

其中，`Set-Cookie` 表示服务器让浏览器保存一个 Cookie。后续浏览器请求同一网站时，会自动携带对应 Cookie。

# 五、HTTP请求调试

## 1、浏览器Network面板

### （1）打开Network面板

浏览器 Devtools 的 Network 面板可以用来观察页面发出的 HTTP 请求和接收的 HTTP 响应。学习 HTTP 时，它比单纯看概念更重要，因为它能直接展示真实网页中的请求方法、请求头、请求体、状态码、响应头、响应体。

以 Chrome 浏览器为例，可以通过以下方式打开开发者工具：

- 右键页面空白处或页面元素，点击**检查**
- macOS 快捷键 `Command + Option + I`
- Windows/Linux 快捷键 `Ctrl + Shift + I`
- 按`F12`

打开开发者工具后，切换到 **Network** 面板。

![[Pasted image 20260515002512.png|800]]


### （2）请求列表

刷新页面，浏览器发出的请求就会显示在请求列表中：

![[Pasted image 20260515002624.png]]


请求列表中通常可以看到这些信息：

| 内容        | 说明                                                                    |
| --------- | --------------------------------------------------------------------- |
| Name      | 请求的资源名称或接口名称，例如 `www.deepseek.com`、`.css`、`.js`、`.webp`               |
| Status    | 响应状态码，例如 `200`、`304`、`404`、`500`                                      |
| Type      | 资源类型，例如 `document`、`stylesheet`、`script`、`font`、`binary/octet-stream` |
| Initiator | 触发这个请求的来源，例如 HTML 解析、脚本、某个文件行号                                        |
| Size      | 资源传输大小，可能显示具体大小，也可能显示 `(memory cache)`                                |
| Timeout   | 请求耗时                                                                  |
例如从截图里可以看到：

- `www.deepseek.com` 的 `Status` 是 `304`，`Type` 是 `document`，表示主文档请求命中了协商缓存；
- 多个 `.css` 文件的 `Type` 是 `stylesheet`；
- 多个 `.js` 文件的 `Type` 是 `script`；
- `.woff2` 文件的 `Type` 是 `font`；
- `banner-background.webp` 的 `Type` 显示为 `binary/octet-stream`，说明浏览器把它识别成一段二进制数据流，而不是更具体的图片 MIME 类型。

请求列表上方还有资源类型筛选按钮，例如：

| 筛选项         | 作用                  |
| ----------- | ------------------- |
| `All`       | 显示所有请求              |
| `Fetch/XHR` | 只看接口请求，常用于排查前后端 API |
| `Doc`       | 只看文档请求，例如页面 HTML    |
| `CSS`       | 只看样式文件              |
| `JS`        | 只看 JavaScript 文件    |
| `Font`      | 只看字体文件              |
| `Img`       | 只看图片资源              |
| `Media`     | 只看音频、视频等媒体资源        |
| `Socket`    | 只看 WebSocket 连接     |
| `Wasm`      | 只看 WebAssembly 资源   |
| `Other`     | 其他类型请求              |
排查接口问题时，最常用的是 `Fetch/XHR`；排查页面加载资源时，常会看 `Doc`、`CSS`、`JS`、`Img`、`Font`。


### （3）请求详情标签

点击请求列表中的某一个请求后，会显示该请求的详情。例如：

![[Pasted image 20260515004831.png|800]]

常见标签如下：

| 标签          | 作用                             |
| ----------- | ------------------------------ |
| `Headers`   | 查看请求 URL、请求方法、状态码、响应头、请求头      |
| `Preview`   | 以更友好的形式预览响应内容，例如格式化 JSON 或预览图片 |
| `Response`  | 查看服务器返回的原始响应体                  |
| `Initiator` | 查看这个请求是由谁触发的                   |
| `Timing`    | 查看请求耗时细节，例如排队、连接、等待响应、下载等阶段    |
| `Cookies`   | 查看这次请求和响应涉及的 Cookie            |

## 2、curl命令
### （1）curl基本概念

`curl`是一个常用的**命令行HTTP客户端工具**。通过`curl`，可以直接控制请求URL、请求方法、请求头、请求体、上传文件、是否跟随重定向等内容。

最简单的用法就是直接请求一个URL：

```shell
curl https://example.com
```

这会向 `https://example.com` 发送一个`GET`请求，并把**响应体**输出到终端。

如果请求的是 HTML 页面，终端里通常会看到 HTML 内容；如果请求的是 JSON 接口，终端里通常会看到 JSON 数据。

### （2）发送 GET 请求

`GET`是`curl`请求HTTP URL 的默认方法，所以通常不需要显式写`-X GET`。

例如请求一个公开测试接口：

```shell
curl https://httpbin.org/get
```

这个请求会向 `https://httpbin.org/get` 发送 GET 请求，服务器会返回这次请求的相关信息。

结果：

![[Pasted image 20260515015111.png|600]]

其中：

- `args`表示URL查询参数
- `headers`表示 httpbin 收到的请求头
- `origin`表示 httpbin 看到的请求来源IP
- `url`表示 httpbin 收到的完整请求 URL。

也可以带查询参数：

```shell
curl "https://httpbin.org/get?name=Tom&age=26"
```

![[Pasted image 20260515020439.png|600]]

> 当URL里有&等查询字符，建议加双引号将URL包裹，因为&在Shell里有特殊含义，可能会将URL错误拆分


### （3）查看响应头

默认情况下，`curl` 主要输出响应体。如果想同时看到响应头，可以使用 `-i`。

```shell
curl -i https://example.com
```

输出类似：

```http
HTTP/2 200
content-type: text/html

<!doctype html>
<html>...</html>
```

例如：

```shell
curl -i https://httpbin.org/get
```

> `-i`适合观察状态码、响应头和响应体。

结果：

![[Pasted image 20260517172021.png|600]]


因为这里 curl 走了代理，所以一开始 curl 先向代理服务器发送了 CONNECT 请求，让代理服务器建立到 httpbin.org 的 TCP 连接，所以先看到的是代理服务器返回给`curl`的响应：

```http
HTTP/1.1 200 Connection established
```

当代理建立起`curl`与httpbin.org的TCP隧道后，执行TLS加密后，代理负责原样转发两者的数据。

![[Pasted image 20260517175852.png|500]]

如果只想查看响应头，可以使用`-I`：

```shell
curl -I https://example.com
```

`-I`发送的是`HEAD`请求。服务器只返回响应头，不返回响应体。

示例：

```shell
curl -I https://httpbin.org/get
```

结果：

![[Pasted image 20260517180715.png|500]]

### （4）指定请求方法

使用`-X`可以指定请求方法。

例如发送`DELETE`请求：

```shell
curl -X DELETE https://httpbin.org/delete
```

发送 PUT 请求：

```shell
curl -X PUT https://httpbin.org/put
```

不过需要注意，**很多时候 `curl` 会根据选项自动选择方法**。例如使用 `-d` 提交数据时，`curl` 默认会使用`POST`，因此普通 POST 请求不一定需要写 `-X POST`。

下面这个命令已经会发送 POST 请求：

```shell
curl https://httpbin.org/post -d "name=tom"
```

没有必要写成：

```
curl -X POST https://httpbin.org/post -d "name=tom"
```

后者也能用，但要知道`-d` 本身就会让请求变成 POST。

### （5）添加请求头

使用`-H`可以添加请求头。

例如告诉服务器客户端希望接收`JSON`：

```shell
curl https://httpbin.org/get \
  -H "Accept: application/json"
```

结果：

![[Pasted image 20260517181815.png|400]]

发送认证信息：

```shell
curl -i https://httpbin.org/bearer \
	 -H "Authorization: Bearer token123"
```

结果：

![[Pasted image 20260517182020.png|400]]

多个请求头可以写多个 `-H`：

```shell
curl https://httpbin.org/get \
  -H "Accept: application/json" \
  -H "User-Agent: my-curl-client"
```

结果：

![[Pasted image 20260517182219.png|500]]

这里的 `Accept` 表示客户端希望接收 JSON，`User-Agent` 表示客户端身份。

在测试真实接口时，最常手动添加的是：

```http
Content-Type: application/json
Authorization: Bearer token
Accept: application/json
Cookie: ...
```

### （6）发送传统表单数据

使用`-d`可以发送请求体。

例如提交传统表单数据：

```shell
curl https://httpbin.org/post \
  -d "username=Tom&password=123456"
```

![[Pasted image 20260517182708.png|500]]

使用 `-d` 时，`curl` 默认会发送 POST 请求，并且默认使用类似传统表单的提交方式。

传统表单请求体通常长这样：

```text
username=Tom&password=123456
```

对应的 `Content-Type` 通常是：

```text
application/x-www-form-urlencoded
```

这种格式和 URL 的查询字符串很像，字段之间用`&`连接，键和值之间用`=`连接。

### （7）发送JSON数据

发送 JSON 数据时，需要同时设置`Content-Type`为`application/json`，否则服务器可能不知道应该按`JSON`解析请求体：

```shell
curl https://httpbin.org/post \
	-H "Content-Type: application/json" \
	-d '{"name":"Tom","age":25}'
```

这会发送一个 POST 请求，请求体是：

```json
{
  "name": "Tom",
  "age": 25
}
```

如果 JSON 比较长，可以放到文件中。

例如，创建`user.json`，写入上述的JSON数据，执行：

```shell
curl https://httpbin.org/post \
	-H "Content-Type: application/json" \
	-d @user.json
```

`@user.json` 表示从文件中读取请求体内容。

### （8）发送原始二进制数据

如果要直接发送文件的原始字节内容，可以使用`--data-binary`。

例如上传一张图片的原始二进制内容：

```shell
curl https://httpbin.org/post \
  -H "Content-Type: application/octet-stream" \
  --data-binary @avatar.png
```

这里的 `@avatar.png` 表示从文件读取内容，`--data-binary` 表示按原始字节发送，适合二进制数据。

`application/octet-stream` 表示通用二进制字节流。它不说明这段数据具体是图片、音频、视频还是压缩包，只说明请求体是一段原始字节数据。


### （9）上传文件

如果要模拟浏览器表单上传文件，更常用`-F`。

```shell
curl https://httpbin.org/post \
  -F "username=Tom" \
  -F "avatar=@avatar.png"
```

这里：

```text
username=Tom
```

表示普通表单字段。

```text
avatar=@avatar.png
```

表示上传当前目录下的 `avatar.png` 文件。

使用 `-F` 时，`curl` 会自动使用 `multipart/form-data`，并自动生成 boundary。一般不要手动写：

```text
-H "Content-Type: multipart/form-data"
```

因为 `multipart/form-data` 需要带 boundary，手动设置容易漏掉，导致服务器无法正确解析请求体。

![[Pasted image 20260517185758.png|500]]

### （10）查看详细请求过程

使用 `-v` 可以查看更详细的请求过程。

```shell
curl -v https://example.com
```

输出中，通常以 `>` 开头的是 `curl` 发出的请求内容，以 `<` 开头的是服务器返回的响应内容。

### （11）跟随重定向

默认情况下，`curl` 遇到 `301`、`302` 等重定向时，不一定继续请求新地址。

使用 `-L` 可以跟随重定向：

```shell
curl -L https://httpbin.org/redirect/1
```

如果服务器返回：

```shell
Location: /get
```

加上 `-L` 后，`curl` 会继续请求 `Location` 指向的新地址。

调试登录跳转、短链接、HTTP 跳转 HTTPS 时，经常会用到 `-L`。

### （12）保存响应内容

使用 `-o` 可以把响应保存到指定文件。

```shell
curl https://example.com -o example.html
```

这会把响应内容保存为 `example.html`。

下载图片：

```shell
curl https://httpbin.org/image/png -o image.png
```

使用 `-O` 可以使用远程文件名保存：

```
curl -O https://example.com/files/report.pdf
```

如果 URL 最后是 `report.pdf`，`curl` 会保存为 `report.pdf`。