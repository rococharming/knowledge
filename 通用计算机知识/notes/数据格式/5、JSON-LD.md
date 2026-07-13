---
title: JSON-LD
date: 2026-07-12
tags:
  - data-format
  - json-ld
  - structured-data
  - semantic-web
aliases:
  - JSON for Linked Data
  - 结构化数据
  - Schema.org
---

# 一、JSON-LD 的基本概念

JSON-LD 是 JSON for Linked Data 的缩写，可以理解为“带语义的 JSON”。它仍然使用 [[1、JSON|JSON]] 的对象、数组、字符串等基础语法，但额外加入 `@context`、`@type`、`@id` 等关键字，用来说明数据字段的语义和实体之间的关系。

普通 JSON 主要解决**如何传输结构化数据**的问题，JSON-LD 进一步解决**这些字段到底是什么意思、它们描述的是谁、和其他数据有什么关系**的问题。

示例：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "JSON-LD 入门",
  "datePublished": "2026-07-12",
  "author": {
    "@type": "Person",
    "name": "Alice"
  }
}
</script>
```

这段数据通常不会直接显示在网页正文中，而是作为机器可读的结构化数据嵌入页面。搜索引擎、知识图谱工具和内容抓取程序可以读取它，从而知道这个页面描述的是一篇文章、文章标题是什么、发布时间是什么、作者是谁。

> 简单来说：JSON-LD = JSON 语法 + 语义词汇 + 可链接的实体标识。

# 二、为什么需要 JSON-LD

## 1、普通 JSON 只表达结构，不表达通用语义

普通 JSON 可以表达字段和值，但字段名的含义通常只在某个系统内部成立。

示例：

```json
{
  "name": "Alice",
  "date": "2026-07-12"
}
```

这段 JSON 对人来说容易猜，但对机器来说仍然有歧义：

- `name` 是人名、文章名、产品名，还是组织名？
- `date` 是创建日期、发布日期、修改日期，还是活动开始日期？
- 这份数据描述的是一个人、一篇文章，还是一个网页？

JSON-LD 用 `@type` 和标准词汇表补充这些语义。前面示例里的 `Article`、`headline`、`datePublished`、`Person`、`name` 都来自 Schema.org 这样的公共词汇表，因此不同系统可以用相同语义理解这份数据。

Schema.org 是一套面向网页结构化数据的公共词汇表，由 Google、Microsoft、Yahoo、Yandex 等搜索引擎共同推动。它预先定义了大量“类型”和“属性”：类型用来说明页面描述的对象是什么，例如 `Article`、`Person`、`Product`；属性用来说明对象有哪些信息，例如 `headline`、`author`、`datePublished`。JSON-LD 常用 Schema.org 作为词汇来源，所以网页里的结构化数据不只是“字段名相同”，而是“字段语义也相同”。

## 2、HTML 适合展示，JSON-LD 适合解释

网页 HTML 的主要职责是组织和展示内容。例如一个页面里可能有标题、正文、作者、发布时间、商品价格或 FAQ。

但是 HTML 标签本身通常只能说明“这是一个一级标题”“这是一个段落”“这是一个链接”，很难稳定说明“这是商品价格”“这是作者姓名”“这是文章发布日期”。这也是 RDF、Microdata、JSON-LD 这类结构化标记存在的原因：它们把数据的含义明确写出来。

JSON-LD 的好处是它不需要把语义标记散落到每个 HTML 元素上，而是可以集中放在一个 `script` 数据块里，页面展示逻辑和机器可读数据相对分离。

## 3、典型使用场景

- **搜索引擎优化**：帮助搜索引擎理解页面类型和字段，支持富媒体搜索结果。
- **知识图谱**：把网页中的人、组织、文章、商品、地点等实体连接起来。
- **内容抓取**：让爬虫和数据处理程序稳定提取标题、作者、发布日期、价格等字段。
- **数据集成**：不同系统使用同一套词汇表时，可以更容易合并数据。
- **语音助手和 AI 助手**：让机器更容易回答“这篇文章是谁写的”“这个活动什么时候开始”等问题。

# 三、JSON-LD 的核心关键字

## 1、@context

`@context` 用来声明当前 JSON-LD 使用哪套词汇表。最常见的是 Schema.org：

```json
{
  "@context": "https://schema.org"
}
```

有了 `@context`，`name`、`headline`、`author`、`offers` 等字段就不只是普通字符串键，而是可以被解释为某个词汇表中的语义属性。

也可以使用自定义上下文，为短字段名映射完整含义：

```json
{
  "@context": {
    "name": "https://schema.org/name",
    "homepage": "https://schema.org/url"
  },
  "name": "Alice",
  "homepage": "https://example.com"
}
```

日常网页结构化数据中，直接使用 `"https://schema.org"` 最常见。

## 2、@type

`@type` 表示当前对象是什么类型。类型通常来自 Schema.org。

常见类型：

| 类型 | 含义 | 适合页面 |
|---|---|---|
| `Article` | 通用文章 | 技术文章、长文 |
| `BlogPosting` | 博客文章 | 博客站点 |
| `NewsArticle` | 新闻文章 | 新闻页面 |
| `Product` | 产品 | 电商商品页 |
| `Offer` | 报价 | 商品价格、库存、销售条件 |
| `FAQPage` | 常见问题页面 | 静态 FAQ |
| `QAPage` | 问答页面 | 用户生成的问题和回答 |
| `Event` | 事件 | 会议、演出、活动 |
| `Organization` | 组织 | 公司、学校、机构 |
| `Person` | 人 | 作者、人物、讲师 |
| `WebSite` | 网站 | 站点首页或全站描述 |
| `WebPage` | 网页 | 单个网页描述 |

选择 `@type` 的关键是：它应该和页面主要内容一致。博客文章用 `BlogPosting`，商品页用 `Product`，活动页用 `Event`，不要为了搜索结果展示而标记页面中不存在的内容。

## 3、@id

`@id` 用来给一个实体提供稳定标识。它通常是 URL，也可以是带片段标识的 URL。

示例：

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://example.com/people/alice",
  "name": "Alice"
}
```

