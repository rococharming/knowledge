---
title: 元数据、SEO与Open Graph
date: 2026-07-13
tags: [HTML, 前端基础, SEO, OpenGraph]
aliases:
  - HTML元数据
  - Meta Description
  - Open Graph
---

# 一、网页元数据的作用

网页不仅包含展示给用户的正文，也包含描述页面自身的信息，这些信息称为 **元数据（metadata）**。元数据通常写在 `head` 中，不直接显示在页面正文里。

示例：

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="一份面向初学者的 HTML 元数据学习指南。">
  <title>HTML 元数据学习指南</title>
</head>
```

`meta` 是空元素，不需要结束标签。`head` 的基础结构可回看 [[2、HTML文档骨架与资源引用#三、head 与 body 的分工|head 与 body 的分工]]。

不同元数据面向不同使用者：

| 元数据 | 主要使用者 | 主要作用 |
|---|---|---|
| `charset` | 浏览器 | 决定文本如何解码 |
| `viewport` | 浏览器 | 决定移动端布局视口 |
| Meta Description | 搜索引擎、用户 | 描述页面内容，可能显示在搜索结果中 |
| Open Graph | 社交平台、即时通信工具 | 控制链接分享卡片 |

# 二、SEO 与 Meta Description

## 1、SEO 是什么

SEO（Search Engine Optimization，搜索引擎优化）是通过改进网页内容、结构和技术实现，让搜索引擎更容易理解页面，并让目标用户更容易发现页面。

SEO 包含很多方面：

- 提供有价值且符合搜索需求的内容。
- 使用清晰的页面标题和内容结构。
- 改善加载速度和移动端体验。
- 确保搜索引擎能够正常抓取页面。
- 编写准确的页面描述。

Meta Description 只是 SEO 的一小部分，不能单独决定页面排名。

## 2、Meta Description 的语法

Meta Description 使用 `meta` 元素表示：

```html
<meta
  name="description"
  content="从 HTML 文档结构开始，学习常用元素、属性和语义化标签。"
>
```

其中：

- `name="description"` 表示这是页面描述。
- `content` 保存具体描述内容。

搜索引擎可能把它显示在搜索结果的标题和链接下方：

```text
HTML 入门学习指南
https://learn.example.com/html/getting-started
从 HTML 文档结构开始，学习常用元素、属性和语义化标签。
```

## 3、如何写好页面描述

有效的页面描述应该：

- 准确概括当前页面，而不是描述整个网站。
- 简洁自然，优先传达最重要的信息。
- 包含页面主题相关词语，但不堆砌关键词。
- 对用户有吸引力，同时避免夸张或误导。
- 不同页面使用不同描述。

不推荐：

```html
<meta
  name="description"
  content="HTML,HTML教程,HTML学习,HTML入门,前端,前端教程,网页教程"
>
```

更清晰：

```html
<meta
  name="description"
  content="通过可运行示例学习 HTML 基础，掌握文档结构、常用元素和语义化写法。"
>
```

> [!note] 搜索引擎不一定原样采用描述
> 搜索引擎会根据用户搜索词和页面正文决定摘要，有时使用 Meta Description，有时从正文中截取更相关内容。

# 三、Open Graph

## 1、Open Graph 的作用

Open Graph 是一种网页元数据协议，用于控制链接分享到社交平台或即时通信工具后，预览卡片如何展示。

它通常指定：

- 分享卡片标题。
- 内容类型。
- 预览图片。
- 页面标准地址。
- 内容摘要。

Open Graph 数据同样写在 `head` 中，但通常使用 `property` 属性，而不是 Meta Description 使用的 `name` 属性。

## 2、核心属性

常见 Open Graph 属性：

| 属性 | 作用 | 示例值 |
|---|---|---|
| `og:title` | 分享卡片标题 | `HTML 元数据入门指南` |
| `og:type` | 内容类型 | `article`、`website` |
| `og:image` | 预览图片 | `https://example.com/cover.png` |
| `og:url` | 页面标准地址 | `https://example.com/html/meta` |
| `og:description` | 分享摘要 | `认识 Meta Description 与 Open Graph。` |

示例：

```html
<meta property="og:title" content="HTML 元数据入门指南">
<meta property="og:type" content="article">
<meta
  property="og:image"
  content="https://learn.example.com/assets/html-meta-preview.png"
>
<meta
  property="og:url"
  content="https://learn.example.com/html/meta-tags"
>
<meta
  property="og:description"
  content="认识 Meta Description 与 Open Graph，改善网页在搜索和社交分享中的展示效果。"
>
```

`og:image` 和 `og:url` 通常应使用外部平台能够访问的完整 URL，而不是本地相对路径。

## 3、分享卡片对应关系

Open Graph 属性与社交媒体预览卡片的对应关系如下：

![[assets/HTML-Open-Graph-社交媒体预览.png|500]]

| Open Graph 属性 | 分享卡片中的位置 |
|---|---|
| `og:image` | 卡片预览大图 |
| `og:title` | 内容标题 |
| `og:description` | 标题下方摘要 |
| `og:url` | 页面来源或链接地址 |
| `og:type` | 网页、文章等内容类型 |

# 四、Meta Description 与 Open Graph 的区别

Meta Description 主要面向搜索结果，Open Graph 主要面向社交分享。二者都不会显示在正文中，也都不应被理解为“写了就能直接提高搜索排名”。

| 对比项 | Meta Description | Open Graph |
|---|---|---|
| 主要场景 | 搜索结果摘要 | 社交分享卡片 |
| 常用属性 | `name="description"` | `property="og:..."` |
| 是否显示在正文 | 否 | 否 |
| 是否直接决定排名 | 否 | 否 |
| 主要价值 | 帮助用户判断搜索结果 | 控制分享链接展示效果 |

Open Graph 的价值更多体现在传播体验：分享卡片更清晰时，用户更容易理解链接内容，也更可能点击。

# 五、完整 HTML 示例

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>HTML 元数据入门指南</title>
    <meta
      name="description"
      content="认识 Meta Description 与 Open Graph，改善网页在搜索和社交分享中的展示效果。"
    >

    <meta property="og:title" content="HTML 元数据入门指南">
    <meta property="og:type" content="article">
    <meta
      property="og:image"
      content="https://learn.example.com/assets/html-meta-preview.png"
    >
    <meta
      property="og:url"
      content="https://learn.example.com/html/meta-tags"
    >
    <meta
      property="og:description"
      content="认识 Meta Description 与 Open Graph，改善网页在搜索和社交分享中的展示效果。"
    >
  </head>
  <body>
    <main>
      <h1>HTML 元数据入门指南</h1>
      <p>学习如何改善网页在搜索结果和社交分享中的展示。</p>
    </main>
  </body>
</html>
```

# 六、小结

- 元数据描述页面自身信息，通常写在 `head` 中。
- Meta Description 使用 `name="description"` 和 `content` 描述页面内容。
- 搜索引擎可能使用页面描述作为搜索结果摘要，但不保证原样采用。
- Open Graph 控制网页链接在社交平台中的预览卡片。
- `og:title`、`og:type`、`og:image`、`og:url` 和 `og:description` 是常用核心属性。
- `og:image` 和 `og:url` 应使用外部平台可访问的完整 URL。
- 多媒体内容的嵌入与可访问性可继续看 [[5、音视频媒体与字幕可访问性|音视频媒体]]。
