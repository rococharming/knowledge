---
title: HTML 基础
date: 2026-06-29
tags: [frontend, html, 前端基础]
source_count: 1
---

# HTML 基础

## HTML 的定位

HTML 的全称是 **HyperText Markup Language（超文本标记语言）**，用于描述网页的 **内容和结构**。浏览网页时看到的标题、段落、链接、图片、视频等内容，通常都由 HTML 元素组织。

```html
<h1>我的前端学习记录</h1>

<p>这是我学习 HTML 时写下的第一个段落。</p>
```

## HTML / CSS / JavaScript 的分工

在一个现代网站中，HTML、CSS 和 JavaScript 各自承担不同职责：

| 技术         | 作用         | 建筑类比      |
| ---------- | ---------- | --------- |
| HTML       | 组织内容和结构    | 墙体、梁柱和地基  |
| CSS        | 控制颜色、排版和布局 | 室内与外观设计   |
| JavaScript | 添加交互和动态行为  | 水电及自动控制系统 |

- 仅展示少量文字和图片时，只用 HTML 也能完成
- 制作功能完善的现代网站，通常需要 HTML 配合 CSS 和 JavaScript

浏览器通过 [[HTTP 协议]] 从服务器获取 HTML 文档，再解析渲染成用户看到的页面。

## 知识点概览

本篇素材拆分为以下几个核心主题：

- [[HTML 元素]] — 元素的基本结构（开始标签 / 内容 / 结束标签）、嵌套、空元素（void element）
- [[HTML 属性]] — 属性语法、链接与图片的常用属性、布尔属性

## 完整示例

把标题、段落、链接、图片和复选框组合在一起：

```html
<h1>我的 HTML 学习页</h1>

<p>今天学习了 HTML 元素和属性。</p>

<a href="https://html.spec.whatwg.org/" target="_blank">
  查看 HTML 标准
</a>

<img
  src="https://placehold.co/480x240/0f766e/ffffff?text=HTML+Practice"
  alt="绿色背景上写着 HTML Practice 的练习图片"
>

<label>
  <input type="checkbox" checked>
  我已经完成今天的练习
</label>
```

## 关键要点

- HTML 负责网页的内容和结构，CSS 负责样式，JavaScript 负责交互
- 大多数 HTML 元素由开始标签、内容和结束标签组成
- 空元素只有开始标签，不能包含内容
- 属性写在开始标签中，用于补充信息或控制元素行为
- `href` 指定链接地址，`src` 指定图片资源，`alt` 提供图片替代文本
- `checked`、`disabled`、`readonly`、`required` 是常见的布尔属性

## 来源

- [[HTML的作用、元素与属性]]
