---
title: Xcode
date: 2026-05-12
tags: [devtools, toolchain]
source_count: 1
---

# Xcode

Xcode 是 Apple 官方提供的完整集成开发环境（IDE），用于开发 iOS、macOS、watchOS、tvOS 和 visionOS 平台的应用。

## 核心组成

- **图形化代码编辑器**：支持 Swift、Objective-C、C/C++ 等语言的代码编辑、补全和重构
- **Interface Builder**：可视化 UI 设计工具
- **工程管理工具**：管理 [[Xcode project]] 和 [[Xcode workspace]] 文件
- **模拟器**：iOS、watchOS、tvOS、visionOS 设备模拟器
- **调试器**：基于 [[LLDB]] 的图形化调试界面
- **性能分析工具**：Instruments 系列工具（Time Profiler、Memory Graph 等）
- **代码签名与证书管理**：Provisioning Profile、证书和 App ID 管理
- **App 打包与发布**：归档（Archive）、导出（Export）和上传 App Store Connect

## 与 [[Xcode Command Line Tools]] 的关系

| 特性 | Xcode | Xcode Command Line Tools |
|---|---|---|
| 体积 | 大（约 10GB+） | 小（约 1GB） |
| 图形界面 | 有 | 无 |
| 模拟器 | 有 | 无 |
| 工程管理 | 完整支持 | 仅命令行（[[xcodebuild]]） |
| 适用场景 | GUI App 开发、完整工作流 | 终端开发、命令行构建 |

Xcode 安装后会自动包含 Command Line Tools 的核心组件，但两者可以独立存在。通过 [[xcode-select]] 可以在多套工具链之间切换。

## 安装方式

- **App Store**：搜索 "Xcode" 下载安装（推荐，自动更新）
- **Apple Developer 网站**：下载指定版本的 `.xip` 文件，适合需要旧版本或特定版本的场景

安装路径通常为 `/Applications/Xcode.app/Contents/Developer`。

## 来源

- [[Xcode与命令行工具]]
