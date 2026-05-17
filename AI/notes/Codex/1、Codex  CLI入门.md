
# 一、简介

`Codex` 是 OpenAI 提供的 AI 编程代理（AI Coding Agent）。它不是单纯的代码补全工具，而是可以直接参与开发任务的智能体。

它可以在指定项目目录中读取代码、理解代码库结构、修改文件、运行命令、调试问题，并根据任务目标持续推进开发工作。`Codex CLI`是运行在本地终端中的 Codex 形态，可以在你选择的目录中读取、修改和运行代码。

`Codex`的核心能力包括：

- 理解和分析代码库
- 编写代码
- 代码审查
- 调试和修复
- 运行命令并验证结果
- 自动化处理开发任务

Codex 有多种使用形态，例如 Codex CLI、Codex App、IDE Extension 和 Codex Web。本文主要介绍`Codex CLI`，也就是在终端中使用`Codex`。

# 二、安装Codex CLI

开发者最常用的方式是安装 `Codex CLI`。它运行在本地终端中，但在执行任务时会把完成任务所需的上下文发送给模型处理。

可以使用`npm`全局安装：

```shell
npm install -g @openai/codex
```

安装完成后，执行下面命令验证是否安装成功：

```shell
codex --version
```

如果后续想更新`Codex`，可以使用：

```shell
npm install -g @openai/codex@latest
```

如果当前安装方式支持自更新，也可以使用：

```shell
codex update
```

如果不想继续使用，可以卸载：

```shell
npm uninstall -g @openai/codex
```


# 三、登录Codex

第一次安装好 Codex 后，在某个项目目录中执行：

```shell
codex
```

首次运行时需要登录。如果购买了OpenAI的套餐，选择`Sign in with ChatGPT`：

![[Pasted image 20260517221219.png|500]]

然后浏览器会打开登录页面，完成登录后即可使用。


# 四、交互模型运行

在项目根目录直接执行：

```shell
codex
```

`Codex` 会启动一个终端交互界面，也就是 `TUI`（Terminal User Interface）。

交互模式适合边看边改的开发任务。Codex 可以读取代码库、提出计划、修改文件、运行命令，并在过程中让你审阅它的操作。

也可以在命令行指定初始提示启动交互模式：

```shell
codex "给我解释这个代码库"
```

会话开启后，可以：

