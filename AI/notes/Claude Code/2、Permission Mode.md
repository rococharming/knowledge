
# 一、概述

当`Claude Code`想要编辑文件、运行`shell`命令或发起网络请求时，它会暂停并征求你的同意。`Permission Mode`（权限模式）**控制这种暂停发生的频率**。选择的模式会影响整个会话的流程。

# 二、可用模式

`Claude Code`提供了几种模式，每种模式都在便利性和监督性之间做出了不同权衡。下面列出了`Claude Code`的权限模式。

| 模式                  | 无需询问即可执行                                      | 最适合          |
| ------------------- | --------------------------------------------- | ------------ |
| `default`           | 仅读取                                           | 初次使用、敏感工作    |
| `acceptEdits`       | 读取、文件编辑和常用文件系统命令（`mkdir`、`touch`、`mv`、`cp` 等） | 审阅你正在迭代的代码   |
| `plan`              | 仅读取                                           | 在修改前探索代码库    |
| `auto`              | 所有操作，带后台安全检查                                  | 长任务、减少提示疲劳   |
| `dontAsk`           | 仅预批准的工具                                       | 受限的 CI 和脚本环境 |
| `bypassPermissions` | 所有操作                                          | 仅限隔离的容器和虚拟机  |

在除 `bypassPermissions` 以外的所有模式下，对**[[#^protected-path|受保护路径]]的写入永远不会自动批准，以防止意外破坏仓库状态和 Claude 自身的配置。

# 三、切换权限模式

可以在`Claude Code`启动时、中途或作为持久默认值来切换模式。

## 1、会话期间

按`Shift + Tab`循环切换`default` -> `acceptEdits` -> `plan`。当前模式会显示在状态栏中，如下所示：

![[Pasted image 20260509180642.png]]

并非每种模式都会出现在默认循环中：

- `auto`：只有你的账号满足`auto mode`的使用条件才会出现。当在权限模式切换到`auto`时，Claude Code 会先显示一个确认启用的提示。
- `bypassPermissions`：当以 `--permission-mode bypassPermissions`、`--dangerously-skip-permissions`或`--allow-dangerously-skip-permissions`启动后，`bypassPermissions`才会在模式切换循环中出现。`--allow-`变体会将该模式添加到循环中但不激活它
- `dontAsk`：永远不会出现在循环中，使用 `--permission-mode dontAsk` 来设置它

## 2、启动时

启动`claude`时，将模式作为标志传递：

```shell
claude --permission-mode plan
```

> --permission-mode 标志同样适用于带 -p 的非交互式运行。

## 3、作为默认值设置

在设置文件如`settings.json`中设置`defaultMode`：

```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```


# 四、 acceptEdits 模式

`acceptEdits` 是一种更偏向“先执行、后审阅”的权限模式。启用后，Claude 可以在当前工作目录中创建和编辑文件，不需要每次都向你确认。状态栏会显示：`⏵⏵ accept edits on`。

> 适合你信任 Claude 可以直接修改项目文件，但仍然希望通过编辑器、`git diff` 或版本控制工具，在事后统一检查改动

在 `acceptEdits` 模式下，Claude 不只可以自动编辑文件，还可以自动执行一部分常见的文件系统命令，例如`mkdir`、`touch`、`rm`、`rmdir`、`mv`、`cp`、`sed`等。

`acceptEdits`并不是无限制地允许`Claude`修改文件。自动批准只适用于当前工作目录或`additionalDirectories`内的路径，超过该范围、[[#^protected-path|受保护路径]]以及所有其他`Bash`命令仍然会提示。

如果启用了[[Tools#^powershell-tool|PowerShell工具]]，`acceptEdits` 也会自动批准一些常见的 PowerShell 文件操作命令。


# 五、plan 模式

`plan`模式告诉`Claude`在研究并提出更改方案时不实际执行。`Claude`会读取文件、运行`shell`命令进行探索和撰写方案，但不会编辑你的源代码。

在方案准备好后，`Claude`会展示它并询问你如何继续。从提示中你可以：

- 批准并在 auto 模式下开始
- 批准并接受编辑
- 批准并手动审阅每次编辑
- 继续规划并给出反馈
- 使用`Ultraplan`在浏览器中审阅和优化

接受方案还会根据方案内容自动命名会话，除非你已使用 `--name` 或 `/rename` 设置了名称。

按 `Ctrl+G` 可在默认文本编辑器中打开拟议的方案并直接编辑。

如果启用了`showClearContextOnPlanAccept`：

```JSON
{  
  "showClearContextOnPlanAccept": true  
}
```

那么在你批准方案时，每个批准选项旁边都会多一个类似“继续前清除规划上下文”的选项。
它的作用是：

> 在 Claude 开始执行方案之前，清掉前面规划阶段积累的上下文，只保留最终方案或必要信息，让后续执行更干净。


# 六、auto 模式

`auto`模式是一种更自动化的模式。启用后，`Claude Code` 会尽量减少权限确认提示，让`Claude `可以更连续地执行任务。不过，它**不是完全无保护地放行所有操作**，而是会在关键动作执行前交给一个独立的**安全分类器**判断。

> auto = Claude 自动执行 + 分类器提前检查高风险操作
> 适合：你已经信任任务大方向、希望减少中途确认打断的场景。

注意，`auto`目前属于研究预览功能，不要把它当成敏感操作的替代审阅机制。

`auto`模式并非所有用户、套餐、模型可以使用，需要满足：

- **套餐**：Max、Team、Enterprise 或 API。Pro 套餐不可用。
- **管理员**：如果使用的是 Team 或 Enterprise，管理员需要先在 Claude Code 管理设置中启用 `auto` 模式，普通用户才能使用。
- **模型**：Team、Enterprise 和 API 套餐上为 Claude Sonnet 4.6、Opus 4.6 或 Opus 4.7；Max 套餐上仅 Claude Opus 4.7。其他模型（包括 Haiku 和 claude-3 模型）不支持。
- **提供商**：仅限 Anthropic API。

每个被拒绝的操作都会显示通知，并出现在 `/permissions` 的**denied**选项卡下，你可以按 `r` 以手动批准重试。


# 七、dontAsk 模式

`dontAsk` 是一种**完全非交互式**的权限模式。它的核心规则是：

> 凡是原本需要提示你确认的操作，在 `dontAsk` 模式下都不会弹出提示，而是直接拒绝。

在 `dontAsk` 模式下，只有两类操作可以执行：

- 匹配 `permissions.allow` 的操作

例如配置：

```JSON
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(pnpm lint)"
    ]
  }
}
```

那么 Claude 可以执行：

```
npm test
pnpm lint
```

- 只读`Bash`命令

一些不会修改系统或项目状态的 Bash 命令，也可以执行。例如`ls`、`cat`、`pwd`、`grep`、`find`等。

显式的 `ask` 规则会被拒绝而不是提示。例如：

```JSON
{
  "permissions": {
    "ask": [
      "Bash(npm install)"
    ]
  }
}
```

在默认模式下，执行`npm install`会询问你，但`dontAsk`直接拒绝。

# 八、bypassPermissions 模式

`bypassPermissions` 是 Claude Code 中权限最宽松、风险最高的模式，该模式禁用权限提示和安全检查，以便工具调用立即执行。这也包括[[#^protected-path|受保护路径]]。

不过，作为针对文件系统根目录或主目录的删除操作，如 `rm -rf /` 和 `rm -rf ~`，仍然会作为防止模型错误的断路器而提示。

> 建议在隔离环境中使用该模式，例如容器、虚拟机、临时沙箱环境。

你无法从不是以其中一个启用标志启动的会话中进入 `bypassPermissions`；使用其中一个重启以启用它：

```shell
claude --permission-mode bypassPermissions
```

`--dangerously-skip-permissions` 标志是等效的。




# 九、受保护的路径 ^protected-path 

在除了 `byPassPermissions`以外的所有模式下，对一小部分路径的写入永远不会自动批准，者可以防止意外破坏仓库状态和 Claude 自身的配置：

- 在`default`、`acceptEdits`和`plan`中，这些写入会提示
- 在`auto`中，它们被路由到分类器
- 在`dontAsk`中，它们会被拒绝
- 在`byPassPermissions`中，它们被允许

受保护的目录：

- `.git`
- `.vscode`
- `.idea`
- `.husky`
- `.claude`（除了`.claude/commands`、`.claude/agents`、`.claude/skills`和`.claude/worktree`）

受保护的文件：

- `.gitconfig`、`.gitmodules`
- `.bashrc`、`.bash_profile`、`.zshrc`、`.zsh_profile`、`profile`
- `.ripgreprc`
- `.mcp.json`、`.claude.json`

