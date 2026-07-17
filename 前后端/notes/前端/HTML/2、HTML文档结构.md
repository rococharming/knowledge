---
title: HTML文档结构
date: 2026-07-13
tags: [Web, 前端, HTML, 前端基础]
aliases:
  - HTML文档骨架与资源引用
  - HTML Boilerplate
  - 外部资源引用
---

# 一、HTML 文档骨架

HTML 文档骨架是一份网页能够被浏览器正确解析的基础结构。它定义文档类型、页面语言、元数据区域和实际显示内容区域。

一个适合中文页面的基础模板如下：

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

这类模板也常被称为 **HTML boilerplate**。创建新页面时从模板开始，可以减少遗漏，也能让页面行为更稳定。

# 二、文档声明与根元素

## 1、DOCTYPE 声明

`<!doctype html>` 位于文档第一行，用来告诉浏览器使用现代 HTML 标准解析页面：

```html
<!doctype html>
```

它不是普通 HTML 元素，而是文档类型声明。缺少它时，浏览器可能进入兼容旧页面的怪异模式，导致布局行为不符合现代标准。

## 2、html 根元素与 lang

`html` 是整个文档的根元素，页面中的 `head` 和 `body` 都位于它内部：

```html
<html lang="zh-CN">
  <head></head>
  <body></body>
</html>
```

`lang` 声明页面主要语言。中文简体页面通常使用 `zh-CN`。正确的语言声明有助于：

- 屏幕阅读器选择合适发音规则。
- 浏览器提供更准确的翻译提示。
- 搜索引擎理解页面语言。

# 三、head 与 body 的分工

## 1、head 保存页面配置

`head` 保存文档配置和元数据，通常不会直接显示在页面正文中。

常见内容包括：

| 元素 | 作用 |
|---|---|
| `meta` | 声明字符编码、视口、页面描述等元数据 |
| `title` | 设置浏览器标签页标题 |
| `link` | 关联样式表、图标、字体等外部资源 |
| `script` | 加载脚本，常搭配 `defer` |

示例：

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>前端学习清单</title>
  <link rel="stylesheet" href="./css/main.css">
  <script src="./js/main.js" defer></script>
</head>
```

更细的 SEO、Meta Description 和 Open Graph 会在 [[4、HTML元数据|元数据与 Open Graph]] 中展开。

## 2、body 保存可见内容

`body` 保存用户实际看到和操作的页面内容：

```html
<body>
  <main>
    <h1>前端学习清单</h1>
    <p>今天完成 HTML 文档结构练习。</p>
  </main>
</body>
```

标题、段落、列表、图片、链接、表单、音视频和嵌入内容通常都属于 `body`。

# 四、字符编码与视口

## 1、UTF-8 字符编码

字符编码规定字符如何转换成字节。网页保存编码与浏览器解析编码不一致时，页面可能出现乱码。

现代网页通常使用 UTF-8：

```html
<meta charset="UTF-8">
```

这个声明应尽量靠近 `head` 开头，让浏览器尽早确定编码。

示例：

```html
<p>你好，世界！</p>
<p>Crème brûlée</p>
<p>学习 HTML 很有趣。</p>
```

UTF-8 可以表示中文、拉丁字母变体、标点符号和大量 Unicode 字符。

> [!warning] 声明编码不等于转换文件编码
> HTML 中写了 `charset="UTF-8"`，文件本身也需要以 UTF-8 保存。只改声明不会自动转换原文件编码。

## 2、viewport 视口设置

移动端网页通常需要下面这行：

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

它告诉浏览器让页面布局宽度跟随设备宽度，并以正常比例显示。缺少它时，移动浏览器可能把页面当作宽桌面页面缩小显示，导致文字很小、交互困难。

# 五、link 元素与外部资源

## 1、link 的基本作用

`link` 用于建立当前 HTML 文档与外部资源之间的关系。它通常放在 `head` 中，是一个空元素，不能包含内容。

常见用途：

- 引入外部 CSS 样式表。
- 设置网站图标。
- 提前连接字体、接口或静态资源服务器。
- 声明预加载或替代资源。

关于空元素的基础概念，可回看 [[1、HTML基础#3、空元素|空元素]]。

## 2、引入外部样式表

```html
<link rel="stylesheet" href="./css/main.css">
```

| 属性 | 作用 |
|---|---|
| `rel` | 说明外部资源与当前文档的关系 |
| `href` | 指定资源地址 |

假设项目结构如下：

```text
my-page/
├── index.html
└── css/
    └── main.css
```

那么 `./css/main.css` 表示从当前 HTML 文件所在目录开始，进入 `css` 文件夹查找 `main.css`。

## 3、预连接与网站图标

字体服务或跨域资源有时可以提前建立连接：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

`preconnect` 是性能提示，不会替代真正的字体或样式表请求。只有页面确实会访问目标服务器时，它才有意义。

设置网站图标：

```html
<link rel="icon" href="./assets/code-icon.png" type="image/png">
```

网站图标通常显示在浏览器标签页标题旁边，帮助用户识别页面。

# 六、完整模板

下面是一份可以作为练习起点的完整模板：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>我的编程书签</title>
    <meta name="description" content="整理常用编程学习资源的个人书签页。">

    <link rel="icon" href="./assets/bookmark-icon.png" type="image/png">
    <link rel="stylesheet" href="./css/main.css">
    <script src="./js/main.js" defer></script>
  </head>
  <body>
    <main>
      <h1>我的编程书签</h1>
      <p>在这里整理常用的学习资源。</p>
    </main>
  </body>
</html>
```

# 七、小结

- HTML 文档骨架由 `DOCTYPE`、`html`、`head` 和 `body` 构成。
- `DOCTYPE` 让浏览器按现代标准解析页面。
- `html lang="zh-CN"` 声明页面主要语言。
- `head` 保存配置与元数据，`body` 保存可见内容。
- `meta charset="UTF-8"` 声明字符编码，但文件本身也要保存为 UTF-8。
- `meta viewport` 是移动端页面的基础配置。
- `link` 用于关联样式表、图标、字体连接等外部资源。
- 脚本加载和语义化分组会在 [[3、HTML分组与脚本|下一篇]] 继续整理。
