
>[!todo]
>- [ ] 安装主题，CSS片段修改部分主题样式
>- [ ] qmd 本地 Markdown 搜索引擎
>- [ ] 打造图床




## Claudian 插件

`Claudian`插件可以理解为 Claude Code 等 Agent 在 Obsidian 的快捷入口。

使用`Claudian`插件的前提：本机已经安装好并可以正常使用对应 AI Agent。

`Claudian` 没有上架 Obsidian 社区插件市场，需要从 GitHub 下载：<https://github.com/YishenTu/claudian>

安装方式是下载如图所示的三个文件，并复制到当前仓库的 `.obsidian/plugins/claudian/` 目录下：
![[assets/Pasted image 20260622004608.png]]

随后，在**设置 -> 第三方插件**中点击刷新，并启用 `Claudian`：

![[assets/Pasted image 20260622004632.png]]

此时，左侧边栏会出现 `Claudian` 图标：

点击后，右侧会打开 `Claudian` 界面，之后就可以通过自然语言与AI交流控制 Obsidian 仓库。

不过，在正式使用前，建议先完成一些基础设置：

![[assets/Pasted image 20260622004730.png]]

首先，在**通用**设置中，可以将界面语言改为**简体中文**：

![[assets/Pasted image 20260622004747.png]]


然后，将媒体文件夹改为自己指定的附件目录，例如这里使用`assets`：

![[assets/Pasted image 20260622004820.png]]

还可以继续配置具体 AI Agent，例如  Claude Code：

![[assets/Pasted image 20260622004844.png]]

完成设置后，就可以在 `Claudian` 中直接对话：

![[assets/Pasted image 20260622004903.png|500]]





## 设置行内代码高亮

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

