---
title: Rust Wiki 索引
date: 2026-05-14
---

# Rust Wiki 索引

## summaries

- [[Rust 安装与开发环境配置]] — Rust 入门指南摘要，涵盖工具链概览、IDE 配置及包管理
- [[Rust 基础语法]] — Rust 语言核心基础语法系统梳理，涵盖变量、类型、控制流、函数与注释
- [[所有权]] — 所有权系统学习笔记整体摘要，涵盖内存管理、所有权规则、移动与Copy
- [[引用和切片]] — 引用、解引用与切片学习笔记整体摘要，涵盖借用规则、悬垂引用、切片
- [[size_of 与 size_of_val]] — `std::mem` 中查看内存大小两个函数的对比与使用场景
- [[Rust 字符串]] — Rust 字符串处理综合摘要，涵盖字面量、String/&str、索引遍历及相关类型

## entities

- [[rustup]] — Rust 工具链管理器，负责安装、更新和切换 Rust 编译器版本
- [[rustc]] — Rust 官方编译器，将 .rs 源文件编译为可执行文件或库
- [[Cargo]] — Rust 的构建工具和包管理工具，项目开发的核心工具

## concepts

- [[变量与可变性]] — let 绑定、mut 可变性声明、变量遮蔽（shadowing）与作用域
- [[常量与静态变量]] — const 编译期常量与 static 静态存储的区别、static mut 与 unsafe
- [[数据类型]] — 标量类型（整型、浮点型、布尔型、字符型）与复合类型（数组、元组）的完整梳理
- [[控制流]] — if 表达式、loop/while/for 循环、循环标签与范围语法
- [[函数]] — 表达式语言特征、参数与返回值、函数签名与声明顺序
- [[注释]] — 行注释、块注释、文档注释、rustdoc 与文档测试
- [[所有权系统]] — Rust 内存管理核心机制，所有权三大规则与 RAII
- [[移动]] — 所有权转移的默认行为，涵盖函数传参、控制流与复合类型
- [[Copy]] — 按位复制的标记 trait，与移动相对
- [[Edition]] — Rust 语言规则的可选版本包机制，兼顾稳定性与进化性
- [[语义化版本]] — Cargo 依赖管理中的版本号解析规则（^、~、精确版本）
- [[size_of 与 size_of_val]] — `std::mem` 中查询类型与值内存大小的两个核心函数
- [[引用与借用]] — 共享引用 `&T`、可变引用 `&mut T`、借用规则与非词法生命周期
- [[解引用]] — 显式与自动解引用、方法调用中的自动借用、比较运算符解引用
- [[切片]] — 切片引用 `&[T]` 的创建、范围语法、胖指针本质与常用方法
- [[字符串类型]] — Rust 核心字符串类型：字面量、String/&str、内存结构、创建修改与索引遍历
- [[字符串相关类型]] — 非 UTF-8 场景下的专用类型：PathBuf、OsString、CString、Vec<u8> 及选择指南

## comparisons

_（暂无）_

## overviews

_（暂无）_

## syntheses

_（暂无）_

## recipes

- [[Cargo 命令速查]] — Cargo 核心命令分类速查，涵盖创建、构建、测试、依赖管理
- [[rustup 命令速查]] — rustup 工具链安装、更新、切换命令速查
- [[RsProxy 镜像源配置]] — 国内环境下通过 RsProxy 加速 Rust 安装和依赖下载
- [[VS Code Rust 开发环境配置]] — 在 VS Code 中配置 rust-analyzer 等插件搭建 Rust 开发环境
- [[RustRover 开发环境配置]] — JetBrains 专用 Rust IDE 的配置与核心功能使用

## snippets

- [[size_of 与 size_of_val 速查]] — `size_of` / `size_of_val` 速查代码示例

## patterns

_（暂无）_

## projects

_（暂无）_

## exercises

_（暂无）_

## resources

_（暂无）_
