---
title: Obsidian Web Clipper
date: 2026-07-12
tags:
  - Obsidian
  - Web-Clipper
  - 浏览器插件
  - 知识管理
aliases:
  - Web Clipper
  - Obsidian 剪藏
---

# 一、概述

Obsidian Web Clipper 是 Obsidian 官方推出的浏览器插件，用于将网页内容以 Markdown 形式直接保存到 Obsidian Vault，方便离线阅读、标注和整理。

它不仅可以保存文本形态的网页，还可以一键获取 YouTube 视频里的文字稿。所有的内容最终都会以 Markdown 格式保存下来。

核心特点：

- **一键剪藏网页**：把网页正文以及标题、作者、发布日期等元数据保存到 Obsidian
- **高亮与选择保存**：可以在网页上高亮重要段落并选择特定页面元素保存
- **阅读器模式**：它带有类似阅读器的干净视图，适合将网页中的广告、侧边栏等干扰去掉再阅读或剪藏
- **隐私和可控性好**：内容保存到本地知识库，不收集个人数据

# 二、安装

可以从浏览器官方扩展商店获取 Obsidian Web Clipper。

也可以进入 https://obsidian.md/clipper 添加，如下图所示：

![[assets/Pasted image 20260622011526.png|600]]

如果是 Google 浏览器，点击 **Add to Chrome** 添加；如果是其他浏览器，点击 `More browsers` 选择支持的浏览器添加。

添加之后，就可以在浏览器上使用 Obsidian Web Clipper 插件了：

![[assets/Pasted image 20260622011703.png|600]]



# 三、快速上手：第一次剪藏

## 1、捕获页面

默认情况下，Obsidian Web Clipper 会尝试智能提取页面的主要文章内容，排除页面上的其他元素。

要将页面保存到 Obsidian，点击 **添加到 Obsidian** 按钮：

![[assets/Pasted image 20260712172429.png|300]]


弹出提示，选择"打开 Obsidian"：

![[assets/Pasted image 20260622012525.png|400]]

此时，网页内容以 Markdown 的形式保存到了本地 Obsidian 仓库下的 `Clippings` 目录。

结果如下：

![[assets/Pasted image 20260712171656.png|600]]


## 2、下载图片

使用 Obsidian Web Clipper 时，图片不会自动下载。图片会链接到其网络 URL。这可以节省仓库空间，但意味着在离线状态下或 URL 失效时图片将无法访问。

![[assets/Pasted image 20260712171912.png|600]]

可以在 Obsidian 中使用 <kbd>Command</kbd> + <kbd>P</kbd>（macOS）或 <kbd>Ctrl</kbd> + <kbd>P</kbd>（Windows）唤出命令面板，搜索 **下载当前文件内的所有附件** 来下载任何文件中的图片。

![[assets/Pasted image 20260622013542.png|500]]

![[assets/Pasted image 20260712172023.png|600]]

或者在**设置 -> 快捷键**中为**下载当前文件内的所有附件**设置快捷键。


## 3、界面功能

Obsidian Web Clipper 界面分为四个部分：

1. 顶部栏：切换模板、界面变量、高亮、打开阅读视图，在页面中打开以及设置
2. 属性：显示从页面中提取的元数据，这些数据将作为属性保存到 Obsidian 顶部的属性列表
3. 笔记内容：保存到 Obsidian 中的正文内容
4. 底部栏：允许你选择要保存到仓库的文件夹，并添加到 Obsidian

![[assets/Pasted image 20260712172340.png|300]]

# 四、模板与变量

## 1、模板的概念

模板决定了剪藏内容以什么格式保存到 Obsidian。Web Clipper 允许创建模板，自动捕获和组织网页中的元数据。官方示例模板可参考 https://github.com/kepano/clipper-templates 。

要**创建**模板，进入 Web Clipper 设置并点击侧边栏中的**新建模板**按钮。

![[assets/Pasted image 20260622030528.png]]

模板使用了变量和筛选器，让你可以自定义内容的保存方式。

## 2、变量

### （1）概念

Obsidian Web Clipper 的模板并不是一段固定文本。模板中的变量会在剪藏网页时，被替换为当前页面中的实际数据。

例如，在模板中写入：

```
# 原始正文

{{content}}
```

剪藏网页后，`{{content}}` 会被替换为 Web Clipper 从当前页面中提取出的正文。

变量的基本语法是：

```
{{变量}}
```

例如 `{{title}}`、`{{url}}`、`{{author}}`、`{{content}}` 等。


