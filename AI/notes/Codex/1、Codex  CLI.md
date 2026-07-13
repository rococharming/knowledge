
# 一、简介

`Codex` 是 OpenAI 提供的 AI 编程代理（AI Coding Agent）。它不是单纯的代码补全工具，而是可以直接参与开发任务的智能体。

`Codex`的核心能力包括：

- 理解和分析代码库
- 编写代码
- 修改文件
- 运行命令
- 调试和修复问题
- 审查代码变更
- 根据结果继续迭代
- 自动化处理开发任务

`Codex`有多种使用形态：

- `Codex CLI`
- `Codex App`
- `Codex IDE Extension`
- `Codex Web / Codex Cloud`

本篇介绍`Codex CLI`，也就是在终端中使用 `Codex`。

> Codex CLI 运行在本地终端，但它并不是完全离线工具。它会把完成任务所需的上下文发送给模型处理，然后在本地执行文件读取、文件修改、命令运行等操作。

# 二、安装并登录Codex CLI

## 1、安装

开发者最常用的方式是安装 `Codex CLI`。

可以使用 `npm` 全局安装：

```shell
npm install -g @openai/codex
```

安装完成后，执行下面命令验证是否安装成功：

```shell
codex --version
```

如果后续想更新 `Codex CLI`，可以使用：

```shell
npm install -g @openai/codex@latest
```

也可以使用：

```shell
codex update
```

如果不想继续使用，可以卸载：

```shell
npm uninstall -g @openai/codex
```


## 2、登录

第一次安装好`Codex CLI`后，进入某个项目目录，执行：

```shell
codex
```

首次运行时需要登录。首次运行时需要登录。`Codex CLI` 支持两种主要登录方式：

1. 使用 ChatGPT 账号登录
2. 使用 API Key登录

如果你已经购买了支持 Codex 的 ChatGPT 套餐，通常选择：`Sign in with ChatGPT`

![[assets/Pasted image 20260517221219.png|500]]

浏览器会打开登录页面，完成登录后即可使用。

登录完成后，`Codex CLI` 会缓存登录信息，下次启动时会复用。

如果想要退出登录，在会话中执行斜杠命令`/logout`：

```text
/logout
```


# 三、基本使用

## 1、交互模式开启对话

在某个项目路径下直接执行：

```shell
codex
```

`Codex CLI` 会启动一个终端交互界面，也就是 `TUI`（Terminal User Interface），进入交互模式。

**交互模式适合边看边改的开发任务**。它会打开一个 full-screen terminal UI，Codex 可以读取仓库、修改文件并运行命令，用户可以实时审查它的动作。

会话开启后，可以直接在对话中输入：

- 自然语言任务
- 代码片段
- 文件路径
- 截图或图片
- slash command
- skill 调用等

也可以在命令行指定初始提示启动交互模式：

```shell
codex "给我解释这个代码库"
```

该初始提示会作为会话开始时的第一个任务要求。


## 2、非交互模式运行任务

执行 `codex exec` 可以让 `Codex CLI` 以非交互方式完成任务：

```shell
codex exec "你好"
```

`codex exec` 也有短别名：

```shell
codex e "你好"
```

非交互模式适合脚本或CI风格的任务，它会把结果输出到`stdout`，并支持恢复之前的 exec session。

`codex exec`的任务参数也可从标准输入读取。

例如：

```shell
cat prompt.txt | codex exec -
```

这里的 `-` 表示从 `stdin` 读取 prompt。


## 3、模型与推理能力

在`Codex`中，大多数任务推荐使用`gpt-5.5`（如果可用）。它是 OpenAI 当前最新的前沿模型，适用于：

- 复杂编码任务
- 计算机操作
- 知识工作
- 研究型工作流

如果 gpt-5.5 还不可用，则继续使用 gpt-5.4。

对于需要额外快速响应的任务，ChatGPT Pro 用户可以使用 GPT-5.3-Codex-Spark（研究预览版）。

