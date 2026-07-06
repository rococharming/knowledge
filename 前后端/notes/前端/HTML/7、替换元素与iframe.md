---
title: 替换元素与iframe
date: 2026-07-05
tags: [HTML, 前端基础, iframe, 可访问性]
source_count: 1
---

# 一、替换元素

## 1、替换元素的概念

替换元素（replaced element）是指内容由外部资源或浏览器内部控件决定，而不是由元素中的普通 HTML 内容决定的元素。

例如，`img` 元素通过 `src` 加载图片：

```html
<img
  src="./images/mountain.jpg"
  alt="晨雾中的群山"
>
```

浏览器最终在 `img` 所在位置显示的是外部图片文件。可以把这个过程理解为：

```text
HTML中的img元素
       │
       │ src指定资源
       ▼
外部图片替换元素原本的显示区域
```

替换元素通常具有资源自身提供的尺寸和比例。例如，一张图片文件可能天然具有 `1200 × 800` 的尺寸，这称为资源的固有尺寸。

## 2、常见替换元素

常见替换元素包括：

| 元素 | 外部或内部内容来源 |
|---|---|
| `img` | 图片文件 |
| `video` | 视频资源及浏览器播放器 |
| `iframe` | 另一个网页或独立 HTML 文档 |
| `embed` | PDF、媒体等外部内容 |
| `object` | 图片、PDF 或其他外部资源 |

有些元素只在特定情况下表现为替换元素。例如：

```html
<input
  type="image"
  src="./images/submit-button.png"
  alt="提交"
>
```

`input type="image"` 使用图片作为提交按钮，属于替换元素；普通的 `input type="text"` 则通常不按同样方式理解。

## 3、样式能够控制什么

页面样式可以控制替换元素在当前页面中的外部表现，例如：

- 显示宽度和高度
- 页面中的位置
- 边框和圆角
- 透明度和滤镜

但样式不能直接修改外部资源内部的内容。

例如，可以改变 `img` 的显示尺寸，却不能通过普通页面样式把图片中的蓝色天空直接改成红色。要修改图片本身，通常需要编辑图片文件或使用专门的图像处理方式。

`iframe` 也类似。当前页面可以调整 `iframe` 的宽度和高度，但通常不能直接修改被嵌入网页内部的标题、段落和按钮。

> [!note] 元素外部与资源内部
> 替换元素属于当前页面，可以控制它的外部显示区域；被加载的资源拥有自己的内容和结构，不能简单地当作当前元素的子内容修改。

# 二、iframe元素

## 1、iframe的作用

`iframe` 是 inline frame（内联框架）的缩写，用于在当前网页中嵌入另一份 HTML 内容。

可以嵌入的内容包括：

- 视频播放器
- 地图
- 其他网页
- 当前项目中的另一个 HTML 文件
- 直接写在属性中的 HTML 片段

基础语法如下：

```html
<iframe
  src="./pages/course-preview.html"
  title="课程内容预览"
  width="640"
  height="360"
></iframe>
```

`iframe` 不是空元素，必须保留结束标签 `</iframe>`。

## 2、独立的浏览上下文

`iframe` 中的页面拥有自己的 HTML 文档、`head` 和 `body`，可以独立加载资源和运行脚本。

```text
当前页面
├── 当前页面的标题、段落和按钮
└── iframe
    └── 另一个独立页面
        ├── 自己的head
        └── 自己的body
```

因此，`iframe` 并不是简单地把目标页面的元素复制到当前页面，而是在当前页面中创建一个独立的嵌入区域。

这也解释了为什么当前页面的普通样式不能直接修改 `iframe` 内部的内容：两个页面拥有各自的文档环境。

# 三、iframe的常用属性

## 1、src、width与height

`src` 指定要嵌入的页面地址：

```html
<iframe
  src="./pages/contact.html"
  title="联系方式"
  width="600"
  height="400"
></iframe>
```

- `src` 指定嵌入内容的位置
- `width` 设置嵌入区域的宽度
- `height` 设置嵌入区域的高度

`src` 可以使用当前项目中的相对路径，也可以使用外部网站提供的嵌入地址。

> [!warning] 普通网页地址不一定允许嵌入
> 网站可以通过安全策略禁止自己的页面被其他网站放入 `iframe`。因此，能在浏览器中正常打开的网址，不一定能被嵌入。

## 2、title属性

`title` 用于说明 `iframe` 中嵌入的内容：

```html
<iframe
  src="./pages/registration-form.html"
  title="课程报名表"
></iframe>
```