### （2）查看当前页面变量

不同网站提供的元数据并不完全相同，点击 Web Clipper 页面上的 `...` 图标可以访问当前页面的变量：

![[assets/Pasted image 20260712173326.png|300]]


制作模板时，可以先检查页面提供了哪些数据，再决定使用哪种变量。

例如，某些网页可以正确识别 `{{author}}`、`{{published}}`，另一些网页可能无法识别这些信息，此时需要改用 Meta、Schema.org、选择器或提示变量。

### （3）变量类型

Web Clipper 支持五类变量：

| 类型            | 数据来源                  | 主要特点            |
| ------------- | --------------------- | --------------- |
| 预设变量          | Web Clipper 自动解析的页面信息 | 简单、通用           |
| Meta 变量       | HTML 中的 `<meta>` 标签   | 适合描述、封面和分享信息    |
| Schema.org 变量 | 页面中的 JSON-LD 结构化数据    | 语义明确，适合文章、图书和商品 |
| 选择器变量         | 页面中的 HTML 元素          | 精确，但依赖网站结构      |
| 提示变量          | 语言模型对页面的分析结果          | 灵活，但速度较慢且可能产生费用 |

这些变量可以在同一个模板中组合使用。

### （4）预设变量

预设变量由 Web Clipper 根据当前页面自动生成，通常适用于大多数网站。

常用预设变量：

| 变量                  | 内容                   |
| ------------------- | -------------------- |
| `{{title}}`         | 页面标题                 |
| `{{url}}`           | 当前页面 URL             |
| `{{author}}`        | 页面作者                 |
| `{{site}}`          | 网站名称或发布者             |
| `{{domain}}`        | 当前页面域名               |
| `{{description}}`   | 页面描述或摘要              |
| `{{image}}`         | 页面社交分享图片 URL         |
| `{{favicon}}`       | 网站图标 URL             |
| `{{published}}`     | 页面发布日期               |
| `{{date}}`          | 执行剪藏时的当前日期           |
| `{{time}}`          | 执行剪藏时的当前日期和时间        |
| `{{words}}`         | 内容字数                 |
| `{{content}}`       | 主要内容，Markdown 格式     |
| `{{contentHtml}}`   | 主要内容，HTML 格式         |
| `{{selection}}`     | 当前选中的文本，Markdown 格式  |
| `{{selectionHtml}}` | 当前选中的文本，HTML 格式      |
| `{{highlights}}`    | Web Clipper 中创建的高亮内容 |
| `{{fullHtml}}`      | 未处理的完整页面 HTML        |

主要的内容变量是 `{{content}}`，它包含文章内容、高亮内容或者页面上选中的文本。

注意，`{{content}}` 会尝试提取页面的主要内容，这可能并不总是你想要的。这种情况下，可使用其他预设变量或选择器变量提取所需内容。

### （5）Meta 变量

HTML 网页的 `<head>` 中通常包含 `<meta>` 元素，用于描述页面标题、摘要、作者、摘要图等信息。有关 `<meta>` 的详细介绍，参考 [[前后端/notes/前端/HTML/4、Meta元数据与Open Graph|Meta 元数据与 Open Graph]]。

示例：

```html
<meta name="description" content="一篇介绍 Rust 所有权的文章">

<meta property="og:title" content="Rust 所有权">
<meta property="og:image" content="https://example.com/cover.png">
```

这些信息一般不直接显示在网页正文，但会被搜索引擎和社交平台用于生成网页预览。

#### 1）提取 name 类型 Meta 标签

语法：

```
{{meta:name:名称}}
```

例如：

```
{{meta:name:description}}
```

对应：

```html
<meta name="description" content="一篇介绍 Rust 所有权的文章">
```

返回结果：

```
一篇介绍 Rust 所有权的文章
```

常见变量：

- `{{meta:name:author}}`
- `{{meta:name:description}}`
- `{{meta:name:keywords}}`

#### 2）提取 property 类型 Meta 标签

语法：

```
{{meta:property:属性名}}
```

例如：

```
{{meta:property:og:title}}
{{meta:property:og:description}}
{{meta:property:og:image}}
```

其中，`og:*` 属于 Open Graph 数据，主要用于生成社交分享卡片。

例如，可以在属性区域中配置：

```yaml
cover: "{{meta:property:og:image}}"
description: "{{meta:property:og:description}}"
```

Meta 变量适合在预设变量为空或结果不准确时使用，但前提是网页本身提供了对应的 `<meta>` 标签。


### （6）Schema.org 变量