在会话中，执行`/model`命令可以切换模型：

![[assets/Pasted image 20260517234142.png|600]]

选择指定的模型之后，会要求你选择模型推理能力：

![[assets/Pasted image 20260517234245.png|600]]

当然，在启动 CLI 时也可以直接指定模型，例如：

```shell
codex --model gpt-5.5
```

当正在使用 gpt‑5.4 或 gpt‑5.5 时，可以用`Fast mode`来提高响应速度：

- `/fast` 切换开启/关闭
- `/fast on` 开启
- `/fast off` 关闭
- `/fast status` 查看当前状态。  

开启`Fast mode`后，模型响应速度提升，但计算成本也增加。


## 4、图片

### （1）图片输入

`Codex`除了可以输入文本，还可以输入图片：

- 可在交互式对话框中直接粘贴图片
- 或在命令行中通过`--image`或`-i`提供图片文件

如果是在交互式对话中粘贴图片，粘贴后的效果如下：

![[assets/Pasted image 20260517235136.png|500]]

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


### （2）图片生成

`Codex`也可以生成图片，内置图片生成使用`gpt-image-2`模型。

可以直接在对话框中通过自然语言描述想要生成的图片：

```text
请在当前目录下生成一张雪纳瑞小狗图片
```

如果希望修改或扩展图片，可附加参考图像并在提示中说明如何操作。

`Codex`会自动触发`imagegen` skill的调用来生成或操作图片。

也可以显示调用，在提示词中加入：

```text
$imagegen 帮我生成一张小猫图片
```

> 注意，`Codex`调用Skill使用的是`$`符号而不是`/`。


## 5、恢复对话

`Codex`会将会话记录保存在本地，可选择历史旧会话继续。

执行：

```shell
codex resume
```

会打开一个历史会话记录列表供我们选择：

![[assets/Pasted image 20260517231147.png|500]]

选择对应的会话按 <kbd>Enter</kbd> 键即可恢复对话。

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


## 6、语法高亮与主题

`Codex`的 TUI 会对 Markdown 中的代码块和文件差异（diff）进行语法高亮，使得代码在审阅或调试时更容易浏览和理解。

通过`/theme`打开主题选择器，可以预览主题的实时效果，选择自己喜欢的主题。选择的主题会保存到`~/.codex/config.toml`配置文件中的`tui.theme`中。

当然，也可以在 `~/.codex/themes` 目录下添加自定义的 `.tmTheme` 文件，然后在主题选择器中即可选用这些自定义主题。


## 7、清空上下文

执行`/clear`可以清空终端并开始新会话，旧会话仍然可以通过会话历史恢复。

按下 <kbd>Ctrl</kbd> + <kbd>L</kbd> 只会清空屏幕，但不会开始新的对话，仍然在当前会话中。


## 8、复制最近一次的输出

执行`/copy`或按下 <kbd>Ctrl</kbd> + <kbd>O</kbd> 可以复制`Codex`最近一次已完成的输出。如果当前回合仍在运行，`Codex`会复制最近一次已经完成的输出，而不是复制正在生成中的文本。


## 9、运行本地shell命令

在对话框中输入 <kbd>!</kbd>，可以切换到`Shell Mode`，之后可以执行Shell命令并查看结果。

![[assets/Pasted image 20260521012525.png|600]]


## 10、运行中输入

当`Codex`正在执行任务时，此时输入框新的提示词按 <kbd>Enter</kbd> 会注入当前会话，`Codex`会停下来先分析新的提示词再继续任务。

如果按 <kbd>Tab</kbd> 则将新提示词、斜杠命令、! shell命令排队到下一回合，也就是等当前回合任务结束。


## 11、搜索提示词历史

在`Codex`的输入框中，按 <kbd>Ctrl</kbd> + <kbd>R</kbd> 可以搜索之前输入过的提示词历史。它适合在你想复用、修改或找回某条旧提示词时使用。

![[assets/Pasted image 20260521013607.png|500]]

