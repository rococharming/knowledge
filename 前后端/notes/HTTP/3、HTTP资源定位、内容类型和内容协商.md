# 一、HTTP资源概述
## 1、资源的含义

HTTP 访问的核心对象是**资源**。

资源不只是服务器上的某个文件，而是客户端可以通过 HTTP 访问到的任何内容或对象。

它可以是：

- HTML 页面
- CSS文件、JavaScript文件、图片等静态资源
- JSON、XML等数据文件
- 订单、文章、用户等抽象的业务对象

在 Web 开发中，经常会看到这样的地址：

```http
GET /articles/1 HTTP/1.1
Host: example.com
```

这里的`/articles/1`可以表示编号为`1`的文章资源。客户端通过URL找到这个资源，再通过HTTP方法表达要对这个资源做什么操作。

可以这样理解：URL表示资源位置，HTTP方法表示操作意图，状态码表示处理结果，Header表示附加信息，Body承载具体数据。

## 2、资源表示形式

资源和资源的表示形式不是一回事。

例如，`/articles/1`表示“编号为1的文章”，但服务器可以用不同形式返回它：

- 返回HTML，直接在浏览器显示
- 返回JSON，供前端或其他程序读取
- 返回XML，供某些系统集成使用
- 返回中文版本或英文版本
- 返回经过gzip、br等方式压缩后的内容

同一个资源可以有多种表示形式，客户端和服务器之间需要通过 HTTP Header 协商返回哪一种形式。

例如：

```http
GET /articles/1 HTTP/1.1
Host: example.com
Accept: application/json  
Accept-Language: zh-CN
```

这个请求表示客户端想访问 `/articles/1` 这个资源，并且更希望服务器返回 JSON 格式和简体中文内容。

# 二、URL 与 URI

## 1、URI、URL 与 URN

URI 是 Uniform Resource Identifier 的缩写，表示统一资源标识符。它的作用是标识一个资源。

URL 是 Uniform Resource Locator 的缩写，表示统一资源定位符。**URL不仅标识资源，还说明如何定位这个资源**。

实际 Web 开发中，大多数时候说“网址”、“接口地址”、“资源地址”，通常指的就是URL。

例如：

```
https://www.example.com/articles/1
```

这个地址既标识了一个资源，也说明了访问它的访问方式：使用`https`协议，访问`www.example.com`这台主机上的`/articles/1`路径。

URN是另一类URI，用于通过名字标识资源，但它在日常 Web 开发中不如 URL常见。


## 2、URL的基本结构

一个完整 URL 通常由**协议、主机、端口、路径、查询参数和片段标识**组成。

例如：

```text
https://www.example.com:443/articles/1?lang=zh#comments
```

可以拆成：

|部分|示例|含义|
|---|---|---|
|scheme|`https`|使用的协议|
|host|`www.example.com`|服务器主机名|
|port|`443`|端口号|
|path|`/articles/1`|资源路径|
|query|`lang=zh`|查询参数|
|fragment|`comments`|页面片段标识|
其中：

- `scheme`决定使用什么协议访问资源。常见的有`http`和`https`
- `host`表示要访问哪台服务器，它可以是域名，也可以是IP地址
- `port`表示服务器上的端口。如果省略端口，HTTP默认使用80端口，HTTPS默认使用443端口
- `path`表示服务器上的资源路径
- `query`用于传递查询参数，通常用于筛选、分页、排序或搜索
- `fragment`用于标识页面内部的某个位置，例如跳转到评论区。它不会发送给服务器，而是由浏览器在客户端本地处理。

## 3、路径与查询参数

路径通常用于表示**资源本身**。

例如：

```text
/articles/1
/users/42
/orders/20260518001
```

这些路径看起来像是在访问某个具体资源。

查询参数通常用于**对资源集合进行筛选、分页、排序或搜索**。

例如：

```text
/articles/?category=rust&page=2
/products?keyword=keyboard&sort=price
```