Schema.org 变量用于读取网页里的结构化数据。很多网站会在页面中嵌入 [[通用计算机知识/notes/数据格式/5、JSON-LD|JSON-LD]]，用一段机器可读的数据说明“这个页面描述的是什么对象，以及这个对象有哪些属性”。

可以把三者关系理解为：

- **Schema.org**：公共词汇表，规定 `Article`、`Person`、`Book`、`headline`、`datePublished` 等类型和属性是什么意思。
- **JSON-LD**：把这些类型和属性写进网页的一种 JSON 格式。
- **Web Clipper 的 Schema.org 变量**：从网页里的 JSON-LD 中按类型和属性路径取值。

例如，网页中可能有这样的 JSON-LD：

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Rust 所有权",
  "datePublished": "2026-07-12",
  "author": {
    "@type": "Person",
    "name": "Tom"
  }
}
```

这段数据的语义是：

- `@type: "Article"` 表示这个对象是一篇文章
- `headline` 表示文章标题
- `datePublished` 表示发布日期
- `author` 表示作者
- `author.name` 表示作者姓名

对于文章、图书、商品、电影、视频、食谱等页面，如果网站提供了质量较好的 JSON-LD，Schema.org 变量通常比 CSS 选择器更稳定。CSS 选择器依赖页面 HTML 结构，页面一改版就可能失效；Schema.org 变量依赖语义字段，只要结构化数据还在，取值路径通常更稳定。

Schema.org 变量的基本语法是：

```
{{schema:@Type:key}}
```

其中：

- `@Type` 表示要读取哪一种 Schema.org 类型，例如 `@Article`、`@Book`、`@Product`
- `key` 表示要读取该类型下的哪个属性，例如 `headline`、`name`、`isbn`

示例：

```
{{schema:@Article:headline}}
{{schema:@Article:datePublished}}
{{schema:@Book:name}}
{{schema:@Book:isbn}}
```

这些变量的含义是：

- `{{schema:@Article:headline}}`：读取文章标题
- `{{schema:@Article:datePublished}}`：读取文章发布日期
- `{{schema:@Book:name}}`：读取图书名称
- `{{schema:@Book:isbn}}`：读取图书 ISBN

如果属性本身是一个嵌套对象，可以使用 `.` 继续向下访问。

例如，作者信息不是一个简单字符串，而是一个对象：

```json
{
  "@type": "Article",
  "author": {
    "@type": "Person",
    "name": "Tom"
  }
}
```

访问作者姓名：

```
{{schema:@Article:author.name}}
```

这里的 `author.name` 表示先进入 `author` 对象，再读取里面的 `name` 属性。

如果属性是数组，可以使用下标访问某个元素，也可以使用 `[*]` 访问所有元素。

例如，一篇文章有多个作者：

```json
{
  "@type": "Article",
  "author": [
    {
      "name": "Tom"
    },
    {
      "name": "Jerry"
    }
  ]
}
```

读取第一个作者：

```
{{schema:@Article:author[0].name}}
```

读取第二个作者：

```
{{schema:@Article:author[1].name}}
```

读取所有作者：

```
{{schema:@Article:author[*].name}}
```

`[*]` 返回的是数组，通常需要配合 `join` 等筛选器，把多个值合并成适合写入笔记属性或正文的文本：

```
{{schema:@Article:author[*].name|join:", "}}
```

结果：

```
Tom, Jerry
```

如果不确定网页使用的是 `Article`、`NewsArticle`、`BlogPosting` 还是其他类型，可以省略 `@Type`，让 Web Clipper 在页面的结构化数据中查找对应属性：

```
{{schema:author}}
{{schema:name}}
{{schema:datePublished}}
```

这种写法更省事，但精确度较低。如果页面里有多个结构化对象，例如同时有 `Article`、`WebPage`、`Organization`，同名属性可能来自不同对象。能确定类型时，优先使用 `{{schema:@Type:key}}` 这种完整写法。


### （7）选择器变量

选择器变量通过 CSS 选择器查找页面中的 HTML 元素。

语法：

```
{{selector:CSS选择器}}
```

例如，页面中存在：

```html
<h1>Rust 所有权</h1>
<span class="author">Tom</span>
```

可以使用：

```
{{selector:h1}}
{{selector:.author}}
```

常见 CSS 选择器：

|选择器|含义|
|---|---|
|`h1`|所有 `<h1>` 元素|
|`.author`|`class="author"` 的元素|
|`#article`|`id="article"` 的元素|
|`article h1`|`article` 内部的 `<h1>`|
|`.post > .title`|`.post` 的直接子元素 `.title`|
|`article p`|`article` 内部的所有段落|
|`a.main-link`|类名为 `main-link` 的链接|

