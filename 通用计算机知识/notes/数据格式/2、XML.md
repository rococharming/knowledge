---
title: XML数据格式
date: 2026-07-03
tags: [计算机基础, 数据格式, XML, data-format]
aliases:
  - XML数据格式
  - XML
---

# 一、XML概述

XML 是 **Extensible Markup Language（可扩展标记语言）** 的缩写，是一种使用文本表示结构化数据的标记语言。

XML 本身不规定一套固定标签，而是提供一组语法规则，让使用者根据数据含义定义标签。例如，可以使用 XML 描述一本书：

```xml
<book>
  <title>计算机网络基础</title>
  <author>张明</author>
  <price currency="CNY">68</price>
</book>
```

这里的 `book`、`title`、`author` 和 `price` 都不是 XML 预先定义的标签，而是根据“书籍”这一数据模型自行设计的。

XML 的核心作用是：

> 使用带有名称的标签表达数据的层级、含义和关系。

常见使用场景包括：

- 系统或工具的配置文件
- 不同程序之间的数据交换
- 文档格式和办公文件
- Web Service 消息
- RSS、Atom 等订阅格式
- SVG 矢量图形

XML 是纯文本格式，可以使用文本编辑器打开，也便于程序读取和生成。但它描述的是数据，不负责决定数据如何显示。

# 二、XML的树形结构

## 1、元素与根元素

XML 文档由元素组成。一个普通元素包含开始标签、内容和结束标签：

```xml
<title>计算机网络基础</title>
```

其中：

- `<title>` 是开始标签
- `计算机网络基础` 是元素内容
- `</title>` 是结束标签

一份完整 XML 文档必须只有一个最外层的根元素，其他元素都位于根元素内部：

```xml
<library>
  <book>
    <title>计算机网络基础</title>
  </book>
  <book>
    <title>操作系统原理</title>
  </book>
</library>
```

这份数据可以理解为一棵树：

```text
library
├── book
│   └── title
└── book
    └── title
```

其中：

- `library` 是根元素
- `book` 是 `library` 的子元素
- `title` 是 `book` 的子元素

下面的写法不合法，因为它具有两个并列的最外层元素：

```xml
<book>第一本书</book>
<book>第二本书</book>
```

可以增加一个根元素解决：

```xml
<books>
  <book>第一本书</book>
  <book>第二本书</book>
</books>
```

## 2、属性

属性写在元素的开始标签中，用于补充元素信息：

```xml
<price currency="CNY">68</price>
```

在这个例子中：

- `price` 是元素名
- `currency` 是属性名
- `CNY` 是属性值
- `68` 是元素的文本内容

属性值必须使用单引号或双引号包裹：

```xml
<book id="b001" category='computer'>
  <title>计算机网络基础</title>
</book>
```

同一个元素中不能出现两个同名属性：

```xml
<!-- 错误：id属性重复 -->
<book id="b001" id="b002"></book>
```

元素和属性都能表达数据。通常可以按照下面的思路选择：

- 数据具有独立结构或将来可能继续扩展时，使用子元素
- 数据只是主体的简短附加信息时，可以使用属性

例如，作者有姓名、邮箱等结构时，使用元素更容易扩展：

```xml
<author>
  <name>张明</name>
  <email>zhangming@example.com</email>
</author>
```

## 3、空元素

没有文本和子元素的元素可以使用完整写法：

```xml
<cover></cover>
```

也可以使用自闭合写法：

```xml
<cover />
```

这两种写法在 XML 中表示相同的空元素。

需要注意，XML 中的 `/>` 确实表示自闭合；这与 HTML 空元素末尾的 `/` 没有实际作用不同。

# 三、XML语法规则

## 1、标签必须正确闭合

XML 对标签闭合要求严格。每个非空元素都必须具有对应的结束标签：

```xml
<!-- 正确 -->
<title>操作系统原理</title>

<!-- 错误：缺少结束标签 -->
<title>操作系统原理
```

## 2、元素必须正确嵌套

后开始的元素必须先结束：

```xml
<!-- 正确 -->
<book>
  <title>操作系统原理</title>
</book>
```

标签不能交叉嵌套：

```xml
<!-- 错误 -->
<book>
  <title>操作系统原理</book>
</title>
```

可以把它理解成括号配对：

```text
<book> <title> 内容 </title> </book>
  (       (             )       )
```

## 3、标签区分大小写

XML 的元素名和属性名区分大小写：

```xml
<title>XML基础</title>
```

必须使用完全相同的结束标签：

```xml
<!-- 错误：title与Title大小写不同 -->
<title>XML基础</Title>
```

`book`、`Book` 和 `BOOK` 在 XML 中会被视为三个不同的名称。

## 4、命名规则