`/articles`表示文章列表资源，`category=rust`和`page=2`表示查询条件，用来进一步限定要获取哪些文章。可以理解为：请求文章列表，并筛选出分类为rust的文章，同时获取第2页的数据。

`/products` 表示商品列表资源，后面的 `keyword=keyboard` 和 `sort=price` 是查询参数，用来描述查询条件和排序方式。可以理解为：请求商品列表，并搜索关键词为`keyboard`的商品，同时按照价格进行排序。

**在接口设计中，常见写法是用路径表示资源层级，用查询参数表示附加条件**。


## 4、URL编码

URL 中有些字符具有特殊含义，例如 `/`、`?`、`&`、`=`、`#`。它们用于分隔路径、查询字符串、查询参数和片段标识。

如果这些字符本身也出现在要传递的数据中，例如搜索关键词、文章标题、文件名或表单字段值，就可能和 URL 的结构符号发生冲突。URL 编码用于把这些字符转换成安全的表示形式，避免解析时产生歧义。

例如，搜索关键词中包含空格时，空格通常会被编码为 `%20`：

```text
https://example.com/search?q=hello%20world
```

如果搜索关键词中包含 `&` 和 `=`，也需要进行编码：

```text
https://example.com/search?q=rust%26sort%3Dprice
```

这个 URL 表示搜索的关键词是：

```
rust&sort=price
```

而不是新增一个 `sort=price` 查询参数。

中文也会被编码成百分号形式：

```text
https://example.com/search?q=HTTP%E5%8D%8F%E8%AE%AE
```

浏览器通常会自动处理 URL 编码。手写请求、拼接 URL 或调试接口时，需要注意查询参数里的特殊字符是否被正确编码。

# 三、资源类型与MIME Type

## 1、MIME Type 基本概念

`MIME Type`用来描述内容的数据类型，全称为 Multipurpose Internet Mail Extensions（多用途互联网邮件扩展）。服务器返回响应时，会通过`Content-Type`告诉客户端响应体是什么格式。

例如：

```text
Content-Type: text/html
Content-Type: application/json
Content-Type: image/png
Content-Type: text/css
Content-Type: application/javascript
```

浏览器拿到响应后，会根据 `Content-Type` 决定如何处理响应体。`text/html` 会被当作 HTML 页面解析，`application/json` 会被当作 JSON 数据处理，`image/png` 会被当作 PNG 图片显示。

## 2、type/subtype结构

MIME Type 通常由`type/subtype`两部分组成。

常见示例：

| MIME Type                  | 含义            |
| -------------------------- | ------------- |
| `text/html`                | HTML 文档       |
| `text/css`                 | CSS 样式文件      |
| `text/plain`               | 普通文本          |
| `application/json`         | JSON 数据       |
| `application/javascript`   | JavaScript 代码 |
| `application/octet-stream` | 通用二进制数据       |
| `image/png`                | PNG 图片        |
| `image/jpeg`               | JPEG 图片       |
| `audio/mpeg`               | MPEG 音频       |
| `video/mp4`                | MP4 视频        |
`type`表示大类，`subtype`表示具体格式，比如 `image/png` 和 `image/jpeg` 都属于图片类型，但具体编码格式不同。

## 3、Content-Type 响应头

服务端返回响应时，通常会使用 `Content-Type` 说明响应体类型。

例如返回 HTML：

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!doctype html>
<html>
  <head>
    <title>Example</title>
  </head>
  <body>
    <h1>Hello HTTP</h1>
  </body>
</html>
```

返回 JSON：

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "id": 1,
  "title": "HTTP"
}
```

`charset=utf-8` 是 `Content-Type` 的参数，用来说明文本编码。对于 HTML、JSON、CSS、JavaScript 等文本内容，编码会影响客户端如何把字节解析成字符。

## 4、Content-Type 请求头

客户端发送请求体时，也需要通过 `Content-Type` 告诉服务器请求体是什么格式。

例如提交 JSON 数据：

```http
POST /api/articles HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "title": "HTTP",
  "category": "network"
}
```

