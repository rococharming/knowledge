---
title: 替换元素、iframe与嵌入安全
date: 2026-07-13
tags: [HTML, 前端基础, iframe, 安全, 可访问性]
aliases:
  - 替换元素与iframe
  - HTML iframe
  - 嵌入安全
---

# 一、替换元素的概念

替换元素（replaced element）是指：元素在页面中的显示内容由外部资源或浏览器内部控件决定，而不是由元素标签内部的普通 HTML 内容决定。

例如：

```html
<img
  src="./images/mountain.jpg"
  alt="晨雾中的群山"
>
```

浏览器最终在 `img` 所在位置显示外部图片文件。可以把它理解为：

```text
HTML 中的 img 元素
       │
       │ src 指定资源
       ▼
外部图片替换元素显示区域
```

# 二、常见替换元素

## 1、替换元素清单

常见替换元素：

| 元素 | 内容来源 |
|---|---|
| `img` | 图片文件 |
| `video` | 视频资源和浏览器播放器 |
| `audio` | 音频资源和浏览器播放器 |
| `iframe` | 另一个网页或独立 HTML 文档 |
| `embed` | PDF、媒体等外部内容 |
| `object` | 图片、PDF 或其他外部资源 |

有些元素只在特定情况下表现为替换元素：

```html
<input
  type="image"
  src="./images/submit-button.png"
  alt="提交"
>
```

`input type="image"` 使用图片作为提交按钮，属于替换元素；普通文本输入框通常不按同样方式理解。

## 2、样式能控制什么

页面 CSS 可以控制替换元素的外部表现：

- 显示宽度和高度。
- 页面中的位置。
- 边框和圆角。
- 透明度和滤镜。
- 与周围内容的间距。

但 CSS 通常不能直接修改外部资源内部内容。例如，页面可以改变 `img` 显示尺寸，却不能把图片文件里的蓝色天空直接改成红色。`iframe` 也类似，当前页面可以调整嵌入区域尺寸，但不能随意修改被嵌入网页内部的标题、段落和按钮。

> [!note] 区分元素外部与资源内部
> 替换元素属于当前页面，可以控制外部显示区域；被加载资源拥有自己的内容和结构，不能简单当作当前元素的子内容修改。

# 三、iframe 的基本用法

## 1、iframe 是独立浏览上下文

`iframe` 是 inline frame（内联框架）的缩写，用于在当前网页中嵌入另一份 HTML 内容。

```html
<iframe
  src="./pages/course-preview.html"
  title="课程内容预览"
  width="640"
  height="360"
></iframe>
```

`iframe` 不是空元素，必须保留结束标签 `</iframe>`。

嵌入页面拥有自己的 HTML 文档、`head` 和 `body`：

```text
当前页面
├── 当前页面的标题、段落和按钮
└── iframe
    └── 另一个独立页面
        ├── 自己的 head
        └── 自己的 body
```

因此，`iframe` 并不是把目标页面的元素复制到当前页面，而是在当前页面中创建一个独立的嵌入区域。

## 2、src、width 与 height

```html
<iframe
  src="./pages/contact.html"
  title="联系方式"
  width="600"
  height="400"
></iframe>
```

- `src` 指定嵌入内容地址。
- `width` 设置嵌入区域宽度。
- `height` 设置嵌入区域高度。

`src` 可以是当前项目中的相对路径，也可以是外部网站提供的嵌入地址。

> [!warning] 普通网页地址不一定允许嵌入
> 网站可以通过安全策略禁止自己的页面被其他网站放入 `iframe`。能在浏览器中打开的网址，不一定能被嵌入。

## 3、title 与可访问性

`title` 用于说明 `iframe` 中嵌入的内容：

```html
<iframe
  src="./pages/registration-form.html"
  title="课程报名表"
></iframe>
```

不推荐：

```html
<iframe src="./pages/registration-form.html" title="iframe"></iframe>
```

准确的 `title` 可以帮助屏幕阅读器用户在进入嵌入区域前理解其用途。

# 四、iframe 权限与加载属性

## 1、allowfullscreen 与 allow

`allowfullscreen` 允许嵌入内容请求全屏：

```html
<iframe
  src="https://player.example.com/embed/course-101"
  title="HTML 基础课程视频"
  width="640"
  height="360"
  allowfullscreen
></iframe>
```

`allow` 声明嵌入页面可以请求哪些浏览器功能：

```html
<iframe
  src="https://player.example.com/embed/course-101"
  title="HTML 基础课程视频"
  allow="autoplay; fullscreen; picture-in-picture"
  allowfullscreen
></iframe>
```

