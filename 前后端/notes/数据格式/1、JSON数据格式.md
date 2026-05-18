# 一、JSON简介

`JSON`全称是 JavaScript Object Notation，即 JavaScript 对象表示法。

它是一种轻量级的数据交换格式，常用于：

- 前后端接口通信
- 配置文件
- 日志数据
- 程序之间的数据传输
- API请求和响应体

虽然`JSON`起源于JavaScript，但它并不只属于 JavaScript。现在几乎所有主流语言都支持 JSON，包括 Rust、Go、Java、Python、JavaScript、C# 等。

`JSON`的核心作用是：**用一种简单、通用、文本化的格式表达结构化数据**。

示例：

```json
{
  "name": "Alice",
  "age": 18,
  "is_student": true
}
```

这段 JSON 表示一个对象，其中包含三个字段：`name`、`age` 和 `is_student`。


# 二、JSON的基本数据类型

`JSON` 支持的数据类型很少，但足够表达大多数常见数据结构。

## 1、对象

JSON对象使用`{}`包裹，内部由一组键值对组成。

示例：

```json
{
  "name": "Alice",
  "age": 18
}
```

**对象中的键必须是字符串，因此必须用双引号`" "`包起来**。

正确写法：

```json
{
  "name": "Alice"
}
```

错误写法：

```json
{
  name: "Alice"
}
```

这和 JavaScript 对象字面量不同。在 JavaScript 中，对象键有时可以不加引号，但标准JSON中，键必须使用双引号。


## 2、数组

JSON 数组使用 `[]` 包裹，表示一组有序数据。

示例：

```json
[
  "Rust",
  "Go",
  "Python"
]
```

数组中可以存放对象：

```json
[
  {
    "name": "Alice",
    "age": 18
  },
  {
	"name": "Bob",  
	"age": 20  
  }
]
```

也可以存放不同类型的数据：

```json
[
  "hello",
  123,
  true,
  null
]
```

不过在实际接口设计中，通常建议数组中的元素结构保持一致，这样更容易解析和维护。

## 3、字符串

JSON字符串必须使用双引号`" "`包裹。

示例：

```json
{
  "message": "Hello JSON"
}
```

不能使用单引号。

错误写法：

```json
{
  "message": 'Hello JSON'
}
```

字符串中可以使用转义字符，例如：

```json
{
  "text": "Hello\nWorld",
  "quote": "He said: \"Hi\""
}
```

其中 `\n` 表示换行，`\"` 表示字符串中的双引号。

## 4、数字

JSON 中的数字**不区分整数和浮点数字面量类型**，只统一表示为 number。

示例：

```json
{
  "age": 18,
  "price": 99.5,
  "temperature": -3.2
}
```

需要注意的是，JSON 本身没有 `i32`、`u64`、`f64` 这类具体类型。具体解析成什么类型，由使用 JSON 的编程语言决定。例如在 Rust 中，可以把 JSON 数字反序列化成 `i32`、`u64`、`f64` 等具体类型。

## 5、布尔值

JSON 中的布尔值只有两个：`true`和`false`。

示例：

```json
{
  "enabled": true,
  "deleted": false
}
```

注意必须是小写，不能写成 `True` 或 `False`。

## 6、null

`null` 表示空值、缺失值或没有值。

示例：

```json
{
  "nickname": null
}
```

`null` 不等于空字符串 `""`，也不等于数字 `0`。

```json
{
  "empty_string": "",
  "zero": 0,
  "nothing": null
}
```

这三个值含义不同：

- `""` 表示有一个字符串，只是内容为空
- `0` 表示有一个数字，值为 0
- `null` 表示这里没有具体值

# 三、JSON的语法规则

## 1、键必须使用双引号

JSON 对象中的键必须是字符串，并且必须使用双引号。

正确写法：

```json
{
  "name": "Alice"
}
```

错误写法：

```json
{
  name: "Alice"
}
```

这也是很多人刚接触 JSON 时容易写错的地方。

## 2、字符串必须使用双引号

JSON 字符串也必须使用双引号，不能使用单引号。

正确写法：

```json
{  
  "language": "Rust"  
}
```

错误写法：

```json
{  
  "language": 'Rust'  
}
```

## 3、最后一个字段后面不能有逗号

**JSON不允许尾随逗号**。

正确写法：

```json
{
  "name": "Alice",
  "age": 18
}
```

错误写法：

```json
{  
  "name": "Alice",  
  "age": 18,  
}
```

数组也是一样。

错误写法：

```json
[
  "Rust",
  "Go",
]
```

这和很多编程语言不一样。Rust、JavaScript、Python 中很多场景允许尾随逗号，但标准 JSON 不允许。


## 4、注释不是标准JSON的一部分

标准JSON不支持注释。

错误写法：

```json
{
  // 用户名
  "name": "Alice"
}
```

如果需要在配置文件中写注释，可以考虑使用 `JSONC`、`YAML`、`TOML` 等格式。

