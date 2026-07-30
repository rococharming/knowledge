
伪类和伪元素都用于描述普通选择器难以直接表达的目标，它们选中的对象不同：
- 伪类：选中元素的某种状态或位置
- 伪元素：选择元素内部的某个部分，或创建一个虚拟部分

## 伪类选择器

伪类使用一个冒号`:`：

```css
选择器:伪类 {
	属性: 值;
}
```

### 描述元素的状态

表示用户交互状态

| 伪类          | 含义         |
| ----------- | ---------- |
| `:hover`    | 鼠标悬停       |
| `:active`   | 元素正在被点击    |
| `:focus`    | 元素获得焦点     |
| `:checked`  | 单选框或复选框已选中 |
| `:disabled` | 表单元素被禁用    |
| `:enabled`  | 表单元素可用     |

### 描述元素的位置

根据元素在父元素中的位置进行选择。

```html
<ul>
  <li>苹果</li>
  <li>香蕉</li>
  <li>橙子</li>
</ul>
```

选中第一个 `li`：

```css
li:first-child {
	color: red;
}
```

选中最后一个 `li`：

```css
li:last-child {
  color: blue;
}
```

选中第二个`li`：

```css
li:nth-child(2) {
  color: green;
}
```

选中所有奇数位置的 `li`：

```css
li:nth-child(odd) {
  background-color: #eee;
}
```

### 条件筛选

一些伪类用于排除、匹配或判断元素。

`:not()`：选择不符合条件的元素

```css
button:not(.primary) {
  color: gray;
}
```

`:is()`：合并多个选择器 

```
:is(h1, h2, h3) {
  font-family: sans-serif;
}
```

相当于：

```css
h1,
h2,
h3 {
  font-family: sans-serif;
}
```

 `:has()`

根据元素内部是否包含某个元素进行选择：

```
.card:has(img) {
  padding-top: 0;
}
```

表示选中内部包含 `<img>` 的 `.card` 元素。

## 伪元素选择器

伪元素通常使用两个冒号`::`：

```css
选择器::伪元素 {
  属性: 值;
}
```

例如：

```css
p::first-line {
  color: red;
}
```

这里不是选中整个 `<p>` 元素，而是选中：

> `<p>` 元素显示出来的第一行文字。

### 选中元素的某个部分

`::first-letter`：选中第一个字母或第一个字符
`::selection`：选中用户用鼠标框选的文字

### 创建虚拟内容

最常用的伪元素：

`::before`
`::after`

它们可以在元素内容的前面或后面插入虚拟内容。

```html
<p class="notice">系统维护中</p>
```

```css
.notice::before {
  content: "提示："; 
  color: red;
}
```

页面上会显示为：

```
提示：系统维护中
```

但 HTML 中实际上没有“提示：”这几个字，它是 CSS 生成的内容。

使用 `::after`：

```css
.notice::after {
  content: "!";
}
```

最终视觉效果类似：

```
系统维护中!
```

### content 属性

`::before`和`::after`通常必须设置`content`，否则伪元素不会生成。

```css
.box::before {
  content: "";
}
```

即使不需要显示文字，也经常要写空字符串：

```css
.box::before {
  content: "";
  display: block;
  width: 10px;
  height: 10px;
  background-color: red;
}
```

这会创建一个虚拟的小方块。

常见伪元素包括：

| 伪元素              | 含义           |
| ---------------- | ------------ |
| `::before`       | 在元素内容前创建虚拟内容 |
| `::after`        | 在元素内容后创建虚拟内容 |
| `::first-letter` | 选中第一个字符      |
| `::first-line`   | 选中第一行        |
| `::selection`    | 选中用户框选的文字    |
| `::placeholder`  | 选中输入框占位文字    |
| `::marker`       | 选中列表项目符号     |
