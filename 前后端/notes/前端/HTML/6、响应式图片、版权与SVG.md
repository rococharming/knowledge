---
title: 响应式图片、版权与SVG
date: 2026-07-13
tags: [HTML, 前端基础, 图像优化, SVG, 版权]
aliases:
  - HTML图像优化
  - 响应式图片
  - SVG矢量图
---

# 一、图像优化的目标

图像通常是网页中体积最大的资源之一。未经处理的大图会增加下载量、延长加载时间，并消耗用户流量。

图像优化主要关注四件事：

1. 尺寸是否接近实际显示需求。
2. 格式是否适合图像内容。
3. 压缩是否平衡体积与质量。
4. 是否兼顾可访问性和版权合规。

`img` 的 `src` 与 `alt` 基础可回看 [[1、HTML元素、属性与基础语义#3、图片属性：src 与 alt|图片属性]]。

# 二、尺寸与响应式图片

## 1、不要只靠 CSS 缩小大图

如果页面只需要以 `640 × 480` 显示图片，却提供 `3840 × 2160` 原图，浏览器仍然要下载完整大图后再缩小显示。

> [!tip] CSS 改变显示尺寸，不改变传输体积
> `width` 和 `height` 只能改变图片在页面中的显示大小，不会自动让服务器传输更小文件。

准备图片时，应让资源尺寸尽量接近实际显示需求。

## 2、像素密度描述符

同一张图片在高像素密度屏幕上可能需要更高清版本。例如显示尺寸是 `400 × 300`，可以准备普通版和两倍版：

```html
<img
  src="./images/workspace-400.jpg"
  srcset="
    ./images/workspace-400.jpg 1x,
    ./images/workspace-800.jpg 2x
  "
  width="400"
  height="300"
  alt="摆放着显示器和键盘的学习桌"
>
```

| 描述符 | 含义 |
|---|---|
| `1x` | 面向普通像素密度屏幕 |
| `2x` | 面向两倍像素密度屏幕 |

这两个版本在页面中显示尺寸相近，但 `2x` 图片包含更多像素，在高像素密度屏幕上更清晰。

## 3、宽度描述符与 sizes

当图片显示宽度会随页面变化时，可以提供不同固有宽度的候选资源：

```html
<img
  src="./images/library-800.jpg"
  srcset="
    ./images/library-480.jpg 480w,
    ./images/library-800.jpg 800w,
    ./images/library-1280.jpg 1280w
  "
  sizes="(max-width: 600px) 100vw, 800px"
  width="800"
  height="533"
  alt="阳光照进一间安静的图书馆"
>
```

| 片段 | 作用 |
|---|---|
| `480w`、`800w`、`1280w` | 声明图片文件自身宽度 |
| `sizes` | 告诉浏览器图片在不同条件下预计显示多宽 |
| `src` | 默认资源和后备资源 |

> [!note] 描述符不要混用
> 同一个 `srcset` 要么使用 `1x`、`2x` 这类像素密度描述符，要么使用 `480w`、`800w` 这类宽度描述符，不要混在一起。

## 4、width 与 height 预留比例

为 `img` 设置 `width` 和 `height`，可以让浏览器在图片下载前预留正确比例，减少内容突然移动：

```html
<img
  src="./images/course-cover.webp"
  width="640"
  height="360"
  alt="HTML 课程封面"
>
```

再用 CSS 控制响应式缩放：

```css
img {
  max-width: 100%;
  height: auto;
}
```

# 三、格式、压缩与加载

## 1、选择合适格式

| 格式 | 特点 | 常见用途 |
|---|---|---|
| JPEG | 有损压缩，兼容性好，不支持透明 | 照片 |
| PNG | 支持透明，常用无损压缩 | 截图、界面素材 |
| WebP | 支持有损、无损、透明和动画 | 通用网页图片 |
| AVIF | 压缩效率高，支持透明和高动态范围 | 对体积敏感的现代页面 |
| SVG | 矢量格式，缩放不失真 | 图标、Logo、简单插图 |

格式选择要结合图片内容、浏览器支持、编码成本、透明需求和项目处理流程，而不是简单追新。

## 2、picture 提供格式回退

`picture` 可以为同一张图提供不同格式：

```html
<picture>
  <source srcset="./images/course-cover.avif" type="image/avif">
  <source srcset="./images/course-cover.webp" type="image/webp">
  <img
    src="./images/course-cover.jpg"
    width="800"
    height="450"
    alt="笔记本电脑上显示着 HTML 代码"
  >
</picture>
```

浏览器按顺序选择第一个支持的 `source`，最后由内部 `img` 提供展示和替代文本。

## 3、压缩策略

无损压缩适合：

- 需要保留精确像素的截图。
- 简单图形和界面素材。
- 需要透明背景的图片。
- 不能接受压缩伪影的场景。

有损压缩适合照片等细节丰富图像，因为适度丢失信息通常不容易被察觉。

> [!warning] 避免反复压缩有损图片
> 每次重新保存或重新压缩 JPEG 等有损图片，都可能继续丢失数据。应保留高质量原始文件，再从原文件生成发布版本。

## 4、懒加载与替代文本

首屏之外的图片可以使用 `loading="lazy"`：

```html
<img
  src="./images/article-example.webp"
  width="800"
  height="450"
  loading="lazy"
  alt="文章中的 HTML 代码示例"
>
```

首屏关键图片通常不应懒加载，否则可能延迟主要内容显示。

具有内容意义的图片应提供准确 `alt`。纯装饰图片使用空值：

```html
<img src="./images/decorative-line.svg" alt="">
```

# 四、图片版权与许可

## 1、网上能看到不等于可自由使用

图片通常从创作完成时就受到版权保护。能下载、能右键保存，不代表可以放进自己的网页。

合法使用图片通常需要具备依据：

- 自己创作并拥有相关权利。
- 获得权利人明确授权。
- 购买符合使用场景的许可证。
- 按开放许可证条款使用。
- 图片确实属于公有领域。
- 使用方式符合当地版权例外。

**All Rights Reserved（保留所有权利）** 通常表示版权人没有通过通用许可开放复制、修改或传播权限。

## 2、Creative Commons 与 CC0

Creative Commons（CC，知识共享协议）包含多种条件：

| 标记 | 含义 |
|---|---|
| BY | 署名 |
| SA | 相同方式共享 |
| NC | 非商业使用 |
| ND | 禁止演绎 |

常见组合：

- CC BY：允许使用和修改，但必须署名。
- CC BY-SA：必须署名，改编作品使用相同许可。
- CC BY-NC：必须署名，且不能用于商业用途。
- CC BY-ND：必须署名，且不能发布修改版本。

CC0 是权利人尽可能放弃相关版权和邻接权、贡献给公众使用的工具。即使使用 CC0 图片，也要留意商标、肖像权、隐私权和当地法律限制。

## 3、授权核查清单

使用外部图片前，可以记录：

- 图片作者和原始来源。
- 许可名称及版本。
- 获取图片和许可信息的日期。
- 是否允许商业使用。
- 是否允许修改。
- 署名方式。
- 原始许可页面或授权证明。

> [!warning] 版权规则因地区而异
> 涉及商业发布或授权不明确时，应核对原始授权文件，必要时咨询专业人士。

# 五、SVG 矢量图

## 1、位图与矢量图

PNG、JPEG、WebP 等通常是位图，用像素网格保存图像。放大超过原始尺寸时，可能出现模糊或锯齿。

SVG（Scalable Vector Graphics，可缩放矢量图形）用点、线、曲线和路径描述图形，不依赖固定像素网格，因此缩放时边缘仍然清晰。

SVG 适合：

- 图标。
- Logo。
- 简单插图。
- 数据图形。
- 需要根据主题改变颜色的图形。

SVG 不适合细节复杂的照片。

## 2、SVG 结构与 viewBox

```html
<svg
  width="120"
  height="120"
  viewBox="0 0 120 120"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-labelledby="sun-title"
>
  <title id="sun-title">太阳图标</title>
  <circle
    cx="60"
    cy="60"
    r="38"
    fill="gold"
    stroke="darkorange"
    stroke-width="4"
  />
</svg>
```

`viewBox="0 0 120 120"` 定义内部坐标系统和可视区域。浏览器会把这套坐标映射到实际显示尺寸。

常见 SVG 元素：

| 元素 | 作用 |
|---|---|
| `circle` | 绘制圆形 |
| `rect` | 绘制矩形 |
| `line` | 绘制直线 |
| `polyline` | 绘制多段折线 |
| `polygon` | 绘制封闭多边形 |
| `path` | 绘制复杂路径 |

## 3、img 引用与内联 SVG

像普通图片一样引用：

```html
<img
  src="./icons/check.svg"
  width="48"
  height="48"
  alt="操作成功"
>
```

直接写进 HTML：

```html
<button class="confirm-button" type="button">
  <svg viewBox="0 0 24 24" aria-hidden="true">
    <path
      d="M5 12.5L9.5 17L19 7.5"
      fill="none"
      stroke="currentColor"
      stroke-width="2.5"
    ></path>
  </svg>
  确认
</button>
```

| 方式 | 优点 | 注意事项 |
|---|---|---|
| `img` 引用 | HTML 简洁，文件可缓存 | 页面 CSS 不容易直接控制 SVG 内部 |
| 内联 SVG | 可用 CSS 和 JavaScript 控制内部元素 | 会增加 HTML 体积 |

不可信来源的 SVG 不应直接内联到页面中，应先检查或清理脚本、事件属性和外部资源引用。

# 六、完整示例

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>图像优化示例</title>
  </head>
  <body>
    <main>
      <h1>前端图像优化</h1>

      <picture>
        <source
          srcset="./images/workspace-480.avif 480w, ./images/workspace-960.avif 960w"
          type="image/avif"
        >
        <source
          srcset="./images/workspace-480.webp 480w, ./images/workspace-960.webp 960w"
          type="image/webp"
        >
        <img
          src="./images/workspace-960.jpg"
          srcset="./images/workspace-480.jpg 480w, ./images/workspace-960.jpg 960w"
          sizes="(max-width: 600px) 100vw, 960px"
          width="960"
          height="640"
          loading="lazy"
          alt="桌面上摆放着用于学习前端开发的电脑"
        >
      </picture>
    </main>
  </body>
</html>
```

# 七、小结

- 图像优化要同时考虑尺寸、格式、压缩、加载和可访问性。
- `srcset` 配合像素密度描述符适合固定显示尺寸的高清适配。
- `srcset` 配合宽度描述符和 `sizes` 适合响应式图片。
- `picture` 可以提供 AVIF、WebP 和传统格式的回退。
- `width` 和 `height` 能帮助浏览器预留图片比例，减少布局跳动。
- `loading="lazy"` 适合首屏之外图片。
- 网络图片要核对版权和许可，不能默认自由使用。
- SVG 适合图标、Logo 和简单插图，不适合复杂照片。
- 嵌入外部页面和替换元素可继续看 [[7、替换元素、iframe与嵌入安全|iframe 与嵌入安全]]。
