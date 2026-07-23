---
title: JSON 与 package.json
date: 2026-07-23
tags: [nodejs, npm, json, package-json]
aliases:
  - package.json
  - npm 项目配置
  - JSON 配置文件
---

# 一、JSON

JSON 是一种轻量级数据格式，用来表示结构化数据。它看起来像 JavaScript 对象，但本质上是一种独立的数据文本格式，常用于配置文件、接口数据和工具之间的信息交换。

在 npm 项目里，`package.json` 就是一个 JSON 文件。理解 JSON 的基本规则，是读懂 npm 项目配置的前提。

## 1、基本形态

JSON 最常见的形态是对象。对象用 `{}` 包起来，里面由一组 key-value 组成：

```json
{
  "name": "hello-npm",
  "version": "1.0.0",
  "private": true
}
```

这里有三个字段：

- `"name"`：项目或包的名字；
- `"version"`：版本号；
- `"private"`：是否禁止发布到 npm Registry。

可以先把 JSON 理解成一张结构化信息表：左边是字段名，右边是字段值。

## 2、值类型

JSON 支持的值类型很少，这也是它适合作为通用数据格式的原因。

| 类型 | 示例 | 说明 |
|---|---|---|
| 字符串 | `"hello"` | 必须使用双引号 |
| 数字 | `18`、`3.14` | 不加引号 |
| 布尔值 | `true`、`false` | 表示真假 |
| 空值 | `null` | 表示没有值 |
| 数组 | `["dev", "start"]` | 一组有顺序的值 |
| 对象 | `{"type": "module"}` | 一组 key-value |

示例：

```json
{
  "name": "text-counter",
  "version": "0.1.0",
  "keywords": ["cli", "text", "count"],
  "private": true,
  "author": null
}
```

`keywords` 是数组，表示多个关键词；`author` 是 `null`，表示暂时没有填写作者。

## 3、语法规则

JSON 的规则比 JavaScript 对象更严格。常见规则如下：

- 字段名必须使用双引号；
- 字符串必须使用双引号；
- 每个字段之间用英文逗号分隔；
- 最后一个字段后面不能有逗号；
- 不能写注释；
- 只能表达数据，不能写函数、变量或表达式。

错误示例：

```json
{
  name: "hello-npm",
  "version": "1.0.0",
}
```

这里有两个问题：`name` 没有双引号，最后一行后面多了一个逗号。

正确写法：

```json
{
  "name": "hello-npm",
  "version": "1.0.0"
}
```

> 需要注意：`package.json` 不能写注释。如果想解释某个配置，通常把解释写进学习笔记或项目 README，而不是写进 JSON 文件本身。

# 二、package.json

`package.json` 是 npm 项目的描述文件。它告诉 npm：这个项目叫什么、版本是多少、入口文件在哪里、有哪些命令、依赖哪些包。

在第 1 天的 [[1、Node.js 和 npm|Node.js 和 npm]] 中，Package 被理解为由 `package.json` 描述的软件包。到了第 2 天，重点就是亲手创建并读懂这个描述文件。

## 1、核心作用

一个 npm 项目通常至少有一个 `package.json`。它的作用可以分成三类：

| 作用 | 说明 | 典型字段 |
|---|---|---|
| 描述项目 | 记录项目名称、版本、简介、作者等信息 | `name`、`version`、`description` |
| 管理运行方式 | 记录项目可以执行哪些统一命令 | `scripts` |
| 管理依赖关系 | 记录项目需要哪些外部包 | `dependencies`、`devDependencies` |

入门阶段可以先记住一句话：

> `package.json` 是 npm 项目的身份证和说明书。

## 2、常见字段

一个最小 npm 项目可能长这样：