服务器看到 `Content-Type: application/json` 后，会按 JSON 格式解析请求体。

如果 `Content-Type` 和实际请求体不匹配，服务器可能无法正确解析请求。例如请求头声明是 JSON，但请求体实际是普通表单格式，就可能得到 `400 Bad Request` 或其他业务错误响应。

# 四、内容协商

## 1、内容协商基本概念

内容协商是客户端和服务器围绕“资源表示形式”进行选择的过程。

客户端通过请求头表达自己希望接收什么内容，服务器根据客户端偏好和自身能力选择合适的响应形式。

常见内容协商请求头包含：

| 请求头               | 作用           |
| ----------------- | ------------ |
| `Accept`          | 客户端希望接收的媒体类型 |
| `Accept-Language` | 客户端希望接收的语言   |
| `Accept-Encoding` | 客户端支持的压缩编码   |
服务端响应时，会用对应的响应头说明最终返回的内容形式。

| 响应头                | 作用        |
| ------------------ | --------- |
| `Content-Type`     | 实际返回的媒体类型 |
| `Content-Language` | 实际返回的语言   |
| `Content-Encoding` | 实际使用的压缩编码 |

内容协商流程可以表示为：

```text
客户端 / 浏览器                         Web 服务器
     │                                      │
     │  Accept: application/json            │
     │  Accept-Language: zh-CN              │
     │  Accept-Encoding: gzip               │
     │ ───────────────────────────────────▶ │
     │                                      │
     │  根据客户端偏好选择响应形式              │
     │                                      │
     │  Content-Type: application/json       │
     │  Content-Language: zh-CN              │
     │  Content-Encoding: gzip               │
     │ ◀─────────────────────────────────── │
```


## 2、Accept

`Accept`表示客户端希望接收的内容类型。

例如：

```text
Accept: text/html
```

表示客户端希望接收 HTML。

```
Accept: application/json
```

表示客户端希望接收 JSON。

浏览器访问页面时，通常会发送比较复杂的`Accept`：

```text
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
```

它的意思是：

浏览器优先希望服务器返回：

```
text/html
application/xhtml+xml
image/avif
image/webp
```

也可以接受：

```text
application/xml
```

但优先级稍低，因为它带了：

```text
q=0.9
```

最后：

```
*/*;q=0.8
```

表示其他任意类型也可以接受，但优先级更低。

API 调用中常见写法更直接：

```http
GET /api/articles/1 HTTP/1.1
Host: example.com
Accept: application/json
```

这个请求表示客户端希望服务器返回 JSON 格式的数据。

## 3、Accept-Language

`Accept-Language` 表示客户端希望接收的语言版本。

例如：

```text
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
```

这个请求头表示：优先使用简体中文，其次是中文，再其次是英文。

服务器可以根据这个请求头返回不同语言版本的内容。

例如响应：

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Language: zh-CN

<!doctype html>
<html lang="zh-CN">
  ...
</html>
```

`Content-Language: zh-CN` 表示这次响应内容使用的是简体中文。


## 4、Accept-Encoding

`Accept-Encoding` 表示客户端支持的内容编码，最常见的是压缩编码。

例如：

```
Accept-Encoding: gzip, br, zstd
```

这表示客户端支持 `gzip`、`br` 和 `zstd` 压缩格式。

如果服务器选择使用 gzip 压缩响应体，会返回：

```text
Content-Encoding: gzip
```

一个响应可以同时包含 `Content-Type` 和 `Content-Encoding`：

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Encoding: gzip

<gzip 压缩后的字节数据>
```

`Content-Type` 描述原始内容是什么类型，`Content-Encoding` 描述内容在传输前经过了什么编码处理。也就是说，这个响应的原始内容是 JSON，但实际传输的是 gzip 压缩后的字节数据。客户端需要先解压，再按 JSON 解析。

## 5、q权重

`q` 是 quality value，用来表示客户端偏好程度。取值范围通常是 `0` 到 `1`，数值越大优先级越高。

