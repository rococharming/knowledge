
# 一、概述

当`Claude Code`想要编辑文件、运行shell命令或发起网络请求时，默认会暂停并请求你的确认。

`Permission Mode`（权限模式）用来**控制这种提示出现的频率**。

不同权限模式本质上是在**便利性**和**监督性**之间做权衡：

- 越严格的模式，越适合敏感项目、生产环境、配置文件修改等场景；
- 越宽松的模式，越适合长任务、批量修改、临时实验环境等场景。

权限模式只决定基础行为。除此之外，还可以通过`permission.allow`、`permission.ask`、`permission.deny`等规则进一步控制具体工具或命令的权限。不过，`bypassPermissions`会跳过权限层，因此这些权限规则不再会生效。

# 二、权限模式的分类

`Claude Code` 提供了几种权限模式，每种模式的自动批准范围不同。

| 模式                  | 无需询问即可执行                                      | 适合场景           |
| ------------------- | --------------------------------------------- | -------------- |
| `default`           | 仅读取                                           | 初次使用、敏感工作      |
| `acceptEdits`       | 读取、文件编辑和常用文件系统命令（`mkdir`、`touch`、`mv`、`cp` 等） | 迭代代码并在事后统一审阅   |
| `plan`              | 仅读取                                           | 修改前先探索代码库并制定方案 |
| `auto`              | 所有操作，但会经过后台安全检查                               | 长任务、减少提权限提示打断  |
| `dontAsk`           | 仅预批准工具和只读Bash命令                               | 受限 CI 、脚本环境    |
| `bypassPermissions` | 所有操作                                          | 隔离容器、虚拟机、临时沙箱  |

