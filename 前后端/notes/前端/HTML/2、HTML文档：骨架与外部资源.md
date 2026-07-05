---
title: HTML文档：骨架与外部资源
date: 2026-07-03
tags: [HTML, 前端基础, HTML文档结构]
source_count: 1
---

# 一、link元素

## 1、link元素的作用

`link` 元素用于建立当前 HTML 文档与外部资源之间的联系，常见用途包括：

- 引入外部 CSS 样式表
- 引入网站图标
- 提前连接外部资源所在的服务器

`link` 是一个 **空元素（void element）** ，不能包含内容，也不需要结束标签。关于空元素的基本概念，可以参考 [[1、HTML基础：元素与属性#2、空元素|空元素]]。

`link` 元素通常放在 `head` 元素中，因为它描述的是文档配置或文档与外部资源的关系，而不是直接展示在网页中的内容。

## 2、引入外部样式表

使用 `link` 元素可以将外部 CSS 文件应用到当前网页：

```html
<link rel="stylesheet" href="./css/main.css">
```

其中包含两个重要属性：

| 属性 | 作用 |
|---|---|
| `rel` | 说明外部资源与当前 HTML 文档之间的关系 |
| `href` | 指定外部资源所在的位置 |

在这个例子中：

- `rel="stylesheet"` 表示被链接的资源是一张样式表
- `href="./css/main.css"` 表示样式表位于当前目录下的 `css` 文件夹中

路径开头的 `./` 代表 **当前目录** 。假设项目结构如下：

```text
my-page/
├── index.html
└── css/
    └── main.css
```

那么，在 `index.html` 中可以使用 `./css/main.css` 找到这份样式表。

> [!tip] HTML与CSS分离
> 将页面结构写在 HTML 文件中，将样式写在独立的 CSS 文件中，可以减少重复代码，也更便于维护和复用。

## 3、引入外部字体

一个页面中可以使用多个 `link` 元素，分别加载样式表、字体和图标等不同资源。

下面以 Noto Sans SC 字体为例：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap"
>
```

`rel="preconnect"` 告诉浏览器提前与指定服务器建立连接。这样，当浏览器随后正式请求字体文件时，可以减少连接所需的等待时间。

第二个 `link` 上的 `crossorigin` 是一个布尔属性，表示该连接需要按跨源方式处理。

> [!note] preconnect只是一种性能提示
> 它不会替代真正的字体或样式表请求。只有页面确实会访问相应服务器时，提前连接才有意义。

## 4、设置网站图标

`link` 元素还可以设置 **favicon（网站图标）** ：

```html
<link rel="icon" href="./assets/code-icon.png" type="image/png">
```

- `rel="icon"` 表示链接的资源是网站图标
- `href` 指定图标文件的位置
- `type="image/png"` 说明资源的媒体类型是 PNG 图片

网站图标通常显示在浏览器标签页的网站标题旁边，可以帮助用户快速识别不同的网站。

# 二、HTML文档模板

## 1、什么是HTML文档模板

HTML 文档模板也常称为 **HTML boilerplate** ，它是一份可以重复使用的基础结构，包含 HTML 文档正常工作所需的核心元素。

创建新页面时从模板开始，可以：

- 避免遗漏必要的文档结构
- 提高创建页面的速度
- 让网页在不同浏览器中得到一致、规范的解析
- 方便在此基础上继续添加项目配置

一个适合中文网页的基础模板如下：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>前端学习清单</title>
  </head>
  <body>
    <h1>今天的学习任务</h1>
    <p>认识 HTML 文档的基本结构。</p>
  </body>
</html>
```

## 2、DOCTYPE声明

HTML 文档的第一行通常是 `DOCTYPE` 声明：

```html
<!doctype html>
```

它告诉浏览器使用现代 HTML 标准解析当前文档，从而避免浏览器进入兼容旧网页的怪异模式。

> [!note] DOCTYPE不是HTML元素
> `<!doctype html>` 是文档类型声明，不是普通的 HTML 标签或元素。

## 3、html根元素

`html` 是整个 HTML 文档的根元素，页面中的其他 HTML 元素都应位于它的内部：

```html
<html lang="zh-CN">
  <!-- head和body位于这里 -->
</html>
```

`lang` 属性用于声明页面内容的主要语言。中文简体页面通常使用 `zh-CN`：

```html
<html lang="zh-CN">
```

正确设置页面语言有助于屏幕阅读器选择合适的发音规则，也有助于浏览器提供翻译等功能。

## 4、head与body

`html` 元素内部主要分为 `head` 和 `body` 两部分：

```html
<html lang="zh-CN">
  <head>
    <!-- 文档配置和元数据 -->
  </head>
  <body>
    <!-- 页面上展示的主要内容 -->
  </body>
</html>
```

二者的职责不同：

| 元素 | 主要作用 | 常见内容 |
|---|---|---|
| `head` | 保存文档配置和元数据 | `meta`、`title`、`link` |
| `body` | 保存用户在页面中看到的主要内容 | 标题、段落、图片、链接 |

## 5、head中的常用元素

一个常见的 `head` 结构如下：

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>前端学习清单</title>
  <link rel="stylesheet" href="./css/main.css">
</head>
```

- `meta` 用于提供字符编码、移动设备视口等元数据
- `title` 决定浏览器标签页或窗口上显示的标题
- `link` 用于关联外部样式表等资源

`meta name="viewport"` 让页面宽度跟随设备屏幕宽度，并以正常比例显示，是移动端网页的常见配置。

## 6、body中的页面内容

网页中要实际展示给用户的主要内容应写在 `body` 中：

```html
<body>
  <h1>前端学习清单</h1>
  <p>今天完成 HTML 文档结构练习。</p>
</body>
```

标题、段落、图片、链接、表单等元素通常都属于 `body` 的内容。

# 三、UTF-8字符编码

## 1、什么是字符编码

计算机最终以二进制数据保存文本。 **字符编码（character encoding）** 规定了字符与字节数据之间的对应关系，使计算机知道一组字节应被解释成哪个字符。

一个字节由 8 个二进制位组成。网页中的文字、标点和符号，都会按照指定的字符编码转换为一个或多个字节。

如果文档保存时使用的编码与浏览器解析时使用的编码不一致，页面就可能出现乱码。

## 2、UTF-8的作用

UTF-8 是 Web 中广泛使用的 Unicode 字符编码。它可以表示 Unicode 字符集中的字符，包括：

- 汉字和其他语言文字
- 拉丁字母及其变体
- 标点符号
- 数学和技术符号
- Emoji

在 HTML 中，可以通过 `meta` 元素声明 UTF-8：

```html
<meta charset="UTF-8">
```

该元素应放在 `head` 中，并尽量靠近 `head` 的开头，让浏览器尽早确定文档编码。

## 3、UTF-8示例

下面的页面同时包含中文、带重音符号的字母和 Emoji：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>字符编码练习</title>
  </head>
  <body>
    <h1>多语言问候</h1>
    <p>你好，世界！</p>
    <p>Crème brûlée</p>
    <p>学习使人快乐 📚</p>
  </body>
</html>
```

声明 UTF-8 后，浏览器可以按照正确的编码解释这些字符。

> [!warning] 声明编码不等于转换编码
> HTML 中声明 `UTF-8` 的同时，文件本身也应以 UTF-8 编码保存。仅修改 `charset`，不会自动转换文件原有的编码。

# 四、完整模板

将本篇涉及的内容组合起来，可以得到下面这份基础模板：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>我的编程书签</title>

    <link rel="icon" href="./assets/bookmark-icon.png" type="image/png">
  </head>
  <body>
    <main>
      <h1>我的编程书签</h1>
      <p>在这里整理常用的学习资源。</p>
    </main>
  </body>
</html>
```

以后创建新的 HTML 文件时，可以先复制这份模板，再根据项目需要修改语言、标题和页面内容。

# 五、总结

- `link` 用于建立 HTML 文档与外部资源之间的关系
- `rel="stylesheet"` 表示链接的资源是样式表，`href` 指定资源位置
- `rel="preconnect"` 可以提示浏览器提前连接外部服务器
- `rel="icon"` 用于设置网站图标
- `link` 通常放在 `head` 中，并且不需要结束标签
- HTML 文档模板提供了创建网页所需的基础结构
- `html` 是根元素，其内部主要分为 `head` 和 `body`
- `head` 保存文档配置和元数据，`body` 保存页面的主要内容
- `<meta charset="UTF-8">` 用于声明文档采用 UTF-8 字符编码
- HTML 文件本身也应以 UTF-8 编码保存
