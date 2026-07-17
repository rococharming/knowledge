---
title: serde和serde_json
date: 2026-06-04
tags: [Rust, RustCrate, serde, serde_json]
aliases:
  - serde和serde_json
---

# 一、serde和serde_json定位

## 1、serde简介

`serde`是Rust生态常用的**序列化和反序列化**框架。它提供了一套通用机制，用来在 **Rust 数据结构和外部数据格式之间转换**。

`serde`负责定义转换能力，具体的数据格式由对应的格式库负责，例如：

| 格式          | 常见库          | 作用                      |
| ----------- | ------------ | ----------------------- |
| JSON        | `serde_json` | Rust 数据结构 ↔ JSON        |
| TOML        | `toml`       | Rust 数据结构 ↔ TOML        |
| YAML        | `serde_yaml` | Rust 数据结构 ↔ YAML        |

`serde`核心是两个Trait：

|Trait|方向|含义|
|---|---|---|
|`Serialize`|Rust → 外部格式|把 Rust 值写出去|
|`Deserialize`|外部格式 → Rust|把外部数据读进来|
通常不需要手动实现这两个 Trait，而是通过 `#[derive(Serialize, Deserialize)]` 自动生成实现。

## 2、serde_json简介

`serde_json`专门负责 JSON 格式的解析和生成。

`serde`本身是通用框架，`serde_json`是基于`serde`的 JSON 格式实现。

常见使用场景包括：

| 场景                 | 常用 API                          |
| ------------------ | ------------------------------- |
| 结构体转 JSON 字符串      | `serde_json::to_string`         |
| 结构体转格式化 JSON 字符串   | `serde_json::to_string_pretty`  |
| JSON 字符串转结构体       | `serde_json::from_str`          |
| JSON 字符串转动态 JSON 值 | `serde_json::from_str::<Value>` |
| 构造动态 JSON 值        | `serde_json::json!`             |

# 二、安装依赖

## 1、Cargo.toml配置

在`Cargo.toml`中添加：

```toml
[dependencies]  
serde = { version = "1.0.228", features = ["derive"] }  
serde_json = "1.0.150"
```

这里的 `features = ["derive"]` 用于启用 `#[derive(Serialize, Deserialize)]`。

如果只手动实现 `Serialize` / `Deserialize`，理论上不一定需要 `derive` feature。但日常开发中基本都会使用派生宏，所以通常直接这样配置。

## 2、基本导入

```rust
use serde::{Serialize, Deserialize};
```

导入`serde`的两个`Trait`。


# 三、结构体与JSON的相互转换

## 1、定义可序列化的结构体

```rust
use serde::{Deserialize, Serialize};  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
    email: String,  
    active: bool,  
}
```

这里的含义是：

|派生项|作用|
|---|---|
|`Debug`|允许使用 `{:?}` 或 `{:#?}` 打印调试信息|
|`Serialize`|允许把 `User` 转成 JSON|
|`Deserialize`|允许把 JSON 解析成 `User`|

## 2、结构体转JSON字符串

```rust
use serde::{Deserialize, Serialize};  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
    email: String,  
    active: bool,  
}  
  
  
fn main() {  
    let user = User {  
        id: 1,  
        name: "Tom".to_string(),  
        email: "tom@example.com".to_string(),  
        active: true,  
    };  
  
    let compact = serde_json::to_string(&user).unwrap();  
    let pretty = serde_json::to_string_pretty(&user).unwrap();  
  
    println!("{}", compact);  
    println!("{}", pretty);  
  
}
```

输出：

![[assets/Pasted image 20260603205320.png|400]]

`serde_json::to_string()`生成紧凑 JSON，适合网络传输和存储。

`serde_json::to_string_pretty()`生成带缩进的JSON，适合调试、日志和配置文件查看。

## 3、JSON字符串转结构体

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
    email: String,
    active: bool,
}

fn main() {
    let s = r#"{
	"id": 1,
	"name": "Tom",
	"email": "tom@example.com",
	"active": true
}"#;

    let user: User = serde_json::from_str(s).unwrap();

    println!("{:#?}", user);
}
```

结果：

![[assets/Pasted image 20260603210920.png|200]]

> 这里 s 使用 原始字符串 可以减少 JSON 中双引号的转义。

如果是普通字符串，就需要写成：

```rust
let s = "{  
    \"id\": 1,  
    \"name\": \"Tom\",  
    \"email\": \"tom@example.com\",  
    \"active\": true  
}";
```

# 四、serde 常用属性

`serde`可以通过`#[serde(...)]`修改默认映射规则，例如字段重命名、默认值、跳过字段、扁平化结构等。属性可以作用在结构体、枚举、枚举变体或字段上。

