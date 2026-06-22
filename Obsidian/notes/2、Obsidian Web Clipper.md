# 一、概述

Obsidian Web Clipper 是 Obsidian 官方推出的浏览器插件，用于将网页内容以 Markdown 形式直接保存到 Obsidian Vault，方便离线阅读、标注和整理。

它不仅可以保存文本形态的网页，还可以一键获取 YouTube 视频里的文字稿。所有的内容最终都会以 Markdown 格式保存下来。

核心特点：

- **一键剪藏网页**：把网页正文以及标题、作者、发布日期等元数据保存到 Obsidian
- **高亮与选择保存**：可以在网页上高亮重要段落并选择特定页面元素保存
- **阅读器模式**：它带有类似阅读器的干净视图，适合将网页中的广告、侧边栏等干扰去掉再阅读或剪藏
- **隐私和可控性好**：内容保存到本地知识库，不收集个人数据

# 二、安装

可以从所使用的浏览器官方扩展商店获取 Obsidian Web Clipper。

也可以进入 https://obsidian.md/clipper 添加，如下图所示：

![[Pasted image 20260622011526.png|800]]

如果是 Google 浏览器，点击**Add to Chrome**添加；如果是其他浏览器，点击`More browsers`选择支持的浏览器添加。

添加之后，就可以在浏览器上使用 Obsidian Web Clipper 插件了：

![[Pasted image 20260622011703.png|800]]



# 三、快速上手：第一次剪藏

## 1、捕获页面

默认情况下，Obsidian Web Clipper 会尝试智能提取页面的主要文章内容，排除页面上的其他元素。

要将页面保存到 Obsidian，点击 **添加到Obsidian** 按钮：

![[Pasted image 20260622012029.png|300]]

弹出提示，选择"打开 Obsidian"：

![[Pasted image 20260622012525.png|400]]

此时，网页内容以 Markdown 的形式保存到了本地 Obsidian 仓库下的`raw`目录。

结果如下：

![[Pasted image 20260622013045.png|600]]


## 2、下载图片

使用 Obsidian Web Clipper 时，图片不会自动下载。图片会链接到其网络 URL。这可以节省仓库空间，但意味着在离线状态下或 URL 失效时图片将无法访问：

![[Pasted image 20260622013257.png|400]]

可以在 Obsidian 中使用 `Command + P`（macOS）或`Ctrl + P`（Windows）唤出命令面板，搜索**下载当前文件内的所有附件**来下载任何文件中的图片。

![[Pasted image 20260622013542.png|500]]

![[Pasted image 20260622013554.png|400]]

或者在**设置 -> 快捷键**中为**下载当前文件内的所有附件**设置快捷键。


## 3、界面功能

Obsidian Web Clipper 界面分为四个部分：

1. 顶部栏：切换模板、开启高亮、阅读视图，以及访问设置
2. 属性：显示从页面中提取的元数据，这些数据将作为属性保存到 Obsidian
3. 笔记内容：保存到 Obsidian 中的正文内容
4. 底部栏：允许你选择要保存到仓库的文件夹，并添加到 Obsidian

![[Pasted image 20260622015615.png]]

# 四、模板与变量

## 1、模板的概念

模板决定了剪藏内容以什么格式保存到 Obsidian。Web Clipper 允许创建模板，自动捕获和组织网页中的元数据。示例模板可参考 https://github.com/kepano/clipper-templates 。

要**创建**模板，进入 Web Clipper 设置并点击侧边栏中的**新建模板**按钮。

![[Pasted image 20260622030528.png]]

模板使用了变量和筛选器，让你可以自定义内容的保存方式。

## 2、变量

### （1）概念

Obsidian Web Clipper 的模板并不是一段固定文本。模板中的变量会在剪藏网页时，被替换为当前页面中的实际数据。

例如，在模板中写入：

```
# 原始正文

{{content}}
```

剪藏网页后，`{{content}}`会被替换为 Web Clipper 从当前页面中提取出的正文。

变量的基本语法是：

```
{{变量}}
```

例如`{{title}}`、`{{url}}`、`{{author}}`、`{{content}}`等。


### （2）查看当前页面变量

不同网站提供的数据并不完全相同，点击 Web Clipper 页面上的 `...` 图标可以访问当前页面的变量：

![[Pasted image 20260622101038.png|300]]

制作模板时，应先检查页面提供了哪些数据，再决定使用哪种变量。

