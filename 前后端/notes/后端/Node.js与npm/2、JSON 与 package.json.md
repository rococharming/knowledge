---
title: JSON 与 package.json
date: 2026-07-29
tags:
  - nodejs
  - npm
  - json
  - package-json
aliases:
  - package.json
  - npm 项目配置
  - JSON 配置文件
---

# 一、核心边界

`package.json` 是 npm 项目的描述文件。它告诉 npm：这个项目叫什么、版本是多少、有哪些脚本、依赖哪些包，以及是否允许发布。

这篇笔记只关注一个目标：能读懂一个最小 `package.json`，并理解 `npm run dev` 为什么会执行某个 JavaScript 文件。

![[assets/node-npm-package-json-map-handdrawn.svg|620]]

> 简单来说：`package.json` 像 npm 项目的控制文档；npm 读取它来安装依赖、执行脚本、准备发布；Node.js 通常只负责运行脚本最终指向的 JavaScript 文件。

# 二、JSON

`package.json` 必须是合法 JSON。JSON 是一种用文本表示结构化数据的格式，常用于配置文件、接口数据和程序之间的信息交换。更完整的 JSON 规则可以看 [[通用计算机知识/notes/数据格式/1、JSON|JSON]]。

## 1、基本形态

最小 JSON 对象长这样：

```json
{
  "name": "hello-package-json",
  "private": true,
  "keywords": ["node", "npm"]
}
```

可以先把 JSON 理解成一张结构化信息表：左边是字段名，右边是字段值。

| 位置 | 读法 | 例子 |
|---|---|---|
| `"name"` | 字段名，也叫 key | 必须用双引号 |
| `"hello-package-json"` | 字段值，也叫 value | 这是字符串 |
| `true` | 布尔值 | 不是字符串，所以不加引号 |
| `["node", "npm"]` | 数组 | 表示一组有顺序的值 |

## 2、语法规则

JSON 的规则比 JavaScript 对象更严格。入门阶段先记住这几条：

- 字段名必须使用双引号；
- 字符串必须使用双引号；
- 字段之间用英文逗号分隔；
- 最后一个字段后面不能有逗号；
- 不能写注释；
- 只能表达数据，不能写函数、变量或表达式。

错误示例：

```json
{
  name: "hello-package-json",
  "version": "1.0.0",
}
```

这里有两个问题：`name` 没有双引号，最后一行后面多了一个逗号。

正确写法：

```json
{
  "name": "hello-package-json",
  "version": "1.0.0"
}
```

> 需要注意：`package.json` 不能写注释。如果想解释某个配置，通常把解释写进学习笔记或项目 README，而不是写进 JSON 文件本身。

# 三、package.json

在 [[1、Node.js 和 npm|Node.js 和 npm]] 中，Package 被理解为由 `package.json` 描述的软件包。到了这里，重点是读懂这个描述文件里面最常见的几类字段。

## 1、项目身份

`name` 和 `version` 回答“这个项目是谁、当前版本是多少”。

示例：

```json
{
  "name": "hello-package-json",
  "version": "1.0.0",
  "private": true
}
```

常见字段可以这样理解：

| 字段 | 作用 | 入门理解 |
|---|---|---|
| `name` | 项目或包的名字 | 发布包时尤其重要；本地练习也建议写清楚 |
| `version` | 项目或包的版本 | 和 `name` 一起标识一个具体版本 |
| `private` | 是否禁止发布 | 练习项目或应用项目可设为 `true`，避免误发布 |

如果未来把项目发布到 npm Registry，`name` 会成为别人安装它时使用的包名，`version` 会用于区分不同发布版本。学习项目不需要发布，设置 `"private": true` 更稳妥。

## 2、脚本菜单

`scripts` 像项目的命令菜单。它把一条底层命令绑定到一个脚本名上，让团队可以用统一命令运行项目。

示例：