提取元素属性：

```
{{selector:CSS选择器?属性名}}
```

例如：

```html
<img class="hero" src="https://example.com/cover.png">

<a class="main-link" href="/article/1">查看文章</a>
```

提取图片地址：

```
{{selector:img.hero?src}}
```

提取链接地址：

```
{{selector:a.main-link?href}}
```

`?src` 和 `?href` 表示读取元素属性，而不是元素中的文本。

如果没有指定属性，选择器变量默认返回匹配元素的文本内容。

如果选择器匹配到多个元素，Web Clipper 会返回数组。

例如：

```html
<span class="tag">Rust</span>
<span class="tag">所有权
</span><span class="tag">编程语言</span>
```

使用：

```
{{selector:.tag}}
```

得到的结果相当于：

```
[  
	"Rust",  
	"所有权",  
	"编程语言"
]
```

可以使用 `join` 将其连接为字符串：

```
{{selector:.tag|join:", "}}
```

结果：

```
Rust, 所有权, 编程语言
```

也可以在模板逻辑中循环处理：

```
{% for tag in selector:.tag %}
- {{tag}}
{% endfor %}
```

### （8）提示变量

提示变量是给解释器使用的。详见[[#七、解释器|解释器]]。

## 3、筛选器

筛选器允许修改模板中的变量。

语法：

```
{{variable|filter}}
```

筛选器适用于任何类型的变量。

筛选器可以链式使用，例如：

```
{{variable|filter1|filter2}}
```

示例：转换和修改日期

```
{{date|date: "YYYY-MM-DD"}}
```

将当前日期转换为 "YYYY-MM-DD" 格式。

## 4、模板逻辑

Web Clipper 支持模板逻辑，包括条件判断、循环和变量赋值。

### （1）条件判断

基本语法：

```
{% if %}

{% endif %}
```

示例：

```
{% if author %}
Author: {{author}}
{% endif %}
```

使用 `{% else %}` 提供备用内容，使用 `{% elseif %}` 串联多个条件：

```
{% if status == "published" %}
Live article
{% elseif status == "draft" %}
Draft article
{% else %}
Unknown status
{% endif %}
```


### （2）变量赋值

使用 `{% set %}` 可以在模板中创建一个临时变量，后面再通过 `{{变量名}}` 使用它。

语法：

```
{% set 变量名 = 表达式 %}
```

其中，等号左边是新变量的名字，等号右边是要保存的值。右边既可以是普通变量，也可以是经过筛选器处理后的结果。

示例：

```
{% set slug = title|lower|replace:" ":"-" %}
File: {{slug}}.md
```

这段模板的意思是：先根据页面标题生成一个适合放进文件名里的 `slug`，再把 `slug` 拼进文件名。

假设当前页面标题是：

```
Rust Ownership Guide
```

表达式会按从左到右的顺序处理：

1. `title`：取当前页面标题，得到 `Rust Ownership Guide`
2. `|lower`：把标题转成小写，得到 `rust ownership guide`
3. `|replace:" ":"-"`：把空格替换成连字符，得到 `rust-ownership-guide`
4. `{% set slug = ... %}`：把最终结果保存到 `slug`

所以后面的：

```
File: {{slug}}.md
```

会输出：

```
File: rust-ownership-guide.md
```

需要注意的是，`{% set %}` 本身不会直接输出内容，它只是先保存一个中间结果。真正输出内容的是 `{{slug}}`。


### （3）回退值

使用 `??` 运算符在变量为空或未定义时提供回退值：

```
{{title ?? "Untitled"}}
```

如果 `title` 为空、未定义或为假值，则会使用回退值 `"Untitled"`。

这是等效 `if` 语句的简写：

```
{% if title %}
{{title}}
{% else %}
Untitled
{% endif %}
```

还可以链式回退多个值：

```
{{title ?? headline ?? "No title"}}
```


### （4）循环

使用 `{% for %}` 遍历数组：

```
{% for item in schema:author %}
- {{item.name}}
{% endfor %}
```

## 5、设置模板触发条件

如果为不同类型的网页创建了多个模板，建议为模板设置触发条件，让 Web Clipper 根据当前网址自动选择合适的模板。

在编辑模板页面顶部，可以找到模板触发器，在这里可以填写用于匹配网页的 URL：

![[assets/Pasted image 20260622164010.png|500]]


例如，创建了“视频笔记” 和 “技术文章” 两个模板。

对于视频模板增加：

```
https://www.youtube.com/watch
```

当在 YouTube 的视频页面打开 Web Clipper 时，扩展会自动选择视频模板。

对于技术模板增加：

```
https://doc.rust-lang.org/
```

这样，在 Rust 官方文档页面打开 Web Clipper 时，扩展会自动选择技术文章模板。

通过模板触发器，可以让不同类型的网站自动匹配对应模板，避免每次剪藏时手动切换。

## 6、模板最佳实践

模板不只是决定正文长什么样，也决定剪藏后的笔记是否方便检索、回看和继续加工。一个实用模板通常包含三部分：

- **属性区**：保存标题、作者、来源、发布日期、标签等元数据，方便后续检索。
- **正文区**：保存网页主体内容、高亮摘录或 AI 摘要。
- **来源区**：保留原始 URL 和剪藏时间，方便回到原网页。

例如，一个技术文章模板可以写成：

```markdown
---
title: "{{title}}"
author: "{{author ?? schema:@Article:author.name ?? meta:name:author}}"
published: "{{published ?? schema:@Article:datePublished}}"
source: "{{url}}"
site: "{{site}}"
tags:
  - clippings
  - article
created: {{date|date: "YYYY-MM-DD"}}
---

# {{title}}

> 来源：{{url}}

## 摘要

{{description ?? meta:name:description}}

## 高亮

{{highlights}}

## 正文

{{content}}
```

这个模板有几个思路：

1. 属性区尽量保存稳定元数据，例如标题、作者、发布时间、来源链接。
2. 作者和发布时间使用回退值：优先使用预设变量，取不到时再尝试 Schema.org 或 Meta 变量。
3. `{{highlights}}` 和 `{{content}}` 分开保存，方便区分自己标记的重点和网页原文。
4. `source: "{{url}}"` 建议保留，避免以后只剩剪藏内容却找不到原网页。

不同类型页面可以建立不同模板。例如，技术文章重视作者、发布时间和正文；视频页面可能更重视频道、视频链接和转录文本；资料型页面则可以增加 `category`、`status`、`rating` 等属性。


# 五、阅读器

Obsidian Web Clipper 内置了一个名为阅读器的阅读视图，可以去除网页中的杂乱元素，以简洁、易读的格式呈现文章主要内容。

通过在 Obsidian Web Clipper 界面顶部栏的书本按钮激活阅读视图：

![[assets/Pasted image 20260622020313.png|300]]

效果如下：

![[assets/Pasted image 20260622020348.png|800]]

# 六、高亮

Obsidian Web Clipper 不只是"整页剪藏"，还可以先在网页上挑选重点内容，再把这些重点保存进 Obsidian。

通过界面顶部栏的荧光笔形状的高亮按钮开启高亮工具：

![[assets/Pasted image 20260622021317.png|300]]

开启高亮工具后，直接在网页中选择内容即可。

![[assets/Pasted image 20260622021538.png|600]]

像平时复制文字一样，用鼠标拖动选择文本。选择完成后，这段文字会被加入当前页面的高亮记录。

![[assets/Pasted image 20260622021646.png|600]]

开启高亮模式后，也可以点击图片、引用块、代码块等网页元素，Web Clipper 会尝试把对应元素加入高亮。

通常可以再次点击已经高亮的内容，或者在高亮管理界面（设置 -> 高亮）中删除它。

再次点击高亮按钮，可以退出高亮模式。

高亮工具除了在实时网页中使用，同样也可以在阅读器视图下使用。

高亮操作完成后，Web Clipper 已经知道你选中了哪些内容，但你还需要决定：**剪藏到 Obsidian 时，高亮内容应该怎么出现在笔记里**。

为此，Web Clipper 提供了三个选项。

![[assets/Pasted image 20260622022558.png|600]]

1. 高亮页面内容

Web Clipper 仍然会保存网页正文，只是把你高亮过的部分用 Obsidian 高亮语法标记出来。

例如网页原文是：

```
Rust 的所有权系统能够在编译期管理内存安全。
```

你高亮了"在编译期管理内存安全"，剪藏结果可能变成：

```
Rust 的所有权系统能够==在编译期管理内存安全==。
```

在 Obsidian 阅读视图中，`==内容==` 会显示为高亮效果。

这种方式适合想保存完整文章，同时想保留自己标记的重点，希望以后阅读全文能看到重点位置。

2. 替换页面内容

表示 Web Clipper 不要全文，只保存划出的重点。

3. 不执行任何操作

Web Clipper 正常保存原文，高亮另行处理。

这并不意味着高亮丢失。高亮仍然被 Web Clipper 保存，只是不会自动修改模板中的 `{{content}}`。

这种方式通常与 `{{highlights}}` 变量配合使用。

例如：

```markdown
# {{title}}

## 我的摘录

{{highlights}}

## 网页正文

{{content}}
```

`{{content}}` 和 `{{highlights}}` 的区别：

1. `{{content}}` 表示网页的主要内容。它会受到前面三个高亮选项的影响：

| 高亮选项   | `{{content}}` 的结果     |
| ------ | --------------------- |
| 高亮页面内容 | 网页全文，高亮部分带有 `==...==` |
| 替换页面内容 | 只包含高亮内容               |
| 不做任何操作 | 原始网页全文，不插入高亮标记        |
2. `{{highlights}}` 专门表示当前网页上的高亮记录。它不依赖 `{{content}}` 如何处理，可以单独放到模板中。

# 七、解释器

Obsidian Web Clipper 包含 AI 处理能力。它不只是把网页原文复制到 Obsidian，还可以在剪藏前让语言模型对网页进行总结、翻译、提取或改写，再把处理结果写入笔记。

普通 Web Clipper 的工作方式是：

1. 读取网页内容
2. 根据模板整理格式
3. 保存到 Obsidian

启用解释器后，工作方式变为：

1. 读取网页内容
2. 把网页内容和提示词发送给模型
3. 模型根据提示词返回摘要、翻译或提取结果等
4. 将结果填入模板
5. 保存到 Obsidian

普通模板变量直接读取网页中的现成数据，例如 `{{title}}`、`{{url}}`、`{{content}}` 等。这些变量不会让 AI 处理内容，只是提取网页已有的信息。

解释器提示变量则使用自然语言指令，让模型对网页内容进行总结、翻译、提取或改写。其语法为 `{{"提示词"}}`，例如 `{{"用三句话总结这篇文章"}}`，结果也可以像其他变量一样链式使用筛选器。

示例：

```
# AI 摘要

{{"用简体中文总结和提炼这篇文章的核心内容。请用 Why How What 结构告诉读者这篇文章为什么值得读"}}

# 原始正文

{{content}}
```

要开启解释器功能，需要在设置中启用解释器：

![[assets/Pasted image 20260622024353.png|600]]

然后需要配置提供商和模型。Interpreter 包含几个预设提供商。

![[assets/Pasted image 20260622131207.png|600]]

要使用这些提供商，需要一个 API 密钥，可以通过登录提供商的账户获取。这里选择 DeepSeek 并填入密钥：

![[assets/Pasted image 20260622131311.png|600]]

此外，还需要选择模型：

![[assets/Pasted image 20260622131355.png|400]]

这里选择速度更快的 DeepSeek Chat，因为对于 AI 总结等任务，不太需要复杂推理模型，更快，成本也低。

启用模型：

![[assets/Pasted image 20260622131518.png]]

之后在 Web Clipper 页面，会看到解释按钮：

![[assets/Pasted image 20260622131617.png]]

默认情况下，需要手动点击解释才会替换解释器变量。如果不想手动点击，也可以在前面的设置中启用自动运行：

![[assets/Pasted image 20260622131725.png|400]]

默认情况下，解释器使用整个页面的 HTML 作为其上下文（`{{fullHtml}}`）：

![[assets/Pasted image 20260622132035.png|400]]

但这会消耗更多的 Token 且运行较慢。

因此，使用解释器前需要注意两点：

- **隐私**：如果页面包含账号信息、内部文档、付费内容、私人通信等敏感内容，不建议直接使用解释器处理整页 HTML。
- **成本**：上下文越长，消耗的 Token 越多，速度也越慢。`{{fullHtml}}` 往往包含导航、脚本、样式和无关元素，通常比 `{{content}}` 更贵也更慢。

更稳妥的做法是，只把真正需要模型处理的内容交给解释器。例如，可以把默认解释器上下文改成：

```
{{content}}
```

如果只希望模型处理自己标记的重点，也可以使用：

```
{{highlights}}
```

如果需要同时给模型标题、来源和正文，可以组合少量变量：

```
Title: {{title}}
URL: {{url}}

{{content}}
```

这样既能减少无关内容，也能降低 Token 消耗，并让模型更专注于真正需要处理的文本。
