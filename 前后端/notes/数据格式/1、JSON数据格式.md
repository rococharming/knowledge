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

