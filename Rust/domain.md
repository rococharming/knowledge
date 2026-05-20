---
title: Rust 领域规则
date: 2026-05-09
domain: Rust
---

# Rust 领域规则

## 领域概述

Rust 编程语言学习与实践。涵盖语言核心概念（所有权、生命周期、 trait 系统）、标准库与生态工具链（Cargo、Clippy）、并发与异步编程、系统编程实践，以及工程化项目经验。

## 分类体系

wiki 页面按以下子目录组织：

- `summaries/` — 单个来源的摘要，如文章、书籍章节、视频
- `entities/` — 实体页面，如 crates、工具、关键人物、组织
- `concepts/` — 概念页面，如所有权、生命周期、trait、unsafe、宏
- `comparisons/` — 对比分析，如 Rust vs Go、RefCell vs Mutex、async runtime 比较
- `overviews/` — 领域概览，如标准库模块导览、Cargo 工作区结构
- `syntheses/` — 综合结论与最佳实践，如 Rust 项目目录规范、错误处理策略
- `recipes/` — 可复用的解决方案与操作指南，如配置文件读取、HTTP 客户端调用
- `snippets/` — 常用代码片段与惯用法，如错误传播样板、迭代器链式操作
- `patterns/` — Rust 特有的设计模式实现，如 RAII、类型状态模式、访问者模式
- `projects/` — 完整项目示例与架构分析，如 CLI 工具、Web 服务、嵌入式项目
- `exercises/` — 练习题与解题思路，如 Rustlings 题解、算法实现
- `resources/` — 学习资源索引，如官方文档路径、推荐书籍、社区工具链汇总

## 标签体系

领域初始标签（统一使用英文，便于检索和 Dataview 查询）。标签是动态扩展的——以下只是种子标签，LLM 在 ingest 时会根据素材内容自动补充：

- `#rust` — 通用 Rust 相关内容
- `#ownership` — 所有权与借用机制
- `#concurrency` — 并发编程：线程、锁、通道、原子操作
- `#memory-safety` — 内存安全：零成本抽象、unsafe、智能指针
- `#cargo` — Cargo 工具链：依赖管理、构建配置、workspace
- `#async` — 异步编程：async/await、Future、运行时
- `#lifetime` — 生命周期：标注规则、省略规则、复杂场景

**标签添加原则**：
- 初始标签作为 ingest 时的参考基准
- 当素材涉及新的子主题时，自动创建新标签（如 `#macro`、`#ffi`、`#wasm`）
- 定期 review 标签使用情况，合并过于细分的标签

## qmd 配置

- collection 名称：`knowledge-rust`
- 索引路径：`./wiki/`

## 特殊约定

- **代码块规范**：所有 Rust 代码块使用 `rust` 语言标识，关键示例优先给出可编译的完整代码，复杂场景配合 `no_run` 或 `ignore` 标注
- **Crate 名称处理**：首次提及 crate 时标注 crates.io 名称，如 `serde`（[crates.io/crates/serde](https://crates.io/crates/serde)），后续可直接用 `serde`
- **版本标注**：涉及 Rust 版本特性的内容，在页面中标注 `edition` 和最低支持 Rust 版本（MSRV）