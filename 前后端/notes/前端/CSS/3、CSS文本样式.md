---
title: CSS文本样式
date: 2026-08-05
tags: [Web, 前端, CSS, 文本样式]
aliases:
  - CSS Text
  - CSS字体样式
---

# 一、字体样式

CSS 文本样式用于控制网页中文字的外观。字体样式这一组重点解决“文字看起来是什么样”的问题，例如颜色、字体、字号、斜体、粗细和装饰线。

需要先明确一点：CSS 不能直接“修改文字本身”，它修改的是包住文字的 HTML 元素样式。也就是说，浏览器先根据 HTML 找到元素，再根据 CSS 把样式画出来。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>字体样式示例</title>
  <style>
    .text-demo {
      color: #1d4ed8;
      font-family: Arial, "Microsoft YaHei", sans-serif;
      font-size: 20px;
      font-style: normal;
      font-weight: 700;
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <p class="text-demo">这是一段被 CSS 修饰的文字。</p>
</body>
</html>
```

这段代码统一使用 `.text-demo` 作为示例类名。后面只改这一组规则里的不同属性，观察文字外观如何变化。

## 1、字体颜色

`color` 设置文字颜色。它影响的是文本前景色，不是背景色。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>字体颜色</title>
  <style>
    .text-demo {
      color: #e11d48;
    }
  </style>
</head>
<body>
  <p class="text-demo">这段文字会显示为红色。</p>
</body>
</html>
```

常见颜色写法：

| 写法 | 示例 | 说明 |
|---|---|---|
| 颜色关键字 | `red` | 适合学习和快速演示 |
| 十六进制 | `#e11d48` | 实际开发常用，设计稿里经常出现 |
| `rgb()` | `rgb(225 29 72)` | 用红、绿、蓝三个通道表示颜色 |
| `rgb()` 带透明度 | `rgb(225 29 72 / 70%)` | 颜色带透明效果 |

十六进制颜色也可以简写。例如 `#ff0000` 可以写成 `#f00`，它们都表示纯红色。

## 2、字体族

`font-family` 设置字体列表。它不是只写一个字体，而是写一个按优先级排列的字体候选列表。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>字体族</title>
  <style>
    .text-demo {
      font-family: Arial, "Microsoft YaHei", sans-serif;
    }
  </style>
</head>
<body>
  <p class="text-demo">浏览器会按顺序选择可用字体。</p>
</body>
</html>
```

浏览器会按顺序尝试：先看有没有 `Arial`，再看有没有 `"Microsoft YaHei"`，最后使用 `sans-serif` 这类通用字体兜底。

书写字体族时注意两点：

- 字体名包含空格时，建议加引号，例如 `"Microsoft YaHei"`。
- 列表最后最好放一个通用字体族，例如 `sans-serif`、`serif`、`monospace`。

常见通用字体族：

| 字体族 | 大致效果 | 常见场景 |
|---|---|---|
| `sans-serif` | 无衬线字体，笔画干净 | 网页正文、界面文字 |
| `serif` | 衬线字体，笔画末端有装饰 | 长文章、偏传统的排版 |
| `monospace` | 等宽字体，每个字符宽度接近 | 代码、终端、表格数字 |

中文网页常见写法：

```css
.text-demo {
  font-family: Arial, "Microsoft YaHei", "PingFang SC", sans-serif;
}
```

## 3、字体大小

`font-size` 设置文字大小。入门阶段可以先使用 `px`，因为它直观、稳定，适合观察效果。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>字体大小</title>
  <style>
    .text-demo {
      font-size: 24px;
    }
  </style>
</head>
<body>
  <p class="text-demo">这段文字的字号是 24px。</p>
</body>
</html>
```

浏览器通常会给 `body` 一个默认字号，常见是 `16px`。为了让页面更可控，实际项目里经常会给 `body` 设置基础字号：

```css
body {
  font-size: 16px;
}
```

字号不是越大越好。正文要优先保证阅读舒适，标题再通过更大的字号形成层级。

## 4、字体风格

`font-style` 控制文字是否使用斜体。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>字体风格</title>
  <style>
    .text-demo {
      font-style: italic;
    }
  </style>
</head>
<body>
  <p class="text-demo">这段文字会以斜体显示。</p>
</body>
</html>
```

常用值：

| 值 | 含义 |
|---|---|
| `normal` | 普通字体 |
| `italic` | 斜体 |

`em`、`i` 等元素在浏览器默认样式中通常会显示为斜体。如果只是想取消默认斜体，可以这样写：

```css
em,
i {
  font-style: normal;
}
```

## 5、字体粗细

`font-weight` 设置文字粗细。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>字体粗细</title>
  <style>
    .text-demo {
      font-weight: 700;
    }
  </style>
</head>
<body>
  <p class="text-demo">这段文字会更粗。</p>
</body>
</html>
```

常用值：

| 值 | 含义 |
|---|---|
| `normal` | 正常粗细，通常等于 `400` |
| `bold` | 加粗，通常等于 `700` |
| `400` | 正常粗细 |
| `700` | 加粗 |

数字值通常写在 `100` 到 `900` 之间。实际显示效果还取决于当前字体是否提供对应粗细：如果字体没有某个字重，浏览器会尽量匹配一个接近的效果。

## 6、字体装饰

`text-decoration` 设置文字上的装饰线，例如下划线、上划线和删除线。严格说它不是“字体本身”的属性，而是文字装饰属性；但在入门阶段，它常和字体颜色、大小、粗细一起学习。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>字体装饰</title>
  <style>
    .text-demo {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <p class="text-demo">这段文字有下划线。</p>
</body>
</html>
```

常用值：

| 值 | 含义 |
|---|---|
| `none` | 没有装饰线 |
| `underline` | 下划线 |
| `overline` | 上划线 |
| `line-through` | 删除线 |

常见用法是控制链接样式：

```css
a {
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
```

取消链接下划线时要小心。链接仍然需要有清楚的视觉提示，否则用户可能分不出哪些文字可以点击。

## 7、组合示例

实际写样式时，通常不会只设置一个字体属性，而是把一组文字外观一起定义。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>字体样式组合</title>
  <style>
    body {
      font-family: Arial, "Microsoft YaHei", "PingFang SC", sans-serif;
      font-size: 16px;
      color: #111827;
    }

    .text-demo {
      color: #1d4ed8;
      font-size: 24px;
      font-style: italic;
      font-weight: 700;
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <p class="text-demo">这是一段组合了多种字体样式的文字。</p>
</body>
</html>
```

`body` 适合放全站通用的字体、字号和文字颜色；具体元素再用类选择器覆盖某些样式。这样既统一，又不会让每个元素都重复写一堆规则。

# 二、文本布局

文本布局这一组属性重点解决“文字在自己的盒子里怎么排”的问题，例如水平对齐、首行缩进、字符间距和行高。

这类属性通常对块级元素更直观，例如 `p`、`div`、`section`、`article`。因为文本需要先放在一个有宽度的盒子里，浏览器才知道它应该左对齐、居中、两端对齐，或者在多行之间留多少空间。

## 1、文本对齐

`text-align` 控制文本在当前块级盒子里的水平对齐方式。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>文本对齐</title>
  <style>
    .text-demo {
      width: 360px;
      padding: 16px;
      border: 1px solid #d1d5db;
      text-align: center;
    }
  </style>
</head>
<body>
  <p class="text-demo">这段文字会在盒子里水平居中。</p>
</body>
</html>
```

常用值：

| 值 | 含义 |
|---|---|
| `left` | 左对齐，很多浏览器环境下是默认效果 |
| `right` | 右对齐 |
| `center` | 水平居中 |
| `justify` | 两端对齐，通过调整空隙让每一行贴近左右两边 |

`text-align` 对盒子里的行内内容也会生效。例如图片本身是行内级内容时，可以让父元素 `text-align: center;` 来让图片居中。

`justify` 更适合较长段落。短文本、按钮文字、导航项强行两端对齐，通常会出现难看的空隙。

## 2、首行缩进

`text-indent` 设置块级元素第一行文本前面的缩进量，常见于文章段落。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>首行缩进</title>
  <style>
    .text-demo {
      width: 520px;
      line-height: 1.8;
      text-indent: 2em;
    }
  </style>
</head>
<body>
  <p class="text-demo">
    CSS 可以控制段落的首行缩进。中文文章里常见的“首行空两个字”，就可以用 text-indent: 2em 来表达。
  </p>
</body>
</html>
```

`em` 是相对单位，`1em` 通常等于当前元素的字体大小。因此 `text-indent: 2em;` 可以理解为“首行缩进两个当前字号的宽度”。

`text-indent` 只影响第一行。如果段落自动换行，第二行及后面的行不会继续缩进。

## 3、字符间距

`letter-spacing` 设置字符之间的额外间距。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>字符间距</title>
  <style>
    .text-demo {
      font-size: 28px;
      letter-spacing: 4px;
    }
  </style>
</head>
<body>
  <p class="text-demo">山野徒步路线</p>
</body>
</html>
```

`letter-spacing` 的值可以是正数，也可以是负数：

```css
.text-demo {
  letter-spacing: 2px;
}
```

正数会让字符更疏，负数会让字符更紧。负值要谨慎使用，过小可能导致字符挤在一起，影响阅读。

这个属性常用于标题、标签、导航项等短文本。正文段落通常不需要明显增加字符间距。

## 4、行高

`line-height` 设置一行文字占用的高度。它影响多行文本的上下间距，也可以影响单行文字在行盒中的垂直位置。



示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>行高</title>
  <style>
    .text-demo {
      width: 520px;
      font-size: 18px;
      line-height: 1.8;
    }
  </style>
</head>
<body>
  <p class="text-demo">
    行高会影响多行文本之间的距离。行高太小，文字会显得拥挤；行高合适，段落读起来更轻松。
  </p>
</body>
</html>
```

`line-height` 常见写法有两种：

| 写法 | 示例 | 含义 |
|---|---|---|
| 数字 | `line-height: 1.6;` | 当前字体大小的 `1.6` 倍 |
| 长度 | `line-height: 28px;` | 每行固定占用 `28px` 高 |

实际写正文时，更推荐使用不带单位的数字，例如 `line-height: 1.6;`。它会随着当前 `font-size` 计算，更适合继承和响应式排版。

单行文本垂直居中时，也经常看到这种写法：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>单行文本垂直居中</title>
  <style>
    .text-demo {
      width: 240px;
      height: 48px;
      border: 1px solid #d1d5db;
      text-align: center;
      line-height: 48px;
    }
  </style>
</head>
<body>
  <p class="text-demo">单行文字垂直居中</p>
</body>
</html>
```

这段代码让盒子的 `height` 和 `line-height` 都是 `48px`，单行文字会看起来垂直居中。

需要注意的是，这个技巧只适合单行文字。多行文本、按钮复杂布局或图标文字混排，后面更常用 Flex 布局来处理垂直居中。

## 5、布局汇总

| 属性 | 作用 | 常用值 | 注意事项 |
|---|---|---|---|
| `text-align` | 控制文本水平对齐 | `left`、`right`、`center`、`justify` | 主要看父级块盒子的宽度 |
| `text-indent` | 控制首行缩进 | `2em`、`20px` | 只影响第一行 |
| `letter-spacing` | 控制字符间距 | `2px`、`normal` | 正文不要过度使用 |
| `line-height` | 控制一行文字占用的高度 | `1.6`、`28px` | 正文推荐不带单位的数字 |

文本布局的主线可以记成一句话：先确定文字所在盒子的宽度，再决定它在水平方向怎么对齐、第一行是否缩进、字符之间多远、每一行占多高。

# 三、font 简写

`font` 是字体相关属性的简写属性，可以在一条声明里同时设置字号、行高、字体族、斜体和粗细等属性。

它适合给一个组件或整个页面统一设置基础字体样式。比如很多网站会在 `body` 上设置一套默认字体：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>font 简写</title>
  <style>
    body {
      font: 16px/1.6 Arial, "Microsoft YaHei", sans-serif;
      color: #111827;
    }
  </style>
</head>
<body>
  <p>这段文字使用 body 上统一设置的字体样式。</p>
</body>
</html>
```

上面的 `font: 16px/1.6 Arial, "Microsoft YaHei", sans-serif;` 可以拆成：

```css
body {
  font-size: 16px;
  line-height: 1.6;
  font-family: Arial, "Microsoft YaHei", sans-serif;
}
```

## 1、基本语法

`font` 简写常见结构如下：

```css
.text-demo {
  font: font-style font-weight font-size/line-height font-family;
}
```

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>font 简写语法</title>
  <style>
    .text-demo {
      font: italic 700 24px/1.5 Arial, "Microsoft YaHei", sans-serif;
    }
  </style>
</head>
<body>
  <p class="text-demo">这段文字同时设置了斜体、粗细、字号、行高和字体族。</p>
</body>
</html>
```

这条声明大致等价于：

```css
.text-demo {
  font-style: italic;
  font-weight: 700;
  font-size: 24px;
  line-height: 1.5;
  font-family: Arial, "Microsoft YaHei", sans-serif;
}
```

## 2、必写和顺序

`font` 简写有严格的书写规则：

| 规则 | 说明 |
|---|---|
| `font-size` 必须写 | 否则整条 `font` 声明无效 |
| `font-family` 必须写 | 并且要放在最后 |
| `line-height` 可选 | 如果写，必须紧跟在 `font-size` 后面，用 `/` 分隔 |
| `font-style`、`font-weight` 可选 | 如果写，要放在 `font-size` 前面 |

正确示例：

```css
.text-demo {
  font: 20px Arial, sans-serif;
}

.text-demo {
  font: 20px/1.6 Arial, sans-serif;
}

.text-demo {
  font: italic 700 20px/1.6 Arial, sans-serif;
}
```

错误示例：

```css
.text-demo {
  font: Arial, sans-serif 20px;
}
```

这条写法把 `font-family` 放到了字号前面，不符合 `font` 简写的解析规则。

## 3、省略会重置

简写属性的一个重要特点是：没有写到的子属性，通常会被重置为默认值。`font` 也是如此。

示例：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>font 简写重置</title>
  <style>
    .text-demo {
      font-style: italic;
      font-weight: 700;
      font: 20px/1.6 Arial, "Microsoft YaHei", sans-serif;
    }
  </style>
</head>
<body>
  <p class="text-demo">这段文字不会保持斜体和加粗。</p>
</body>
</html>
```

虽然前面写了 `font-style: italic;` 和 `font-weight: 700;`，但后面的 `font` 简写没有写斜体和粗细，所以它们会回到默认效果。

如果希望保留斜体和加粗，就要把它们也写进 `font` 简写里：

```css
.text-demo {
  font: italic 700 20px/1.6 Arial, "Microsoft YaHei", sans-serif;
}
```

## 4、使用建议

`font` 简写适合用在两类地方：

- **全局基础文字**：例如在 `body` 上统一设置 `font-size`、`line-height` 和 `font-family`。
- **组件级文字样式**：例如标题、按钮、卡片摘要需要一组稳定字体样式。

初学时，如果只是改某一个属性，优先写具体属性：

```css
.text-demo {
  font-size: 18px;
}
```

如果要一次设置一整组字体规则，再使用 `font` 简写：

```css
.text-demo {
  font: 18px/1.7 Arial, "Microsoft YaHei", sans-serif;
}
```

这样更不容易因为简写重置而把已有样式意外覆盖。