XML 名称可以包含字母、数字、连字符、下划线等字符，但应遵守以下规则：

- 名称不能以数字开头
- 名称不能以任意大小写形式的 `xml` 开头
- 名称不能包含空格
- 名称中不能直接使用 `<`、`>` 等保留字符

示例：

```xml
<!-- 推荐 -->
<book-title>XML基础</book-title>
<publish_year>2026</publish_year>

<!-- 不合法或不推荐 -->
<1book>XML基础</1book>
<book title>XML基础</book title>
```

实际项目还应统一使用一种命名风格，避免同时混用 `book-title`、`book_title` 和 `BookTitle`。

# 四、声明、注释与字符引用

## 1、XML声明

XML 文档可以在第一行使用 XML 声明：

```xml
<?xml version="1.0" encoding="UTF-8"?>
```

- `version="1.0"` 表示使用 XML 1.0
- `encoding="UTF-8"` 表示文档使用 UTF-8 字符编码

XML 声明不是普通元素，没有结束标签。如果存在，它应位于文档开头。

完整示例：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<message>
  <sender>小林</sender>
  <content>你好，XML！</content>
</message>
```

声明的编码应与文件实际使用的编码一致，否则解析器可能无法正确读取内容。关于 UTF-8 可以参考 [[通用计算机知识/notes/1、字符编码#六、UTF-8|UTF-8]]。

## 2、注释

XML 注释使用下面的语法：

```xml
<!-- 这是一条注释 -->
```

注释不会作为普通数据内容处理：

```xml
<book>
  <!-- 书名用于页面展示 -->
  <title>XML基础</title>
</book>
```

XML 注释不能嵌套，注释内容中也不能出现连续的两个连字符 `--`。

## 3、字符引用

左尖括号、与号等字符在 XML 中具有语法含义。如果需要把它们作为普通文本使用，应写成字符引用：

| 字符 | 字符引用 | 说明 |
|---|---|---|
| `<` | `&lt;` | 左尖括号 |
| `>` | `&gt;` | 右尖括号 |
| `&` | `&amp;` | 与号 |
| `'` | `&apos;` | 单引号 |
| `"` | `&quot;` | 双引号 |

例如，希望文本内容表示 `5 < 10`：

```xml
<expression>5 &lt; 10</expression>
```

希望表示公司名称 `A & B`：

```xml
<company>A &amp; B</company>
```

尤其需要注意，普通文本中的 `&` 也必须转义，否则解析器会把它当作字符引用的开头。

## 4、CDATA区段

如果一段文本中包含大量 `<` 和 `&`，逐个转义会影响可读性。可以使用 CDATA 区段告诉解析器暂时把内容当作普通文本：

```xml
<example><![CDATA[
  if (a < b && b > 0) {
    print("valid");
  }
]]></example>
```

CDATA 的开始标记是 `<![CDATA[`，结束标记是 `]]>`。

# 五、命名空间

当一份 XML 文档组合多套标签时，不同来源可能使用相同的元素名，造成名称冲突。

例如，`table` 既可能表示家具中的桌子，也可能表示 HTML 表格：

```xml
<document>
  <table>木制书桌</table>
  <table>网页数据表格</table>
</document>
```

XML 命名空间使用 `xmlns` 声明一个名称前缀，用于区分不同的词汇体系：

```xml
<document
  xmlns:furniture="https://example.com/furniture"
  xmlns:web="https://example.com/web"
>
  <furniture:table>
    <furniture:material>木材</furniture:material>
  </furniture:table>

  <web:table>
    <web:column>姓名</web:column>
  </web:table>
</document>
```

在这里：

- `furniture` 和 `web` 是命名空间前缀
- `xmlns:furniture` 和 `xmlns:web` 分别声明前缀对应的命名空间
- `furniture:table` 与 `web:table` 因所属命名空间不同，不会发生冲突

命名空间 URI 的主要作用是提供唯一标识，不代表浏览器一定会访问该网址下载内容。

# 六、格式正确与结构有效

满足 XML 基本语法规则的文档称为 **格式正确（well-formed）** 的 XML，例如：

- 只有一个根元素
- 标签正确闭合
- 元素正确嵌套
- 属性值使用引号包裹
- 名称大小写匹配

但格式正确只说明语法没有问题，不代表数据结构符合业务要求。

假设图书数据规定每本书必须有书名和作者，下面的 XML 虽然语法正确，却缺少作者：

```xml
<book>
  <title>XML基础</title>
</book>
```

可以使用 DTD 或 XML Schema 描述允许出现的元素、属性、顺序和数据类型，再使用工具进行验证。

| 工具 | 作用 |
|---|---|
| DTD | 使用较早的规则语法描述 XML 结构 |
| XML Schema（XSD） | 使用 XML 语法描述结构，并支持更丰富的数据类型和约束 |