如果多个 JSON-LD 数据块引用同一个 `@id`，机器就可以理解它们描述的是同一个实体。这对知识图谱和复杂页面很重要。

## 4、@value 和 @language

`@value` 用来显式表示一个值，`@language` 用来标注文本语言。

示例：

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": {
    "@value": "示例产品",
    "@language": "zh"
  }
}
```

普通单语言网页通常不需要这样写，直接写 `"name": "示例产品"` 就够了。多语言内容、国际化站点或数据交换场景中，`@language` 会更有价值。

## 5、@graph

`@graph` 用来在一个 JSON-LD 数据块中声明多个实体。

示例：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebPage",
      "@id": "https://example.com/article/json-ld",
      "name": "JSON-LD 入门"
    },
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Example"
    }
  ]
}
</script>
```

当一个页面同时需要描述网页本身、站点、组织、文章、作者、面包屑导航等多个对象时，`@graph` 比分散写多个互不关联的 `script` 更清晰。不同实体之间还可以通过 `@id` 互相引用。

# 四、常见结构示例

## 1、文章

文章页面通常使用 `Article`、`BlogPosting` 或 `NewsArticle`。

示例：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "如何理解 JSON-LD",
  "description": "介绍 JSON-LD 的概念、语法和使用场景。",
  "datePublished": "2026-07-12T10:00:00+08:00",
  "dateModified": "2026-07-12T12:00:00+08:00",
  "author": {
    "@type": "Person",
    "name": "Alice"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "image": "https://example.com/cover.png",
  "url": "https://example.com/json-ld"
}
</script>
```

这里的重点不是把页面正文复制进 JSON-LD，而是提供文章的关键元数据：标题、摘要、发布时间、作者、发布者、封面图和 URL。

## 2、产品与报价

产品页面通常使用 `Product`，价格和库存放在嵌套的 `Offer` 中。

示例：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "无线耳机",
  "image": "https://example.com/headphone.png",
  "description": "一款支持主动降噪的无线耳机。",
  "sku": "HP-001",
  "brand": {
    "@type": "Brand",
    "name": "Example Audio"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/products/headphone",
    "priceCurrency": "CNY",
    "price": "299.00",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition"
  }
}
</script>
```

