---
title: macOS 领域规则
date: 2026-05-12
domain: macOS
---

# macOS 领域规则

## 领域概述

macOS 开发环境设置、工具链配置及系统相关知识的记录与整理

## 分类体系

wiki 页面按以下子目录组织：

- `summaries/` — 单篇文章/教程/官方文档的摘要（如某篇 Homebrew 配置教程）
- `entities/` — 具体工具/软件/框架的实体页面（如 [[Homebrew]]、[[Fish]]、[[Alacritty]]）
- `concepts/` — 概念性知识（如 dotfiles 管理哲学、PATH 环境变量加载顺序）
- `comparisons/` — 同类工具的对比分析（如 Homebrew vs MacPorts、Fish vs Zsh）
- `overviews/` — 领域概览（如 macOS 开发环境全景、前端工具链概览）
- `syntheses/` — 综合结论与最佳实践（如 macOS 开发环境最佳实践、Shell 配置规范）
- `recipes/` — 可复用配置模板与操作流程（如一键初始化脚本、常见问题排查流程）

## 标签体系

领域初始标签（统一使用英文，便于检索和 Dataview 查询）。标签是动态扩展的——以下只是种子标签，LLM 在 ingest 时会根据素材内容自动补充：

- `#homebrew` — Homebrew 包管理器相关（安装、配置、Tap、Formula、Cask）
- `#shell` — Shell 配置与使用（Fish、Zsh、Bash、别名、函数、提示符）
- `#terminal` — 终端模拟器配置（iTerm2、Alacritty、Kitty、WezTerm）
- `#devtools` — 开发工具链（IDE、编辑器、LSP、调试器、版本控制）
- `#system-config` — 系统级配置（系统偏好设置、权限、安全、网络、输入法）
- `#dotfiles` — 配置文件管理（仓库组织、同步策略、加密、模板化）
- `#toolchain` — 编译/构建工具链（Xcode、LLVM、Rust、Node、Python）
- `#macos-tips` — 系统技巧与隐藏功能（快捷键、 defaults 命令、自动化）

**标签添加原则**：
- 初始标签作为 ingest 时的参考基准
- 当素材涉及新的子主题时，自动创建新标签
- 定期 review 标签使用情况，合并过于细分的标签

## qmd 配置

- collection 名称：`knowledge-macos`
- 索引路径：`./wiki/`

## 特殊约定

- **命令行示例优先使用 Fish shell**：用户当前环境为 Fish，示例应使用 Fish 语法；如需跨 Shell 兼容，应标注差异
- **工具安装优先记录 Homebrew 方式**：macOS 下 Homebrew 是首选包管理器，安装命令以 `brew install` 为主，特殊情况下标注替代方案
- **配置文件路径标注版本差异**：不同 macOS 版本（Ventura/Sonoma/Sequoia）配置路径可能不同，涉及系统路径时应注明适用版本
