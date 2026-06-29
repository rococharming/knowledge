---
title: HTML 属性
date: 2026-06-29
tags: [frontend, html, 前端基础]
source_count: 1
---

# HTML 属性

**属性（attribute）** 写在元素的开始标签中，用于提供额外信息或调整元素的行为。属性依附于 [[HTML 元素]]，对空元素同样适用。

## 属性的语法

基本语法：

```html
<element attribute="value">内容</element>
```

属性通常由三部分组成：

- 属性名
- 等号 `=`
- 使用引号包裹的属性值

属性值可以是字符串或数字，具体类型取决于属性本身。

## 链接的 href 和 target 属性

`a` 元素也叫 **锚元素（anchor element）**，用于创建超链接。开始标签与结束标签之间的文本是用户可以点击的部分。

```html
<a href="https://developer.mozilla.org/zh-CN/docs/Web/HTML" target="_blank">
  阅读 MDN HTML 文档
</a>
```

- `href` 指定链接的目标地址；没有它，链接就没有跳转目的地
- `target="_blank"` 表示在新的浏览器标签页中打开链接

## 图片的 src 和 alt 属性

显示图片时，需要通过 `src` 属性指定图片的位置：

```html
<img src="https://placehold.co/480x240/2563eb/ffffff?text=Learn+HTML">
```

为了提高可访问性，图片通常还应添加 `alt` 属性：

```html
<img
  src="https://placehold.co/480x240/2563eb/ffffff?text=Learn+HTML"
  alt="蓝色背景上写着 Learn HTML 的示例图片"
>
```

- `src` 指定要显示的图片资源
- `alt` 提供简短、准确的替代文本

当图片加载失败时，浏览器可能显示 `alt` 文本。更重要的是，屏幕阅读器可以读取它，从而帮助无法直接看到图片的用户理解图片内容。

> [!tip] 如何编写 alt 文本
> 描述图片传达的关键信息，而不是简单写"这是一张图片"。纯装饰图片可以使用空值 `alt=""`。

## 布尔属性（boolean attribute）

有些属性不需要设置属性值，只要出现在标签中就表示启用。这类属性称为 **布尔属性（boolean attribute）**。

例如 `input` 元素接收用户输入，将 `type` 设置为 `checkbox` 可创建复选框：

```html
<input type="checkbox" checked>
```

`checked` 表示复选框默认处于选中状态：

- 存在 `checked`：默认选中
- 移除 `checked`：默认不选中

其他常见布尔属性：

| 属性 | 作用 |
|---|---|
| `disabled` | 禁用元素，使其无法正常交互 |
| `readonly` | 内容只读，用户不能修改 |
| `required` | 表单提交前必须填写 |

例如，下面的文本输入框默认不可使用：

```html
<input type="text" disabled>
```

移除 `disabled` 后，用户便可以点击并输入内容。

> [!warning] 布尔属性看的是"是否存在"
> 对于布尔属性，决定状态的是属性是否出现在标签中，而不是给它写上 `true` 或 `false`。

## 来源

- [[HTML的作用、元素与属性]]
