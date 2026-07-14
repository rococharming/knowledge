---
title: HTML引用、缩写、地址与时间
date: 2026-07-14
tags: [HTML, 前端基础, 语义化HTML, 可访问性, 文本语义]
aliases:
  - HTML引用与时间语义
  - blockquote与q
  - abbr address time
---

# 一、文本与时间语义元素解决什么问题

HTML 不只负责把文字显示出来，还要说明这些文字在内容中的身份：这是引用、这是缩写、这是联系信息、这是一个可被机器识别的时间。

这类元素通常不会带来复杂的默认样式，但会让页面对浏览器、搜索引擎和辅助技术更清晰。它们延续的是 [[9、语义化HTML|语义化 HTML]] 的核心原则：先表达内容含义，再把外观交给 CSS。

本篇整理四组常用元素：

| 元素 | 语义 | 典型场景 |
|---|---|---|
| `blockquote` | 块级引用 | 长引用、多段引用 |
| `q` | 行内引用 | 段落中的短句引用 |
| `abbr` | 缩写、首字母缩略词 | HTML、CSS、API 等缩写说明 |
| `address` | 联系信息 | 作者、公司、站点维护者的联系方式 |
| `time` | 日期或时间 | 发布时间、活动时间、预约时间 |

# 二、blockquote 与 q：长引用和短引用

## 1、blockquote 表示块级引用

`blockquote` 用于表示从其他来源引用的一整块内容，适合较长的引用、独立成段的引用，或者包含多个段落的引用。

示例：

```html
<blockquote cite="https://www.freecodecamp.org/news/learn-to-code-book/">
  <p>
    Can you imagine what it would be like to be a successful developer?
    To have built software systems that people rely upon?
  </p>
</blockquote>
```

这里 `blockquote` 表示整段内容来自外部来源。`cite` 属性提供来源 URL，它不会直接显示在页面上，但能为搜索引擎、辅助技术和后续维护提供语义信息。

> [!note] `cite` 属性不是可见出处
> `cite` 属性提供机器可读的来源信息；如果希望用户在页面上看到出处，需要额外写可见文本。

## 2、多段引用可以放在同一个 blockquote 中

如果一段引用包含多个自然段，可以在同一个 `blockquote` 中放多个 `p` 元素。

示例：

```html
<blockquote cite="https://www.freecodecamp.org/news/learn-to-code-book/">
  <p>Build your projects. Show them to your friends.</p>
  <p>Build your network. Help the people you meet along the way.</p>
  <p>It is not too late. Life is long.</p>
</blockquote>
```

这些 `p` 都属于同一段来源引用。浏览器通常会让 `blockquote` 相对周围内容缩进，但不要把它理解为“缩进样式工具”；它的核心语义是“这是一段块级引用”。

## 3、cite 元素用于标记作品标题

如果要在页面上显示引用来源，可以在 `blockquote` 外写一段可见说明，并用 `cite` 元素标记作品标题。

示例：

```html
<figure>
  <blockquote cite="https://www.freecodecamp.org/news/learn-to-code-book/">
    <p>
      Can you imagine what it would be like to be a successful developer?
    </p>
  </blockquote>
  <figcaption>
    Quincy Larson,
    <cite>How to Learn to Code and Get a Developer Job</cite>
  </figcaption>
</figure>
```

这里有三个层次：

- `blockquote` 表示引用内容。
- `cite` 属性保存来源 URL。
- `cite` 元素标记作品标题。

