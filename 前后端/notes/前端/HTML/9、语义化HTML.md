---
title: 语义化HTML
date: 2026-07-13
tags: [Web, 前端, HTML, 前端基础]
aliases:
  - 语义化HTML、结构层级与表现分离
  - HTML结构层级
  - 表现与语义分离
---

# 一、语义化 HTML 的基本概念

语义化 HTML 指的是：根据内容的含义选择元素，而不是只根据默认样式选择元素。HTML 不只是把文字放到页面上，它还负责告诉浏览器、搜索引擎和辅助技术“这段内容是什么”。

例如，段落应该使用 `p`：

```html
<p>
  今天整理了旅行笔记。
  其中最难忘的是傍晚时分的城市天际线。
</p>
```

这里 `p` 的语义是“一段正文”。相比只用 `div` 包住文字，`p` 能更明确地表达内容类型。

语义化元素不一定改变视觉效果，但会改变页面结构的可理解性。前面已经接触过 `header`、`nav`、`main`、`section`、`footer` 等语义化容器，可回看 [[3、HTML分组与脚本#二、div 与语义化容器|div 与语义化容器]]。

# 二、为什么要关心语义化

## 1、帮助辅助技术理解页面

屏幕阅读器等辅助技术会依赖 HTML 结构向用户说明页面内容。语义越清晰，用户越容易快速跳转到导航、主内容、标题、表单和链接。

对比：

```html
<div class="navigation">
  <div>首页</div>
  <div>文章</div>
  <div>关于</div>
</div>
```

更好的写法：

```html
<nav aria-label="主导航">
  <a href="./index.html">首页</a>
  <a href="./articles.html">文章</a>
  <a href="./about.html">关于</a>
</nav>
```

第二种写法不仅能显示导航链接，还能让辅助技术知道这是一组导航。

## 2、有利于搜索引擎理解内容

搜索引擎会解析页面结构，判断哪些内容是标题、正文、导航、主要内容和补充信息。语义化 HTML 能帮助搜索引擎更准确地理解页面主题。

SEO 不只是堆关键词。更稳定的做法是：用清晰标题组织内容，用合适元素表达结构，用准确元数据补充页面信息。元数据和搜索展示相关内容可继续看 [[4、HTML元数据|元数据与 SEO]]。

## 3、提升开发维护体验

语义化结构对开发者也更友好。看到 `nav` 就知道是导航，看到 `main` 就知道是页面主要内容，看到 `article` 就知道是一块可独立阅读的内容。

不清晰的结构：

```html
<div class="top">
  <div class="links">
    <a href="./index.html">首页</a>
  </div>
</div>
```

更清晰的结构：

```html
<header>
  <nav>
    <a href="./index.html">首页</a>
  </nav>
</header>
```

这类结构在项目变大后尤其重要，因为维护代码时不必在一堆 `div` 中猜测每一层的含义。

# 三、标题层级决定文档结构

## 1、h1 到 h6 表示标题级别

标题元素 `h1` 到 `h6` 表示文档标题层级。数字越小，级别越高。

常见结构如下：

```html
<main>
  <h1>前端学习路线</h1>

  <section>
    <h2>HTML 基础</h2>
    <p>学习网页内容结构。</p>
  </section>

  <section>
    <h2>CSS 基础</h2>
    <p>学习网页样式与布局。</p>
  </section>
</main>
```

`h1` 是页面最高级标题，`h2` 用于划分主要小节。一个页面通常只需要一个最主要的 `h1`，然后用多个 `h2` 组织内容。

## 2、不要跳级

标题层级应该像目录一样逐级展开，不要直接从 `h1` 跳到 `h3`。

不推荐：

```html
<section>
  <h1>前端学习路线</h1>
  <h3>HTML 入门</h3>
  <h2>CSS 入门</h2>
</section>
```

更合理：

```html
<section>
  <h1>前端学习路线</h1>
  <h2>HTML 入门</h2>
  <h2>CSS 入门</h2>
</section>
```

跳级会让屏幕阅读器用户误以为中间缺少内容，也会让搜索引擎和维护者更难判断页面结构。

> [!warning] 标题不是用来调字号的
> 不要因为 `h1` 默认更大，就把普通大字写成 `h1`。标题元素用于表达结构，字体大小应交给 CSS。

## 3、段落里不要塞标题

标题是结构元素，不应该放在普通段落内部。

不推荐：

```html
<article>
  <p>
    下面是重点：
    <h1>大型促销活动</h1>
  </p>
</article>
```

更合理：

```html
<article>
  <p>下面是重点：</p>
  <h2>大型促销活动</h2>
</article>
```

浏览器可能会尝试修正错误结构，但它的修正结果不一定符合开发者预期。写出有效、清晰的 HTML，能减少浏览器“猜测”的空间。

# 四、表现型 HTML 与语义化 HTML

## 1、表现型 HTML 关注外观

表现型 HTML 指的是用 HTML 元素直接控制视觉样式，而不是表达内容含义。早期 HTML 中常见的表现型元素包括 `font`、`center` 和 `big`。

例如：

```html
<font size="5" color="blue">这段文字又大又蓝。</font>
```

```html
<center>
  <p>这段内容居中显示。</p>
</center>
```

```html
<p>
  普通文字
  <big>更大的文字</big>
</p>
```

这些元素现在都不推荐使用。它们把“内容结构”和“视觉样式”混在一起，不利于可访问性、维护和响应式设计。

## 2、现代写法：HTML 管语义，CSS 管样式

现代 Web 开发通常遵循关注点分离：

| 层 | 负责什么 | 示例 |
|---|---|---|
| HTML | 内容结构与语义 | `article`、`nav`、`h1`、`p` |
| CSS | 外观、布局与响应式 | 颜色、字号、居中、间距 |
| JavaScript | 交互与状态变化 | 点击事件、动态渲染 |

同样的视觉效果，可以改成语义清晰的 HTML 加 CSS：

```html
<p class="lead-text">这段文字用于页面导语。</p>
```

```css
.lead-text {
  color: blue;
  font-size: 1.25rem;
  text-align: center;
}
```

这里 `p` 仍然表达“段落”，`class` 只是提供样式挂载点。`class` 的基础用法可回看 [[3、HTML分组与脚本#三、id 与 class|id 与 class]]。

## 3、语义化元素示例

常用语义化元素：

| 元素 | 语义 | 适合内容 |
|---|---|---|
| `header` | 页面或区块头部 | 标题、导航、介绍信息 |
| `nav` | 导航区域 | 主导航、目录、分页链接 |
| `main` | 页面主要内容 | 当前页面独有核心内容 |
| `section` | 有主题的内容区块 | 课程章节、功能分区 |
| `article` | 可独立分发或阅读的内容 | 博客文章、新闻、卡片文章 |
| `figure` | 插图、图表、代码示例等独立媒体 | 图片、图表、说明文字 |
| `footer` | 页面或区块底部 | 版权、补充链接、作者信息 |

示例：

```html
<article>
  <header>
    <h2>HTML 语义化入门</h2>
    <p>整理网页结构时，先判断内容含义。</p>
  </header>

  <figure>
    <img src="./images/html-outline.png" alt="一个由标题和章节组成的 HTML 文档大纲">
    <figcaption>HTML 文档大纲示意图。</figcaption>
  </figure>
</article>
```

`figure` 和图片相关语义可继续关联 [[6、HTML图片|响应式图片与 SVG]]。

# 五、选择元素的实用判断

## 1、先问内容是什么

选择元素时，可以先问自己：

- 这是不是页面主要内容？如果是，考虑 `main`。
- 这是不是导航链接集合？如果是，考虑 `nav`。
- 这是不是一篇可独立阅读的内容？如果是，考虑 `article`。
- 这是不是具有标题的主题区域？如果是，考虑 `section`。
- 只是为了布局或样式分组吗？如果是，可以使用 `div`。

这个判断顺序能避免“所有东西都用 `div`”。

## 2、不要为了默认样式选元素

HTML 元素的默认样式只是浏览器提供的基础外观，不应该决定元素选择。

| 错误思路 | 更好的思路 |
|---|---|
| 想要大字，所以用 `h1` | 这是几级标题？字号交给 CSS |
| 想要居中，所以用 `center` | 内容语义照常写，居中交给 CSS |
| 想要蓝色文字，所以用 `font` | 文字语义照常写，颜色交给 CSS |
| 不知道用什么，所以全用 `div` | 先判断是否有合适语义元素 |

## 3、结构清晰比元素数量更重要

语义化不是把所有语义元素都塞进页面，而是让结构刚好表达内容。简单页面可以很简单，复杂页面再分出更多区域。

示例：

```html
<main>
  <h1>今日学习记录</h1>

  <article>
    <h2>语义化 HTML</h2>
    <p>今天学习了标题层级、语义化容器和表现分离。</p>
  </article>
</main>
```

这段结构不复杂，但已经比纯 `div` 更清楚。

# 六、完整示例

下面是一份语义清晰、标题层级合理、样式职责分离的小页面：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>学习笔记首页</title>
    <link rel="stylesheet" href="./styles.css">
  </head>
  <body>
    <header>
      <nav aria-label="主导航">
        <a href="./index.html">首页</a>
        <a href="./html.html">HTML</a>
        <a href="./css.html">CSS</a>
      </nav>
    </header>

    <main>
      <h1>前端学习笔记</h1>

      <section aria-labelledby="html-title">
        <h2 id="html-title">HTML</h2>
        <p class="lead-text">HTML 负责描述网页内容结构与语义。</p>

        <article>
          <h3>语义化结构</h3>
          <p>根据内容含义选择元素，让页面更容易被人和机器理解。</p>
        </article>
      </section>
    </main>

    <footer>
      <p>持续整理前端基础知识。</p>
    </footer>
  </body>
</html>
```

对应 CSS：

```css
.lead-text {
  color: #1f4f8f;
  font-size: 1.125rem;
}
```

这里的关键是：HTML 负责结构，CSS 负责视觉。`h1`、`h2`、`h3` 按层级出现，`nav`、`main`、`section`、`article` 和 `footer` 都能表达各自区域的含义。

# 七、小结

- 语义化 HTML 是根据内容含义选择元素，而不是根据默认样式选择元素。
- 语义清晰有利于辅助技术、搜索引擎和开发维护。
- 标题层级应从 `h1` 逐级展开，不要随意跳级。
- `font`、`center`、`big` 等表现型元素已经不推荐使用。
- 现代写法应让 HTML 负责语义，CSS 负责样式，JavaScript 负责交互。
- 不确定用什么元素时，先判断内容含义；没有合适语义时再使用 `div`。
