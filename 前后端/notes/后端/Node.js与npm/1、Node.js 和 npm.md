---
title: Node.js 和 npm
date: 2026-07-29
tags:
  - nodejs
  - npm
  - registry
  - package-manager
aliases:
  - Node npm Registry
  - npm 基础
  - Node.js 与 npm
---

# 一、核心边界

学习 Node.js 和 npm 时，最先要分清两个问题：谁在运行 JavaScript，谁在管理项目依赖。`node` 是运行时命令，负责执行 JavaScript；`npm` 是包管理器命令，负责安装依赖、运行项目脚本、发布软件包。

一个常见场景是：下载一个 JavaScript 项目后，README 通常会写：

```bash
npm install
npm run dev
```

这两行都以 `npm` 开头，但含义不同：`npm install` 主要是在准备依赖；`npm run dev` 主要是让 npm 读取 `package.json` 里的脚本，再执行脚本右侧配置的命令。脚本右侧可能是 `node index.js`，也可能是 `vite`、`tsx`、`nest start` 或其他开发工具。

> 简单来说：Node.js 解决“JavaScript 在哪里运行”的问题，npm 解决“项目依赖和脚本如何管理”的问题。

# 二、Node.js

Node.js 是浏览器之外的 JavaScript 运行环境。它让 JavaScript 不再只能运行在网页里，也可以作为命令行程序、后端服务、构建工具和自动化脚本运行在操作系统之上。

## 1、运行环境

可以先用下面的心智模型理解：

![[assets/Pasted image 20260721002759.png|500]]

在浏览器里，JavaScript 由浏览器内置的 JavaScript 引擎执行；在命令行里，JavaScript 可以由 Node.js 执行。

示例：

```js
console.log("Hello");
```

这段代码如果放在浏览器页面里，通常由浏览器执行；如果保存为 `index.js` 并执行：

```bash
node index.js
```

则由 Node.js 执行。这里的主语是 Node.js：启动运行时，读取 `index.js`，执行其中的 JavaScript 代码。

## 2、执行能力

Node.js 的核心价值是把 JavaScript 带到浏览器之外，让它可以访问文件系统、网络、进程、命令行参数等操作系统能力。

有了 Node.js，就可以使用 JavaScript 编写：

- 命令行程序；
- 后端服务器；
- 构建工具；
- 自动化脚本；
- 开发工具。

如果已有 Rust 经验，可以暂时类比为：

![[assets/Pasted image 20260721011345.png|500]]

这个类比并不完全精确：Rust 通常先编译为机器码再运行，而 Node.js 内部会通过 JavaScript 引擎解释、即时编译和执行代码。但在入门阶段，这个类比足够帮助建立“谁在运行代码”的直觉。

## 3、组成结构

Node.js 不是由一种语言完整写成的单体程序，而是多种语言和组件组合而成的运行时。入门阶段不需要深入源码，但需要知道它大致由哪些部分提供能力。

| 组成 | 作用 |
|---|---|
| V8 | 执行 JavaScript 代码 |
| libuv | 提供事件循环、线程池和异步 I/O 基础 |
| Node.js 核心模块 | 提供 `fs`、`http`、`path`、`process` 等内置能力 |
| 绑定层 | 连接 JavaScript 代码与底层 C / C++ 能力 |

可以粗略理解为：Node.js 使用 V8 提供 JavaScript 执行能力，使用 libuv 实现事件循环、工作线程和异步行为，再通过内置模块把这些能力暴露给 JavaScript 程序。

# 三、npm 生态

npm 是 Node.js 生态中默认使用的包管理器。安装 Node.js 时，通常也会同时安装 npm CLI，所以它们经常一起出现，但它们不是同一个程序。

## 1、npm CLI

npm CLI 是终端里的 `npm` 命令，用来安装依赖、卸载依赖、运行脚本、发布包等。`node` 和 `npm` 都常出现在终端里，但它们解决的问题不同：

| 工具 | 主要职责 | 典型命令 |
|---|---|---|
| Node.js | 运行 JavaScript | `node src/index.js` |
| npm CLI | 管理项目和软件包 | `npm install picocolors` |

执行 JavaScript 文件时，使用的是 `node`：

```bash
node src/index.js
```

含义是：启动 Node.js，并让 Node.js 运行 `src/index.js` 这个 JavaScript 文件。

![[assets/Pasted image 20260721011646.png|500]]

安装软件包时，使用的是 `npm`：