`iframe` 的内容对使用屏幕阅读器的用户不一定直观。准确的 `title` 可以帮助用户在进入嵌入区域之前了解它的用途。

不推荐使用没有实际信息的标题：

```html
<iframe src="./pages/registration-form.html" title="iframe"></iframe>
```

更合适的写法是：

```html
<iframe src="./pages/registration-form.html" title="课程报名表"></iframe>
```

## 3、allowfullscreen属性

`allowfullscreen` 是布尔属性，用于允许嵌入内容进入全屏模式：

```html
<iframe
  src="https://player.example.com/embed/course-101"
  title="HTML基础课程视频"
  width="640"
  height="360"
  allowfullscreen
></iframe>
```

该属性常用于视频播放器。只有嵌入内容本身提供全屏功能时，用户才能实际使用它。

## 4、allow属性

`allow` 用于声明嵌入页面可以使用哪些浏览器功能。允许的功能之间通常使用分号分隔：

```html
<iframe
  src="https://player.example.com/embed/course-101"
  title="HTML基础课程视频"
  allow="autoplay; fullscreen; picture-in-picture"
  allowfullscreen
></iframe>
```

这个例子允许嵌入内容请求：

| 功能 | 作用 |
|---|---|
| `autoplay` | 自动播放媒体 |
| `fullscreen` | 进入全屏模式 |
| `picture-in-picture` | 使用画中画模式 |

`allow` 可以理解为给嵌入页面的一份功能许可清单。将某项功能写入 `allow`，只是允许嵌入页面提出使用请求，并不保证浏览器一定批准。例如，自动播放仍可能受到浏览器策略或用户设置限制。

不要无条件复制一长串权限。应根据嵌入内容的实际需求，只开放必要功能。

## 5、referrerpolicy属性

当浏览器请求 `iframe` 页面时，可能会通过 `Referer` 请求头告诉目标网站当前页面的来源。`referrerpolicy` 用于控制发送多少来源信息。

```html
<iframe
  src="https://map.example.com/embed/city-center"
  title="市中心地图"
  referrerpolicy="strict-origin-when-cross-origin"
></iframe>
```

`strict-origin-when-cross-origin` 的常见行为可以概括为：

- 同源请求可以携带较完整的来源地址
- 跨源请求通常只携带来源的协议、域名和端口
- 从 HTTPS 页面请求不安全的 HTTP 资源时，不发送来源信息

这个值也是现代浏览器中常见的默认策略。学习初期只需要知道，它用于控制嵌入请求向外部网站透露多少当前页面信息。

## 6、loading属性

首屏之外的 `iframe` 可以使用 `loading="lazy"` 延迟加载：

```html
<iframe
  src="./pages/interactive-example.html"
  title="交互练习"
  width="640"
  height="480"
  loading="lazy"
></iframe>
```

浏览器可以等到该区域接近可视范围时再加载嵌入页面，从而减少页面初次打开时的网络请求和资源消耗。

# 四、嵌入视频与地图

## 1、嵌入视频

视频平台通常会提供专门的嵌入地址和 `iframe` 代码。通用结构如下：

```html
<iframe
  src="https://player.example.com/embed/course-101"
  title="HTML基础课程视频"
  width="640"
  height="360"
  allow="fullscreen; picture-in-picture"
  allowfullscreen
></iframe>
```

这里应使用平台提供的嵌入地址，而不是直接复制普通播放页面的网址。

例如，普通页面和嵌入页面可能分别是：

```text
普通播放页面：https://video.example.com/watch/course-101
嵌入地址：    https://player.example.com/embed/course-101
```

嵌入地址通常只保留播放器，而不会显示完整网站的导航和评论区域。

## 2、嵌入地图

地图服务也可以通过 `iframe` 提供可缩放和拖动的交互地图：

```html
<h1>西湖周边地图</h1>

<iframe
  src="https://www.openstreetmap.org/export/embed.html?bbox=120.0%2C30.1%2C120.3%2C30.4&amp;layer=mapnik"
  title="杭州西湖周边地图"
  width="640"
  height="420"
  loading="lazy"
></iframe>

<p>
  <a href="https://www.openstreetmap.org/#map=12/30.25/120.15">
    在新页面中查看完整地图
  </a>
</p>
```

除了嵌入地图，额外提供普通链接，可以让无法正常使用嵌入内容的用户在新页面中访问地图。

# 五、使用srcdoc嵌入HTML

`srcdoc` 可以直接提供一小段 HTML，而不需要加载另一个文件：

