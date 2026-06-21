
# 一、安装 Obsidian 

进入 [Obsidian官网](https://obsidian.md/download)下载安装 Obsidian。

# 二、基础设置

## 1、语言设置

点击左下角的**设置**按钮：

![[Pasted image 20260621220748.png]]

进入设置界面：

![[Pasted image 20260621220840.png]]

在**关于 -> 语言**中，将界面语言切换为**简体中文**。

## 2、设置始终更新内部链接

在**设置 -> 文件与链接**中，开启**始终更新内部链接**。

开启后，当被引用的笔记发生重命名或移动时，Obsidian 会自动更新链接，减少手动维护链接的成本。

![[Pasted image 20260621221403.png]]


## 3、附件存储路径

为了统一管理图片、PDF 等附件资源，建议为附件指定固定目录。

在**设置 -> 文件与链接 -> 附件默认存放路径**中，选择**指定的附件文件夹**，然后在**附件文件夹路径**中填写用于存放附件的目录，例如这里使用的是 `assets`。

![[Pasted image 20260621223046.png]]

## 4、命令面板

macOS 使用 `Command + P` 可以快速打开命令面板；Windows 上对应快捷键是 `Ctrl + P`。

![[Pasted image 20260621223141.png]]

命令面板可以快速执行 Obsidian 的各种操作，例如插入表格、打开设置项、切换视图等。

## 5、笔记属性

打开命令面板，输入**属性列表，选择**属性列表：显示当前笔记的属性列表**并回车：

![[Pasted image 20260621223254.png]]

此时，右侧边栏会出现一个圆圈内包含感叹号的图标：

![[Pasted image 20260621223329.png]]

点击该图标后，可以查看或添加当前笔记的属性。

也可以直接在笔记开头输入 `---` 并回车，手动创建属性区：

![[Pasted image 20260621223404.png]]

# 三、打通 AI

## 1、启用 Obsidian CLI

AI Agent 本身已经具备读写 `Markdown` 文件的能力，但 Obsidian 笔记并不只是普通的 Markdown 文档，它还包含双向链接、属性、标签、Bases、附件嵌入等知识管理结构。

如果只让 AI 直接读写文件，它需要自行理解这些结构，既容易出错，也会消耗更多上下文。因此，更稳妥的方式是启用 Obsidian CLI，让 AI 通过 Obsidian 提供的命令行接口操作仓库。

开始之前，需要先在 Obsidian 中启用 CLI。

在**设置 -> 关于 -> 高级**中，开启**命令行界面**：

![[Pasted image 20260621225242.png]]

如下图所示：

![[Pasted image 20260621225254.png]]

点击**注册**后，Obsidian 会将 `obsidian` 命令行程序加入 `PATH` 环境变量。

完成后，就可以在终端中通过 `obsidian` 命令操作 Obsidian 仓库，例如新建文件：

![[Pasted image 20260621225330.png]]

日常使用时，不需要自己掌握 Obsidian CLI 命令，因为它主要是提供给 AI Agent 调用的接口。AI 学习 CLI 的用法，再通过它更规范地管理 Obsidian 仓库。

## 2、操作 Obsidian 仓库的方式

想要使用 AI Agent 操作 Obsidian 仓库，主要有三种方式：

- 使用操作系统自带终端或Agent App，在 Obsidian 外部操作仓库
- 使用 Obsidian 的 `Terminal` 插件，在 Obsidian 内嵌终端中操作仓库
- 使用 Obsidian 的 `Claudian` 插件，在 Obsidian 中操作仓库

可以按照个人喜欢选择哪一种方式。这里介绍两种内嵌方式。

### （1）Terminal 插件

打开**设置 -> 第三方插件**，关闭安全模式：

![[Pasted image 20260622003621.png]]

然后选择**社区插件市场**，点击浏览：

![[Pasted image 20260622003656.png]]

搜索`Terminal`：

![[Pasted image 20260622003725.png]]

点击安装：

![[Pasted image 20260622003738.png]]

安装完成后，点击启用：

![[Pasted image 20260622003754.png]]

此时，Obsidian 左侧边栏会出现 `Terminal` 图标：

![[Pasted image 20260622003818.png|300]]

点击图标后，会弹出如下界面：

![[Pasted image 20260622003840.png]]

由于这里希望在 Obsidian 内部使用终端，因此选择**整合式**：

![[Pasted image 20260622003919.png]]


此时，窗口下方会出现终端面板，并默认使用系统配置的 `zsh` shell。

为了之后能更方便地以整合式打开终端，并指定其他 shell，可以在**设置 -> 第三方插件 -> 已安装插件**中找到 `Terminal` 插件。

![[Pasted image 20260622004001.png]]

点击设置：

![[Pasted image 20260622004020.png]]


在默认设置中选择**整合式**。

然后在**配置**中找到整合式对应的配置，点击编辑：

![[Pasted image 20260622004041.png|400]]

例如想使用`fish` shell，可以将 shell 替换为 `fish`，即写入`fish`可执行文件的路径：

![[Pasted image 20260622004129.png|400]]


设置完成后，以后在 Obsidian 左侧点击 `Terminal` 按钮，就可以直接打开 `fish shell`：

![[Pasted image 20260622004241.png]]


### （2）Claudian 插件

`Claudian`插件可以理解为 Claude Code 等 Agent 在 Obsidian 的快捷入口。

使用`Claudian`插件的前提：本机已经安装好并可以正常使用对应 AI Agent。

`Claudian` 没有上架 Obsidian 社区插件市场，需要从 GitHub 下载：<https://github.com/YishenTu/claudian>

安装方式是下载如图所示的三个文件，并复制到当前仓库的 `.obsidian/plugins/claudian/` 目录下：
![[Pasted image 20260622004608.png]]

随后，在**设置 -> 第三方插件**中点击刷新，并启用 `Claudian`：

![[Pasted image 20260622004632.png]]

此时，左侧边栏会出现 `Claudian` 图标：

点击后，右侧会打开 `Claudian` 界面，之后就可以通过自然语言与AI交流控制 Obsidian 仓库。

不过，在正式使用前，建议先完成一些基础设置：

![[Pasted image 20260622004730.png]]

首先，在**通用**设置中，可以将界面语言改为**简体中文**：

![[Pasted image 20260622004747.png]]


然后，将媒体文件夹改为自己指定的附件目录，例如这使用`assets`：

![[Pasted image 20260622004820.png]]

还可以继续配置具体 AI Agent，例如  Claude Code：

![[Pasted image 20260622004844.png]]

完成设置后，就可以在 `Claudian` 中直接对话：

![[Pasted image 20260622004903.png|500]]

## 3、安装 obsidian-cli skill

为了让 AI 更容易使用 Obsidian CLI，可以为 AI Agent 安装对应的 `skill`。

Obsidian 的 CEO `Kepano` 编写了一组 Obsidian 相关的 skills，仓库地址是：<https://github.com/kepano/obsidian-skills>。

最简单的安装方式，是将该 Git 仓库中的 `skills` 目录复制到当前 Obsidian 仓库根目录下的 `.claude` 文件夹（claude code）或`.agents`文件夹（codex）中。

复制完成后，可以通过简单对话验证 skill 是否被正确加载。

需要注意的是，如果请求比较泛化，例如“请帮我在当前目录创建一篇名为 AI 创建的笔记，内容是当前日期”，AI Agent 未必会自动调用相关 skill。

因此，更稳妥的做法是在记忆文件中补充明确规则，例如在`CLAUDE.md`（claude code）或`AGENTS.md`（codex）中写明：当操作 Obsidian 仓库时，优先使用 Obsidian 相关 skill

例如可以直接让 AI 补充规则：

![[Pasted image 20260622003000.png]]

验证效果如下：

![[Pasted image 20260622003049.png]]

![[Pasted image 20260622003057.png]]

# 四、个性化设置

## 1、设置主题

在**设置 -> 外观 -> 主题**中，可以选择适合自己的主题：

![[Pasted image 20260622005701.png]]

例如，这里下载并使用了 `Things` 主题。


## 2、设置段落首行缩进

在笔记右上角，可以在**阅读模式**和**编辑模式**之间切换。

![[Pasted image 20260622005753.png|400]]

默认阅读模式下，段落不会进行首行缩进。Markdown 中输入`Tab`键会解析为代码块。

可以使用 CSS snippet：源文件仍然保持干净，缩进效果只在阅读视图渲染时生效。

在**设置 -> 外观 -> CSS 代码片段**中，可以添加 CSS 文件：

![[Pasted image 20260622010027.png|500]]

新增 `body-text-indent.css`，设置段落首行缩进：

```css
.markdown-preview-view p {
  text-indent: 2em;
}
```

回到**设置 -> 外观 -> CSS 代码片段**，启用该 CSS 文件：

![[Pasted image 20260622010132.png|500]]


## 3、设置行内代码高亮

`Things` 主题的行内代码默认高亮不够明显，因此可以通过 CSS snippet 单独增强。

效果：让\` \`包裹的内容以紫色高亮显示，使其与普通正文更容易区分。

新增并启用 `inline-code-highlight.css`：

```css
.cm-inline-code {
  color: #e0a0ff !important;
  background-color: rgba(180, 100, 255, 0.15) !important;
  padding: 1px 4px;
  border-radius: 3px;
}

.markdown-preview-view code {
  color: #e0a0ff !important;
  background-color: rgba(180, 100, 255, 0.15) !important;
  padding: 1px 4px;
  border-radius: 3px;
}
```