## 1、字段重命名

外部 JSON 字段不一定符合 Rust 命名习惯。例如 JSON 使用 `user_id`，Rust 结构体中希望使用 `id`。

```rust
use serde::{Deserialize, Serialize};  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    #[serde(rename = "user_id")]  
    id: u64,  
    name: String,  
    email: String,  
    active: bool,  
}  
  
  
fn main() {  
    let s = r#"{
	"id": 1,
	"name": "Tom",
	"email": "tom@example.com",
	"active": true
}"#;

    let user: User = serde_json::from_str(s).unwrap();  
  
    println!("{:#?}", user);  
  
}
```

`#[serde(rename = "user_id")]`同时影响序列化和反序列化：Rust 字段名为`id`，JSON字段名为`user_id`。


## 2、批量字段命名规则

如果 JSON 使用 `camelCase`，Rust使用 `snake_case`，可以在结构体上统一配置：

```rust
use serde::{Deserialize, Serialize};  
  
#[derive(Debug, Serialize, Deserialize)]  
#[serde(rename_all = "camelCase")]  
struct User {  
    user_id: u64,  
    user_name: String,  
    user_email: String,  
    is_active: bool,  
}  
  
  
fn main() {  
  
    let s = r#"{  
    "userId": 1,    
    "userName": "Tom",    
    "userEmail": "tom@example.com",    
    "isActive": true
}"#;  
  
    let user: User = serde_json::from_str(s).unwrap();  
  
    println!("{:#?}", user);  
  
}
```

结果：

![[assets/Pasted image 20260603212524.png|200]]

此时字段映射关系是：

| Rust 字段      | JSON 字段     |
| ------------ | ----------- |
| `user_id`    | `userId`    |
| `user_name`  | `userName`  |
| `user_email` | `userEmail` |
| `is_active`  | `isActive`  |

> 如果只有个别字段命名特殊，用 `rename`；如果整体命名风格一致，用 `rename_all`。


## 3、可选字段

JSON中某些字段可能不存在，可以使用`Option<T>`表示。

```rust
use serde::{Deserialize, Serialize};  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
    email: Option<String>,  
    active: bool,  
}  
  
  
fn main() {  
  
    let s = r#"{  
    "id": 1,    
    "name": "Tom",    
    "active": true
}"#;  
  
    let user: User = serde_json::from_str(s).unwrap();  
  
    println!("{:#?}", user);  

```

结果：

![[assets/Pasted image 20260603212946.png|200]]

由于 JSON 字符串中没有 `email` 字段，所以这里结构体`email`为 None。

`Option<T>` 适合表示外部数据中确实可能缺失的字段。

## 4、序列化时跳过None

默认情况下，`Option::None`会被序列化为 JSON 的 null。

```rust
use serde::{Deserialize, Serialize};  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
    email: Option<String>,  
    active: bool,  
}  
  
  
fn main() {  
  
    let user = User {  
        id: 1,  
        name: "Tom".to_string(),  
        email: None,  
        active: true,  
    };  
  
    let pretty = serde_json::to_string_pretty(&user).unwrap();  
  
    println!("{}", pretty);  
}
```

结果：

![[assets/Pasted image 20260603213434.png|200]]

如果希望`None`字段不出现在 JSON 字段中，可以使用：

```rust
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
  
    #[serde(skip_serializing_if = "Option::is_none")]  
    email: Option<String>,  
    active: bool,  
}
```

`skip_serializing_if` 用于在满足某个条件时跳过字段，`Option::is_none` 表示当字段值为 `None` 时跳过。

## 5、缺失字段使用默认值

如果 JSON 缺少某个字段，而结构体字段不是`Option<T>`，默认反序列化会失败。

```rust
use serde::{Deserialize, Serialize};  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
    email: String,  
    active: bool,  
}  
  
  
fn main() {  
  
    let s = r#"{  
    "id": 1,   
    "name": "Tom", 
    "active": true
}"#;  
  
    let user: User = serde_json::from_str(s).unwrap();  
  
    println!("{:#?}", user);  
  
}
```

运行panic：

```
thread 'main' (122852) panicked at src/main.rs:20:46:
called `Result::unwrap()` on an `Err` value: Error("missing field `email`", line: 5, column: 1)
```

此时会报错，因为 `email` 是必填字段。

可以使用 `#[serde(default)]`：

