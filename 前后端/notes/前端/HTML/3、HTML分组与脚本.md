---
title: HTML分组与脚本
date: 2026-07-13
tags: [HTML, 前端基础, 语义化HTML, JavaScript]
aliases:
  - 语义化分组、标识符与脚本加载
  - div与section
  - id与class
---

# 一、分组元素解决结构组织问题

网页内容通常不是一堆孤立元素，而是由导航、主体、卡片、文章、侧栏、页脚等区域组成。分组元素的作用，就是把相关内容组织在一起，并尽量表达这组内容的含义。

HTML 分组有两条基本原则：

- 有明确语义时，优先使用语义化元素。
- 只是为了样式、布局或脚本操作时，再使用通用容器。

# 二、div 与语义化容器

## 1、div 的作用

`div` 是没有特定语义的通用块级容器。它常用于布局、样式分组或为 JavaScript 提供操作区域。

示例：

```html
<div class="study-card">
  <h2>HTML 基础</h2>
  <p>学习网页的结构与语义。</p>
</div>
```

这里的 `div` 本身不表示“文章”“导航”或“页眉”，只是把一组内容包在一起。

## 2、section 表示独立主题

`section` 表示文档中具有独立主题的一块区域，通常应该有标题：

```html
<section>
  <h2>网页结构</h2>
  <p>HTML 用于组织网页内容。</p>
</section>

<section>
  <h2>网页样式</h2>
  <p>CSS 用于控制网页的外观和布局。</p>
</section>
```

对比：

| 元素 | 是否有语义 | 适用场景 |
|---|---|---|
| `div` | 否 | 通用分组、布局容器、样式挂载点 |
| `section` | 是 | 文档中具有明确主题的独立区域 |
| `main` | 是 | 页面主要内容 |
| `nav` | 是 | 导航链接区域 |
| `header` | 是 | 页面或区块头部 |
| `footer` | 是 | 页面或区块底部 |

> [!tip] 先判断含义，再选择元素
> 如果 `main`、`article`、`nav`、`section`、`header` 或 `footer` 能准确描述内容，就优先使用它们；没有合适语义时再使用 `div`。

## 3、避免 div 滥用

不清晰的结构：

```html
<div class="page-header">
  <div class="navigation">
    <div class="navigation-link">首页</div>
  </div>
</div>
```

更清晰的写法：

```html
<header>
  <nav>
    <a href="./index.html">首页</a>
  </nav>
</header>
```

语义化结构更便于维护，也能帮助辅助技术理解页面结构。

# 三、id 与 class

## 1、id 是文档内唯一标识

`id` 用于给元素提供当前文档内唯一的标识符：

```html
<h1 id="page-title">前端学习路线</h1>
```

CSS 可以用 `#` 选择它：

```css
#page-title {
  color: darkgreen;
}
```

JavaScript 也可以通过 `id` 获取元素：

```javascript
const title = document.getElementById("page-title");
```

同一个 HTML 文档中，每个 `id` 值都应保持唯一。多个元素共享样式或状态时，应使用 `class`。

## 2、class 是可复用分类

`class` 可以应用到多个元素，也可以让一个元素拥有多个类名：

```html
<div class="note-card featured">重点笔记</div>
<div class="note-card">普通笔记</div>
```

CSS 使用 `.` 选择类名：

```css
.note-card {
  padding: 16px;
  border: 1px solid gray;
}

.featured {
  background-color: lightyellow;
}
```

对比：

| 对比项 | `id` | `class` |
|---|---|---|
| 是否应唯一 | 是 | 否 |
| 一个元素可使用几个 | 一个 `id` 值 | 多个类名 |
| CSS 选择符 | `#name` | `.name` |
| 常见用途 | 锚点、唯一元素、脚本定位 | 批量样式、状态、组件变体 |

## 3、命名建议

`id` 和 `class` 值不要包含空格。推荐使用有意义的英文、数字、连字符或下划线：

```html
<section id="html-basics" class="lesson-section">
  <h2>HTML 基础</h2>
</section>
```

命名不必追求复杂，关键是可读、稳定、风格一致。