例如，某些网页可以正确识别`{{author}}`、`{{published}}`，另一些网页可能无法识别这些信息，此时需要改用 Meta、Schema.org、选择器或提示变量。

### （3）变量类型总览

Web Clipper 支持五类变量：

|类型|数据来源|主要特点|
|---|---|---|
|预设变量|Web Clipper 自动解析的页面信息|简单、通用|
|Meta 变量|HTML 中的 `<meta>` 标签|适合描述、封面和分享信息|
|Schema.org 变量|页面中的 JSON-LD 结构化数据|语义明确，适合文章、图书和商品|
|选择器变量|页面中的 HTML 元素|精确，但依赖网站结构|
|提示变量|语言模型对页面的分析结果|灵活，但速度较慢且可能产生费用|

这些变量可以在同一个模板中组合使用。

### （4）预设变量

预设变量由 Web Clipper 根据当前页面自动生成，通常适用于大多数网站。

主要的内容变量是`{{content}}`，它包含文章内容、高亮内容或者页面上选中的文本。注意，`{{content}}`会尝试提取页面的主要内容，这可能并不总是你想要的。这种情况下，可使用其他预设变量或选择器变量提取所需内容。

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

### （5）Meta 变量

HTML 网页的 `<head>` 中通常包含 `<meta>` 元素，用于描述页面标题、摘要、作者、摘要图等信息。

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

```YAML
cover: "{{meta:property:og:image}}"
description: "{{meta:property:og:description}}"
```

Meta 变量适合在预设变量为空或结果不准确时使用，但前提是网页本身提供了对应的 `<meta>` 标签。


### （6）Schema.org 变量

很多网页会使用 JSON-LD 提供结构化数据，明确描述页面中的对象。

JSON-LD 会在 JSON 中加入一些具有明确意义的字段：

```json
{
  "@type": "Article",
  "headline": "Rust 所有权",
  "datePublished": "2026-06-20",
  "author": {
    "@type": "Person",
    "name": "Tom"
  }
}
```

这段数据明确表示：

- `headline` 是文章标题
- `datePublished` 是发布日期
- `author` 是作者
- `author.name` 是作者姓名

因此，对于文章、图书、商品、电影、视频和食谱等页面，Schema.org 变量通常比 CSS 选择器更稳定。

Schema 变量的语法：

```
{{schema:@Type:key}}
```

示例：

```
{{schema:@Article:headline}}
{{schema:@Article:datePublished}}
{{schema:@Book:name}}
{{schema:@Book:isbn}}
```

其中：

- `@Article`、`@Book` 是 Schema 类型
- `headline`、`name`、`isbn` 是属性名

如果数据结构是嵌套类型的：

```json
{
  "@type": "Article",
  "author": {
    "@type": "Person",
    "name": "Tom"
  }
}
```

访问作者名字：

```
{{schema:@Article:author.name}}
```

属性路径中的 `.` 表示继续访问下一层对象。

假设文章包含多个作者：

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

访问第一个作者：

```
{{schema:@Article:author[0].name}}
```

访问第二个作者：

```
{{schema:@Article:author[1].name}}
```

访问所有作者：

```
{{schema:@Article:author[*].name}}
```

`[*]` 返回数组，因此通常需要配合 `join` 等筛选器：

```
{{schema:@Article:author[*].name|join:", "}}
```

结果：

```
Tom, Jerry
```

当不知道页面使用的是 `Article`、`NewsArticle` 还是其他类型时，可以省略 `@Type`：

```
{{schema:author}}
{{schema:name}}
{{schema:datePublished}}
```


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

如果没有指定属性，选择器变量默认返回匹配元素的文本内容。

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

提示变量通过解释器调用语言模型，让模型根据自然语言指令分析当前页面。

语法：

```
{{"提示词"}}
```

例如：

```
{{"用三句话总结这篇文章"}}
```

提示词外侧的双引号不能省略，它用于区分提示变量和普通变量：

```
{{title}}
{{"提取文章标题"}}
```

其中：

- `{{title}}` 是预设变量
- `{{"提取文章标题"}}` 是提示变量

提示变量只有在启用并配置解释器后才能使用，相关配置会在七、解释器中说明。

提示变量的结果也可以继续使用筛选器：

```
{{"总结这篇文章"|blockquote}}
```