```rust
use serde::{Deserialize, Serialize};  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
  
    #[serde(default)]  
    email: String,  
    active: bool,  
}  
  
  
fn main() {  
  
    let s = r#"{  
    "id": 1,   
    "name": "Tom", 
    "active": true
}"#;    
  
    let user: User = serde_json::from_str(s).unwrap();  
  
    println!("{:#?}", user);  
  
}
```

此时结果为：

![[assets/Pasted image 20260603214202.png|200]]

因为`String`的默认值是""。

也可以指定自定义默认值函数：

```rust
use serde::{Deserialize, Serialize};  
  
fn default_email() -> String {  
    "null@null".to_string()  
}  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
  
    #[serde(default = "default_email")]  
    email: String,  
    active: bool,  
}  
  
  
fn main() {  
  
    let s = r#"{  
    "id": 1,    
    "name": "Tom",    
    "active": true
}"#;  
  
    let user: User = serde_json::from_str(s).unwrap();  
  
    println!("{:#?}", user);  
  
}
```

输出结果：

![[assets/Pasted image 20260603214406.png|200]]

`default` 适合处理外部数据字段缺失，但业务上可以接受默认值的场景。


## 6、跳过字段

有些字段只在程序内部使用，不希望出现在 JSON 中，也不希望从 JSON 中读取，可以使用`#[serde(skip)]`。

```rust
use serde::{Deserialize, Serialize};  
  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
    #[serde(skip)]  
    email: String,  
    active: bool,  
}  
  
  
fn main() {  
  
    let user = User {  
        id: 1,  
        name: "Tom".to_string(),  
        email: "tom@example.com".to_string(),  
        active: true,  
    };  
  
    let pretty = serde_json::to_string_pretty(&user).unwrap();  
  
    println!("{}", pretty);  
  
}
```

结果：

![[assets/Pasted image 20260603214753.png|200]]

序列化时不会出现`email`字段。

反序列化时JSON中出现 email，该字段也不会被读取，而是使用该字段类型的默认值。

```rust
use serde::{Deserialize, Serialize};  
 
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
  
    #[serde(skip)]  
    email: String,  
    active: bool,  
}  
  
  
fn main() {  
  
    let s = r#"{  
    "id": 1,    
    "name": "Tom",    
    "email": "tom@example.com",    
    "active": true  
}"#;  
  
    let user: User = serde_json::from_str(s).unwrap();  
  
    println!("{:#?}", user);  
  
}
```

这里 `String` 的默认值是 `""`。

![[assets/Pasted image 20260603215041.png|200]]

## 7、扁平化字段

`#[serde(flatten)]`可以把嵌套结构展开到同一层 JSON 中。

```rust
use serde::{Deserialize, Serialize};  
  
  
#[derive(Debug, Serialize, Deserialize)]  
struct Score {  
    math: u32,  
    english: u32,  
}  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
  
    #[serde(flatten)]  
    score: Score,  
}  
  
  
fn main() {  
  
    let user = User {  
        id: 1,  
        name: "Tom".to_string(),  
        score: Score {  
            math: 90,  
            english: 100,  
        }  
    };  
  
    let pretty = serde_json::to_string_pretty(&user).unwrap();  
  
    println!("{}", pretty);  
}
```

虽然 Rust 结构中 `score` 是一个嵌套结构体，但 JSON 中没有额外的 `score` 层级。

也可以从这种扁平 JSON 反序列化回来：

```rust
use serde::{Deserialize, Serialize};  
  
  
#[derive(Debug, Serialize, Deserialize)]  
struct Score {  
    math: u32,  
    english: u32,  
}  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
  
    #[serde(flatten)]  
    score: Score,  
}  
  
  
fn main() {  
  
    let s = r#"{  
    "id": 1,    
    "name": "Tom",    
    "math": 90,    
    "english": 100
}"#;  
  
    let user: User = serde_json::from_str(s).unwrap();  
  
    println!("{:#?}", user);  
}
```

结果：

![[assets/Pasted image 20260603215905.png|200]]

`flatten` 常用于把公共字段、扩展字段或嵌套配置展开到父结构中。


# 五、serde_json::Value的使用

## 1、动态JSON值

如果 JSON 结构不稳定，或者暂时不想定义结构体，可以使用`serde_json::Value`。

```rust
use serde_json::Value;  
  
  
  
fn main() {  
  
    let s = r#"{  
    "id": 1,    
    "name": "Tom",    
    "tags": ["rust", "serde"],    
    "profile": {        
	    "active": true    
	}
}"#;  
  
    let value = serde_json::from_str::<Value>(s).unwrap();  
  
    println!("{}", value["name"]);  
    println!("{}", value["tags"][0]);  
    println!("{}", value["profile"]["active"]);  
  
}
```

