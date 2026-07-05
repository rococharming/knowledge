---
title: HTML结构：分组标识与脚本
date: 2026-07-03
tags: [HTML, 前端基础, 语义化HTML]
source_count: 1
---

# 一、div与内容分组

## 1、div元素的作用

`div` 是一个通用的块级容器，用于将多个 HTML 元素组织在一起。`div` 本身不表示特定含义，只负责分组。

示例：

```html
<div>
  <h2>今日学习进度</h2>
  <p>已经完成三个 HTML 知识点。</p>
</div>
```

在实际开发中，通常会在以下情况使用 `div`：

- 将需要应用相同 CSS 样式的元素组合起来
- 为页面布局创建容器
- 为 JavaScript 提供一个操作区域
- 没有更合适的语义化元素可用

例如，可以通过 `class` 为整个卡片容器应用样式：

```html
<div class="study-card">
  <h2>HTML基础</h2>
  <p>学习网页的结构与语义。</p>
</div>
```

## 2、div与section的区别

`div` 没有语义，而 `section` 表示文档中一个具有独立主题的区域。

例如，一组介绍前端三项核心技术的内容可以写成：

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

浏览器和辅助技术可以从 `section` 理解这是一段有主题的内容，而 `div` 只表示一个普通容器。

| 元素 | 是否具有语义 | 适用场景 |
|---|---|---|
| `div` | 否 | 通用分组、布局、样式容器 |
| `section` | 是 | 文档中具有明确主题的独立区域 |

`section` 通常应包含一个标题，用于说明这一部分的主题。

> [!tip] 先考虑语义，再使用div
> 如果 `main`、`article`、`nav`、`section`、`header` 或 `footer` 等元素能够准确描述内容，就优先使用这些语义化元素；没有合适元素时再使用 `div`。

## 3、避免过度使用div

虽然 `div` 很常见，但不应把页面中的所有内容都包裹成层层嵌套的 `div`：

```html
<!-- 不推荐：元素的含义不清晰 -->
<div class="page-header">
  <div class="navigation">
    <div class="navigation-link">首页</div>
  </div>
</div>
```

使用语义化元素后，结构会更加清楚：

```html
<header>
  <nav>
    <a href="./index.html">首页</a>
  </nav>
</header>
```

语义化结构更便于开发者阅读，也能帮助搜索引擎和屏幕阅读器理解页面。

# 二、id与class属性

## 1、id属性

`id` 属性为 HTML 元素提供一个在当前文档中唯一的标识符。

```html
<h1 id="page-title">前端学习路线</h1>
```

这个 `id` 可以被 CSS、JavaScript 和页面内链接引用。例如，CSS 使用 `#` 选择具有指定 `id` 的元素：

```css
#page-title {
  color: darkgreen;
}
```

JavaScript 也可以通过 `id` 获取这个元素：

```javascript
const title = document.getElementById("page-title");
```

同一份 HTML 文档中，每个 `id` 值都应保持唯一：

```html
<!-- 正确：两个元素的id不同 -->
<h1 id="page-title">前端学习路线</h1>
<h2 id="html-section">HTML基础</h2>
```

如果多个元素需要共享同一种标识，应使用 `class`，而不是重复使用同一个 `id`。

## 2、id的命名

`id` 值不能包含空白字符。下面的写法不合适：

```html
<h1 id="page title">前端学习路线</h1>
```

浏览器会把空格保留在 `id` 值中，这会给 CSS 选择和 JavaScript 操作带来麻烦。可以改用连字符：

```html
<h1 id="page-title">前端学习路线</h1>
```

HTML 允许 `id` 使用许多不同字符，但为了便于在 CSS 和 JavaScript 中引用，建议：

- 使用有意义的英文名称
- 使用字母、数字、连字符 `-` 或下划线 `_`
- 不要使用空格
- 保持命名风格一致

## 3、class属性

`class` 用于为元素指定一个或多个可复用的类名。与 `id` 不同，同一个类名可以应用到多个元素。

```html
<div class="note-card">
  <p>复习 HTML 元素。</p>
</div>
```

CSS 使用 `.` 选择具有指定 `class` 的元素：

```css
.note-card {
  padding: 16px;
  border: 1px solid gray;
}
```

多个元素可以共享同一个类名：

```html
<div class="note-card">HTML笔记</div>
<div class="note-card">CSS笔记</div>
<div class="note-card">JavaScript笔记</div>
```

## 4、一个元素使用多个class

`class` 属性可以包含多个类名，类名之间使用空格分隔：

```html
<div class="note-card featured">重点笔记</div>
```

这个 `div` 同时具有 `note-card` 和 `featured` 两个类，可以分别应用两组样式：

```css
.note-card {
  padding: 16px;
  border-radius: 8px;
}

.featured {
  background-color: lightyellow;
}
```

类名的顺序通常不会决定样式优先级。CSS 样式最终如何覆盖，取决于选择器优先级和规则出现顺序等因素。

## 5、id与class的选择

| 对比项 | `id` | `class` |
|---|---|---|
| 是否应唯一 | 是，同一文档中应唯一 | 否，可以重复使用 |
| 一个元素可使用几个 | 一个 `id` 值 | 多个类名 |
| CSS 选择符 | `#name` | `.name` |
| 常见用途 | 锚点、唯一元素、JavaScript 定位 | 批量设置样式、表示可复用状态 |

选择原则：

- 多个元素共享样式或行为时，使用 `class`
- 需要标识文档中的唯一元素时，使用 `id`
- 不要仅为了添加 CSS 样式而给每个元素创建 `id`

# 三、HTML字符引用

## 1、为什么需要字符引用

某些字符在 HTML 中具有特殊含义。例如，浏览器看到左尖括号后跟标签名时，会把它解释为 HTML 标签。