- 直接在对话中输入提示词、代码片段或图片（参考[[#^image-input|图片输入]]）
- 在执行更改前查看Codex的计划，并逐步批准或拒绝
- 在 TUI 中阅读带语法高亮的 Markdown 代码块和差异（diff），然后使用 `/theme` 预览并保存喜欢的主题。
- 使用`/clear`清空终端并开始新会话，或按`Ctrl+L`清屏但不启动新会话。
- 使用`/copy`或`Ctrl+O`复制最近完成的输出，如果当前回合仍在输出，则复制最近已完成的内容而非进行中的文本。
- 当`Codex`正在处理某项任务过程中，按`Tab`键，可将后续文本、斜杠命令（/command）或 `!` shell 命令排队到下一回合。
- 在对话框中按`Ctrl + R`，可以搜索之前的提示历史，按 Enter 选择匹配结果，按 Esc 取消。
- 使用`Ctrl+C`或`/exit`结束交互会话


# 五、模型与推理能力

在 Codex 中，大多数任务 **推荐使用 gpt-5.5**（如果可用）。它是 OpenAI 最新的前沿模型，适用于：

- 复杂编码任务
- 计算机操作
- 知识工作
- 研究型工作流

如果 gpt-5.5 还不可用，则继续使用 gpt-5.4。

对于需要额外快速响应的任务，**ChatGPT Pro 用户**可以使用 GPT-5.3-Codex-Spark（研究预览版）。

在会话中，执行`/model`命令可以切换模型：

![[Pasted image 20260517234142.png|600]]

选择指定的模型之后，会要求你选择模型推理能力：

![[Pasted image 20260517234245.png|600]]

当然，在启动 CLI 时也可以直接指定模型，例如：

```shell
codex --model gpt-5.5
```

当正在使用 **gpt‑5.4**或 **gpt‑5.5** 时，可以用**Fast mode**来提高响应速度：使用命令 `/fast on` 开启、`/fast off` 关闭、`/fast status` 查看当前状态。  

开启 Fast mode 后，模型响应速度提升（约提升 1.5 倍），但计算成本也增加：GPT‑5.4 大约是原来的 2 倍，GPT‑5.5 大约是原来的 2.5 倍。


# 六、恢复对话

`Codex`会将会话记录保存在本地，可从中断处继续。

执行：

```shell
codex resume
```

会打开一个历史会话记录列表供我们选择：

![[Pasted image 20260517231147.png|600]]

选择对应的会话按`Enter`键即可恢复对话。

其他命令：

```shell
codex resume --all         # 显示当前工作目录之外的会话
codex resume --last        # 直接回复最近一次对话
codex resume <SESSION_ID>  # 恢复指定会话
```

非交互式自动化运行同样支持恢复：

```shell
codex exec resume --last "修复你发现的竞态条件"
codex exec resume <SESSION_ID> "执行这个计划"
```

**交互式与非交互式**：

- 交互式：一次次查看过程、审批修改，像聊天一样
- 非交互式：`codex exec`，适合脚本，CI/CD或自动化场景，不会打开`TUI`


# 七、图片

## 1、图片输入 ^image-input

你可以附加截图或设计规格文件，让 Codex **在处理文本提示时同时读取图片内容**。

- 可在交互式对话框中直接粘贴图片
- 或在命令行中提供图片文件

如果是在交互式对话中粘贴图片，粘贴后的效果如下：

![[Pasted image 20260517235136.png|500]]

如果在命令行提供图片文件：

```shell
# 单张图片
codex -i screenshot.png "解释这个错误"


# 多张图片
codex --image img1.png,img2.jpg "总结这些图表"
```

说明：

- 支持常见格式，如 PNG、JPEG
- 多张图片使用逗号分隔
- 可以结合文字说明提供上下文信息

## 2、图片生成

可以直接让`Codex`在CLI中生成或编辑图片。如果希望修改或扩展图片，可附加参考图像并在提示中说明：

- 可以用自然语言提示
- 也可以显示调用图片生成技能：在提示中加入 `$imagegen`

内置图片生成使用 **gpt-image-2** 模型。


# 八、语法高亮与主题

`Codex`的 TUI 会对 Markdown 中的代码块和文件差异（diff）进行语法高亮，使得代码在审阅或调试时更容易浏览和理解。

- 使用`/theme`打开主题选择器
- 可以实时预览主题效果
- 选择的主题会保存到`~/.codex/config.toml`中的`tui.theme`中

也可以在 `~/.codex/themes` 目录下添加自定义的 `.tmTheme` 文件，在主题选择器中即可选用这些自定义主题。


# 九、本地代码审查

`Codex CLI`提供本地代码审查功能，可以在**不修改工作区文件**的情况下分析代码变更，并生成可执行的反馈建议。

通过 `/review` 命令启动，你可以选择不同的审查模式，针对未提交的更改、指定提交或者基准分支生成详细报告，也可以自定义审查指令。

## 1、启动代码审查

输入`/resume`会打开审查预设（review presets），如下图所示：


![[Pasted image 20260518002722.png]]

- 根据你选择的模式，读取 diff
- 生成建议，包括潜在问题、风险点、优化建议

本地代码审查**默认使用当前会话模型**。可通过`config.toml`配置`review_model`来覆盖默认模型，例如：

```toml
[review]  
review_model = "gpt-5.5"
```


## 2、审查模式

`Codex`提供四种主要审查模式，可根据场景选择：

### （1）对比基准分支（Review against a base branch）

对比基准分支功能，主要用于在功能分支开发过程中，将当前分支的改动与指定的基准分支（通常是`main`或`develop`）进行比较和审查，帮助开发者提前发现潜在问题、优化点或高风险改动。

示例：

```shell
/review base-branch main
```

说明：

- `main`是指定的基准分支
- `Codex`会自动找到当前分支与`main`的merge base（最近共同祖先提交）
- 生成从 merge base 到当前分支头的差异审查报告

示例图：

```shell
A──B──C──D──E  (main)
        \
         F──G──H  (feature)
```

这里的`C`就是merge base，Codex 会只审查从 `C` 到 `H` 的差异部分。

对比基准分支适合在**创建Pull Request之前**：当开发完一个功能分支，准备提交PR时。执行 `/review base-branch main` 本地检查改动是否有潜在问题。提前修复或优化，减少代码审核反馈。

### （2）审查未提交更改（Review Uncommited changes）

审查未提交更改功能，用于检查当前分支中已暂存、未暂存或未跟踪的本地改动，帮助开发者在提交之前发现潜在问题。

示例：

```shell
/review uncommitted
```

说明：

- Codex 会扫描当前工作区中所有暂存和未暂存文件，以及未跟踪文件
- 自动生成针对这些改动的审查报告，包括潜在 bug、逻辑问题、性能建议和安全隐患

适合场景：**提交前的本地预审**，确保代码质量，提高提交质量，减少 PR 反馈。


### （3）审查指定提交（Review a commit）

审查指定提交功能，用于对 **历史提交或特定 commit** 生成审查报告，帮助开发者分析单个提交的质量和潜在问题。

示例：

```shell
/review commit <commit-sha>
```

说明：

- `<commit-sha>` 是你想审查的提交 SHA
- Codex 会读取该提交对应的差异内容，生成针对该提交的审查报告，包括逻辑错误、性能问题和潜在冲突

假设 Git 分支如下：

```
A──B──C──D──E  (main)
        \
         F──G──H  (feature)
```

- 当前想审查提交 `G`
- Git 计算 `G` 的 parent commit = F
- Codex 会生成  F → G 的 diff 报告

适合场景：

- 审查单个重要提交或 bug 修复
- 进行回溯性分析，检查提交是否引入风险
- 对长期功能分支中某个关键提交进行重点审查

### （4）自定义审查指令（Custom review instructions）

自定义审查指令功能允许开发者输入 **自定义提示**，指导 Codex 聚焦特定检查目标，例如性能、安全或可访问性。

```shell
/review custom "重点检查可访问性回退和代码风格"
```

说明：

- `"重点检查可访问性回退和代码风格"` 是自定义提示，告诉 Codex 审查器**关注特定问题**
- 默认是基于当前分支的最新提交（HEAD）和工作区改动进行审查，也可以结合其他模式：

```shell
/review base-branch main custom "重点检查可访问性回退和代码风格"
/review commit <SHA> main custom "重点检查可访问性回退和代码风格"
```