> 在除 `bypassPermissions` 以外的所有模式下，对[[#^protected-path|受保护路径]]的写入永远不会自动批准，以防止意外破坏仓库状态或 Claude Code自身配置。

# 三、切换权限模式

可以在**会话中、启动时或配置文件中**切换权限模式。

## 1、会话期间切换

在 CLI 中，可以按 `Shift + Tab` 循环切换：

```text
default -> acceptEdits -> plan
```

当前模式会显示在状态栏中，如下所示：

![[Pasted image 20260509180642.png|500]]

这里`accept edits on`即为`acceptEdits`模式。

并不是所有模式都会出现在默认循环中：

- `auto`：只有账号满足 `auto` 模式使用条件时才会出现。第一次切换到 `auto` 时，Claude Code 会显示确认启用提示。
- `bypassPermissions`：只有在启动时使用了 `--permission-mode bypassPermissions`、`--dangerously-skip-permissions` 或 `--allow-dangerously-skip-permissions` 后，才会出现在模式循环中。其中 `--allow-dangerously-skip-permissions` 只是把该模式加入循环，不会直接启用。
- `dontAsk`：永远不会出现在循环中，使用 `--permission-mode dontAsk` 来设置它

## 2、启动时切换

启动`claude`时，可以通过 `--permission-mode` 指定模式：

```shell
claude --permission-mode plan
```

这个参数也适用于 `-p` 非交互式运行：

```shell
claude -p "run tests" --permission-mode dontAsk
```


## 3、设置为默认模式

可以在`Claude Code`的设置文件中配置默认模式，如在`~/settings.json`中设置：

```json
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

如果只想让某个项目默认进入`plan`模式，也可以在项目的`.claude/settings.json`中设置：

```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

# 四、default模式

`default`是`Claude Code`的默认权限模式，也是最保守、最适合初次使用的模式。

在这个模式下，`Claude`可以直接读取项目文件、分析代码、搜索内容，但当它想要执行可能改变系统或项目状态的操作时，会先暂停并请求你的确认。

例如下面这些操作通常会触发确认：

- 编辑文件
- 创建、删除、移动文件
- 运行可能修改项目状态的shell命令
- 安装依赖
- 发起网络请求


# 五、 acceptEdits 模式

`acceptEdits` 是一种偏向**先执行、后审阅**的权限模式。

启用后，Claude 可以在当前工作目录中创建和编辑文件，不需要每次都向你确认。状态栏会显示：`⏵⏵ accept edits on`。

它适合这样的场景：**你愿意让 Claude 直接修改项目文件，但仍然希望通过编辑器、`git diff` 或版本控制工具在事后统一检查改动**。

在 `acceptEdits` 模式下，Claude 不只可以自动编辑文件，还可以自动执行一部分常见文件系统命令，例如：

- mkdir
- touch
- rm
- rmdir
- mv
- cp
- sed

这些命令如果带有安全的环境变量前缀，例如 `LANG=C`、`NO_COLOR=1`，或者通过 `timeout`、`nice`、`nohup` 等包装执行，也可以被自动批准。

`acceptEdits`并不是无限制放行，自动批准只适用于：

- 当前工作目录
- 配置在`additionalDirectories`中的目录

下面这些情况仍然会触发提示：

- 路径超出了当前工作目录和`addtionalDirectories`
- 写入[[#^protected-path|受保护路径]]；
- 执行其他 Bash 命令

如果启用了[[Tools#^powershell-tool|PowerShell工具]]，`acceptEdits` 也会自动批准部分常见 PowerShell 文件操作，例如 `Set-Content`、`Add-Content`、`Clear-Content`、`Remove-Item` 及其常见别名，但同样受路径范围和受保护路径规则限制。


# 六、plan 模式

`plan`模式用于**先研究、后修改**。在这个模式下，`Claude`会先阅读项目文件、探索代码库并撰写修改方案，但不会直接编辑源代码。

需要注意：`plan`模式并不等于所有探索命令都可以无提示执行。它的权限提示规则仍然和`default`模式一致。也就是说，读取类操作通常可以直接执行，但需要权限提示的shell命令仍然会提示。

当方案准备好之后，`Claude Code`会展示计划并询问如何继续。你可以选择：

- 批准并在`auto`模式下开始执行
- 批准并进入`acceptEdits`
- 批准并手动审阅每次编辑
- 继续规划并给出反馈

接受方案后，`Claude`会退出`plan`模式，并切换到你选择的执行模式。接受方案还会根据方案内容自动命名会话，除非你已经通过 `--name` 或 `/rename` 设置了会话名称。

如果觉得在终端里编辑计划不方便，可以按 `Ctrl + G`，用默认文本编辑器打开拟议方案并直接修改。

如果启用了`showClearContextOnPlanAccept`：

```JSON
{  
  "showClearContextOnPlanAccept": true  
}
```

那么在批准方案时，每个批准选项旁边都会多一个“继续前清除规划上下文”之类的选项。

它的作用是：在`Claude`开始执行方案之前，清掉规划阶段积累的大量上下文，只保留最终方案或必要信息，让后续执行阶段更干净。

# 七、auto 模式

`auto`是更自动化的权限模式。启用后，`Claude Code`会尽量减少权限确认提示，让 Claude 可以更连续地执行任务。

但 `auto` 并不是无保护地放行所有操作，它会在关键动作执行前交给一个**独立的分类器模型**判断。也就是说，auto = Claude Code自动执行 + 分类器后台检查高风险操作。

`auto` 模式适合你已经信任任务大方向，希望减少中途确认打断的场景。但它仍然是研究预览功能，不能替代你对敏感操作的审阅。

`auto` 模式要求 Claude Code 版本为 `v2.1.83` 或更高，账号还需要满足这些条件：

- 套餐：Max、Team、Enterprise 或 API；Pro 不可用。
- 管理员：Team 和 Enterprise 中，管理员需要先在 Claude Code 管理设置中启用 `auto` 模式。管理员也可以通过 managed settings 中的 `permissions.disableAutoMode = "disable"` 禁用该模式。
- 模型：Team、Enterprise 和 API 套餐上为 Claude Sonnet 4.6、Opus 4.6 或 Opus 4.7；Max 套餐上仅 Claude Opus 4.7。其他模型（包括 Haiku 和 claude-3 模型）不支持。
- 提供商：仅限 Anthropic API。

`auto` 模式下，每个动作会按固定顺序判断：

1. 如果匹配`allow`或`deny`规则，直接按规则处理
2. 只读操作，以及工作目录内的普通文件编辑，会自动批准，但[[#^protected-path|受保护路径]]除外
3. 其他操作交给分类器判断
4. 如果分类器阻止操作，Claude 会收到原因并尝试替代方案

每个被拒绝的操作都会显示通知，并出现在 `/permissions` 的 `Recently denied` 选项卡中。你可以按 `r` 手动批准并重试。

如果分类器连续阻止 3 次，或在当前会话中累计阻止 20 次，`auto` 模式会暂停，Claude Code 会恢复权限提示。你批准被提示的操作后，`auto` 模式会继续。


# 八、dontAsk 模式

`dontAsk` 是一种**完全非交互式**的权限模式。它的核心规则是：

> 凡是原本需要询问你确认的操作，在 `dontAsk` 模式下都不会弹出提示，而是直接拒绝。

在 `dontAsk` 模式下，只有两类操作可以执行：

1. 匹配 `permissions.allow` 的操作

例如：

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

```shell
npm test
pnpm lint
```

2. 只读Bash命令

一些不会修改系统或项目状态的 Bash 命令也可以执行，例如`ls`、`cat`、`pwd`、`grep`、`find`等。


显式的 `ask` 规则在 `dontAsk` 模式下不会触发提示，而是直接拒绝。

例如：

```JSON
{
  "permissions": {
    "ask": [
      "Bash(npm install)"
    ]
  }
}
```

在默认模式下，执行 `npm install` 会询问你；但在 `dontAsk` 模式下，它会被直接拒绝。

# 九、bypassPermissions 模式

`bypassPermissions` 是 Claude Code 中权限最宽松、风险最高的模式，它会禁用权限提示和安全检查，以便工具调用立即执行。

从 `v2.1.126` 开始，这也包括[[#^protected-path|受保护路径]]。更早版本对受保护路径仍然可能提示。

不过，针对**文件系统根目录或用户主目录的删除操作**仍然会触发提示，例如：

```shell
rm -rf /
rm -rf ~
```

这是为了防止模型错误造成灾难性后果。

官方建议只在隔离环境中使用该模式，例如：

- 容器
- 虚拟机
- 临时沙箱环境

不要在真实主机、重要项目或有敏感凭据的环境中随意使用。

你不能从一个普通会话中直接切换进 `bypassPermissions`。必须在启动时使用相关参数：

```shell
claude --permission-mode bypassPermissions
```

或者：

```shell
claude --dangerously-skip-permissions
```

`--dangerously-skip-permissions` 与 `--permission-mode bypassPermissions` 等效。

如果只是想让 `bypassPermissions` 出现在模式切换循环中，但不立即启用，可以使用：

```shell
claude --allow-dangerously-skip-permissions
```

在 Linux 和 macOS 上，`Claude Code` 不允许在 root 或 sudo 权限下启动 `bypassPermissions`，除非当前环境被识别为沙箱。管理员也可以通过 managed settings 禁用该模式：

```json
{
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  }
}
```

# 十、受保护的路径 ^protected-path 

在除 `bypassPermissions` 以外的所有模式下，对一小部分路径的写入永远不会被自动批准。这是为了防止意外破坏仓库状态、编辑器配置、shell 配置或 Claude Code 自身配置。

不同模式下的行为如下：

|模式|写入受保护路径时的行为|
|---|---|
|`default`|提示确认|
|`acceptEdits`|提示确认|
|`plan`|提示确认|
|`auto`|交给分类器判断|
|`dontAsk`|直接拒绝|
|`bypassPermissions`|允许|
受保护的目录包括：

- `.git`
- `.vscode`
- `.idea`
- `.husky`
- `.claude`（除了`.claude/commands`、`.claude/agents`、`.claude/skills`和`.claude/worktree`）

受保护的文件包括：

- `.gitconfig`、`.gitmodules`
- `.bashrc`、`.bash_profile`、`.zshrc`、`.zsh_profile`、`profile`
- `.ripgreprc`
- `.mcp.json`、`.claude.json`