| 功能 | 作用 |
|---|---|
| `autoplay` | 自动播放媒体 |
| `fullscreen` | 进入全屏模式 |
| `picture-in-picture` | 使用画中画模式 |

不要无条件复制很长的权限列表，应按嵌入内容实际需要开放。

## 2、referrerpolicy

浏览器请求嵌入页面时，可能通过 `Referer` 请求头发送当前页面来源。`referrerpolicy` 用于控制发送多少来源信息：

```html
<iframe
  src="https://map.example.com/embed/city-center"
  title="市中心地图"
  referrerpolicy="strict-origin-when-cross-origin"
></iframe>
```

学习初期只需记住：它用于控制当前页面向外部嵌入地址透露多少来源信息。

## 3、loading 懒加载

首屏之外的 `iframe` 可以使用 `loading="lazy"`：

```html
<iframe
  src="./pages/interactive-example.html"
  title="交互练习"
  width="640"
  height="480"
  loading="lazy"
></iframe>
```

浏览器可以等嵌入区域接近可视范围时再加载，减少页面初次打开时的网络请求。

# 五、嵌入视频、地图与 srcdoc

## 1、嵌入视频

视频平台通常提供专门的嵌入地址：

```html
<iframe
  src="https://player.example.com/embed/course-101"
  title="HTML 基础课程视频"
  width="640"
  height="360"
  allow="fullscreen; picture-in-picture"
  allowfullscreen
></iframe>
```

应使用平台提供的嵌入地址，而不是直接复制普通播放页地址。

## 2、嵌入地图

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

额外提供普通链接，可以让无法正常使用嵌入内容的用户在新页面中访问地图。

## 3、srcdoc 直接嵌入 HTML

`srcdoc` 可以直接提供一小段 HTML，而不加载另一个文件：

```html
<iframe
  title="课程完成提示"
  srcdoc="<h2>练习完成</h2><p>你已经掌握 iframe 的基础用法。</p>"
  width="500"
  height="200"
></iframe>
```

如果同时提供 `srcdoc` 和 `src`，支持 `srcdoc` 的浏览器通常优先使用 `srcdoc`。

`srcdoc` 适合简短、可信的静态内容。不要把未经处理的用户输入直接放入 `srcdoc`。

# 六、iframe 的安全边界

## 1、同源限制

浏览器使用同源策略限制页面访问不同来源的内容。来源通常由协议、域名和端口共同决定。

例如：

```text
当前页面：https://learn.example.com
嵌入页面：https://map.example.net
```

两个页面域名不同，属于跨源。当前页面通常不能直接读取或修改嵌入页面中的标题、段落和表单内容。

同源策略防止恶意页面随意读取其他网站的嵌入内容，是浏览器安全模型的重要部分。

## 2、sandbox 属性

`sandbox` 可以进一步限制嵌入页面的能力：

```html
<iframe
  src="./pages/user-example.html"
  title="用户提交的示例"
  sandbox
></iframe>
```

只写空 `sandbox` 会启用一组严格限制。可以按需放开能力：

```html
<iframe
  src="./pages/form-preview.html"
  title="表单预览"
  sandbox="allow-forms"
></iframe>
```

常见值：

| 值 | 放开的能力 |
|---|---|
| `allow-forms` | 允许提交表单 |
| `allow-scripts` | 允许运行脚本 |
| `allow-popups` | 允许打开弹出页面 |
| `allow-downloads` | 允许触发下载 |

> [!warning] 不要随意组合高权限
> 对同源内容同时使用 `allow-scripts` 和 `allow-same-origin` 可能显著削弱沙箱限制。没有明确需求时，不要照搬不理解的配置。

# 七、完整示例

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iframe 练习</title>
  </head>
  <body>
    <main>
      <h1>iframe 练习</h1>

      <section>
        <h2>课程视频</h2>
        <iframe
          src="https://player.example.com/embed/course-101"
          title="HTML 基础课程视频"
          width="640"
          height="360"
          allow="fullscreen; picture-in-picture"
          allowfullscreen
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

# 八、小结

- 替换元素的内容由外部资源或浏览器内部控件决定。
- `img`、`audio`、`video` 和 `iframe` 都是常见替换元素。
- 页面可以控制替换元素外部尺寸和位置，但通常不能直接修改资源内部内容。
- `iframe` 会创建独立浏览上下文，不是简单复制目标页面元素。
- `title` 对 `iframe` 可访问性很重要。
- `allow` 和 `allowfullscreen` 用于声明嵌入内容可请求的能力。
- `loading="lazy"` 适合首屏之外的嵌入内容。
- 同源策略和 `sandbox` 是理解 `iframe` 安全边界的关键。
