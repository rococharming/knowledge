---
title: npm scripts
date: 2026-07-29
tags:
  - nodejs
  - npm
  - npm-scripts
  - package-json
aliases:
  - npm scripts
  - npm run
  - scripts 字段
---

# 一、核心边界

`npm scripts` 是写在 `package.json` 里的项目命令菜单。它把常用底层命令包装成统一入口，让项目成员不用记住每条具体命令，只需要执行约定好的 `npm run ...`。

在 [[2、JSON 与 package.json|JSON 与 package.json]] 中，`scripts` 是 `package.json` 的一个字段；这一篇单独展开它：左边是脚本名，右边是真正执行的命令。

![[assets/npm-scripts-menu.png|620]]

> 简单来说：npm 负责读取 `scripts` 菜单，Node.js 负责运行脚本右侧指向的 JavaScript 文件。

# 二、scripts

`scripts` 是一个 JSON 对象。对象里的每一项都表示一条项目命令：字段名是脚本名，字段值是实际要执行的命令字符串。

## 1、最小结构

示例：

```json
{
  "name": "scripts-lab",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "node index.js",
    "test": "node test.js",
    "hello": "node hello.js"
  }
}
```

这里可以分成两边看：

| 位置 | 含义 | 例子 |
|---|---|---|
| 左边脚本名 | npm 要查找的菜单项 | `dev`、`test`、`hello` |
| 右边命令 | 真正会被执行的命令 | `node index.js` |

所以 `scripts` 不是“自动运行代码”的地方，而是“给命令起名字”的地方。

## 2、映射关系

执行 `npm run` 时，npm 会根据脚本名去 `package.json` 里查对应字段。

| 你输入 | npm 查找 | 真正执行 |
|---|---|---|
| `npm run dev` | `scripts.dev` | `node index.js` |
| `npm run hello` | `scripts.hello` | `node hello.js` |
| `npm run test` | `scripts.test` | `node test.js` |

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

这里和 [[1、Node.js 和 npm|Node.js 和 npm]] 的分工一致：你输入的是 npm 命令，但最终输出来自某个 `.js` 文件；npm 负责查菜单，Node.js 负责运行文件。

# 三、执行规则

npm scripts 不只是字符串替换。它有一些固定规则，会影响脚本在哪里执行、怎样找到命令、哪些脚本可以简写。

## 1、执行位置

脚本通常从 `package.json` 所在目录执行。这个目录可以理解为 npm 项目的根目录。

示例：

```text
npm-scripts-lab/
├── package.json
├── index.js
└── src/
    └── server.js
```

如果 `package.json` 里写：

```json
{
  "scripts": {
    "dev": "node src/server.js"
  }
}
```

那么 `src/server.js` 是从 `package.json` 所在目录开始计算的相对路径。

## 2、本地命令

脚本运行时，本地依赖提供的命令通常可以直接写在 `scripts` 里。后面安装 TypeScript、ESLint、测试工具后，经常会看到这种写法：

```json
{
  "scripts": {
    "build": "tsc",
    "lint": "eslint ."
  }
}
```

这里的 `tsc` 和 `eslint` 通常来自项目本地依赖。这样做的好处是：项目脚本优先使用当前项目声明的工具版本，而不是依赖每个人电脑上的全局命令。

## 3、退出结果

脚本里的命令成功或失败，会影响 npm 命令本身的结果。比如测试脚本失败时，`npm test` 也会失败。

这条规则对自动化很重要：后面在 CI、测试和部署里，工具会根据脚本退出结果判断项目是否通过检查。入门阶段先记住：脚本不是只输出文字，它还会向外报告成功或失败。

# 四、常用命令

大多数自定义脚本都用 `npm run 脚本名` 执行。少数常用脚本有快捷入口，但不必一开始就背很多。

## 1、普通脚本

普通脚本使用：

```bash
npm run 脚本名
```

示例：

```bash
npm run dev
npm run hello
npm run build
```

忘记项目有哪些脚本时，可以执行：

```bash
npm run
```

npm 会列出当前项目中可用的脚本。读陌生项目时，这比猜命令更可靠。

## 2、快捷脚本

`start` 和 `test` 是常见脚本名，npm 提供了快捷写法：

| 完整写法 | 快捷写法 | 读取位置 |
|---|---|---|
| `npm run start` | `npm start` | `scripts.start` |
| `npm run test` | `npm test` | `scripts.test` |

入门阶段可以统一使用 `npm run xxx`；看到 `npm test` 和 `npm start` 时，知道它们是常见快捷入口即可。

# 五、实践：新增脚本

这个实践用于验证一件事：新增 npm script，本质上就是在 `package.json` 的 `scripts` 对象里新增一组“脚本名 → 命令”的映射。

## 1、创建目录

创建并进入练习目录：

```bash
mkdir npm-scripts-lab
cd npm-scripts-lab
```

## 2、写入文件

创建 `package.json`，写入：

```json
{
  "name": "npm-scripts-lab",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "node index.js",
    "hello": "node hello.js",
    "test": "node test.js"
  }
}
```

创建 `index.js`，写入：

```js
console.log("dev script: running index.js");
```

创建 `hello.js`，写入：

```js
console.log("hello script: running hello.js");
```

创建 `test.js`，写入：

```js
console.log("test script: running test.js");
```

## 3、运行对照

执行：

```bash
npm run dev
npm run hello
npm test
```

应该依次看到：

```text
dev script: running index.js
hello script: running hello.js
test script: running test.js
```

这说明三条 npm 命令分别读取了 `scripts.dev`、`scripts.hello` 和 `scripts.test`。

## 4、新增脚本

在 `scripts` 里新增一条：

```json
"bye": "node bye.js"
```

如果它不是最后一行，前一项后面要补英文逗号；如果它是最后一行，自己后面不要加逗号。

然后创建 `bye.js`：

```js
console.log("bye script: running bye.js");
```

最后运行：

```bash
npm run bye
```

如果看到：

```text
bye script: running bye.js
```

说明已经掌握了 npm scripts 的核心用法：把项目命令写进 `package.json`，再用 `npm run 脚本名` 通过统一入口执行。
