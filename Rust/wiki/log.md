---
title: Rust Wiki 操作日志
date: 2026-07-17
---

# Rust Wiki 操作日志

## 2026-07-20 Ingest: Rust安装与开发环境配置

- 来源: [[Rust安装与开发环境配置]]
- 类型: articles
- 创建: [[Rust 工具链与开发环境导览]], [[rustup]], [[rustc]], [[Cargo]], [[Rust Edition]], [[Rust 安装与镜像源配置]], [[Rust IDE 环境配置]]
- 更新: [[Rust/wiki/index|Rust Wiki 索引]], [[index|知识库领域目录]]
- 级联更新: 跳过；Rust wiki 此前无主题页面，本轮新页面之间已互链。
- 修正: 未发现与既有 wiki 页面的事实冲突；qmd 在 Codex 沙箱内因无法写入 `~/.cache/qmd/index.sqlite` 的 SQLite 临时文件而误报 sqlite-vec 不可用，已在沙箱外完成索引刷新与 embedding。

## 2026-07-21 Ingest: 变量绑定与常量

- 来源: [[变量绑定与常量]]
- 类型: articles
- 创建: [[Rust 变量绑定与常量基础]]
- 更新: [[Rust Edition]], [[Rust/wiki/index|Rust Wiki 索引]], [[index|知识库领域目录]]
- 级联更新: 更新 [[Rust Edition]]，补充 Edition 2024 中 `static_mut_refs` lint 对 `static mut` 引用的影响。
- 修正: 未发现与既有 wiki 页面的事实冲突；素材中的编译器诊断截图仅作为原文佐证，本轮未嵌入 concepts 页面。

## 2026-07-21 Ingest: 基本数据类型

- 来源: [[基本数据类型]]
- 类型: articles
- 创建: [[Rust 基本数据类型]]
- 更新: [[Rust 变量绑定与常量基础]], [[Rust/wiki/index|Rust Wiki 索引]], [[index|知识库领域目录]]
- 级联更新: 更新 [[Rust 变量绑定与常量基础]] 的相关页面，建立变量绑定与类型系统基础之间的双向入口。
- 修正: 未发现与既有 wiki 页面的事实冲突；素材中的运行输出截图和字面量示意图未嵌入 concepts 页面，相关信息已转写为结构化文字。

## 2026-07-21 Ingest: 控制流

- 来源: [[控制流]]
- 类型: articles
- 创建: [[Rust 控制流]]
- 更新: [[Rust 基本数据类型]], [[Rust/wiki/index|Rust Wiki 索引]], [[index|知识库领域目录]]
- 级联更新: 更新 [[Rust 基本数据类型]] 的布尔类型段落，补充 `if` / `while` 条件必须是 `bool` 的控制流入口。
- 修正: 未发现与既有 wiki 页面的事实冲突；素材中的循环标签运行结果截图未嵌入 concepts 页面，相关行为已用代码和文字说明。

## 2026-07-21 Ingest: 函数、语句与表达式

- 来源: [[函数、语句与表达式]]
- 类型: articles
- 创建: [[Rust 函数、语句与表达式基础]]
- 更新: [[Rust 控制流]], [[Rust 基本数据类型]], [[Rust 变量绑定与常量基础]], [[Rust/wiki/index|Rust Wiki 索引]], [[index|知识库领域目录]]
- 级联更新: 更新 [[Rust 控制流]] 中 `if` / `loop` 作为表达式的说明；更新 [[Rust 基本数据类型]] 中 `()` 单元类型与函数返回值的联系；更新 [[Rust 变量绑定与常量基础]] 的相关页面入口。
- 修正: 未发现与既有 wiki 页面的事实冲突；素材没有需要保留的高价值图片。

## 2026-07-21 Ingest: 注释与rustdoc

- 来源: [[注释与rustdoc]]
- 类型: articles
- 创建: [[Rust 注释与 rustdoc 文档]]
- 更新: [[Cargo]], [[Rust/wiki/index|Rust Wiki 索引]], [[index|知识库领域目录]]
- 级联更新: 更新 [[Cargo]] 的常用命令说明，补充 `cargo doc` 调用 `rustdoc` 生成 API 文档的关系。
- 修正: 未发现与既有 wiki 页面的事实冲突；素材中的 docs.rs 与 `cargo doc` 界面截图未嵌入 concepts 页面，相关信息已转写为结构化文字。

## 2026-07-28 Ingest: 所有权

- 来源: [[所有权]]
- 类型: articles
- 创建: [[Rust 所有权系统]]
- 更新: [[Rust 变量绑定与常量基础]], [[Rust 基本数据类型]], [[Rust 函数、语句与表达式基础]], [[Rust 控制流]], [[Rust/wiki/index|Rust Wiki 索引]], [[index|知识库领域目录]]
- 级联更新: 更新 [[Rust 变量绑定与常量基础]], [[Rust 基本数据类型]], [[Rust 函数、语句与表达式基础]], [[Rust 控制流]] 的相关页面入口；候选 [[Rust 工具链与开发环境导览]] 仅高层提及所有权，未改。
- 修正: 未发现与既有 wiki 页面的事实冲突；保留 `String` 栈/堆、Move、Clone、Copy 四类解释性内存示意图，未保留装饰性或纯操作截图。