结果：

![[assets/Pasted image 20260603220646.png|100]]

`Value` 可以表示任意合法 JSON 值，例如对象、数组、字符串、数字、布尔值和 `null`。

## 2、get与索引访问

访问`Value`时有两种常见方式。

第一种是使用索引：

```rust
println!("{}", value["name"]);
```

第二种是使用 `get`：

```rust
if let Some(name) = value.get("name") {
	println!("{}", name);
}
```

| 写法                  | 字段不存在时           |
| ------------------- | ---------------- |
| `value["name"]`     | 返回 `Value::Null` |
| `value.get("name")` | 返回 `None`        |
`get` 更适合严谨处理，因为它能区分字段不存在和字段值本身就是 `null` 的情况。


## 3、从 Value 中取具体类型

`Value` 本身是动态 JSON 值，如果要取出具体 Rust 类型，需要使用对应方法：

| 方法            | 目标类型                          |
| ------------- | ----------------------------- |
| `as_str()`    | `Option<&str>`                |
| `as_u64()`    | `Option<u64>`                 |
| `as_i64()`    | `Option<i64>`                 |
| `as_f64()`    | `Option<f64>`                 |
| `as_bool()`   | `Option<bool>`                |
| `as_array()`  | `Option<&Vec<Value>>`         |
| `as_object()` | `Option<&Map<String, Value>>` |

```rust
use serde_json::Value;  
  
  
  
fn main() {  
  
    let s = r#"{  
    "id": 1,    
    "name": "Tom",    
    "tags": ["rust", "serde"],    
    "profile": {        
	    "active": true    
	}
}"#;  
  
    let value = serde_json::from_str::<Value>(s).unwrap();  
  
    let id = value["id"].as_i64().unwrap();  
    let name= value["name"].as_str().unwrap();  
    let tags = value["tags"].as_array().unwrap();  
    let profile = value["profile"].as_object().unwrap();  
  
    println!("id: {}", id);  
    println!("name: {}", name);  
    println!("tags: {:?}", tags);  
    println!("profile: {:?}", profile);  
}
```


如果 JSON 结构稳定，结构体比 `Value` 更推荐；如果 JSON 结构临时、不稳定、只读取少数字段，`Value` 更方便。

## 4、使用 json! 构造 JSON

`serde_json::json!` 可以直接用接近 JSON 的语法构造 `Value`。

```rust
use serde_json::json;  
  
  
  
fn main() {  
  
    let value = json!({  
        "name": "Tom",  
        "age": 20,  
        "tags": ["rust", "serde"]  
    });  
  
    println!("{}", value);  
  
}
```

`json!` 的返回值是 `serde_json::Value`。它适合临时构造 JSON，例如写测试数据、拼接请求体、构造简单响应。


# 六、结构体与 Value 的互相转换

## 1、结构体转 Value

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
}

fn main() {
    let user = User {
        id: 1,
        name: String::from("Tom"),
    };

    let value = serde_json::to_value(&user).unwrap();

    println!("{}", value);
}
```

输出结果：

```text
{"id":1,"name":"Tom"}
```

`to_value` 适合在强类型数据和动态 JSON 之间转换。


## 2、Value 转结构体

```rust
use serde::{Deserialize, Serialize};  
use serde_json::json;  
  
#[derive(Debug, Serialize, Deserialize)]  
struct User {  
    id: u64,  
    name: String,  
}  
  
fn main() {  
    let value = json!({  
       "id": 1,  
       "name": "Tom"  
    });  
  
    let user: User = serde_json::from_value(value).unwrap();  
  
    println!("{:#?}", user);  
}
```

`from_value` 适合先用 `Value` 接收 JSON，再在某个节点上转换成具体结构体。

例如：

```rust
use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: u64,
    name: String,
}

fn main() {
    let s = r#"
    {
        "code": 200,
        "data": {
            "id": 1,
            "name": "Tom"
        }
    }
    "#;

    let value: Value = serde_json::from_str(s).unwrap();

    let user: User = serde_json::from_value(value["data"].clone()).unwrap();

    println!("{:#?}", user);
}
```

这里先把整个 JSON 解析成 `Value`，再把 `data` 字段转换成 `User`。


# 七、枚举的 JSON 表示

## 1、默认外部标签表示

Serde 对枚举有多种 JSON 表示方法。默认方式是外部标签，也就是把变体名作为最外层 key。

```rust
use serde::{Deserialize, Serialize};  
  
  
#[derive(Debug, Serialize, Deserialize)]  
enum Message {  
    Text { content: String },  
    Color(u8, u8, u8),  
    Move { x: i32, y: i32 },  
    Quit  
}  
  
