---
title: CSS基础
date: 2026-07-29
tags: [Web, 前端, CSS, 前端基础]
aliases:
  - CSS入门
  - Cascading Style Sheets
  - CSS规则语法
---

# 一、CSS 的定位

CSS（Cascading Style Sheets，层叠样式表）负责描述网页的视觉表现：颜色、字体、间距、边框、布局、响应式变化和部分动画效果。HTML 负责表达内容结构与语义，CSS 则告诉浏览器这些结构应该如何呈现。

在一个页面里，三者的分工可以这样理解：

| 技术 | 核心职责 | 例子 |
|---|---|---|
| HTML | 内容结构与语义 | 标题、段落、图片、列表 |
| CSS | 视觉表现与布局 | 字号、颜色、间距、Flex、Grid |
| JavaScript | 交互与状态变化 | 点击按钮、请求数据、更新页面 |

![[css-basic-rendering-flow.png|700]]

这里的关键是：CSS 通常不改变 HTML 本身表达的语义，而是把样式规则应用到 HTML 元素上。前面学习 HTML 时已经接触过内容结构和语义，相关基础可回看 [[前后端/notes/前端/HTML/1、HTML基础|HTML 基础]]。

# 二、规则语法

## 1、规则的组成

CSS 的基本单位是一条 **规则（rule）**。一条常见规则由选择器和声明块组成：

```css
.profile-card {
  background-color: white;
  border: 1px solid #ddd;
  padding: 16px;
}
```

其中：

- `.profile-card` 是 **选择器（selector）**，表示这条规则要命中哪些元素。
- `{ ... }` 是 **声明块（declaration block）**，里面放具体样式。
- `background-color: white;` 是一条 **声明（declaration）**。
- `background-color` 是 **属性（property）**，`white` 是 **值（value）**。

简单来说，选择器负责“找谁”，声明负责“改成什么样”。

## 2、声明的写法

一条声明用冒号连接属性和值，通常用分号结束：

```css
color: #1f2937;
font-size: 18px;
line-height: 1.6;
```

最后一条声明的分号在语法上可以省略，但实际写代码时建议保留。这样以后追加新声明时，不容易因为漏分号造成样式失效。

CSS 对很多属性名和值不区分大小写，但实际开发中通常统一使用小写和短横线命名，例如 `background-color`、`font-size`。自定义类名也建议保持可读，而不是写成无意义缩写。

## 3、选择器的作用

选择器决定样式规则命中哪些元素。最常见的三类基础选择器是：

| 选择器 | 写法 | 命中对象 |
|---|---|---|
| 元素选择器 | `p` | 所有 `p` 元素 |
| 类选择器 | `.note` | 所有 `class` 包含 `note` 的元素 |
| ID 选择器 | `#main-title` | `id` 为 `main-title` 的元素 |

示例：

```html
<article class="profile-card">
  <h2 id="main-title">Ada Lovelace</h2>
  <p class="note">第一位程序员。</p>
</article>
```

```css
h2 {
  color: #111827;
}

.note {
  color: #4b5563;
}

#main-title {
  font-size: 28px;
}
```

这里 `h2` 命中所有二级标题，`.note` 命中带有 `note` 类名的元素，`#main-title` 只命中指定 ID 的元素。`class` 和 `id` 的 HTML 基础可回看 [[前后端/notes/前端/HTML/3、HTML分组与脚本#三、id 与 class|id 与 class]]。

# 三、引入方式

## 1、外部样式表

最常见的做法是把 CSS 写在单独的 `.css` 文件里，再在 HTML 的 `head` 中用 `<link>` 引入：

```html
<link rel="stylesheet" href="./styles.css">
```

```css
/* styles.css */
body {
  font-family: system-ui, sans-serif;
  color: #1f2937;
}
```

外部样式表适合真实项目，因为它能让结构和样式分离，也方便多个页面复用同一份样式。`link` 元素与外部资源的基础可回看 [[前后端/notes/前端/HTML/2、HTML文档结构#五、link 元素与外部资源|外部资源]]。

## 2、内部样式表

内部样式表一般写在 HTML 的`<head>`元素内的 `<style>` 元素中：

```html
<style>
  .notice {
    color: #b45309;
    background-color: #fff7ed;
  }
</style>
```

这种方式适合小实验、单页示例或临时演示。真实项目中如果样式越来越多，通常应该拆到外部 CSS 文件里。

## 3、行内样式

行内样式写在元素的 `style` 属性中：

```html
<p style="color: #2563eb;">这段文字是蓝色的。</p>
```

行内样式离元素最近，适合极少量一次性样式，但不适合长期维护。它会让结构和样式混在一起，也会增加后续覆盖样式的难度。

> [!warning] 初学时优先用外部 CSS
> 练习页面也可以从外部样式表开始。这样更容易养成“HTML 管结构、CSS 管表现”的习惯。

# 四、默认样式

## 1、浏览器样式

即使没有写任何 CSS，HTML 页面也会有一些基础外观。浏览器会提供一份默认样式，通常称为 **用户代理样式（user-agent styles）**。

常见默认表现包括：

| 元素 | 常见默认表现 | 作用 |
|---|---|---|
| `h1` - `h6` | 不同字号和加粗 | 表达标题层级 |
| `p` | 段落上下间距 | 区分正文段落 |
| `a` | 蓝色和下划线 | 暗示可点击链接 |
| `blockquote` | 缩进 | 区分引用内容 |
| `ul` / `ol` | 缩进、项目符号或编号 | 表达列表结构 |
| `hr` | 横线和上下间距 | 表达主题分隔 |

这些默认样式让纯 HTML 页面也能保持基本可读。它们不是 HTML 元素自带的“固定外观”，而是浏览器先帮页面提供了一层基础 CSS。

## 2、覆盖默认样式

自己写的 CSS 可以覆盖浏览器默认样式：

```css
a {
  color: #2563eb;
  text-decoration-thickness: 2px;
}

blockquote {
  margin-left: 0;
  padding-left: 16px;
  border-left: 4px solid #d1d5db;
}
```

覆盖默认样式时要注意语义和可用性。比如链接默认有下划线，是为了让用户看出它可以点击；如果删除下划线，通常需要用颜色、悬停状态或其他视觉线索补回来。