输入几个字段后，会显示以前输入过的提示词，此时按 <kbd>Enter</kbd> 接受匹配，或按 <kbd>Esc</kbd> 取消。


## 12、提示编译器

当在输入框中编写提示语需要换行，按 <kbd>Ctrl</kbd> + <kbd>J</kbd>。

在编写较长的提示语时，可以按 <kbd>Ctrl</kbd> + <kbd>G</kbd> 切换到完整编辑模式，然后将编辑后的内容发给模型，这样更方便。

但前提是需要设置好环境变量`VISUAL`或`EDITOR`。

可以在对应的 shell 配置文件中加入：

```shell
export VISUAL="code --wait"
```


## 13、@引用工作区文件

在 Codex 的输入框中输入 `@`，可以打开一个面向当前工作区根目录的模糊文件搜索界面。按 <kbd>Tab</kbd> 或 Enter 可以把当前高亮的文件路径插入到消息中。

![[assets/Pasted image 20260521021403.png|500]]


## 14、编辑历史消息并从中分叉

当输入框为空时，连续按两次 <kbd>Esc</kbd> 可以编辑上一条用户消息。继续按 <kbd>Esc</kbd> 可以在 transcript 中继续向前回溯，然后按 <kbd>Enter</kbd> 可以从那个位置分叉出新的对话路径。


## 15、设置工作根目录与额外可写目录

`codex --cd <path>`用来指定`Codex`的**工作根目录**。你可以在任意目录下启动 Codex，不需要先手动 `cd` 到项目目录。Codex 启动后，会把 `<path>` 当作当前任务的主要工作区，TUI 顶部也会显示当前活动路径。

例如：

```shell
codex --cd ~/Projects/my-app
```

等价于你先执行：

```shell
cd ~/Projects/my-app
codex
```

`--add-dir` 用来给 Codex 额外授权其他可写目录。默认情况下，Codex 的主要工作范围是当前工作根目录。如果你的任务需要同时修改多个目录，比如前端、后端、共享包，就可以用 `--add-dir` 把其他目录也加入可写范围。官方命令行参考也说明，`--add-dir` 会在主工作区之外授予额外目录的写入权限，并且可以重复使用多次。

示例：

```shell
codex --cd apps/frontend --add-dir ../backend --add-dir ../shared
```


## 16、退出会话

执行`/exit`或者按 <kbd>Ctrl</kbd> + <kbd>C</kbd> 退出会话。

# 四、网页搜索

`Codex`内置了一个由 OpenAI 第一方提供的网页搜索工具。

对于`Codex CLI`中的本地任务，**`Codex`默认启用网页搜索**，并从网页搜索缓存中提供结果。这个缓存是由 OpenAI 维护的网页结果索引，因此缓存模式返回的是预先索引好的结果，而不是实时抓取网页。
这样可以减少来自任意实时网页内容的提示注入风险（比如一些恶意指令）。

不过，即使结果来自缓存索引，网页内容本身也可能是错的、过时的、带偏见的、恶意的，或者包含误导 agent 的指令。

如果使用`--yolo`，或者其他具有完整访问权限的沙盒设置，网页搜索默认会使用实时结果。

如果要获取最新数据，可以在单次运行中传入`--search`：

```shell
codex --search
```

或者在基础配置`.codex/config.toml`中设置：

```toml
"web_search" = "live"
```

如果你想关闭网页搜索，可以写：

```toml
web_search = "disabled"
```







# 二、本地代码审查

`Codex CLI`提供本地代码审查功能，可以在**不修改工作区文件**的情况下分析代码变更，并生成可执行的反馈建议。

通过 `/review` 命令启动，你可以选择不同的审查模式，针对未提交的更改、指定提交或者基准分支生成详细报告，也可以自定义审查指令。

## 1、启动代码审查

输入`/resume`会打开审查预设（review presets），如下图所示：


![[assets/Pasted image 20260518002722.png]]

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
