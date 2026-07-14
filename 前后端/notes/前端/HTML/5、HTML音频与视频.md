---
title: HTML音频与视频
date: 2026-07-13
tags: [HTML, 前端基础, 多媒体, 可访问性]
aliases:
  - 音视频媒体与字幕可访问性
  - audio与video
  - HTML字幕
---

# 一、HTML 多媒体的基本思路

HTML 使用 `audio` 和 `video` 在网页中嵌入媒体内容：

| 元素 | 用途 | 常见格式 |
|---|---|---|
| `audio` | 播放音乐、播客、语音 | MP3、WAV、Ogg |
| `video` | 播放教学视频、动画、影片 | MP4、WebM、Ogg |

媒体能否播放，不只取决于文件扩展名，还取决于容器格式和编码格式。实际项目中常为同一内容准备多个版本，让浏览器选择自己支持的资源。

# 二、audio 元素

## 1、嵌入音频

最简单的音频写法：

```html
<audio src="./media/morning-podcast.mp3"></audio>
```

这会加载音频，但页面默认不显示播放器。需要添加 `controls`：

```html
<audio src="./media/morning-podcast.mp3" controls></audio>
```

`controls` 是布尔属性，只要出现就表示显示浏览器内置播放控件。布尔属性规则可回看 [[1、HTML基础#4、布尔属性|布尔属性]]。

## 2、常用 audio 属性

| 属性 | 类型 | 作用 |
|---|---|---|
| `src` | 普通属性 | 指定音频文件位置 |
| `controls` | 布尔属性 | 显示播放控件 |
| `loop` | 布尔属性 | 播放结束后循环 |
| `muted` | 布尔属性 | 初始静音 |
| `autoplay` | 布尔属性 | 请求自动播放 |
| `preload` | 普通属性 | 提示浏览器预加载策略 |

示例：

```html
<audio
  src="./media/forest-ambience.mp3"
  controls
  loop
  muted
></audio>
```

## 3、preload 预加载

`preload` 提示浏览器在用户播放前加载多少媒体数据：

```html
<audio
  src="./media/morning-podcast.mp3"
  controls
  preload="metadata"
></audio>
```

| 值 | 含义 |
|---|---|
| `none` | 不主动预加载 |
| `metadata` | 只预加载时长等元信息 |
| `auto` | 浏览器可自行决定是否预加载更多内容 |

`preload` 只是提示，浏览器可能根据网络、流量策略和用户设置调整行为。

# 三、video 元素

## 1、嵌入视频

```html
<video src="./media/html-introduction.mp4" controls width="640"></video>
```

常见属性：

- `src` 指定视频文件。
- `controls` 显示播放控件。
- `width` 设置播放器显示宽度。
- `poster` 设置播放前封面图。

实际项目通常用 CSS 控制响应式尺寸：

```css
video {
  max-width: 100%;
  height: auto;
}
```

## 2、poster 封面图

`poster` 是 `video` 特有属性，用于设置视频播放前或加载期间显示的封面：

```html
<video
  src="./media/html-introduction.mp4"
  controls
  width="640"
  poster="./images/html-course-cover.jpg"
></video>
```

封面图能提前说明视频主题，也能避免视频未加载时出现空白区域。

# 四、source 与多格式回退

## 1、为什么需要 source

不是所有浏览器都支持同一种容器和编码。为了提高兼容性，可以在 `audio` 或 `video` 内部放多个 `source`，让浏览器按顺序选择可播放资源。

容器与编码可以这样理解：

- MP4、WebM、Ogg 是容器格式。
- H.264、VP9、AV1、AAC、Opus 是编码格式。
- 浏览器需要同时支持容器和内部编码，才能播放。

## 2、音频多格式

```html
<audio controls>
  <source src="./media/morning-podcast.ogg" type="audio/ogg">
  <source src="./media/morning-podcast.mp3" type="audio/mpeg">
  <p>你的浏览器无法播放该音频。</p>
</audio>
```

## 3、视频多格式

```html
<video
  controls
  width="640"
  poster="./images/html-course-cover.jpg"
>
  <source src="./media/html-introduction.webm" type="video/webm">
  <source src="./media/html-introduction.mp4" type="video/mp4">
  <p>你的浏览器不支持 HTML 视频播放。</p>
</video>
```

浏览器会按 `source` 顺序检查，选择第一个支持的资源。如果全部不支持，显示元素内部的后备内容。

## 4、type 属性

`type` 声明媒体 MIME 类型，帮助浏览器先判断支持情况：

| 文件 | MIME 类型 |
|---|---|
| MP3 | `audio/mpeg` |
| WAV | `audio/wav` |
| Ogg 音频 | `audio/ogg` |
| MP4 视频 | `video/mp4` |
| WebM 视频 | `video/webm` |

> [!tip] 单资源用 `src`，多资源用 `source`
> 只有一个媒体文件时，直接在 `audio` 或 `video` 上写 `src` 即可；需要兼容多格式时，用多个 `source` 更清晰。

# 五、自动播放与用户控制权

## 1、autoplay 的限制

`autoplay` 请求浏览器自动播放媒体：

```html
<video
  src="./media/product-preview.mp4"
  autoplay
  muted
  loop
  playsinline
></video>
```

现代浏览器通常会阻止带声音的自动播放，所以自动播放视频一般同时使用 `muted`。`playsinline` 表示在支持的移动设备上尽量页面内播放，而不是自动全屏。

> [!warning] 不要依赖自动播放传达关键信息
> 自动播放可能受浏览器策略、省电模式或用户偏好影响。页面的重要信息应能在不播放媒体的情况下被理解。

## 2、优先保留用户控制权

普通音频和主要视频内容通常应提供 `controls`。自动播放、循环播放和背景声音都要谨慎使用，避免打扰用户或影响使用辅助技术的人。

# 六、字幕与可访问性

## 1、track 元素

`track` 用于为视频提供字幕、说明或其他文本轨道：

```html
<video
  controls
  width="640"
  poster="./images/html-course-cover.jpg"
>
  <source src="./media/html-introduction.mp4" type="video/mp4">
  <track
    src="./captions/html-introduction-zh.vtt"
    kind="subtitles"
    srclang="zh"
    label="简体中文"
    default
  >
</video>
```

常用属性：

| 属性 | 作用 |
|---|---|
| `src` | 指定字幕文件位置 |
| `kind` | 指定文本轨道类型 |
| `srclang` | 指定字幕语言 |
| `label` | 设置播放器中显示的字幕名称 |
| `default` | 默认启用该文本轨道 |

字幕文件通常使用 WebVTT 格式，扩展名为 `.vtt`。

## 2、不要只依赖媒体

为了提高可访问性，应根据内容提供：

- 视频字幕。
- 音频文字稿。
- 重要画面的文字说明。
- 无法播放媒体时的后备内容。

# 七、完整示例

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML 多媒体示例</title>
  </head>
  <body>
    <main>
      <h1>HTML 多媒体示例</h1>

      <audio controls preload="metadata">
        <source src="./media/intro.ogg" type="audio/ogg">
        <source src="./media/intro.mp3" type="audio/mpeg">
        <p>你的浏览器无法播放该音频。</p>
      </audio>

      <video controls width="640" poster="./images/course-cover.jpg">
        <source src="./media/course.webm" type="video/webm">
        <source src="./media/course.mp4" type="video/mp4">
        <track
          src="./captions/course-zh.vtt"
          kind="subtitles"
          srclang="zh"
          label="简体中文"
          default
        >
        <p>你的浏览器不支持 HTML 视频播放。</p>
      </video>
    </main>
  </body>
</html>
```

# 八、小结

- `audio` 用于音频，`video` 用于视频。
- `controls` 显示浏览器内置播放控件。
- `poster` 为视频设置播放前封面。
- 多格式兼容时，用多个 `source` 让浏览器选择可播放资源。
- `type` 可声明 MIME 类型，减少无效下载尝试。
- `autoplay` 受浏览器策略限制，不应用来承载关键信息。
- `track` 可以添加字幕，提高视频可访问性。
- 图像、响应式图片和 SVG 可继续看 [[6、HTML图片|响应式图片与 SVG]]。