`figure` 和 `figcaption` 让引用与说明形成一组独立内容，相关结构可回看 [[9、语义化HTML#3、语义化元素示例|语义化元素示例]]。

## 4、q 表示行内短引用

`q` 用于段落中的短引用。它是行内元素，适合引用几个词或一句短话。

示例：

```html
<p>
  As Quincy Larson said,
  <q cite="https://www.freecodecamp.org/news/learn-to-code-book/">
    Momentum is everything.
  </q>
</p>
```

多数现代浏览器会自动给 `q` 的内容加引号。和 `blockquote` 一样，`q` 也可以使用 `cite` 属性提供来源 URL。

## 5、如何选择 blockquote 和 q

| 问题 | 选择 |
|---|---|
| 引用内容是否独立成块、较长或包含多段？ | 用 `blockquote` |
| 引用内容是否只是段落中的短句？ | 用 `q` |
| 是否需要给用户看到出处？ | 额外写可见出处，可配合 `cite` 元素 |
| 是否只是想让文字缩进或加引号？ | 用 CSS 或普通文本，不要滥用引用元素 |

需要注意的是，如果使用 `blockquote` 时希望开头和结尾出现引号，通常需要自己写入引号；`blockquote` 不会像 `q` 那样自动补引号。

# 三、abbr：让缩写更容易理解

## 1、abbr 表示缩写

`abbr` 用于标记缩写、首字母缩略词和首字母拼读词。它的价值是说明“这段短文本是一个缩写”，并且可以通过 `title` 属性提供完整含义。

示例：

```html
<p>
  <abbr title="HyperText Markup Language">HTML</abbr>
  is the foundation of the web.
</p>
```

这里 `HTML` 是缩写，`title` 写出完整形式。浏览器可能会显示虚线下划线，并在鼠标悬停时显示提示，但具体样式取决于浏览器。

## 2、缩写、首字母缩略词和首字母拼读词

常见缩写可以分为两类：

| 类型 | 读法 | 示例 |
|---|---|---|
| Acronym | 像单词一样读 | NASA、GUI |
| Initialism | 一个字母一个字母读 | HTML、CSS、API |

它们都可以用 `abbr` 表示。是否区分 acronym 和 initialism，更多是写作和发音层面的判断；在 HTML 中，统一使用 `abbr` 即可。

## 3、第一次出现时优先解释完整含义

当缩写可能让读者困惑时，第一次出现应写出完整含义，后续再使用缩写。

示例：

```html
<p>
  <abbr title="Application Programming Interface">API</abbr>
  is a way for programs to communicate with each other.
</p>
```

这种写法同时照顾了视觉阅读和机器可读语义。对于非常常见、上下文已经足够明确的缩写，不必每次都使用 `abbr`，否则文本会变得啰嗦。

> [!tip] 只给需要解释的缩写加 abbr
> `abbr` 的目标是补充理解，不是把每一个大写单词都标记一遍。优先处理第一次出现、专业性较强或容易误解的缩写。

# 四、address：表示联系信息

## 1、address 的语义是联系信息

`address` 用于表示与当前页面、文章、站点或某个区块相关的联系信息。它可以包含作者、组织、邮寄地址、电话、邮箱、社交链接等。

示例：

```html
<address>
  <p>Company Name</p>
  <p>
    1234 Elm Street<br>
    Springfield, IL 62701<br>
    United States
  </p>
  <p>
    Phone:
    <a href="tel:+15555555555">+1 (555) 555-5555</a>
  </p>
  <p>
    Email:
    <a href="mailto:contact@company.com">contact@company.com</a>
  </p>
</address>
```

这里 `address` 的重点不是“地址排版”，而是“这是一组联系方式”。`br` 用于在邮寄地址中保留自然换行，空元素的基础概念可回看 [[1、HTML基础#3、空元素|空元素]]。

## 2、tel 与 mailto 链接

联系方式经常搭配链接使用：

```html
<p>
  <a href="tel:+15555555555">Call us</a>
</p>

<p>
  <a href="mailto:contact@company.com">Email us</a>
</p>
```

`tel:` 链接可在支持电话能力的设备上发起拨号；`mailto:` 链接会尝试打开用户默认邮件客户端。链接的基础属性和安全习惯可回看 [[8、HTML链接|HTML 链接]]。

## 3、不要把所有地址都写成 address

`address` 表示联系信息，不是所有“地理地址”都应该用它。

适合使用 `address` 的场景：

- 公司联系页中的公司地址、电话、邮箱。
- 文章作者的联系方式。
- 网站页脚中的站点维护者联系信息。

不适合使用 `address` 的场景：

- 游记里提到的某个景点地址。
- 小说正文中的一段地址。
- 订单详情里普通展示的配送地址。

如果只是普通内容中的地点信息，使用 `p`、`span`、`dl` 等更合适。描述列表可回看 [[10、HTML文本语义与描述列表#五、描述列表 dl、dt 与 dd|描述列表]]。

# 五、time：让日期和时间机器可读

## 1、time 表示具体时间或日期

`time` 用于表示日期、时间、日期时间或持续时间。它可以让页面中人类可读的时间，同时拥有机器可读的格式。

示例：

```html
<p>
  The reservation is for
  <time datetime="20:00">8:00 PM</time>.
</p>
```

用户看到的是 `8:00 PM`，机器读取的是 `20:00`。这对搜索引擎、日历工具、浏览器处理和结构化信息都更友好。

## 2、datetime 提供标准格式

`datetime` 属性保存机器可读的时间值。常见写法包括：

| 表达 | 示例 |
|---|---|
| 年 | `2026` |
| 年月 | `2026-07` |
| 日期 | `2026-07-14` |
| 本地时间 | `20:00` |
| 日期时间 | `2026-07-14T20:00` |
| 带时区日期时间 | `2026-07-14T20:00:00+08:00` |
| 持续时间 | `PT2H30M` |

示例：

```html
<p>
  The workshop starts on
  <time datetime="2026-07-14T20:00:00+08:00">
    July 14, 2026 at 8:00 PM
  </time>.
</p>
```

这里 `T` 用于分隔日期和时间，`+08:00` 表示东八区时区偏移。

## 3、什么时候使用 time

适合使用 `time` 的场景：

- 文章发布日期、更新时间。
- 活动开始时间、结束时间。
- 预约、会议、课程时间。
- 商品促销截止时间。
- 可被日历或搜索引擎理解的日期。

普通文本里只是泛泛说“明天”“晚上”“很久以前”，如果没有明确时间点，不一定需要使用 `time`。

> [!warning] 可见文本和 datetime 不要互相矛盾
> 如果页面显示“June 15”，但 `datetime` 写成 `2026-07-14`，机器和用户会得到不同信息。维护时间内容时要同时检查可见文本和 `datetime`。

# 六、整体选择方法

## 1、先判断文本角色

这些元素的选择可以按文本角色判断：

| 内容角色 | 推荐元素 |
|---|---|
| 一整段或多段外部引用 | `blockquote` |
| 段落中的短引用 | `q` |
| 缩写或首字母形式 | `abbr` |
| 联系方式 | `address` |
| 明确日期或时间 | `time` |

这和 [[10、HTML文本语义与描述列表|文本语义元素]] 的判断方式一致：不要先看默认样式，而要先判断这段内容在表达什么。

## 2、属性负责补充机器可读信息

本篇元素经常通过属性补充语义：

| 属性 | 常见元素 | 作用 |
|---|---|---|
| `cite` | `blockquote`、`q` | 引用来源 URL |
| `title` | `abbr` | 缩写的完整含义 |
| `href` | `a` | 电话、邮箱或外部链接 |
| `datetime` | `time` | 机器可读日期或时间 |

属性是 HTML 语义的重要组成部分。属性的基础结构可回看 [[1、HTML基础#三、属性为元素补充信息|属性为元素补充信息]]。

## 3、一个综合示例

示例：

```html
<article>
  <h1>Web Accessibility Notes</h1>

  <p>
    <abbr title="HyperText Markup Language">HTML</abbr>
    semantics help browsers and assistive technologies understand content.
  </p>

  <blockquote cite="https://example.com/accessibility-guide">
    <p>Good structure is the first layer of accessibility.</p>
  </blockquote>

  <p>
    The next workshop starts at
    <time datetime="2026-07-14T20:00:00+08:00">
      8:00 PM on July 14, 2026
    </time>.
  </p>

  <address>
    Contact:
    <a href="mailto:learn@example.com">learn@example.com</a>
  </address>
</article>
```

这段代码把四类信息分别表达清楚：缩写、引用、时间和联系信息。页面样式可以后续用 CSS 控制，但 HTML 本身已经提供了稳定的内容结构。

# 七、小结

`blockquote` 和 `q` 用于区分长引用与短引用，`abbr` 用于给缩写补充完整含义，`address` 用于标记联系信息，`time` 用于让日期和时间机器可读。

它们的共同点是：默认样式不是重点，语义才是重点。写 HTML 时先判断内容角色，再选择元素和属性，能让页面更可访问、更利于维护，也更容易被搜索引擎和工具正确理解。
