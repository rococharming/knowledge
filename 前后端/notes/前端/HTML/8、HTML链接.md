---
title: HTML链接
date: 2026-07-13
tags: [Web, 前端, HTML, 前端基础]
aliases:
  - 链接目标、路径语法与链接状态
  - HTML链接目标
  - HTML路径语法
---

# 一、链接不只是跳转

HTML 中的 `a` 元素用于创建超链接，`href` 决定“去哪里”，`target` 决定“在哪里打开”。链接看起来简单，但它同时涉及浏览上下文、文件路径和用户交互状态。

最基本的链接如下：

```html
<a href="https://example.com">访问示例网站</a>
```

`href` 的基础用法可回看 [[1、HTML基础#2、链接属性：href 与 target|链接属性]]。本篇重点整理三个进一步的问题：

- `target` 如何控制打开位置。
- 绝对路径、绝对 URL 和相对路径有什么区别。
- 链接在 CSS 中有哪些状态。

# 二、target 属性控制打开位置

## 1、target 的基本作用

`target` 是 `a` 元素上的属性，用来告诉浏览器把链接目标打开到哪个浏览上下文中。浏览上下文可以粗略理解为一个标签页、窗口，或者 `iframe` 内部的独立页面区域。

示例：

```html
<a href="https://example.com" target="_blank">
  访问示例网站
</a>
```

这段代码会尝试在新的浏览上下文中打开链接，通常表现为新标签页。

## 2、四个常用取值

`target` 的常用值都以下划线开头：

| 值 | 打开位置 | 典型场景 |
|---|---|---|
| `_self` | 当前浏览上下文 | 默认值，普通站内跳转 |
| `_blank` | 新浏览上下文 | 打开外部网站、文档或参考资料 |
| `_parent` | 当前上下文的父级 | 从 `iframe` 内跳到外层页面 |
| `_top` | 最顶层浏览上下文 | 从多层嵌套框架中跳出到整个标签页 |

如果没有写 `target`，默认就是 `_self`：

```html
<a href="./about.html">关于我们</a>
```

等价于：

```html
<a href="./about.html" target="_self">关于我们</a>
```

## 3、iframe 中的 parent 与 top

`_parent` 和 `_top` 只有在页面被嵌入时才比较容易看出差异。`iframe` 会创建独立浏览上下文，相关概念可回看 [[7、iframe与嵌入#三、iframe 的基本用法|iframe 的基本用法]]。

假设页面结构是：

```text
最外层页面
└── iframe A
    └── iframe B
        └── 当前链接
```

此时：

- `target="_parent"` 会把链接打开到 `iframe A` 这一层。
- `target="_top"` 会直接打开到最外层页面所在的完整标签页。

> [!note] `_unfencedTop`
> HTML 还存在 `_unfencedTop`，主要面向实验性的 Fenced Frame API。日常开发中通常不需要使用它。

## 4、使用 blank 时注意安全

新标签页打开外部链接时，常见写法是：

```html
<a
  href="https://developer.mozilla.org/"
  target="_blank"
  rel="noopener"
>
  MDN 文档
</a>
```

`rel="noopener"` 可以避免新页面通过 `window.opener` 影响原页面。学习阶段可以先形成习惯：外部链接使用 `target="_blank"` 时，顺手补上 `rel="noopener"`。

# 三、绝对路径、绝对 URL 与相对路径

## 1、路径是什么

路径是一段描述文件或目录位置的字符串。网页通过路径找到图片、样式表、脚本、其他页面等资源。

在 HTML 中，路径最常出现在这些属性里：

| 属性 | 常见元素 | 说明 |
|---|---|---|
| `href` | `a`、`link` | 链接页面或外部资源 |
| `src` | `img`、`script`、`iframe` | 加载图片、脚本或嵌入页面 |
| `poster` | `video` | 指定视频封面图 |

外部资源引用的基础结构可回看 [[2、HTML文档结构#五、link 元素与外部资源|link 元素与外部资源]]。

## 2、绝对路径

绝对路径从文件系统或站点根位置开始描述资源位置，包含完整层级。

本地机器上的绝对路径示例：

```html
<a href="/Users/user/Desktop/site/pages/about.html">
  About Page
</a>
```

它从根目录 `/` 开始，一层层进入 `Users`、`user`、`Desktop`、`site`、`pages`，最后找到 `about.html`。

> [!warning] 本地绝对路径不适合发布到网站
> `/Users/user/Desktop/...` 只在某台电脑上成立。网页发布到服务器后，访问者的电脑上通常没有这条路径。

## 3、绝对 URL

绝对 URL 是完整的网络地址，通常包含协议、域名和资源路径：

```html
<a href="https://cdn.example.com/assets/site-logo.svg">
  查看网站 Logo
</a>
```

其中：

- `https` 是协议，说明浏览器如何请求资源。
- `cdn.example.com` 是域名，说明去哪个服务器找。
- `/assets/site-logo.svg` 是服务器上的资源路径。

打开外部网站或引用外部 CDN 资源时，应使用绝对 URL。

## 4、相对路径

相对路径从当前文件所在目录出发查找资源，不包含协议和域名。

假设 `contact.html` 和 `about.html` 在同一个文件夹：

```text
pages/
├── contact.html
└── about.html
```

在 `contact.html` 中可以这样链接到 `about.html`：

```html
<a href="about.html">About Page</a>
```

相对路径更适合站内页面、图片、CSS 和 JavaScript 文件。项目移动到另一个目录或部署到服务器后，只要内部结构不变，链接仍然容易保持有效。

## 5、如何选择

| 写法 | 适合场景 | 例子 |
|---|---|---|
| 绝对路径 | 固定站点根路径或明确的本地文件位置 | `/assets/logo.png` |
| 绝对 URL | 外部网站、外部资源、CDN | `https://example.com/logo.png` |
| 相对路径 | 同一项目内部资源 | `./css/main.css` |

简单来说：

- 链到外部网站，用绝对 URL。
- 链到同一个项目里的文件，优先用相对路径。
- 从站点根目录开始定位资源时，可以用以 `/` 开头的根相对路径。

# 四、斜杠、单点与双点

## 1、斜杠是路径分隔符

斜杠用于分隔目录名和文件名。在 Web 路径中通常使用正斜杠 `/`：

```text
assets/images/logo.png
```

这表示：进入 `assets` 文件夹，再进入 `images` 文件夹，最后找到 `logo.png`。

路径结构不同，含义也不同：

```text
naomis-files/
naomis/files/
```

第一个是名为 `naomis-files` 的目录；第二个是 `naomis` 目录里面的 `files` 目录。

## 2、单点表示当前目录

`.` 表示当前目录。写成 `./` 时，通常是在明确告诉读者和工具：这是从当前文件所在目录开始的相对路径。

示例项目：

```text
my-app/
├── public/
│   ├── favicon.ico
│   └── index.html
└── src/
    ├── index.css
    └── index.js
```

如果 `public/index.html` 要引用同目录下的 `favicon.ico`：

```html
<link rel="icon" href="./favicon.ico">
```

这里的 `./favicon.ico` 表示“从 `index.html` 当前所在的 `public` 目录中找 `favicon.ico`”。

## 3、双点表示父目录

`..` 表示父目录，也就是当前目录的上一层。

仍然使用上面的项目结构，如果 `public/index.html` 要引用 `src/index.css`，需要先回到父目录 `my-app`，再进入 `src`：

```html
<link rel="stylesheet" href="../src/index.css">
```

路径拆开看是：

```text
..          回到 my-app/
/src        进入 src/
/index.css  找到 index.css
```

> [!note] 路径要从“当前文件”出发
> 相对路径不是从整个项目根目录自动开始，也不是从编辑器当前打开的目录开始，而是从写这条路径的 HTML、CSS 或 JS 文件所在位置开始。

# 五、链接状态与 CSS 伪类

## 1、链接状态为什么重要

链接状态用于向用户反馈“这个链接是否访问过、鼠标是否悬停、键盘是否聚焦、是否正在被点击”。这些反馈能帮助用户判断自己当前的位置和操作结果。

浏览器默认会给链接一些样式，例如未访问链接通常是蓝色，访问过的链接通常是紫色。CSS 可以通过伪类自定义这些状态。

## 2、五种常见状态

| 状态 | 含义 | 常见反馈 |
|---|---|---|
| `:link` | 未访问过的链接 | 基础链接颜色 |
| `:visited` | 已访问过的链接 | 提示用户曾经打开过 |
| `:hover` | 鼠标悬停在链接上 | 强调可点击性 |
| `:focus` | 链接获得键盘焦点 | 帮助键盘用户定位 |
| `:active` | 链接正在被激活 | 点击瞬间反馈 |

示例：

```css
a:link {
  color: blue;
}

a:visited {
  color: purple;
}

a:hover {
  color: red;
}

a:focus {
  color: green;
}

a:active {
  color: black;
}
```

## 3、书写顺序

链接伪类建议按下面顺序书写：

```css
a:link {}
a:visited {}
a:hover {}
a:focus {}
a:active {}
```

这个顺序可以避免后写的规则意外覆盖前面的状态。

## 4、不要只依赖颜色

颜色变化很直观，但并不是所有用户都能清楚区分颜色差异。重要链接状态可以配合下划线、轮廓或背景变化。

示例：

```css
a:hover,
a:focus {
  text-decoration-thickness: 2px;
}

a:focus {
  outline: 2px solid currentColor;
  outline-offset: 3px;
}
```

这里 `:hover` 照顾鼠标用户，`:focus` 照顾键盘用户。保留清晰的焦点样式，是链接可访问性的一部分。

# 六、完整示例

下面把链接目标、相对路径和链接状态组合成一个小页面：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>链接练习</title>
    <link rel="stylesheet" href="./styles.css">
  </head>
  <body>
    <main>
      <h1>前端学习链接</h1>

      <p>
        <a href="./pages/about.html">查看关于页面</a>
      </p>

      <p>
        <a
          href="https://developer.mozilla.org/"
          target="_blank"
          rel="noopener"
        >
          打开 MDN 文档
        </a>
      </p>
    </main>
  </body>
</html>
```

对应的 CSS：

```css
a:link {
  color: #0645ad;
}

a:visited {
  color: #6f42c1;
}

a:hover {
  color: #b00020;
}

a:focus {
  outline: 2px solid currentColor;
  outline-offset: 3px;
}

a:active {
  color: #111;
}
```

# 七、小结

- `href` 决定链接目标，`target` 决定链接在哪里打开。
- `_self` 是默认值，`_blank` 通常打开新标签页，`_parent` 和 `_top` 常用于嵌入页面。
- 外部网站使用绝对 URL；项目内部资源优先使用相对路径。
- `/` 分隔路径层级，`.` 表示当前目录，`..` 表示父目录。
- 相对路径要从当前文件所在目录出发理解。
- 链接状态包括 `:link`、`:visited`、`:hover`、`:focus` 和 `:active`。
- 写链接状态 CSS 时，推荐按 `link → visited → hover → focus → active` 的顺序。