```html
<iframe
  title="课程完成提示"
  srcdoc="<h2>练习完成</h2><p>你已经掌握iframe的基础用法。</p>"
  width="500"
  height="200"
></iframe>
```

使用 `srcdoc` 时，属性值中的 HTML 会成为 `iframe` 内部的独立文档内容。

如果同时提供 `srcdoc` 和 `src`，支持 `srcdoc` 的浏览器通常优先使用 `srcdoc`：

```html
<iframe
  src="./pages/fallback.html"
  srcdoc="<p>这里是直接嵌入的内容。</p>"
  title="提示信息"
></iframe>
```

`srcdoc` 适合简短、可信的静态内容。不要把未经处理的用户输入直接放入 `srcdoc`，否则可能把恶意 HTML 或脚本带入页面。

# 六、iframe的安全边界

## 1、同源限制

浏览器使用同源策略限制页面访问不同来源的内容。来源通常由协议、域名和端口共同决定。

例如，当前页面来自：

```text
https://learn.example.com
```

嵌入页面来自：

```text
https://map.example.net
```

两个页面的域名不同，属于跨源。当前页面通常不能直接读取或修改嵌入页面中的标题、段落和表单内容。

这既解释了替换元素“不能直接修改内部内容”的现象，也是一项重要安全措施：如果任意网页都能读取其他网站的嵌入内容，恶意页面就可能窃取用户的邮件、账户信息或私人数据。

## 2、sandbox属性

`sandbox` 可以进一步限制嵌入页面的能力：

```html
<iframe
  src="./pages/user-example.html"
  title="用户提交的示例"
  sandbox
></iframe>
```

只写一个空的 `sandbox` 会启用一组严格限制，例如限制脚本、表单提交和弹出窗口等行为。

可以通过特定值放开必要能力：

```html
<iframe
  src="./pages/form-preview.html"
  title="表单预览"
  sandbox="allow-forms"
></iframe>
```

这个例子只额外允许表单提交。常见值包括：

| 值 | 放开的能力 |
|---|---|
| `allow-forms` | 允许提交表单 |
| `allow-scripts` | 允许运行脚本 |
| `allow-popups` | 允许打开弹出页面 |
| `allow-downloads` | 允许触发下载 |

`sandbox` 遵循“默认限制，再按需放开”的思路。对不完全可信的嵌入内容，应尽量减少开放的能力。

> [!warning] 不要随意组合高权限
> 对同源内容同时使用 `allow-scripts` 和 `allow-same-origin` 可能显著削弱沙箱限制。没有明确需求时，不要照搬不理解的 sandbox 配置。

# 七、完整示例

下面的页面分别嵌入课程视频、地图和直接 HTML 内容：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iframe练习</title>
  </head>
  <body>
    <main>
      <h1>iframe练习</h1>

      <section>
        <h2>课程视频</h2>
        <iframe
          src="https://player.example.com/embed/course-101"
          title="HTML基础课程视频"
          width="640"
          height="360"
          allow="fullscreen; picture-in-picture"
          allowfullscreen
        ></iframe>
      </section>

      <section>
        <h2>学习地点</h2>
        <iframe
          src="https://www.openstreetmap.org/export/embed.html?bbox=120.0%2C30.1%2C120.3%2C30.4&amp;layer=mapnik"
          title="杭州西湖周边地图"
          width="640"
          height="420"
          loading="lazy"
        ></iframe>
      </section>

      <section>
        <h2>完成提示</h2>
        <iframe
          title="练习完成提示"
          srcdoc="<p>你已经完成今天的练习。</p>"
          width="500"
          height="160"
          sandbox
        ></iframe>
      </section>
    </main>
  </body>
</html>
```

# 八、总结

- 替换元素的内容由外部资源或浏览器内部控件决定
- `img`、`video` 和 `iframe` 都是常见替换元素
- 页面可以控制替换元素的外部尺寸和位置，但不能直接修改外部资源内部内容
- `iframe` 在当前页面中创建一个独立的嵌入页面环境
- `src` 指定嵌入地址，`width` 和 `height` 指定嵌入区域尺寸
- `title` 用于描述嵌入内容，对屏幕阅读器用户很重要
- `allow` 声明嵌入页面可以请求使用的浏览器功能
- `allowfullscreen` 允许嵌入内容进入全屏模式
- `srcdoc` 可以直接提供 iframe 内部的 HTML 内容
- 同源策略通常阻止当前页面直接读取或修改跨源 iframe 的内部内容
- `sandbox` 可以限制嵌入页面的脚本、表单和弹窗等能力

