---
title: YAML
date: 2026-07-11
tags: [计算机基础, 数据格式, YAML, data-format]
aliases:
  - YAML
  - YAML语法
  - YAML基础
---

# 一、YAML概述

YAML 是 **YAML Ain't Markup Language** 的缩写，是一种以数据为中心的文本序列化格式。它常用于配置文件、自动化规则、CI/CD 流水线、容器编排和结构化提示词等场景。

YAML 的核心目标是：

> 用接近人类阅读习惯的文本形式，表达层级化的结构化数据。
 
示例：

```yaml
name: Alice
age: 18
is_student: true
skills:
  - Python
  - Rust
  - SQL
```

这段 YAML 表示一个包含姓名、年龄、学生状态和技能列表的数据对象。与 [[1、JSON|JSON]] 相比，YAML 不需要大量花括号和双引号，因此更适合人工编写和维护。

常见使用场景包括：

- 软件配置文件，例如应用配置、日志配置、环境配置
- 自动化工作流，例如 CI/CD 配置、部署脚本、任务编排
- 基础设施描述，例如容器、服务和集群配置
- 结构化文档元数据，例如静态站点生成器中的 front matter
- 复杂提示词或 Agent 配置，用于组织角色、目标、输入、约束和输出格式

# 二、YAML规则结构

## 1、核心规则

最核心的规则就是 **键: 值** 这种键值对的形式表述数据。

>注意`:`是英文冒号且后面有个空格。

```yaml
name: Tom
```

YAML 与对于缩进和空格非常敏感

## 2、基本结构

YAML 主要由三类结构组成：标量、序列和映射。它们分别对应单个值、列表和键值对集合。

### （1）标量

标量（scalar）是单个不可再拆分的值，例如字符串、数字、布尔值和空值。

示例：

```yaml
name: Alice
age: 18
price: 99.5
enabled: true
deleted: false
nickname: null
empty: ~
```

其中：

- `name` 的值是字符串
- `age` 和 `price` 是数字
- `enabled` 和 `deleted` 是布尔值
- `nickname` 和 `empty` 表示空值

字符串通常可以不加引号：

```yaml
message: Hello World
```

但当字符串包含容易被解析器误判的内容时，建议加引号。例如布尔值、冒号、井号、前后空格、日期样式文本等。

```yaml
status: "true"
time: "10:30"
version: "1.0"
comment: "name: value"
```

这里的 `"true"` 是字符串，而不是布尔值 `true`。

引号还区分单引号和双引号：
- 单引号不会转义特殊字符
- 双引号会转义特殊字符，如`\n`解析为换行

数字包含整数和浮点数。

布尔值只有`true`或`false`两种取值。

空值使用`null`或`~`表示。

### （2）序列

序列（sequence）表示一组有序数据，类似编程语言中的数组或列表。每个列表项以短横线和空格开头。

示例：

```yaml
languages:
  - Rust
  - Go
  - Python
```

也可以使用行内写法：

```yaml
languages: [Rust, Go, Python]
```

多行写法更适合较长或嵌套较深的数据；行内写法适合短列表。

### （3）映射

映射（mapping）是一组键值对，类似编程语言中的字典、哈希表或对象。

示例：

```yaml
user:
  name: Alice
  age: 18
  email: alice@example.com
```

其中 `user` 的值又是一个映射，内部包含 `name`、`age` 和 `email` 三个字段。

映射也可以写成行内形式：

```yaml
user: {name: Alice, age: 18, email: alice@example.com}
```

不过在配置文件中，通常更推荐多行写法，因为它更容易阅读、修改和做版本控制 diff。

# 三、YAML的语法规则

YAML 看起来比 JSON 简洁，但它对缩进和空格非常敏感。大多数 YAML 解析错误都来自缩进、冒号、短横线和类型推断。

## 1、使用缩进表示层级

YAML 不使用花括号表示嵌套，而是用缩进表达层级关系。

示例：

```yaml
server:
  host: 127.0.0.1
  port: 8080
  tls:
    enabled: true
    cert_file: /etc/app/cert.pem
```

这段数据可以理解为：

