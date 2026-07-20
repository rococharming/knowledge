---
title: Node.js 和 npm
date: 2026-07-20
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

# 一、Node.js

## 1、运行环境

Node.js 是浏览器之外的 JavaScript 运行环境。它让 JavaScript 不再只能运行在网页里，也可以作为命令行程序、后端服务、构建工具和自动化脚本运行在操作系统之上。

可以先用下面的心智模型理解：

![[assets/Pasted image 20260721002759.png|500]]

在浏览器里，JavaScript 由浏览器内置的 JavaScript 引擎执行；在命令行里，JavaScript 可以由 Node.js 执行。

示例：

```js
console.log("Hello");
```

这段代码如果放在浏览器页面里，通常由浏览器执行；如果保存为 `index.js` 并执行 `node index.js`，则由 Node.js 执行。

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

主要组成可以先这样理解：

| 组成           | 作用                                    |
| ------------ | ------------------------------------- |
| V8           | 执行 JavaScript 代码                      |
| libuv        | 提供事件循环、线程池和异步 I/O 基础                  |
| Node.js 核心模块 | 提供 `fs`、`http`、`path`、`process` 等内置能力 |
| 绑定层          | 连接 JavaScript 代码与底层 C / C++ 能力        |

从实现语言看，Node.js 主要包含：

- C++：Node.js 核心运行时、与 V8 的连接、启动流程等；
- JavaScript：许多 Node.js 内置模块与运行时逻辑；
- C：主要来自 `libuv` 等底层库；
- 另外还包含少量 Python、汇编和构建脚本等。

可以粗略理解为：Node.js 使用 V8 提供 JavaScript 执行能力，使用 libuv 实现事件循环、工作线程和异步行为，再通过内置模块把这些能力暴露给 JavaScript 程序。

# 二、npm 与 Node.js 的关系

npm 是 Node.js 生态中默认使用的包管理器。安装 Node.js 时，通常也会同时安装 npm CLI，所以它们经常一起出现，但它们不是同一个程序。

## 1、职责区分

可以这样区分：

| 工具 | 主要职责 | 典型命令 |
|---|---|---|
| Node.js | 运行 JavaScript | `node src/index.js` |
| npm | 管理项目和软件包 | `npm install picocolors` |

`node` 和 `npm` 都常出现在终端里，但它们解决的问题不同：`node` 关注代码执行，`npm` 关注项目依赖和包管理。

## 2、命令对比

执行 JavaScript 文件时，使用的是 `node`：

```bash
node src/index.js
```

含义是：启动 Node.js，并让 Node.js 运行 `src/index.js` 这个 JavaScript 文件。

![[assets/Pasted image 20260721011646.png|500]]

这里的主角是 Node.js，关注点是“执行代码”。

安装软件包时，使用的是 `npm`：

```bash
npm install picocolors
```

含义是：启动 npm CLI，让 npm 帮当前项目安装名为 `picocolors` 的软件包。

这里的主角是 npm，关注点是“找到包、确定版本、下载包、写入项目依赖信息”。

> 简单来说：`node` 负责运行 JavaScript，`npm` 负责管理 JavaScript 项目依赖。

# 三、npm 生态

npm 不只是终端里的一个命令。它通常指一组围绕 JavaScript 包分发和项目依赖管理建立起来的工具与服务，主要包括 npm CLI、npm Registry 和 npm 网站。

```text
npm
├── npm CLI
├── npm Registry
└── npm 网站
```

## 1、CLI

npm CLI 是终端里的 `npm` 命令，用来执行安装、卸载、运行脚本、发布包等操作。

常见命令包括：

```bash
npm install
npm run
npm uninstall
npm publish
```

当说“执行 npm 命令”时，通常指的就是 npm CLI 在本机工作。

## 2、Registry

npm Registry 是远程的软件包仓库，负责存储软件包本体和元数据。元数据包括包名、版本、依赖关系、发布时间、dist tag 等信息。

可以把它类比为：

