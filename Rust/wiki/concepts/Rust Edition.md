---
title: Rust Edition
date: 2026-07-21
tags: [rust, edition]
source_count: 2
---

# Rust Edition

Rust Edition 是 Rust 语言规则的一组版本集合，用来在“长期稳定”和“语言演进”之间取得平衡。旧项目可以继续按旧 Edition 编译，新项目则可以选择更新的 Edition 使用新的语法、关键字、宏规则或预导入内容。

## 为什么需要 Edition

如果 Rust 只有一套语言规则，语言层面的变化可能导致旧项目在新编译器上无法编译。Edition 通过把语言规则分组，让同一个 [[rustc]] 同时支持多个规则集合，从而避免把语言演进直接变成破坏性升级。

素材中提到 Rust 支持 `2015`、`2018`、`2021`、`2024` Edition。一个项目可以选择其中一个 Edition，编译器会按对应规则解析和编译代码。

## 使用方式

单文件编译时，可以通过 `rustc --edition` 指定：

```shell
rustc main.rs --edition=2021
```

Cargo 项目通常在 `Cargo.toml` 中声明：

```toml
[package]
edition = "2024"
```

## 与工具链版本的关系

Edition 不是 toolchain 通道，也不等同于 `stable`、`beta`、`nightly`。通道描述编译器发布节奏；Edition 描述项目采用哪组语言规则。较新的 Edition 需要足够新的编译器支持，但选择某个 Edition 并不表示项目自动使用 nightly 功能。

## Edition 2024 与 `static mut` 引用

Edition 也可能调整 lint 的默认严格程度。以 [[Rust 变量绑定与常量基础]] 中的 `static mut` 为例，Edition 2024 中 `static_mut_refs` lint 默认是 `deny`，因此默认禁止对 `static mut` 创建共享引用或可变引用。

这会影响类似 `println!("{}", NUM)` 的写法：格式化过程可能在内部创建对 `static mut` 的共享引用。更稳妥的做法是在 `unsafe` 块中先把值复制到局部变量，再打印局部变量。

## 相关页面

- [[rustc]]
- [[Cargo]]
- [[rustup]]
- [[Rust 变量绑定与常量基础]]

## 来源

- [[Rust安装与开发环境配置]]
- [[变量绑定与常量]]