# 四、字符引用

## 1、为什么需要字符引用

某些字符在 HTML 中具有特殊含义。比如正文里直接写 `<button>`，浏览器可能把它当作元素解析。

如果要显示文本形式的标签，应使用字符引用：

```html
<p>请使用 &lt;button&gt; 元素创建按钮。</p>
```

浏览器最终显示为：

```text
请使用 <button> 元素创建按钮。
```

## 2、常见字符引用

| 字符 | 命名字符引用 | 常见用途 |
|---|---|---|
| `<` | `&lt;` | 显示左尖括号 |
| `>` | `&gt;` | 显示右尖括号 |
| `&` | `&amp;` | 显示与号 |
| `"` | `&quot;` | 显示双引号 |
| 不换行空格 | `&nbsp;` | 插入不会自动换行的空格 |

示例：

```html
<p>HTML &amp; CSS 是前端基础。</p>
<p>&lt;h1&gt; 表示一级标题。</p>
```

> [!warning] 不要用 `&nbsp;` 排版
> `&nbsp;` 适合表达“这个空格不能换行”，不适合反复堆叠来控制页面间距。视觉间距应交给 CSS。

# 五、script 元素

## 1、script 的作用

`script` 用于嵌入或加载 JavaScript，为页面添加交互行为。

内联脚本示例：

```html
<button id="welcome-button" type="button">显示欢迎语</button>

<script>
  const button = document.getElementById("welcome-button");

  button.addEventListener("click", function () {
    alert("欢迎开始今天的前端练习！");
  });
</script>
```

内联脚本适合很短的演示。项目代码较多时，应放入独立 JavaScript 文件。

## 2、加载外部脚本

```html
<script src="./js/main.js"></script>
```

`src` 指定脚本文件位置。外部脚本让 HTML 专注内容结构，让 JavaScript 专注交互逻辑，符合关注点分离。

## 3、defer 与脚本位置

传统做法是把脚本放在 `body` 结束标签前：

```html
<body>
  <h1>前端学习页</h1>
  <script src="./js/main.js"></script>
</body>
```

现代写法常把脚本放在 `head` 中，并添加 `defer`：

```html
<head>
  <meta charset="UTF-8">
  <title>前端学习页</title>
  <script src="./js/main.js" defer></script>
</head>
```

`defer` 会让浏览器并行下载脚本，并在 HTML 文档解析完成后执行，避免脚本过早操作尚未创建的元素。

## 4、script 不是空元素

即使通过 `src` 加载外部文件，`script` 也必须写结束标签：

```html
<!-- 正确 -->
<script src="./js/main.js"></script>

<!-- 错误 -->
<script src="./js/main.js" />
```

普通 HTML 文档中，错误写法可能导致后续内容被浏览器误当作脚本内容。

# 六、完整示例

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML 知识卡片</title>
    <script src="./js/main.js" defer></script>
  </head>
  <body>
    <main>
      <h1 id="page-title">HTML 知识卡片</h1>

      <section aria-labelledby="element-title">
        <h2 id="element-title">常用元素</h2>

        <div class="knowledge-card important">
          <p>&lt;section&gt; 用于表示具有主题的内容区域。</p>
          <button id="mark-button" type="button">标记为已掌握</button>
        </div>
      </section>
    </main>
  </body>
</html>
```

对应的 `./js/main.js`：

```javascript
const button = document.getElementById("mark-button");

button.addEventListener("click", function () {
  button.textContent = "已掌握";
});
```

# 七、小结

- `div` 是无语义通用容器，适合布局、样式和脚本挂载。
- 内容有明确主题时，应优先使用 `section` 等语义化元素。
- `id` 是文档内唯一标识，`class` 是可复用分类。
- 字符引用可以安全显示 `<`、`>` 和 `&` 等特殊字符。
- `script` 用于嵌入或加载 JavaScript。
- 外部脚本建议使用 `src` 引入，常配合 `defer` 放在 `head` 中。
- 下一篇会整理 [[4、HTML元数据|元数据、SEO 与 Open Graph]]。