符合某套 DTD 或 XML Schema 规则的文档称为 **有效（valid）** 的 XML。

```text
格式正确：XML语法本身没有错误
有效：不仅语法正确，还符合指定的结构规则
```

# 七、XML与HTML、JSON的区别

## 1、XML与HTML

XML 和 HTML 都使用尖括号标签，但目标不同：

| 对比项 | XML | HTML |
|---|---|---|
| 主要目的 | 描述和交换数据 | 组织网页内容和结构 |
| 标签来源 | 使用者自行定义 | HTML 标准预先定义 |
| 大小写 | 区分大小写 | 标签名通常不区分大小写 |
| 语法容错 | 严格，错误通常导致解析失败 | 浏览器通常会尝试修复错误 |
| 自闭合语法 | `/>` 具有实际意义 | 空元素末尾的 `/` 通常没有作用 |

例如，XML 中的 `book` 标签表示什么，由当前数据格式的设计者决定；HTML 中的 `p`、`img` 等标签则具有标准规定的含义。

## 2、XML与JSON

XML 和 JSON 都能表示结构化数据：

```xml
<book id="b001">
  <title>XML基础</title>
  <price>68</price>
</book>
```

同一份数据可以用 JSON 表示：

```json
{
  "id": "b001",
  "title": "XML基础",
  "price": 68
}
```

| 对比项 | XML | JSON |
|---|---|---|
| 结构表达 | 元素、属性和文本 | 对象、数组和基本值 |
| 文本量 | 标签较多，通常更冗长 | 通常更紧凑 |
| 注释 | 支持 XML 注释 | 标准 JSON 不支持注释 |
| 命名空间 | 原生支持 | 没有内置命名空间机制 |
| 文档内容 | 适合文本与标记混合的文档 | 更适合常见程序数据交换 |
| 结构验证 | DTD、XSD 等成熟体系 | 可使用 JSON Schema 等方案 |

现代 Web API 经常使用 JSON；配置文件、文档标准、企业系统和具有复杂命名空间的数据中仍然可以见到 XML。

# 八、XML与SVG的关系

SVG 是使用 XML 语法定义的矢量图形格式。SVG 文件中的标签描述图形元素，属性描述位置、尺寸和样式：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 100 100"
>
  <circle
    cx="50"
    cy="50"
    r="40"
    fill="gold"
  />
</svg>
```

这个例子同时体现了多项 XML 规则：

- `svg` 是根元素
- `circle` 是 `svg` 的子元素
- `viewBox`、`cx`、`cy`、`r` 和 `fill` 是属性
- `circle` 没有内容，因此使用 `/>` 自闭合
- `xmlns` 声明 SVG 的默认命名空间
- 所有标签都正确嵌套和闭合

正因为 SVG 是文本形式的 XML，开发者可以使用编辑器查看其源码，也可以通过程序生成或修改图形。SVG 的图形知识可以参考 [[前后端/notes/前端/HTML/6、Web图像：优化授权与SVG#2、SVG结构与坐标系统|SVG结构与坐标系统]]。

# 九、完整示例

下面使用 XML 描述一个课程目录：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<catalog xmlns="https://example.com/course-catalog">
  <course id="html-001" level="beginner">
    <title>HTML基础</title>
    <description>学习网页元素、属性和文档结构。</description>
    <duration unit="minute">90</duration>
    <topics>
      <topic>元素与属性</topic>
      <topic>语义化结构</topic>
      <topic>多媒体元素</topic>
    </topics>
  </course>

  <course id="xml-001" level="beginner">
    <title>XML基础</title>
    <description>学习XML的树形结构和语法规则。</description>
    <duration unit="minute">60</duration>
    <topics>
      <topic>元素与属性</topic>
      <topic>命名空间</topic>
      <topic>结构验证</topic>
    </topics>
  </course>
</catalog>
```

这份文档具有一个根元素 `catalog`，其中包含两个 `course` 子元素。每个课程都通过属性记录编号和难度，通过子元素表达标题、说明、时长和主题列表。

# 十、总结

- XML 是用于描述和交换结构化数据的文本标记语言
- XML 标签由格式设计者自行定义
- XML 文档只有一个根元素，数据形成树形结构
- 元素必须正确闭合和嵌套，名称区分大小写
- 属性值必须使用引号包裹，同一元素不能有重复属性
- XML 使用字符引用表示具有语法含义的特殊字符
- XML 声明可以说明版本和字符编码
- 命名空间用于区分不同词汇体系中的同名元素
- 格式正确表示语法无误，有效表示文档还符合指定结构规则
- XML 更适合标记化文档、复杂数据规范和命名空间场景，JSON 通常更紧凑
- SVG 使用 XML 语法描述矢量图形