```json
{
  "name": "hello-npm",
  "version": "1.0.0",
  "description": "My first npm project",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

常见字段含义：

| 字段 | 含义 | 入门理解 |
|---|---|---|
| `name` | 包名或项目名 | npm 用它识别这个项目 |
| `version` | 版本号 | 通常使用 `主版本.次版本.修订版本` |
| `description` | 项目简介 | 给人看的简短说明 |
| `main` | 入口文件 | 别人导入这个包时默认加载的文件 |
| `scripts` | 命令集合 | 用 `npm run` 执行的统一命令 |
| `keywords` | 关键词 | 方便搜索和分类 |
| `author` | 作者 | 可以先留空 |
| `license` | 许可证 | 默认常见值是 `ISC` |

`scripts` 是一个对象，因为它内部还能继续放多条命令。例如：

```json
{
  "scripts": {
    "start": "node index.js",
    "test": "node test.js"
  }
}
```

这里 `"start"` 和 `"test"` 是命令名，右侧字符串是真正会被执行的命令。

# 三、创建项目

创建第一个 npm 项目的核心动作是：新建目录，进入目录，生成 `package.json`，再创建一个 JavaScript 文件运行起来。

## 1、初始化

先创建并进入项目目录：

```bash
mkdir hello-npm
cd hello-npm
```

执行初始化命令：

```bash
npm init -y
```

`npm init` 用来创建 `package.json`；`-y` 表示使用默认答案快速生成文件。

生成后，可以查看目录：

```bash
ls
```

通常会看到：

```text
package.json
```

此时项目目录大致是：

```text
hello-npm/
└── package.json
```

## 2、查看配置

打开 `package.json`，可能会看到类似内容：

```json
{
  "name": "hello-npm",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

这份文件还没有安装任何依赖，也没有真正的业务代码。它只是声明：当前目录已经是一个 npm 项目。

> 简单来说：有了 `package.json`，npm 才知道“这里是一个项目，我应该按这个项目的配置工作”。

## 3、补充代码

创建 `index.js`：

```js
console.log("Hello npm project");
```

此时目录变成：

```text
hello-npm/
├── index.js
└── package.json
```

直接用 Node.js 运行：

```bash
node index.js
```

如果终端输出：

```text
Hello npm project
```

说明这个项目已经可以运行 JavaScript 文件。

# 四、修改脚本

`scripts` 字段用来给项目命令起统一名字。这样以后不必记住底层命令细节，只需要记住 npm 项目约定的命令。

## 1、start 脚本

把 `package.json` 里的 `scripts` 改成：

```json
{
  "scripts": {
    "start": "node index.js"
  }
}
```

注意：这里展示的是片段，不是完整 `package.json`。真实文件里还会有 `name`、`version` 等其他字段。

然后执行：

```bash
npm run start
```

npm 会读取 `package.json` 里的 `scripts.start`，再执行右侧的 `node index.js`。

这个过程可以理解为：

```text
npm run start
      ↓
读取 package.json
      ↓
找到 scripts.start
      ↓
执行 node index.js
```

## 2、特殊命令

`start` 是 npm 的常用脚本名，因此也可以简写为：

```bash
npm start
```

它和下面这条命令在入门阶段可以理解为等价：

```bash
npm run start
```

但不是所有脚本名都有简写。一般脚本推荐使用完整形式：

```bash
npm run 命令名
```

第 6 天会专门学习 npm scripts。今天只需要知道：`scripts` 可以把项目里的常用命令集中写在 `package.json` 中。

# 五、项目边界

`package.json` 不只是一个普通配置文件，它也定义了 npm 项目的边界。

## 1、当前目录

npm 命令通常围绕当前目录工作。当你在 `hello-npm/` 里执行 npm 命令时，npm 会在当前目录或上级目录寻找 `package.json`。

如果找到，npm 就把那个目录当作项目根目录。

示例：

```text
hello-npm/
├── index.js
└── package.json
```

在 `hello-npm/` 中执行：

```bash
npm run start
```

npm 会使用 `hello-npm/package.json` 里的配置。

## 2、项目身份

`name` 和 `version` 共同描述一个包的身份：

```json
{
  "name": "hello-npm",
  "version": "1.0.0"
}
```

如果未来把项目发布到 npm Registry，`name` 会成为别人安装它时使用的包名，`version` 会用于区分不同发布版本。

今天创建的是学习项目，不需要发布。为了避免误发布，可以添加：

```json
{
  "private": true
}
```

`private: true` 表示这个包不允许被发布到 npm Registry，适合个人练习项目和应用项目。

# 六、自测

## 1、检查问题

完成第 2 天后，应该能回答这些问题：

- JSON 和 JavaScript 对象有什么区别？
- 为什么 `package.json` 里的字段名必须加双引号？
- `npm init -y` 做了什么？
- `package.json` 中的 `scripts` 是对象还是数组？
- `npm run start` 最终执行的是哪条命令？
- 为什么练习项目可以设置 `"private": true`？

## 2、今日成果

今天最终应该得到一个可以运行的 npm 项目：

```text
hello-npm/
├── index.js
└── package.json
```

最小可用配置可以整理为：

```json
{
  "name": "hello-npm",
  "version": "1.0.0",
  "private": true,
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  }
}
```

执行：

```bash
npm start
```

能够看到：

```text
Hello npm project
```

这说明已经完成第 2 天目标：理解 JSON 与 `package.json`，并创建第一个 npm 项目。下一步会进入依赖安装，重点是理解 `npm install`、`node_modules` 和依赖记录之间的关系。