```bash
npm install picocolors
```

含义是：启动 npm CLI，让 npm 帮当前项目安装名为 `picocolors` 的软件包。这里的主角是 npm，关注点是“找到包、确定版本、下载包、写入项目依赖信息”。

从生态组成看，npm 通常包括三部分：

```text
npm
├── npm CLI
├── npm Registry
└── npm 网站
```

| 组成 | 面向对象 | 主要作用 |
|---|---|---|
| npm CLI | 本机终端 | 安装、卸载、运行脚本、发布包 |
| npm Registry | 远程服务 | 存储软件包本体和版本元数据 |
| npm 网站 | 开发者 | 搜索包、阅读 README、管理账号和发布权限 |

## 2、脚本运行

`npm run` 的职责是读取 `package.json` 里的 `scripts` 字段，并执行指定脚本。

示例：

```json
{
  "scripts": {
    "dev": "node index.js"
  }
}
```

执行：

```bash
npm run dev
```

npm 会先找到 `scripts.dev`，再执行右侧的 `node index.js`。因此这个流程可以分成三层：

```text
npm run dev
      ↓ 读取 package.json 的 scripts.dev
node index.js
      ↓ 启动 Node.js
执行 JavaScript 文件
```

这也是初学时最容易混淆的地方：`npm run dev` 不一定等于 Node.js 直接运行代码。npm 只是执行脚本入口，真正运行什么，取决于 `package.json` 中脚本右侧写了什么命令。

## 3、包、依赖与仓库

Package、Dependency 和 Registry 是 npm 生态里最基础的三个概念。Package 强调“软件包本身”；Dependency 强调“某个项目依赖另一个包的关系”；Registry 是保存和分发软件包的远程仓库。

一个 npm Package 通常由一组文件和描述信息组成：

示例：

```text
picocolors/
├── package.json
├── picocolors.js
├── README.md
└── LICENSE
```

npm 对 Package 的基本理解是：由 `package.json` 描述的文件或目录。一个包如果要发布到 npm Registry，必须具有 `package.json`。这个文件会描述包名、版本、入口文件、依赖、脚本、许可证等信息。

假设要写一个终端程序，并希望输出绿色文字，可以自己编写 ANSI 颜色控制代码，也可以安装别人已经写好的包：

```bash
npm install picocolors
```

此时关系变成：

```text
你的项目
    ↓ 依赖
picocolors
```

`picocolors` 作为一个软件包时，它是 Package；当它被你的项目需要时，它就是你的项目的 Dependency。

执行 `npm install picocolors` 时，大致会经历：

![[assets/Pasted image 20260721014937.png|500]]

这个过程本质上会发生网络请求：npm CLI 是客户端，npm Registry 是远程服务端。

可以把它类比为：

| 生态      | 包管理器  | 默认公共仓库       |     |
| ------- | ----- | ------------ | --- |
| Rust    | Cargo | crates.io    |     |
| Node.js | npm   | npm Registry |     |

| 概念 | 强调对象 | 例子 |
|---|---|---|
| Package | 一个被发布、安装或引用的软件包本体 | `picocolors` 这个包 |
| Dependency | A 项目需要 B 包才能工作的关系 | 当前项目依赖 `picocolors` |
| Registry | 保存和分发包的远程仓库 | npm Registry |

理解这组关系后，再学习依赖类型、依赖树、Peer Dependency 和 Lockfile 时会更容易。

# 四、环境准备

学习 npm 之前，需要先安装 Node.js。安装 Node.js 后，通常会同时获得 `node` 和 `npm` 两个命令。

## 1、版本选择

Node.js 的版本分为 Current、LTS 和 EOL 等状态。Current 适合尝试新特性，LTS 适合学习和生产项目，EOL 表示该版本线已经结束维护。

截至 2026 年 7 月 29 日，Node.js 26 属于 Current，Node.js 24 和 22 属于 LTS，Node.js 25 已经 EOL。学习和长期项目优先选择 LTS 版本，例如 Node.js 24 LTS。

## 2、fnm 安装

`fnm` 是 Fast Node Manager 的缩写，用来安装、切换和管理多个 Node.js 版本。它原生支持 fish shell，适合 fish 用户管理 Node.js 版本。相比之下，`nvm` 主要面向 bash、zsh 等 POSIX shell，不适合直接在 fish 中使用。

安装流程可以先理解为：