例如，Rust项目中常见的`Cargo.toml`就是 TOML，而不是 JSON。TOML 更适合写配置文件，因为它支持注释，结构也更适合人工编辑。


# 四、JSON的嵌套结构

`JSON`可以通过对象和数组表达嵌套数据。

示例：

```json
{
  "user": {
    "id": 1,
    "name": "Alice"
  },
  "roles": ["admin", "editor"],
  "profile": {
    "email": "alice@example.com",
    "address": {
      "city": "Shanghai",
      "zipcode": "200000"
    }
  }
}
```

这段 JSON 中：

- `user`是一个对象
- `roles`是一个数组
- `profile`是一个对象
- `profile.address`又是一个嵌套对象

`JSON`的嵌套能力很强，但实际使用时不建议嵌套过深。结构过深会增加阅读、解析和维护成本。

# 五、JSON与普通文本

`JSON`本质上是文本。

例如下面这段`JSON`：

```json
{
  "name": "Alice",
  "age": 18
}
```

从存储角度看，它就是一段字符串内容。只有当程序按照 JSON 规则解析它时，它才会变成对象、数组、数字、布尔值等结构化数据。

接口返回的 JSON 数据，在网络上传输时通常只是文本字节。程序收到之后，需要通过 JSON 解析器把它转换成语言内部的数据结构。

以 Rust 为例：

- 网络上传输的是JSON文本
- Rust程序读到的是字符串或字节
- 通过`serde_json`解析后，才能变成Rust结构体、枚举等


# 六、序列化与反序列化

## 1、序列化

**序列化就是把程序中的数据结构转换成JSON字符串**。

例如程序中的一个用户对象：

```rust
User {
	name: "Alice",
	age: 18
}
```

序列化JSON后可能是：

```json
{
  "name": "Alice",
  "age": 18
}
```



## 2、反序列化

**反序列化就是把JSON字符串解析成程序中的数据结构**。

例如有一段 JSON：

```json
{
  "name": "Alice",
  "age": 18
}
```

反序列化之后，可以变成程序中的 `User` 对象或结构体。


## 3、为什么需要序列化和反序列化

程序之间不能直接传递内存中的对象，因为不同语言、不同进程、不同机器的内存结构不一样。

因此常见做法是：

1. 发送方把内部数据结构序列化为JSON文本
2. 通过HTTP、消息队列或文件传递JSON
3. 接收方再把JSON反序列化成自己的内部结构

这也是 JSON 被广泛用于 API 通信的原因。


# 七、JSON的常见使用场景

## 1、HTTP API

前后端通信中，JSON 是最常见的数据格式之一。

请求体示例：

```http
POST /users HTTP/1.1
Content-Type: application/json

{
  "name": "Alice",
  "age": 18
}
```

响应体示例：

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "name": "Alice",
  "age": 18
}
```

这里的 `Content-Type: application/json` 表示消息体使用 JSON 格式。有关HTTP请求与响应详见[[2、HTTP请求与响应|HTTP请求与响应]]。


## 2、配置数据

有些工具会使用 JSON 作为配置格式。

示例：

```json
{
  "theme": "dark",
  "font-size": 14,
  "auto_save": true
}
```

不过如果配置文件需要大量人工编辑，JSON 不一定是最舒服的选择，因为它不支持注释，也不允许尾随逗号。


## 3、日志数据

很多系统会使用 JSON 记录结构化日志。

示例：

```json
{
  "level": "info",
  "message": "user login",
  "user-id": 1001,
  "timestamp": "2026-05-18T10:30:00Z"
}
```

结构化日志的好处是方便机器解析、搜索和统计。


# 八、JSON的局限性

JSON 简单通用，但也有一些限制。

## 1、不支持注释

标准 JSON 不支持注释，因此不适合写需要大量说明的复杂配置文件。

## 2、不区分具体数字类型

JSON 只有统一的 number 类型，不区分 `i32`、`u64`、`f64`。

这意味着在具体语言中解析时，需要自己决定目标类型。如果数字很大，还要注意精度问题。


## 3、不支持日期类型

JSON没有内置日期类型。

日期通常用字符串表示：

```json
{
  "created_at": "2026-05-18T10:30:00Z"
}
```

至于这个字符串是否表示日期、采用什么格式，需要由应用程序自己约定。

## 4、不支持二进制数据

JSON 是文本格式，不能直接存放原始二进制数据。

如果需要在 JSON 中传递二进制内容，通常会先编码成 Base64 字符串。

> Base64 是一种编码方式，用于把 二进制数据转换成普通文本字符串。它常用于把图片、文件、字节数据放进JSON、HTML、邮件、HTTP请求等文本环境中。核心规则：3个字节 -> 4个Base64字符。

示例：

```json
{
  "file_content": "SGVsbG8="
}
```

这会让数据体积变大，因此大量二进制数据通常不直接放在 JSON 中传输。