```text
server
├── host
├── port
└── tls
    ├── enabled
    └── cert_file
```

同一层级的字段必须左侧对齐：

```yaml
# 正确
server:
  host: 127.0.0.1
  port: 8080

# 错误：host 和 port 不在同一层级
server:
  host: 127.0.0.1
    port: 8080
```

## 2、不要使用 Tab 缩进

YAML 缩进必须使用空格，不能使用 Tab。实际项目中通常使用 2 个空格作为一级缩进。

```yaml
app:
  name: demo
  debug: true
```

> 注意：不要在同一个文件中混用 2 空格和 4 空格缩进。解析器可能能读懂其中一部分，但人很容易读错层级。

## 3、冒号后面要有空格

键值对使用 `键: 值` 的形式。冒号后面通常必须有一个空格。

正确写法：

```yaml
name: Alice
```

错误写法：

```yaml
name:Alice
```

第二种写法可能被解析为一个普通字符串，而不是键值对。

## 4、短横线后面要有空格

列表项使用 `- 值` 的形式，短横线后面也需要空格。

正确写法：

```yaml
items:
  - apple
  - orange
```

错误写法：

```yaml
items:
  -apple
  -orange
```

## 5、使用井号写注释

YAML 使用 `#` 表示注释。从 `#` 开始到行尾的内容会被解析器忽略。

示例：

```yaml
# 应用名称
name: demo

port: 8080 # HTTP 服务端口
```

如果 `#` 本身是字符串内容的一部分，建议使用引号：

```yaml
tag: "#backend"
```

# 四、复合结构

YAML 的真正价值在于可以把标量、序列和映射组合起来，表达复杂配置。

## 1、列表中包含对象

常见配置中，经常需要表示“一组对象”。例如一组用户：

```yaml
users:
  - name: Alice
    age: 18
    roles:
      - admin
      - editor
  - name: Bob
    age: 20
    roles:
      - viewer
```

这里 `users` 是一个列表，列表中的每一项都是一个映射。每个用户又包含一个 `roles` 列表。

等价的 JSON 大致如下：

```json
{
  "users": [
    {
      "name": "Alice",
      "age": 18,
      "roles": ["admin", "editor"]
    },
    {
      "name": "Bob",
      "age": 20,
      "roles": ["viewer"]
    }
  ]
}
```

可以看到，YAML 更适合人工阅读；JSON 更适合程序生成和传输。

## 2、对象中包含列表

对象中的某个字段也可以是列表：

```yaml
project:
  name: knowledge-base
  maintainers:
    - Alice
    - Bob
  tags:
    - data-format
    - documentation
```

这种结构适合描述一个主体及其多个属性。

## 3、多行文本

YAML 提供两种常用的多行文本写法：字面量块和折叠块。

字面量块使用 `|`，会尽量保留换行：

```yaml
script: |
  echo "start"
  npm install
  npm run build
```

解析后，文本中的每一行仍然是独立的一行。等价于：`echo "start"\nnpm install\nnpm run build\n`

它适合保存脚本、命令、邮件正文、系统提示词等需要保留换行的内容。

折叠块使用 `>`，会把普通换行折叠为空格，空行仍然表示分段：

```yaml
description: >
  YAML is a human-friendly
  data serialization format.

  It is often used for configuration.
```

解析后，第一段会变成一行，空行会保留为段落分隔。等价于：`YAML is a human-friendly data serialization format.\n\nIt is often used for configuration.\n`

它适合保存较长说明文字。

# 五、小结

YAML 是一种适合人类编写和维护的结构化数据格式。它用缩进表达层级，用冒号表达键值对，用短横线表达列表，因此在配置文件和自动化场景中非常常见。

学习 YAML 时，最重要的是掌握四点：

- 用空格缩进表达层级，不使用 Tab。
- 冒号和短横线后面要有空格。
- 列表、映射和纯量可以互相嵌套。
- 对容易被误判的字符串使用引号。

简单来说，YAML 牺牲了一部分语法严格性，换来了更高的可读性。机器之间传输数据时，[[1、JSON|JSON]] 通常更稳；人维护配置文件时，YAML 往往更顺手。
