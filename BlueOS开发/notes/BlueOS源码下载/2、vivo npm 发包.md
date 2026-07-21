---
title: vivo npm 发包
date: 2026-07-21
tags: [BlueOS, npm, 发包, BDB]
aliases:
  - vivo npm 发布
  - BlueOS npm 发包
---

# 一、vivo npm

vivo npm 是内部 npm Registry，用来发布和安装公司内使用的 JavaScript 包。对 bdb 这种包来说，npm 包不只是 JS 代码，还会携带不同平台的 bdb 原生二进制文件。

内部 Registry 地址：

[https://npm.vmic.xyz/](https://npm.vmic.xyz/)

安装侧可以显式指定 Registry：

```bash
npm install --global @blueos/bdb --registry https://npm.vmic.xyz
```

# 二、BDB 包结构

## 1、入口脚本

`~/bdb-cli/package.json` 里的包名是 `@blueos/bdb`，命令入口是：

```json
{
  "bin": {
    "bdb": "bin/bdb.js"
  }
}
```

用户安装后执行 `bdb`，实际先进入 `bin/bdb.js`。这个 JS 入口只做一件事：根据当前系统和 CPU 架构选择对应的原生二进制，再把参数原样转交给它。

| 平台 | 二进制路径 |
|---|---|
| Windows x64 | `win32-x64/bdb.exe` |
| Linux x64 | `linux-x64/bdb` |
| macOS arm64 | `darwin-arm64/bdb` |
| macOS x64 | `darwin-x64/bdb` |

这类结构和 esbuild 类似：npm 包负责分发，真正运行的是平台相关的 native binary。

## 2、发布配置

`~/bdb-cli/package.json` 已经写了发布 Registry：

```json
{
  "publishConfig": {
    "registry": "https://npm.vmic.xyz",
    "access": "public"
  }
}
```

因此在 `~/bdb-cli` 里执行 `npm publish` 时，npm 会优先使用这个 Registry。命令里再写 `--registry https://npm.vmic.xyz` 只是更显式的兜底。

# 三、发包流程

## 1、登录账号

发布前先登录内部 Registry：

```bash
npm login --registry https://npm.vmic.xyz
```

如果是新用户，先创建账号：

```bash
npm adduser --registry https://npm.vmic.xyz
```

> 密码： 123456


## 2、同步二进制

`@blueos/bdb` 发布的是 CLI 包，发包前必须先把各平台 BDB 二进制同步到 npm 包目录：

```bash
npm run sync-binaries
```

这个脚本会从 GitLab `BlueOS/System/tools_bdb` 项目的 `main` 分支读取最新成功产物，并写入：

| 目标 | GitLab job | 输出文件 |
|---|---|---|
| Windows x64 | `build_windows` | `win32-x64/bdb.exe` |
| Linux x64 | `build_linux` | `linux-x64/bdb` |
| macOS arm64 | `build_macos_arm` | `darwin-arm64/bdb` |
| macOS x64 | `build_macos_intel` | `darwin-x64/bdb` |

如果 GitLab 产物需要认证，本地要先准备环境变量：

```bash
export GITBLUEOS_TOKEN=你的 GitLab Token
```

同步完成后，脚本会打印每个目标文件的字节数。Linux 和 macOS 二进制还会被设置为可执行权限。

## 3、升级版本

每次发布前都要修改 `package.json` 的 `version`。补丁版本通常用：

```bash
npm version patch
```

它本质上会更新 `package.json` 里的 `version` 字段，并默认生成一个 Git tag。只想手动改版本时，也可以直接编辑 `package.json`，但要确保新版本没有在内部 Registry 发布过。

## 4、发布包

确认 Registry、版本号和二进制都正确后发布：

```bash
npm publish
```

如果当前目录或 npm 配置不确定，可以显式指定 Registry：

```bash
npm publish --registry https://npm.vmic.xyz
```

# 四、发布检查

## 1、包内容检查

发布前先看 npm 实际会打进包里的文件：

```bash
npm pack --dry-run
```

`~/bdb-cli/.npmignore` 当前排除了 `.idea/` 和 `scripts/`，但保留了平台目录。因此检查重点是：

- `bin/bdb.js` 是否存在。
- `package.json` 是否存在。
- `win32-x64/bdb.exe`、`linux-x64/bdb`、`darwin-arm64/bdb`、`darwin-x64/bdb` 是否都存在。
- 不要把本地 IDE 配置、临时文件或密钥打进包里。

## 2、安装验证

发布后在干净环境重新安装：

```bash
npm install --global @blueos/bdb --registry https://npm.vmic.xyz
```

再验证命令入口：

```bash
bdb --help
```

如果提示找不到 `bdb`，先检查全局包是否安装成功：

```bash
npm list --global @blueos/bdb
```

然后确认 npm 的全局可执行文件目录已经加入 `PATH`。

# 五、自测问题

- `npm publish` 为什么可以不写 `--registry`？
- `bin/bdb.js` 为什么不直接实现 BDB 功能，而是转发给 native binary？
- 发包前为什么必须执行 `npm run sync-binaries`？
- `npm pack --dry-run` 应该重点检查哪些文件？
- 如果发布后用户执行 `bdb` 失败，应该先检查包安装、入口脚本，还是平台二进制路径？

后续如果需要准备 BlueOS 源码环境，可以继续看 [[BlueOS源码下载|BlueOS 源码下载]]。