fn main() {  
  
    let m1 = Message::Text { content: "Hello World!".to_string() };  
    let m2 = Message::Color(0, 0, 0);  
    let m3 = Message::Move { x: 0, y: 0 };  
    let m4 = Message::Quit;  
  
    println!("{}", serde_json::to_string_pretty(&m1).unwrap());  
    println!("{}", serde_json::to_string_pretty(&m2).unwrap());  
    println!("{}", serde_json::to_string_pretty(&m3).unwrap());  
    println!("{}", serde_json::to_string_pretty(&m4).unwrap());  
  
}
```

结果：

![[assets/Pasted image 20260603223720.png|300]]

- 对于结构体变体，值为对象。
- 对于元组变体，值为数组。
- 对于单元变体，输出结果只有一个键。

## 2、内部标签表示

如果希望JSON 中有一个字段专门表示类型，可以使用 `#[serde(tag = "...")]`。

```rust
use serde::{Deserialize, Serialize};  
  
  
#[derive(Debug, Serialize, Deserialize)]  
#[serde(tag = "type")]  
enum Message {  
    Text { content: String },  
    Move { x: i32, y: i32 },  
    Quit  
}  
  
fn main() {  
  
    let m1 = Message::Text { content: "Hello World!".to_string() };  
    let m2 = Message::Move { x: 0, y: 0 };  
    let m3 = Message::Quit;  
  
    println!("{}", serde_json::to_string_pretty(&m1).unwrap());  
    println!("{}", serde_json::to_string_pretty(&m2).unwrap());  
    println!("{}", serde_json::to_string_pretty(&m3).unwrap());  
  
}
```

结果：

![[assets/Pasted image 20260603224340.png|300]]

注意，`#[serde(tag = "type")]`对元组型变体不可用。

## 3、相邻标签表示

如果希望类型和内容分开放在两个字段中，可以使用：`#[serde(tag = "type", content = "data")]`。

示例：

```rust
use serde::{Deserialize, Serialize};  
  
  
#[derive(Debug, Serialize, Deserialize)]  
#[serde(tag = "type", content = "data")]  
enum Message {  
    Text { content: String },  
    Color(u8, u8, u8),  
    Move { x: i32, y: i32 },  
    Quit  
}  
  
fn main() {  
  
    let m1 = Message::Text { content: "Hello World!".to_string() };  
    let m2 = Message::Color(0, 0, 0);  
    let m3 = Message::Move { x: 0, y: 0 };  
    let m4 = Message::Quit;  
  
    println!("{}", serde_json::to_string_pretty(&m1).unwrap());  
    println!("{}", serde_json::to_string_pretty(&m2).unwrap());  
    println!("{}", serde_json::to_string_pretty(&m3).unwrap());  
    println!("{}", serde_json::to_string_pretty(&m4).unwrap());  
  
}
```

结果：

![[assets/Pasted image 20260603224606.png|300]]

这种格式适合外层固定包含类型字段，具体数据统一放进 `data`、`payload`、`content` 等字段中。


# 八、错误处理

学习示例中常用 `unwrap()`，是为了减少无关代码。但实际项目中，反序列化可能失败，例如：

| 错误原因      | 示例                                 |
| --------- | ---------------------------------- |
| JSON 格式错误 | 少逗号、少引号、多余逗号                       |
| 字段缺失      | 结构体要求 `id`，JSON 中没有                |
| 类型不匹配     | Rust 需要 `u64`，JSON 给了字符串           |
| 字段名不匹配    | Rust 需要 `user_id`，JSON 中是 `userId` |

因此更推荐让函数返回`Result`。

`serde_json::Error` 会包含解析失败的原因和位置，适合向上返回或转换成业务错误。


# 九、常见使用模式

例如读取配置文件。

```rust
use serde::{Deserialize, Serialize};  
  
#[derive(Debug, Serialize, Deserialize)]  
struct Config {  
    host: String,  
    port: u16,  
  
    #[serde(default)]  
    debug: bool,  
}  
  
fn main() -> Result<(), Box<dyn std::error::Error>>{  
  
    let content = std::fs::read_to_string("config.json")?;  
  
    let config = serde_json::from_str::<Config>(&content)?;  
  
  
    println!("{:#?}", config);  
  
    Ok(())  
}
```

示例 `config.json`：

```
{  "host": "127.0.0.1",  "port": 8080}
```

`debug` 字段缺失时会使用 `bool` 的默认值 `false`。