模型生成摘要后，blockquote 筛选器会把它转换为引用块。

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

使用 `{% set %}` 在模板中创建或修改变量。

示例：

```
{% set slug = title|lower|replace:" ":"-" %}
File: {{slug}}.md
```


### （3）回退值

使用 `??` 运算符在变量为空或未定义时提供回退值：

```
{{title ?? "Untitled"}}
```

如果 `title` 为空、未定义或为假值，则会使用回退值 `"Untitled"`。

这是等效`if`语句的简写：

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



# 五、阅读器

Obsidian Web Clipper 内置了一个名为阅读器的阅读视图，可以去除网页中的杂乱元素，以简洁、易读的格式呈现文章主要内容。

通过在 Obsidian Web Clipper 界面顶部栏的书本按钮激活阅读视图：

![[Pasted image 20260622020313.png|200]]

效果如下：

![[Pasted image 20260622020348.png|800]]

# 六、高亮

Obsidian Web Clipper 不只是"整页剪藏"，还可以先在网页上挑选重点内容，再把这些重点保存进 Obsidian。

通过界面顶部栏的荧光笔形状的高亮按钮开启高亮工具：

![[Pasted image 20260622021317.png|300]]

![[Pasted image 20260622021538.png|800]]

开启高亮工具后，直接在网页中选择内容即可。

像平时复制文字一样，用鼠标拖动选择文本。选择完成后，这段文字会被加入当前页面的高亮记录。

![[Pasted image 20260622021646.png]]

开启高亮模式后，也可以点击图片、引用块、代码块等网页元素，Web Clipper 会尝试把对应元素加入高亮。

通常可以再次点击已经高亮的内容，或者在高亮管理界面（设置 -> 高亮）中删除它。

再次点击高亮按钮，可以退出高亮模式。

高亮工具除了在实时网页中使用，同样也可以在阅读器视图下使用。

高亮操作完成后，Web Clipper 已经知道你选中了哪些内容，但你还需要决定：

> 剪藏到 Obsidian 时，高亮内容应该怎么出现在笔记里

为此，Web Clipper 提供了三个选项。

![[Pasted image 20260622022558.png|500]]

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

表示Web Clipper 不要全文，只保存划出的重点。

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

Web Clipper 也包含 AI 处理能力。它不只是把网页原文复制到 Obsidian，还可以在剪藏前让语言模型对网页进行总结、翻译、提取或改写，再把处理结果写入笔记。

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

普通模板变量直接读取网页中的现成数据，例如`{{title}}`、`{{url}}`、`{{content}}`等。这些变量不会让 AI 处理内容，只是提取网页已有的信息。

解释器提示变量则使用自然语言指令，让模型对网页内容进行总结、翻译、提取或改写。其语法为 `{{"提示词"}}`，例如 `{{"用三句话总结这篇文章"}}`，结果也可以像其他变量一样链式使用筛选器。

示例：

```
# AI 摘要

{{"用简体中文总结和提炼这篇文章的核心内容。请用 Why How What 结构告诉读者这篇文章为什么值得读"}}

# 原始正文

{{content}}
```

要开启解释器功能，需要在设置中启用解释器：

![[Pasted image 20260622024353.png|600]]

然后需要配置提供商和模型。Interpreter 包含几个预设提供商。

![[Pasted image 20260622131207.png|600]]

要使用这些提供商，需要一个 API 密钥，可以通过登录提供商的账户获取。这里选择 DeepSeek 并填入密钥：

![[Pasted image 20260622131311.png|600]]

此外，还需要选择模型：

![[Pasted image 20260622131355.png|400]]

这里选择速度更快的 DeepSeek Chat，因为对于 AI 总结等任务，不需要复杂推理模型，更快，成本也低。

启用模型：

![[Pasted image 20260622131518.png]]

之后在 Web Clipper 页面，会看到解释按钮：

![[Pasted image 20260622131617.png]]

默认情况下需要手动点击解释才会替换解释器变量，如果不想手动点击，在前面的设置也可以启动自动运行：

![[Pasted image 20260622131725.png|400]]

默认情况下，解释器使用整个页面的 HTML 作为其上下文（`{{fullHtml}}`），但这会消耗更多的Token且运行较慢。为此，可以在解释器**高级 -> 默认解释器上下文**中使用变量和过滤器覆盖默认上下文：

![[Pasted image 20260622132035.png|400]]

