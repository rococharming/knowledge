---
title: JavaScript基础
date: 2026-07-30
tags: [Web, 前端, JavaScript, 前端基础]
aliases:
  - JS基础
  - JavaScript入门
  - ECMAScript
---

# 一、核心定位

JavaScript 是一种脚本语言，常用来给网页添加交互、状态变化和动态内容。HTML 负责页面结构，CSS 负责视觉表现，JavaScript 负责让页面“根据事情发生而做出反应”。

![[javascript-html-css-browser-handdrawn.png|700]]

在一个网页里，三者可以这样分工：

| 技术 | 核心职责 | 常见例子 |
|---|---|---|
| HTML | 内容结构与语义 | 标题、段落、按钮、表单 |
| CSS | 视觉表现与布局 | 颜色、字号、间距、Flex、Grid |
| JavaScript | 行为与状态 | 点击按钮、校验表单、请求数据、更新页面 |

前面已经学过 HTML 和 CSS。学习 JavaScript 时，可以先把它放在第三层：页面已经有结构和样式后，JavaScript 再根据用户操作或程序状态改变页面。

> 简单来说：HTML 描述“有什么”，CSS 描述“长什么样”，JavaScript 描述“发生事情后怎么办”。

# 二、运行环境

## 1、浏览器

浏览器是前端 JavaScript 最常见的运行环境。JavaScript 代码由浏览器内置的 JavaScript 引擎执行，同时可以通过浏览器提供的 DOM、事件、网络请求等能力控制页面。

示例：

```html
<button id="save-button">保存</button>

<script>
  const button = document.querySelector("#save-button");

  button.addEventListener("click", () => {
     alert()
  });
</script>
```

这里有两层能力需要区分：

- `const`、箭头函数、字符串等属于 JavaScript 语言本身。
- `document.querySelector`、`addEventListener` 属于浏览器提供给 JavaScript 的 Web API。

这也是初学时最容易混淆的边界：JavaScript 语言本身不等于浏览器；浏览器给 JavaScript 提供了操作网页的入口。

## 2、Node.js

JavaScript 也可以运行在浏览器之外。[[前后端/notes/后端/Node.js与npm/1、Node.js 和 npm|Node.js]] 是一种常见的 JavaScript 运行环境，它让 JavaScript 可以编写命令行程序、后端服务、构建工具和自动化脚本。

示例：

```js
console.log("Hello from Node.js");
```

如果这段代码保存为 `index.js`，可以在终端中用 Node.js 运行：

```bash
node index.js
```

同一门语言可以在不同环境中运行，但环境提供的能力不同：浏览器重点提供页面、DOM、事件和网络能力；Node.js 重点提供文件系统、进程、服务端网络等能力。

# 三、页面交互

## 1、事件

网页交互通常从 **事件（event）** 开始。用户点击按钮、输入文字、提交表单、移动鼠标，浏览器都会产生事件；JavaScript 可以注册处理函数，在事件发生时执行代码。

示例：

```html
<p id="message">还没有点击按钮。</p>
<button id="toggle-button">点我</button>

<script>
  const message = document.querySelector("#message");
  const button = document.querySelector("#toggle-button");

  button.addEventListener("click", () => {
    message.textContent = "按钮已经被点击。";
  });
</script>
```

这里的流程是：

```text
用户点击按钮
  ↓
浏览器触发 click 事件
  ↓
JavaScript 执行处理函数
  ↓
页面文字发生变化
```

## 2、状态

**状态（state）** 是程序当前记住的信息。页面是否展开、用户是否登录、购物车里有几个商品、游戏分数是多少，都可以看作状态。

示例：

```html
<p id="count">0</p>
<button id="add-button">加 1</button>

<script>
  let count = 0;
  const countText = document.querySelector("#count");
  const addButton = document.querySelector("#add-button");

  addButton.addEventListener("click", () => {
    count = count + 1;
    countText.textContent = String(count);
  });
</script>
```

`count` 保存当前数字。每次点击按钮，JavaScript 先更新 `count`，再把新的值显示到页面上。后续学习 [[3、变量声明|变量声明]] 时，会继续区分 `let` 和 `const` 分别适合保存什么。

# 四、编写位置

## 1、外部脚本

真实项目通常把 JavaScript 写在单独的 `.js` 文件中，再用 `script` 元素引入：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <title>JavaScript 练习页</title>
    <script src="./main.js" defer></script>
  </head>
  <body>
    <button id="save-button">保存</button>
  </body>
</html>
```

这行 `script` 通常放在 `head` 中。`src` 指向脚本文件，`defer` 表示浏览器会先继续解析 HTML，等文档结构解析完成后再执行 `main.js`。这样脚本执行时，页面里的按钮、段落等元素已经存在，JavaScript 才能安全地查找和操作它们。

也可以把不带 `defer` 的 `script` 放在 `body` 结束标签前：

```html
<body>
  <button id="save-button">保存</button>
  <script src="./main.js"></script>
</body>
```

入门和真实项目中，更推荐使用 `head` + `defer` 的写法：资源位置集中，执行时机也更清楚。外部脚本更容易维护，也能让 HTML、CSS、JavaScript 各自保持清晰边界。

## 2、内部脚本

小实验也可以把 JavaScript 直接写在 HTML 的 `script` 元素中：

```html
<script>
  console.log("页面脚本开始执行");
</script>
```

这种方式适合临时验证概念。等代码变多后，应拆到外部 `.js` 文件里，避免页面结构和交互逻辑混在一起。

# 五、调试入口

浏览器开发者工具里的 Console 是学习 JavaScript 的第一块练习场。后面会频繁看到 `console.log()`，先把它理解为“把括号里的内容显示到控制台，方便观察程序运行结果”。

示例：

```js
console.log("JavaScript 练习页");
```

`console.log()` 的输出不会出现在网页正文里，而是出现在开发者工具的 Console 面板中。它适合开发时观察结果，帮助确认代码是否真的执行。

> [!note] 开发者工具
> 开发者工具是浏览器提供给开发者检查网页的工具集合。它可以查看 HTML 结构、CSS 样式、网络请求、错误信息和 JavaScript 输出。刚开始学习 JavaScript 时，最常用的是 Console 面板。

在浏览器里观察输出，需要打开开发者工具，切换到 `Console` 面板：

![[assets/Pasted image 20260731004025.png|800]]

macOS 常用快捷键：

| 操作      | 快捷键                                                   |
| ------- | ----------------------------------------------------- |
| 打开开发者工具 | <kbd>Command</kbd> + <kbd>Option</kbd> + <kbd>I</kbd> |
| 刷新页面    | <kbd>Command</kbd> + <kbd>R</kbd>                     |
| 硬刷新     | <kbd>Command</kbd> + <kbd>Shift</kbd> + <kbd>R</kbd>  |

刷新页面就是让浏览器重新加载当前页面。普通刷新可能继续使用浏览器缓存里的 HTML、CSS 或 JavaScript 文件；硬刷新会更强地要求浏览器重新获取页面资源。学习 JavaScript 时，如果修改了 `.js` 文件但页面表现没有变化，可以先试一次硬刷新。

> [!warning] 控制台不是页面
> `console.log()` 只是把信息打印到 Console 面板里，不会修改用户看到的网页内容。后面学习 DOM 时，才会正式处理“把内容显示到页面上”的问题。