```text
安装 fnm
      ↓
安装 Node.js LTS
      ↓
使用指定版本
      ↓
检查 node 和 npm 命令
```

安装 `fnm`：

```bash
brew install fnm
```

fish 中需要先加载 `fnm` 环境：

```fish
fnm env --use-on-cd --shell fish | source
```

这一步会为当前 shell 设置 `fnm` 切换 Node.js 版本所需的环境变量。否则执行 `fnm use 24` 时，可能会提示找不到必要的环境变量。

这条命令可以拆开理解：

- `fnm env`：输出 `fnm` 需要的 shell 环境配置；
- `--shell fish`：让输出内容使用 fish shell 语法；
- `--use-on-cd`：进入目录时自动根据项目配置切换 Node.js 版本；
- `| source`：把前面输出的配置立即加载到当前 fish 会话。

如果希望以后每次打开新终端都自动可用，可以把同一行写入 `~/.config/fish/config.fish`。

安装并使用 Node.js 24：

```bash
fnm install 24
fnm use 24
```

## 3、命令检查与帮助

安装完成后，执行：

```bash
node -v
npm -v
```

这两个命令分别查看 Node.js 和 npm CLI 的版本。如果两条命令都能输出版本号，说明本机至少已经可以启动这两个程序。

执行：

```bash
which node
which npm
```

在 macOS 上，结果可能类似：

![[assets/Pasted image 20260721023956.png|600]]

这说明当前使用的是 `fnm` 管理的 Node.js。

执行：

```bash
node -e 'console.log("Hello from Node.js")'
```

这里每个部分的含义是：

- `node`：启动 Node.js；
- `-e`：执行后面的 JavaScript 字符串；
- `console.log()`：向终端输出内容。

如果能看到输出：

```text
Hello from Node.js
```

说明 Node.js 已经可以在命令行中执行 JavaScript。

npm 自带帮助系统。初学阶段不需要记住所有命令，但要知道可以从哪里查。

执行：

```bash
npm --help
npm help install
```

`npm --help` 用来查看 npm 的总体帮助；`npm help install` 用来查看 `install` 子命令的说明。遇到陌生命令时，优先查官方帮助，再结合项目里的 `package.json` 判断命令实际会做什么。

如果遇到安装很慢、包找不到、私有包无法访问等问题，还可以检查 npm Registry 配置：

```bash
npm config get registry
```

通常会看到 npm 公共 Registry 地址。这个结果说明当前 npm CLI 会把安装请求发往哪个远程包仓库。

# 五、实践：最小项目

这个实践用于观察 `npm run dev` 和 `node index.js` 的关系。重点不是学习 JavaScript 语法，而是看清：npm 负责读取项目脚本，Node.js 负责运行 JavaScript 文件。

## 1、创建目录

先创建并进入一个练习目录：

```bash
mkdir hello-node
cd hello-node
```

`mkdir hello-node` 表示创建一个叫 `hello-node` 的文件夹；`cd hello-node` 表示进入这个文件夹。后面创建的 `package.json` 和 `index.js` 都放在这个目录里。

## 2、写入文件

创建 `package.json`，写入：

```json
{
  "name": "hello-node",
  "version": "1.0.0",
  "scripts": {
    "dev": "node index.js"
  }
}
```

这里先只关注 `scripts`：它给项目定义了一个叫 `dev` 的脚本，这个脚本真正执行的是右侧的 `node index.js`。

再创建 `index.js`，写入：

```js
console.log("Hello Node.js");
console.log("This file is running through node.");
```

`console.log(...)` 会在终端输出一行文字。这段代码本身很简单，刚好适合用来观察“谁在执行 JavaScript 文件”。

## 3、运行对照

在 `hello-node` 目录里执行：

```bash
npm run dev
```

如果看到下面两行输出，说明脚本运行成功：

```text
Hello Node.js
This file is running through node.
```

再执行：

```bash
node index.js
```

两次输出相同，但路径不同：

| 命令 | 执行路径 | 关键角色 |
|---|---|---|
| `npm run dev` | 读取 `package.json` 的 `scripts.dev`，再执行 `node index.js` | npm 负责找到并执行脚本 |
| `node index.js` | 直接启动 Node.js 运行 `index.js` | Node.js 负责运行 JavaScript 文件 |

判断标准是：当输出来自 `index.js` 时，真正运行 JavaScript 文件的是 Node.js；npm 只是帮项目找到并执行配置好的脚本。
