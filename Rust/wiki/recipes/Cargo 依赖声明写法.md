---
title: Cargo 依赖声明写法
date: 2026-06-30
tags: [rust, cargo, dependencies, toml]
source_count: 0
---

# Cargo 依赖声明写法

## 核心结论

`[dependencies]` 下一条依赖既可以用 **字符串写法**（只有版本），也可以用 **内联表写法**（`{ ... }`，携带多个字段）。内联表是 TOML 标准语法，等价于展开的 `[dependencies.<name>]` 子表。

## 两种写法对照

```toml
# 字符串写法 —— 仅指定版本，键名即包名
winit = "0.30.13"

# 内联表写法 —— 可携带多个字段
winit30 = { package = "winit", version = "0.30", default-features = false, features = ["rwh_06", "x11"] }
```

内联表等价的多行子表形式：

```toml
[dependencies.winit30]
package = "winit"
version = "0.30"
default-features = false
features = ["rwh_06", "x11"]
```

## 内联表字段速查

| 字段 | 作用 | 说明 |
|---|---|---|
| 等号左的键 | 在当前 crate 中使用的**依赖别名** | 代码里 `use <别名>::...` |
| `package` | 指明**真正的 crates.io 包名** | 别名与真实包名不一致时必须 |
| `version` | 版本范围（语义化版本） | 见 [[语义化版本]] |
| `default-features` | 是否启用该 crate 的默认 feature | `false` 关闭默认特性 |
| `features` | 显式启用的 feature 列表 | 与 `default-features = false` 配合按需裁剪 |
| `optional` | 是否作为可选依赖 | `true` 时由本包 feature 控制 |
| `path` / `git` | 本地路径 / Git 仓库来源 | 不从 crates.io 拉取 |

## package —— 依赖重命名键

**等号左的键是本地别名，`package = "..."` 才是真实包名。** 字符串写法中键名即包名，内联表写法通过 `package` 解耦两者。

典型用途：

- **同包多版本共存**：项目同时用 `winit 0.29` 和 `winit 0.30`。Cargo 不允许同名依赖出现两个版本，于是改名其一：

  ```toml
  winit29 = { package = "winit", version = "0.29" }
  winit30 = { package = "winit", version = "0.30" }
  ```

  代码里分别 `use winit29::...` 和 `use winit30::...`。

- **语义化重命名**：把包名改成更短或更符合本项目习惯的名字（如 `serde_json` 改成 `json`）。

> [!note] package 与 `use ... as ...` 的区别
> `package` 是 Cargo 层面"对外包名 → 对内别名"的映射；Rust 模块系统的 `use ... as ...`（见 [[路径与导入]]）是模块路径层面的重命名。两者作用层不同，但效果类似。

## default-features 与 features —— 按需裁剪特性

- 许多 crate 默认开启一组 feature 以便开箱即用，但可能带来不必要的编译开销或平台依赖。
- `default-features = false` 关闭默认集合，再用 `features = [...]` 精确点亮所需特性。
- 示例：`winit` 关闭默认后只启用 `rwh_06`（Raw Window Handle 0.6 绑定）和 `x11`（Linux X11 后端），得到一个只跑 X11、显式指定 rwh 版本的精简窗口配置。

```toml
[dependencies]
winit = { version = "0.30", default-features = false, features = ["rwh_06", "x11"] }
```

## 版本字段的解析

内联表中的 `version = "0.30"` 与字符串写法 `"0.30"` 解析规则一致，都走 `^0.30` 默认 caret 规则。按 [[语义化版本]] 的 0.x 例外，`^0.30` 实际范围是 `>=0.30.0, <0.31.0`（次版本当主版本边界），确切段由 `Cargo.lock` 锁定。

## 关键要点

- 字符串写法 = 仅版本；内联表写法 = 携带多字段，等价于 `[dependencies.<name>]` 子表。
- `package = "..."` 是核心：等号左是**本地别名**，真实包名在 `package`。常用于同包多版本共存。
- `default-features = false` + `features = [...]` 实现依赖按需裁剪。
- `version` 字段统一走 [[语义化版本]] 解析。

## 关联

- [[Cargo.toml 表语法]] — `[ ]`/`[[ ]]` 表语法，内联表是其延伸
- [[语义化版本]] — `version` 字段的版本范围解析规则
- [[Package与Crate]] — 直接依赖、传递依赖与依赖图
- [[Cargo]] — 执行依赖解析的构建工具实体
- [[路径与导入]] — `use ... as ...` 模块级重命名，与 `package` 对照

## 来源

Query 综合归档（2026-06-30），基于 [[Cargo.toml 表语法]]、[[语义化版本]]、[[Package与Crate]] 及 Cargo 通用规范。
