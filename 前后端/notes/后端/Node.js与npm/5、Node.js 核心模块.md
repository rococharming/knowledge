---
title: Node.js 核心模块
date: 2026-07-30
tags:
  - nodejs
  - core-modules
  - fs
  - path
aliases:
  - Node.js Core Modules
  - fs path process
  - Node.js 内置模块
---

# 一、核心边界

Node.js 不只是运行 JavaScript 的程序，它还自带一组核心模块，让 JavaScript 可以接触操作系统能力：读写文件、处理路径、读取当前进程信息等。

核心模块不需要 `npm install`。它们是 Node.js 自带的工具箱，直接从代码里导入即可。

![[assets/core-modules-map.png|620]]

> 简单来说：普通 JavaScript 只是在运行代码；Node.js 核心模块让代码能和文件、路径、进程这些系统资源打交道。

# 二、三件套

这篇先学习三个最常用的核心模块：`node:fs`、`node:path` 和 `node:process`。它们分别对应文件、路径和当前进程。

## 1、fs

`node:fs` 负责文件系统操作。入门阶段先用它完成两件事：写文件、读文件。

示例：

```js
import { writeFileSync, readFileSync } from "node:fs";

writeFileSync("message.txt", "Hello core modules");

const text = readFileSync("message.txt", "utf8");

console.log(text);
```

这里的 `writeFileSync` 会把文字写入 `message.txt`；`readFileSync` 会把文件内容读回来。第二个参数 `"utf8"` 表示按文本读取，而不是按原始二进制数据读取。

## 2、path

`node:path` 负责路径处理。不同操作系统的路径分隔符可能不同，手写字符串拼路径容易出错，`path` 模块可以把目录名和文件名安全地拼成路径。

示例：

```js
import { join } from "node:path";

const filePath = join("notes", "message.txt");

console.log(filePath);
```

`join("notes", "message.txt")` 表示把 `notes` 和 `message.txt` 拼成一个路径。后面项目目录变复杂时，路径处理会比手写字符串更可靠。

## 3、process

`node:process` 负责当前 Node.js 进程的信息。进程可以先理解为“当前正在运行的这个程序”。

示例：

```js
import process from "node:process";

console.log(process.cwd());
```

`process.cwd()` 会返回当前工作目录，也就是你运行命令时所在的位置。后面写 CLI 工具、读取配置文件、处理命令行参数时，`process` 会经常出现。

# 三、导入方式

现代 Node.js 推荐给核心模块加上 `node:` 前缀，比如 `node:fs`、`node:path`、`node:process`。这能让读代码的人一眼看出：这些模块来自 Node.js 自带能力，不是 npm 安装的第三方包。

## 1、node 前缀

推荐写法：

```js
import { readFileSync } from "node:fs";
import { join } from "node:path";
import process from "node:process";
```

这里有两种导入形态：

| 写法 | 含义 | 例子 |
|---|---|---|
| 命名导入 | 从模块里取出指定工具 | `import { join } from "node:path"` |
| 默认导入 | 导入模块提供的默认对象 | `import process from "node:process"` |

这篇沿用 [[4、模块系统|模块系统]] 里的 ES Module 写法，所以 `package.json` 需要写 `"type": "module"`。

## 2、同步 API

这篇示例使用 `writeFileSync` 和 `readFileSync`。名称里的 `Sync` 表示同步执行：写完文件后再继续下一行，读完文件后再继续下一行。

同步 API 的好处是顺序直观，适合入门观察：

```text
拼出路径
  ↓
写入文件
  ↓
读取文件
  ↓
打印结果
```

需要注意的是：真实后端服务里，大量文件操作通常会优先考虑异步 API。这篇先用同步 API，是为了让执行顺序更容易看清。

# 四、运行链路

把 `fs`、`path`、`process` 放在一起，可以写出一个完整的小程序：先得到当前目录，再拼出文件路径，然后写入文件、读取文件、打印内容。

## 1、完整代码

示例 `app.js`：

```js
import { writeFileSync, readFileSync } from "node:fs";
import { join } from "node:path";
import process from "node:process";

const filePath = join(process.cwd(), "message.txt");

writeFileSync(filePath, "Hello core modules");

const text = readFileSync(filePath, "utf8");

console.log("current folder:", process.cwd());
console.log("file path:", filePath);
console.log("file text:", text);
```

这段代码里，三个模块各自负责一块：

| 代码 | 来源模块 | 作用 |
|---|---|---|
| `process.cwd()` | `node:process` | 获取当前工作目录 |
| `join(...)` | `node:path` | 拼出 `message.txt` 的完整路径 |
| `writeFileSync(...)` | `node:fs` | 写入文件 |
| `readFileSync(...)` | `node:fs` | 读取文件 |

## 2、执行顺序

这段程序的执行顺序可以理解为：

```text
npm run dev
      ↓
读取 package.json 的 scripts.dev
      ↓
执行 node app.js
      ↓
process.cwd() 找到当前目录
      ↓
path.join() 拼出 message.txt 路径
      ↓
fs 写入并读取 message.txt
      ↓
打印目录、路径和文件内容
```

这条链路把前几课连起来了：[[3、npm scripts|npm scripts]] 提供统一入口，[[4、模块系统|模块系统]] 提供导入方式，核心模块提供访问系统能力。

# 五、实践：读写文件

这个实践用于完成一个最小闭环：用 `fs` 写文件，再用 `fs` 读文件，同时用 `path` 和 `process` 确定文件位置。

## 1、创建目录

创建并进入练习目录：

```bash
mkdir core-modules-lab
cd core-modules-lab
```

## 2、写入配置

创建 `package.json`，写入：

```json
{
  "name": "core-modules-lab",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "node app.js"
  }
}
```

这里继续使用 ES Module，所以要写 `"type": "module"`。`dev` 脚本会让 `npm run dev` 执行 `node app.js`。

## 3、写入程序

创建 `app.js`，写入：

```js
import { writeFileSync, readFileSync } from "node:fs";
import { join } from "node:path";
import process from "node:process";

const filePath = join(process.cwd(), "message.txt");

writeFileSync(filePath, "Hello core modules");

const text = readFileSync(filePath, "utf8");

console.log("current folder:", process.cwd());
console.log("file path:", filePath);
console.log("file text:", text);
```

## 4、运行对照

执行：

```bash
npm run dev
```

会看到类似输出：

```text
current folder: /你的路径/core-modules-lab
file path: /你的路径/core-modules-lab/message.txt
file text: Hello core modules
```

同时，目录里会多出一个 `message.txt` 文件。

再把这一行：

```js
writeFileSync(filePath, "Hello core modules");
```

改成：

```js
writeFileSync(filePath, "I can use Node.js core modules");
```

重新执行：

```bash
npm run dev
```

如果最后一行输出变成：

```text
file text: I can use Node.js core modules
```

说明已经完成“写文件 → 读文件 → 打印内容”的闭环。遇到错误时，优先检查导入模块名、`"type": "module"`、文件路径和英文引号。