`Product` 描述产品本身，`Offer` 描述一次销售条件。这样区分后，同一个产品可以在不同渠道、不同价格、不同库存状态下被表达。

## 3、FAQ 页面

FAQ 页面用 `FAQPage`，问题放在 `mainEntity` 数组中。

示例：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "JSON-LD 必须写在 head 里吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "不必须。它可以放在 head 或 body 中，只要页面最终 HTML 中包含有效的 application/ld+json 数据即可。"
      }
    },
    {
      "@type": "Question",
      "name": "JSON-LD 会显示在页面上吗？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "通常不会。它放在 script 数据块中，主要供机器解析。"
      }
    }
  ]
}
</script>
```

`FAQPage` 适合页面已经明确展示了一组预设问题和答案的场景。如果是用户自由提问、答案由社区动态生成，更适合 `QAPage`。

## 4、网站与站内搜索

站点首页或全站可以用 `WebSite` 描述，并通过 `SearchAction` 表达站内搜索入口。

示例：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Example Docs",
  "url": "https://example.com",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://example.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
```

这类结构可以帮助机器理解站点名称、站点 URL，以及搜索 URL 如何构造。

# 五、实践规则与常见陷阱

## 1、内容必须和页面可见内容一致

JSON-LD 不应该凭空声明页面没有展示的信息。例如页面没有真实价格，就不要在 `Offer` 中写价格；页面不是 FAQ，就不要标记成 `FAQPage`。

搜索引擎通常会把结构化数据当作页面内容的补充说明，而不是绕过页面内容的隐藏通道。

## 2、优先选择最贴近的 @type

类型越贴近页面内容，机器越容易准确理解。

- 普通文章用 `Article`。
- 博客文章用 `BlogPosting`。
- 新闻报道用 `NewsArticle`。
- 产品页用 `Product`。
- 活动页用 `Event`。
- 常见问题页用 `FAQPage`。
- 本地商家用 `LocalBusiness`。

如果拿不准，先选择更通用的父类型，再逐步细化。例如不确定是否属于 `BlogPosting` 时，可以先用 `Article`。

## 3、嵌套对象要表达真实关系

JSON-LD 很常见的结构是对象嵌套对象。例如文章嵌套作者、产品嵌套报价、活动嵌套地点。

示例：

```json
{
  "@type": "Event",
  "name": "技术分享会",
  "location": {
    "@type": "Place",
    "name": "上海国际会议中心"
  }
}
```

这里的嵌套不是为了“把字段归类得好看”，而是在表达真实关系：这个活动发生在这个地点。

## 4、数组用于多个同类对象

当一个字段有多个值时，使用数组。例如多个作者、多个 FAQ 问题、多个社交链接。

示例：

```json
{
  "@type": "Organization",
  "name": "Example",
  "sameAs": [
    "https://github.com/example",
    "https://twitter.com/example"
  ]
}
```

数组中的对象最好结构一致，这和普通 JSON 的设计原则相同。

## 5、验证 JSON-LD

写完 JSON-LD 后至少做两层检查：

- **JSON 语法检查**：确认双引号、逗号、花括号、数组结构都合法。
- **结构化数据检查**：确认类型、字段和搜索引擎要求符合预期。

常用工具：

- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [JSON-LD Playground](https://json-ld.org/playground/)
- [Schema.org Validator](https://validator.schema.org/)

# 六、小结

JSON-LD 是一种面向机器理解的 JSON 结构化数据格式。它保留 JSON 的轻量语法，又通过 `@context` 引入词汇表，通过 `@type` 声明实体类型，通过 `@id` 标识实体，通过嵌套对象、数组和 `@graph` 表达更复杂的关系。

在网页开发中，JSON-LD 最常见的搭配是 Schema.org：Schema.org 提供类型和属性词汇，JSON-LD 负责把这些词汇写成网页里的结构化数据。理解这点之后，搜索引擎富媒体结果、知识图谱和结构化数据抓取都会更容易读懂。
