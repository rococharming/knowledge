---
title: JavaScript基础
date: 2026-07-30
tags: [Web, 前端, JavaScript, 前端基础]
aliases:
  - JS基础
  - JavaScript入门
  - ECMAScript
---

# 一、定位

JavaScript 是让网页产生行为和状态变化的编程语言。HTML 负责内容结构，CSS 负责视觉表现，JavaScript 负责响应用户操作、处理数据并更新页面。

![[javascript-html-css-browser-handdrawn.png|600]]

| 技术 | 核心职责 | 常见例子 |
|---|---|---|
| HTML | 内容结构与语义 | 标题、按钮、表单 |
| CSS | 视觉表现与布局 | 颜色、间距、Flex、Grid |
| JavaScript | 行为与状态 | 点击处理、表单校验、请求数据 |

JavaScript 是语言规范；浏览器或 Node.js 则是运行这门语言、并额外提供 API 的环境。不要把 JavaScript 与浏览器混为一谈。

# 二、运行环境

## 1、浏览器

浏览器内置 JavaScript 引擎，并提供 DOM、事件和网络请求等 Web API。下面的 `const`、箭头函数和字符串是语言本身；`document.querySelector()` 与 `addEventListener()` 是浏览器 API。

```html
<button id="save-button">保存</button>

<script>
  const button = document.querySelector("#save-button");

  button.addEventListener("click", () => {
    console.log("已点击");
  });
</script>
```

## 2、Node.js

[[前后端/notes/后端/Node.js与npm/1、Node.js 和 npm|Node.js]] 让 JavaScript 可以在浏览器外运行，常用于命令行工具、后端服务和构建脚本。

```js
console.log("Hello from Node.js");
```

将代码保存为 `index.js` 后，可在终端执行：

```bash
node index.js
```

同一段 JavaScript 在不同环境中的语言规则相同，但可调用的 API 不同。本系列以浏览器 JavaScript 为主。

# 三、编写与执行

## 1、外部脚本

真实项目通常将代码放在 `.js` 文件，再由 HTML 引入。`defer` 会让浏览器先解析 HTML，等文档结构可用后再执行脚本。

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

也可以把不带 `defer` 的 `script` 放在 `body` 结束标签前。学习时可先在 HTML 内写小段脚本；代码变多后应拆到外部文件。

## 2、控制台

`console.log()` 会把值输出到浏览器开发者工具的 Console 面板，不会显示在网页正文中。它是验证代码是否执行、观察变量值的第一种工具。

```js
const message = "Hello, world";

console.log(message);
```

> [!note] 开发者工具
> 以 Chrome 为例，可按 <kbd>F12</kbd> 或右键页面后选择“检查”打开开发者工具，再切到 Console 面板。

![[assets/Pasted image 20260811104613.png|200]]

![[assets/Pasted image 20260731004025.png|600]]

# 四、交互与状态预览

网页交互通常由事件开始：用户点击按钮，浏览器触发 `click` 事件，JavaScript 执行处理函数并改变页面。函数、DOM 与事件会在后续专题展开；这里先用它理解 JavaScript 的用途。

```html
<p id="count">0</p>
<button id="add-button">加 1</button>

<script>
  let count = 0;
  const countText = document.querySelector("#count");
  const addButton = document.querySelector("#add-button");

  addButton.addEventListener("click", () => {
    count += 1;
    countText.textContent = String(count);
  });
</script>
```

`count` 是程序当前记住的 **状态**。每次点击先更新状态，再把结果显示到页面；`let` 与 `const` 的选择见 [[3、变量声明|变量声明]]。