| 生态      | 包管理器  | 默认公共仓库       |
| ------- | ----- | ------------ |
| Rust    | Cargo | crates.io    |
| Node.js | npm   | npm Registry |

执行：

```bash
npm install picocolors
```

大致会经历：

![[assets/Pasted image 20260721014937.png|500]]

这个过程本质上会发生网络请求：npm CLI 是客户端，npm Registry 是远程服务端。

## 3、网站

npm 网站指 npm 的官方 Web 站点：[npmjs.com](https://www.npmjs.com/)。它主要面向人使用，用来搜索和管理包。

常见用途包括：

- 搜索包；
- 查看包的版本；
- 阅读 README；
- 查看维护者；
- 管理账号；
- 管理组织和发布权限。

npm CLI 更偏“机器执行命令”，npm 网站更偏“人查看信息和管理权限”，npm Registry 更偏“远程存储与分发”。

# 四、包与依赖

Package 和 Dependency 经常一起出现，但它们强调的角度不同。

Package 强调“软件包本身”；Dependency 强调“某个项目依赖另一个包的关系”。

## 1、Package

Package 可以翻译成“软件包”。一个 npm Package 通常由一组文件和描述信息组成。

示例：

```text
picocolors/
├── package.json
├── picocolors.js
├── README.md
└── LICENSE
```

npm 对 Package 的基本理解是：由 `package.json` 描述的文件或目录。

一个包如果要发布到 npm Registry，必须具有 `package.json`。这个文件会描述包名、版本、入口文件、依赖、脚本、许可证等信息。

## 2、Dependency

Dependency 可以翻译为“依赖项”。它描述的是一个项目对另一个包的需要。

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

## 3、区别

| 概念 | 强调对象 | 例子 |
|---|---|---|
| Package | 一个被发布、安装或引用的软件包本体 | `picocolors` 这个包 |
| Dependency | A 项目需要 B 包才能工作的关系 | 当前项目依赖 `picocolors` |

理解这个区别后，后续学习依赖类型、依赖树、Peer Dependency 和 Lockfile 时会更容易。

# 五、安装

学习 npm 之前，需要先安装 Node.js。安装 Node.js 后，通常会同时获得 `node` 和 `npm` 两个命令。

## 1、版本选择

Node.js 的版本分为 Current、LTS 和 EOL 等状态。Current 适合尝试新特性，LTS 适合学习和生产项目，EOL 表示该版本线已经结束维护。

截至 2026 年 7 月 21 日，Node.js 26 属于 Current，Node.js 24 和 22 属于 LTS，Node.js 25 已经 EOL。建议使用 Node.js 24 LTS。

## 2、安装方式

本节介绍使用 `fnm` 安装 Node.js。`fnm` 是 Fast Node Manager 的缩写，用来安装、切换和管理多个 Node.js 版本。它原生支持 fish shell，适合当前使用 fish 的开发环境。相比之下，`nvm` 主要面向 bash、zsh 等 POSIX shell，不适合直接在 fish 中使用。

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

安装完成后，执行：

```bash
node -v
npm -v
```

这两个命令分别查看 Node.js 和 npm CLI 的版本。

如果两条命令都能输出版本号，说明本机至少已经可以启动这两个程序。

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

## 3、Registry

npm CLI 的行为会受到配置影响，其中 Registry 是最常见、也最容易影响安装结果的配置项。

执行：

```bash
npm config get registry
```

通常会看到 npm 公共 Registry 地址。

这个结果说明：

```text
npm CLI
   ↓ 网络请求
npm Registry
```

如果后续遇到安装很慢、包找不到、私有包无法访问等问题，Registry 配置就是重要排查入口。

## 4、Help

npm 自带帮助系统，初学阶段不需要记住所有命令，但要知道可以从哪里查。

执行：

```bash
npm --help
npm help install
```

`npm --help` 用来查看 npm 的总体帮助；`npm help install` 用来查看 `install` 子命令的说明。