假设希望网页显示文本 `<button>`，直接写入正文可能会被浏览器当作元素：

```html
<p>请使用 <button> 元素创建按钮。</p>
```

这时可以使用 **字符引用（character reference）** 表示这些特殊字符：

```html
<p>请使用 &lt;button&gt; 元素创建按钮。</p>
```

浏览器最终显示为：

```text
请使用 <button> 元素创建按钮。
```

字符引用也常被称为 HTML 实体。它可以避免 HTML 解析器把需要展示的字符误认为标记语法。

## 2、命名字符引用

命名字符引用以 `&` 开头，以 `;` 结尾，中间是字符的名称。

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

> [!warning] 不要用多个nbsp控制布局
> `&nbsp;` 适合表达确实不能换行的空格，不适合用来反复缩进或排列页面。页面间距应交给 CSS 控制。

## 3、十进制数字字符引用

十进制数字字符引用由 `&#`、十进制数字和分号组成：

```html
<p>&#60;section&#62;</p>
<p>&#169; 2026 前端学习站</p>
```

其中：

- `&#60;` 表示 `<`
- `&#62;` 表示 `>`
- `&#169;` 表示版权符号 `©`

## 4、十六进制数字字符引用

十六进制数字字符引用以 `&#x` 开头，后面跟十六进制数字，并以分号结束：

```html
<p>&#x3C;nav&#x3E;</p>
<p>&#x2605; 收藏内容</p>
```

其中：

- `&#x3C;` 表示 `<`
- `&#x3E;` 表示 `>`
- `&#x2605;` 表示星形符号 `★`

命名、十进制和十六进制引用最终都用于表示字符。对于常见的保留字符，命名引用通常更容易阅读。

# 四、script元素

## 1、script元素的作用

`script` 元素用于在 HTML 文档中嵌入或加载可执行代码。网页开发中，它主要用于运行 JavaScript，为页面添加交互行为，例如：

- 响应按钮点击
- 切换菜单的显示状态
- 校验用户输入
- 更新页面内容
- 制作图片轮播或小游戏

可以直接在 `script` 元素内部编写 JavaScript：

```html
<button id="welcome-button">显示欢迎语</button>

<script>
  const button = document.getElementById("welcome-button");

  button.addEventListener("click", function () {
    alert("欢迎开始今天的前端练习！");
  });
</script>
```

这种方式称为内联脚本，适合非常短的演示代码。项目中的 JavaScript 较多时，通常应保存到独立文件中。

## 2、加载外部JavaScript文件

使用 `src` 属性可以加载外部 JavaScript 文件：

```html
<script src="./js/main.js"></script>
```

- `src` 是 source 的缩写，用于指定脚本文件的位置
- `./` 表示从当前目录开始查找
- `./js/main.js` 表示脚本位于当前目录下的 `js` 文件夹中

假设项目结构如下：

```text
my-page/
├── index.html
└── js/
    └── main.js
```

可以在 `index.html` 中这样加载脚本：

```html
<script src="./js/main.js"></script>
```

外部脚本能够让 HTML 专注于内容结构，让 JavaScript 专注于交互逻辑。这体现了 **关注点分离（separation of concerns）** 的设计原则。

## 3、script的放置位置

传统写法是将 `script` 放在 `body` 结束标签之前：

```html
<body>
  <h1>前端学习页</h1>

  <script src="./js/main.js"></script>
</body>
```

浏览器解析到脚本时，前面的页面元素通常已经创建，因此脚本可以操作这些元素。

另一种常见写法是将脚本放在 `head` 中，并使用 `defer` 属性：

```html
<head>
  <meta charset="UTF-8">
  <title>前端学习页</title>
  <script src="./js/main.js" defer></script>
</head>
```

`defer` 会让浏览器在解析 HTML 的同时下载脚本，并在文档解析完成后执行脚本，从而避免普通脚本阻塞后续 HTML 的解析。

> [!tip] 初学阶段的推荐方式
> 可以把外部脚本放在 `head` 中并添加 `defer`，这样资源引用集中在一起，脚本执行时页面结构也已经解析完成。

## 4、script不能使用空元素写法

`script` 不是空元素。即使通过 `src` 加载外部文件，也必须保留结束标签：

```html
<!-- 正确 -->
<script src="./js/main.js"></script>

<!-- 错误 -->
<script src="./js/main.js" />
```

在普通 HTML 文档中，第二种写法可能导致浏览器把后续内容错误地当作脚本内容。

# 五、完整示例

下面将语义化分组、`id`、`class`、字符引用和外部脚本组合到一个页面中：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML知识卡片</title>
    <script src="./js/main.js" defer></script>
  </head>
  <body>
    <main>
      <h1 id="page-title">HTML知识卡片</h1>

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

对应的 JavaScript 文件 `./js/main.js` 可以写成：

```javascript
const button = document.getElementById("mark-button");

button.addEventListener("click", function () {
  button.textContent = "已掌握";
});
```

# 六、总结

- `div` 是没有特定语义的通用容器，适合分组、布局和添加样式
- 内容具有明确主题时，应优先考虑 `section` 等语义化元素
- `id` 用于唯一标识元素，同一文档中不应重复
- `class` 可以重复使用，一个元素也可以拥有多个类名
- CSS 使用 `#name` 选择 `id`，使用 `.name` 选择 `class`
- 字符引用可以安全显示 `<`、`>` 和 `&` 等具有特殊含义的字符
- 字符引用分为命名引用、十进制数字引用和十六进制数字引用
- `script` 用于嵌入或加载 JavaScript
- 外部 JavaScript 通过 `src` 属性引入，有利于关注点分离
- `script` 不是空元素，必须写结束标签
- 将脚本放在 `head` 中时，可以使用 `defer` 延迟执行