```json
{
  "scripts": {
    "dev": "node index.js",
    "hello": "node hello.js"
  }
}
```

执行：

```bash
npm run dev
```

npm 会读取 `package.json` 里的 `scripts.dev`，再执行右侧的 `node index.js`。

执行：

```bash
npm run hello
```

npm 会读取 `scripts.hello`，再执行右侧的 `node hello.js`。

这个过程可以理解为：

```text
npm run dev
      ↓
读取 package.json
      ↓
找到 scripts.dev
      ↓
执行 node index.js
```

这里的关键是：`npm run` 负责找脚本，`node` 负责运行脚本指向的 JavaScript 文件。

## 3、依赖清单

`dependencies` 和 `devDependencies` 用来记录项目依赖哪些外部包。

示例：

```json
{
  "dependencies": {
    "picocolors": "^1.0.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```

可以先这样区分：

| 字段 | 放什么 | 例子 |
|---|---|---|
| `dependencies` | 应用运行时需要的包 | 服务启动时要用到的库 |
| `devDependencies` | 开发、测试、构建时需要的工具 | TypeScript、测试工具、格式化工具 |

入门阶段不必急着深挖版本符号。先记住：依赖字段描述“这个项目需要哪些包”，npm 会根据这些字段安装对应包。

# 四、最小配置

一个用于学习的最小 `package.json` 可以只保留项目身份和脚本菜单：

```json
{
  "name": "package-json-lab",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "node index.js",
    "hello": "node hello.js"
  }
}
```

这份配置里有三层关系：

| 层次 | 字段 | 作用 |
|---|---|---|
| 项目身份 | `name`、`version`、`private` | 说明项目是谁、版本是多少、是否禁止发布 |
| 脚本入口 | `scripts.dev`、`scripts.hello` | 给底层命令起统一名字 |
| 执行目标 | `node index.js`、`node hello.js` | 真正启动 Node.js 运行文件 |

读 `package.json` 时，可以先按这个顺序看：

1. 先看 `name`，确认项目是谁；
2. 再看 `scripts`，确认怎么启动；
3. 最后看 `dependencies` 和 `devDependencies`，确认依赖哪些包。

# 五、实践：脚本映射

这个实践用于观察 `package.json` 如何影响项目运行。重点不是自己写 JavaScript，而是看清 `scripts` 中“脚本名”和“右侧命令”的映射关系。

## 1、创建目录

先创建并进入练习目录：

```bash
mkdir package-json-lab
cd package-json-lab
```

`mkdir package-json-lab` 表示创建一个练习目录；`cd package-json-lab` 表示进入这个目录。后面创建的 `package.json`、`index.js` 和 `hello.js` 都放在这里。

## 2、写入文件

创建 `package.json`，写入：

```json
{
  "name": "package-json-lab",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "node index.js",
    "hello": "node hello.js"
  }
}
```

创建 `index.js`，写入：

```js
console.log("This is index.js");
```

创建 `hello.js`，写入：

```js
console.log("This is hello.js");
```

这两个 JavaScript 文件只负责输出不同文本，方便观察 npm 脚本到底执行了哪个文件。

## 3、运行对照

在 `package-json-lab` 目录里执行：

```bash
npm run dev
npm run hello
```

应该看到两个不同输出：

```text
This is index.js
This is hello.js
```

两条命令的路径不同：

| 命令 | 读取的脚本 | 最终执行 |
|---|---|---|
| `npm run dev` | `scripts.dev` | `node index.js` |
| `npm run hello` | `scripts.hello` | `node hello.js` |

再把 `package.json` 里的 `dev` 脚本从：

```json
"dev": "node index.js"
```

改成：

```json
"dev": "node hello.js"
```

重新运行：

```bash
npm run dev
```

如果输出变成：

```text
This is hello.js
```

说明已经看清了这篇笔记的核心关系：npm 读取脚本配置，Node.js 执行脚本指向的文件。
