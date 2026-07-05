---
title: HTML基础：元素与属性
date: 2026-07-03
tags: [HTML, 前端基础]
source_count: 1
---

# 一、HTML在网页中的作用

HTML 的全称是 **HyperText Markup Language（超文本标记语言）**，它用于描述网页的 **内容和结构**。

浏览网页时看到的标题、段落、链接、图片和视频等内容，通常都由 HTML 元素组织。例如：

```html
<h1>我的前端学习记录</h1>

<p>这是我学习 HTML 时写下的第一个段落。</p>
```

在一个现代网站中，HTML、CSS 和 JavaScript 通常各自承担不同的职责：

| 技术         | 作用         | 建筑类比      |
| ---------- | ---------- | --------- |
| HTML       | 组织内容和结构    | 墙体、梁柱和地基  |
| CSS        | 控制颜色、排版和布局 | 室内与外观设计   |
| JavaScript | 添加交互和动态行为  | 水电及自动控制系统 |

如果网页只需要展示少量文字和图片，仅使用 HTML 也可以完成；如果要制作功能完善的现代网站，通常还需要配合 CSS 和 JavaScript。

# 二、HTML元素

## 1、元素的基本结构

HTML 使用 **元素（element）** 表示网页内容。大多数元素由三部分组成：

1. 开始标签
2. 内容
3. 结束标签

示例：

```html
<p>每天学习一点前端知识。</p>
```

其中：

- `<p>` 是开始标签
- `每天学习一点前端知识。` 是元素的内容
- `</p>` 是结束标签

开始标签和结束标签都使用尖括号包围标签名。结束标签的左尖括号后面多了一个正斜杠 `/`。

元素的内容不仅可以是文本，也可以是其他 HTML 元素：

```html
<section>
  <h2>今日学习内容</h2>
  <p>认识 HTML 元素和属性。</p>
</section>
```

HTML 标签名不区分大小写，但开发中约定使用 **小写标签名**，这样更统一，也更易于阅读。

## 2、空元素

有些 HTML 元素只有开始标签，不能包含文本或其他元素，也不需要结束标签。这类元素称为 **空元素（void element）**。

例如，`img` 用于在网页中显示图片：

```html
<img>
```

实际开发中也可能看到在右尖括号前添加 `/` 的写法：

```html
<img />
```

在 HTML 中，这两种写法都很常见。末尾的 `/` 并不会让元素“自行闭合”，它在 HTML 语法中没有实际作用；一些代码格式化工具会自动保留这种形式。

> [!note] 空元素没有内容
> 空元素只能有开始标签，但仍然可以在标签中使用属性。

# 三、HTML属性

## 1、属性的概念与语法

**属性（attribute）** 写在元素的开始标签中，用于提供额外信息或调整元素的行为。

基本语法如下：

```html
<element attribute="value">内容</element>
```

属性通常由三部分组成：

- 属性名
- 等号 `=`
- 使用引号包裹的属性值

属性值可以是字符串或数字，具体类型取决于属性本身。

## 2、链接的href和target属性

`a` 元素也叫 **锚元素（anchor element）**，用于创建超链接。开始标签与结束标签之间的文本是用户可以点击的部分。

```html
<a href="https://developer.mozilla.org/zh-CN/docs/Web/HTML" target="_blank">
  阅读 MDN HTML 文档
</a>
```

- `href` 指定链接的目标地址；没有它，链接就没有跳转目的地
- `target="_blank"` 表示在新的浏览器标签页中打开链接

## 3、图片的src和alt属性

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

> [!tip] 如何编写alt文本
> 描述图片传达的关键信息，而不是简单写“这是一张图片”。纯装饰图片可以使用空值 `alt=""`。

## 4、布尔属性

有些属性不需要设置属性值，只要出现在标签中就表示启用。这类属性称为 **布尔属性（boolean attribute）**。

例如，`input` 元素可以接收用户输入。将 `type` 设置为 `checkbox`，可以创建复选框：

```html
<input type="checkbox" checked>
```

`checked` 表示复选框默认处于选中状态：

- 存在 `checked`：默认选中
- 移除 `checked`：默认不选中

其他常见布尔属性包括：

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

> [!warning] 布尔属性看的是“是否存在”
> 对于布尔属性，决定状态的是属性是否出现在标签中，而不是给它写上 `true` 或 `false`。

# 四、完整示例

下面把标题、段落、链接、图片和复选框组合在一起：

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

# 五、总结

- HTML 是用于描述网页内容和结构的标记语言
- 大多数 HTML 元素由开始标签、内容和结束标签组成
- 空元素不能包含内容，只有开始标签
- 属性写在开始标签中，用于补充信息或控制元素行为
- `href` 用于指定链接地址，`src` 用于指定图片资源，`alt` 用于提供图片替代文本
- `checked`、`disabled`、`readonly` 和 `required` 都是常见的布尔属性
- HTML 负责结构，CSS 负责样式，JavaScript 负责交互