例如：

```text
Accept: text/html,application/json;q=0.9,*/*;q=0.8
```

含义是：

| 类型                 | q 值   | 优先级 |
| ------------------ | ----- | --- |
| `text/html`        | `1.0` | 最高  |
| `application/json` | `0.9` | 次高  |
| `*/*`              | `0.8` | 更低  |
如果没有显式写 `q`，默认值是 `1.0`。

`*/*` 表示任意媒体类型。它通常作为兜底选项，表示如果没有更合适的类型，客户端也可以接受其他类型。

`Accept-Language` 也可以使用 `q`：

```
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
```

表示客户端最希望接收 `zh-CN`，其次是 `zh`，再其次是 `en`。


## 6、服务端选择响应形式

服务端会结合客户端请求头和自身能力选择响应形式。

例如客户端请求：

```http
GET /articles/1 HTTP/1.1
Host: example.com
Accept: application/json
Accept-Language: zh-CN
Accept-Encoding: gzip
```

服务器可能返回：

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Language: zh-CN
Content-Encoding: gzip

<gzip 压缩后的 JSON 数据>
```

这表示服务器选择了 JSON 格式、简体中文内容，并使用 gzip 压缩传输。

如果服务器无法提供客户端要求的表现形式，可能返回：

```http
HTTP/1.1 406 Not Acceptable
Content-Type: text/plain

Not Acceptable
```

`406 Not Acceptable` 表示服务器无法根据客户端的内容协商要求生成可接受的响应。实际开发中，很多服务不会严格返回 `406`，而是返回它支持的默认格式。


# 五、常见内容相关响应头

## 1、Content-Type

`Content-Type` 描述响应体或请求体的数据类型。

响应示例：

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
```

请求示例：

```http
POST /api/articles HTTP/1.1
Host: example.com
Content-Type: application/json
```

在响应中，它告诉客户端如何解析响应体；在请求中，它告诉服务器如何解析请求体。


## 2、Content-Length

`Content-Length` 表示消息体的字节长度。

例如：

```text
Content-Length: 1024
```

它表示 Body 部分有 `1024` 个字节。

注意，`Content-Length` 统计的是字节数，不是字符数。英文字符在 UTF-8 中通常占 1 个字节，中文字符通常占多个字节，emoji 也可能占多个字节。


## 3、Content-Encoding

`Content-Encoding` 表示消息体经过了什么编码处理，常见用途是压缩。

例如：

```text
Content-Encoding: gzip
Content-Encoding: br
Content-Encoding: zstd
```

它和 `Content-Type` 关注的问题不同。

```html
Content-Type: text/html  
Content-Encoding: gzip
```

表示原始内容是 HTML，但传输前使用 gzip 压缩过。

客户端收到响应后，需要先根据 `Content-Encoding` 解压，再根据 `Content-Type` 解析内容。

## 4、Content-Language

`Content-Language` 表示响应内容的语言。

例如：

```
Content-Language: zh-CN
```

这个响应头说明返回内容是简体中文。

它常和 `Accept-Language` 配合使用：

```http
GET /docs HTTP/1.1
Host: example.com
Accept-Language: zh-CN,en;q=0.8
```

响应：

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Language: zh-CN
```

## 5、Vary

`Vary`表示服务器的响应会根据哪些请求头发生变化。

例如：

```text
Vary: Accept-Encoding
```

表示同一个 URL 的响应可能会因为 `Accept-Encoding` 不同而变化。支持 gzip 的客户端可能拿到 gzip 压缩版本，不支持 gzip 的客户端可能拿到未压缩版本。

再例如：

```text
Vary: Accept-Language
```

表示同一个 URL 可能根据 `Accept-Language` 返回不同语言版本。

如果响应同时受多个请求头影响，可以写成：

```text
Vary: Accept-Encoding, Accept-Language
```

`Vary` 对缓存很重要。缓存系统需要知道同一个 URL 是否可以直接复用缓存结果，还是要根据请求头区分不同版本。