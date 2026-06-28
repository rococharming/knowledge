# 一、核心理念

> "One loop & Bash is all you need" — 一个工具 + 一个循环 = 一个 Agent。

`harness` 层最核心的东西就是一个**循环**：它是模型与真实世界的第一道连接。

把 `Claude Code` 拆到最本质的形态：

```text
Claude Code = 一个 agent loop
            + 工具（bash、read、write、edit、glob、grep、browser...）
            + 按需加载 skill
            + 上下文压缩
            + 启动 subagent
            + 带依赖图的任务系统
            + 用于团队协作的异步 mailbox
            + 基于 worktree 隔离的并行执行
            + 权限治理
            + hooks 扩展系统
            + 持久化 memory
            + MCP 外部能力路由
```

真正的 `agent` 本身是 `Claude` 模型或第三方模型。`harness` 没有让模型变聪明，因为模型本身已经很智能。`harness` 只是给了模型手、眼睛和一个可以工作的空间。

`agent loop` 是整个智能体运行的核心骨架。无论后面加入工具调用、权限控制、上下文压缩、知识加载、任务系统、子代理，底层都还是这个循环。

循环本身是 `agent`，叠加的各种机制属于 `harness`。==循环是固定的，会变化的是工具、知识、权限。==

```text
Agent = 模型(LLM) + 通用操作环境（Harness）
```

真正做判断的是模型，`harness`负责给模型提供可操作的环境，比如：

- **工具**：Bash、Read、Write、Edit 等
- **知识**：文档、规则、Skills 等
- **权限**：哪些文件能改、哪些命令要确认、哪些操作要禁止


# 二、为什么需要循环

你向大模型提了一个问题：

> "帮我读取下我的目录下有哪些文件"。

模型能输出一条 `bash` 命令，但输出完了就停了 —— 它不会自己跑，也不会看到结果后继续推理。

你可以手动跑一遍，把输出粘贴回对话框，让它接着干。下一个命令出来，你再跑一遍、再贴回去。

每一个来回，你都在做中间层。==而把这个手动来回自动化，就是这一节要做的事。==

没有这个循环时，模型只能给出命令；有了这个循环后，模型可以根据工具结果继续推理和行动。

# 三、解决方案

一个 `while True` 循环：模型调用工具就继续，不调用就停。整个过程只看`stop_reason`是否为`tool_use`：

| 信号 | 含义 | 循环动作 |
| --- | --- | --- |
| `stop_reason == "tool_use"` | 模型举手说"我要用工具" | 执行 → 结果喂回去 → 继续 |
| `stop_reason != "tool_use"` | 模型说"我做完了" | 退出循环 |

# 四、消息流

一次完整的交互可以理解为：

1. 用户输入任务，形成第一条 `user` 消息
2. `harness` 将历史消息、系统提示词和工具定义一起发给模型
3. 模型返回普通文本，或者返回 `tool_use` 块
4. 如果有 `tool_use`，`harness` 执行对应工具
5. `harness` 把工具输出包装成 `tool_result`，作为新的 `user` 消息追加到历史中
6. 回到第 2 步，直到模型不再调用工具

关键点：==工具结果不是直接打印给模型，而是作为对话历史的一部分回传。== 模型因此可以看到刚才命令执行后的真实结果。

![[Pasted image 20260628153353.png|500]]

# 五、Agent Loop 逐行理解

## 1、环境与客户端

先 `load_dotenv(override=True)` 把 `.env` 加载进进程环境变量，再从环境变量读取 Base URL、认证令牌（`auth_token`）和模型名，并做凭据校验：

```python
# 从 .env 文件解析键值对并加载进进程环境变量中
load_dotenv(override=True)

base_url = os.getenv("ANTHROPIC_BASE_URL")
auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
model = os.getenv("MODEL")

# 凭据校验
if not base_url:
    raise ValueError("缺少 ANTHROPIC_BASE_URL，请设置环境变量")
if not auth_token:
    raise ValueError("缺少 ANTHROPIC_AUTH_TOKEN， 请设置环境变量")
if not model:
    raise ValueError("缺少 MODEL，请设置环境变量")

# 用 auth_token 认证时，必须清除可能残留的 ANTHROPIC_API_KEY
# 否则 SDK 会同时发送 x-api-key 和 Authorization: Bearer，API 返回 401
os.environ.pop("ANTHROPIC_API_KEY", None)

# 构造一个客户端对象
client = Anthropic(
            base_url = base_url,
            auth_token = auth_token
       )
```

注意两点：

- 这里客户端用 `auth_token` 而不是 `api_key` 认证。两者对应不同请求头：`api_key` 走 `x-api-key`，`auth_token` 走 `Authorization: Bearer`。接兼容服务商通常用 Bearer Token。
- ==用 `auth_token` 认证时必须 `os.environ.pop("ANTHROPIC_API_KEY", None)` 清掉残留的 `ANTHROPIC_API_KEY`，否则 SDK 会同时发 `x-api-key` 和 `Authorization: Bearer`，API 校验冲突返回 401。==

支持 `ANTHROPIC_BASE_URL`，所以它不只绑定 Anthropic 官方服务，也可以接兼容服务商。

## 2、系统提示词

```python
# 定义系统提示词
system = f"你是一个工作在 {os.getcwd()} 的编码 Agent。使用 bash 来处理任务。执行，不做解释"
```

它把当前工作目录 `os.getcwd()` 嵌进提示词，并要求模型用 bash 行动。这是一个很强的行为约束：本课不是让模型解释方案，而是让模型真的通过工具完成任务。

## 3、工具定义

本课只有一个工具：`bash`。

```python
# 定义工具
tools = [{
    "name": "bash",
    "description": "Run a shell command.",
    "input_schema": {
        "type": "object",
        "properties": { "command": { "type": "string" } },
        "required": ["command"]
    }
}]
```

这是在定义"给模型看的工具说明书"。模型不会直接知道你的 Python 里有什么函数，所以要用这种 JSON-like 的格式告诉它：你可以调用一个叫 `bash` 的工具，调用时必须传什么参数。

- `"name": "bash"` —— 工具名。模型之后如果想用它，会生成一个 `tool_use`，里面的名字就是 `bash`。
- `"description": "Run a shell command."` —— 工具描述，给模型看的，帮助模型判断什么时候该用这个工具。
- `input_schema` —— 定义工具参数的结构。

`input_schema` 各字段含义：

- `"type": "object"` —— 调用 `bash` 时，输入必须是一个对象，例如 `{"command": "ls -la"}`。
- `"properties": {"command": {"type": "string"}}` —— 这个对象里允许有一个字段 `command`，它的值必须是字符串。
- `"required": ["command"]` —— `command` 是必填字段。模型不能只说"我要用 bash"，必须明确给出要执行的命令。

整体等价于告诉模型：

> 有一个工具叫 bash，它可以运行 shell 命令。调用它时，请传入一个对象，里面必须有字段 command，其值必须为字符串。

模型调用后，大概会返回类似这种内容：

```json
{
    "type": "tool_use",
    "id": "xxx",
    "name": "bash",
    "input": {
        "command": "ls -la"
    }
}
```

然后 Python 通过 `block.input["command"]` 拿到命令 `"ls -la"`，再执行 `run_bash("ls -la")`。

## 4、工具执行

`run_bash()` 做了四件事：

1. 拦截明显危险的命令片段，例如 `rm -rf /`、`sudo`、`shutdown`。
2. 用 `subprocess.run(..., shell=True)` 执行命令。
3. 捕获 stdout 和 stderr。
4. 对超时、无输出和系统错误做简单兜底。

```python
# Bash Tool Call
def run_bash(command: str):
    # 危险命令拦截
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"

    # 启动子进程执行命令，阻塞等待它结束
    # 返回一个 CompletedProcess 对象，里面封装了退出码、标准输出、标准错误
    try:
        r = subprocess.run(command, shell=True, cwd=os.getcwd(), capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout(120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"
```

==这是教学版的轻量保护，不是完整权限系统。==

## 5、循环主体

核心函数是 `agent_loop`：

```python
# Agent Loop
def agent_loop(messages: list):

    while True:
        # 向模型发送请求
        response = client.messages.create(
            max_tokens=8000,
            messages=messages,
            model=model,
            system=system,
            tools=tools
        )

        # 模型回复消息加入消息列表
        messages.append({"role": "assistant", "content": response.content})

        # 判断模型是否需要调用工具，即判断 stop_reason 属性是否是 `tool_use`
        if response.stop_reason != "tool_use":
            return

        # 执行每个工具调用，收集结果
        # content 是个列表，因为模型一轮回复可能由多个块组成（先思考、再说话、再调工具）。每个块都是带 type 字段的对象，常见三种：
        # 文本块：TextBlock(type='text', text='模型的回复文字')
        # 思考块（开启 thinking 时出现）：ThinkingBlock(type='thinking', thinking='...思考过程...')
        # 工具调用块：ToolUseBlock(type='tool_use', id='toolu_xxx', name='get_weather', input={'location': '北京'})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"\033[33m$ {block.input["command"]}\033[0m")
                output = run_bash(block.input["command"])
                print(output[:200])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output
                })

        # 将工具调用结果作为 user 信息追加到消息列表回送到模型
        messages.append( {"role": "user", "content": results} )
```

不到 30 行，这就是最小可运行的 agent harness 内核。它不是智能本身，而是让模型能持续行动的最小运行框架：模型负责决策（要不要调工具、调哪个），`harness` 负责执行（调了就跑、结果喂回去）。

### 参数 `messages` 的结构

`messages` 用于保存整个对话历史，例如：

```python
[
    {"role": "user", "content": "帮我查看当前目录"},
    {"role": "assistant", "content": ...},
    {"role": "user", "content": ...},
]
```

注意，`response.content` 不一定只是普通文本，也可能包含工具调用请求。例如模型想执行命令时，`response.content` 里可能包含：

```python
{
    "type": "tool_use",
    "name": "bash",
    "input": {
        "command": "ls"
    }
}
```

### `tool_result` 字段含义

将工具执行结果加入列表时，需要按照 Anthropic 工具调用协议组织：

```python
results.append({
    "type": "tool_result",
    "tool_use_id": block.id,
    "content": output,
})
```

| 字段 | 含义 |
| --- | --- |
| `"type": "tool_result"` | 表示这是工具执行结果 |
| `"tool_use_id": block.id` | 对应模型刚才发出的那个工具调用 ID |
| `"content": output` | 工具执行输出 |

其中 `tool_use_id` 很重要，它把某个工具结果和模型发出的某个工具调用对应起来。==模型一次可能请求多个工具调用，结果需要能准确匹配回去。==

## 6、入口交互

主程序维护一个 `history`：

```python
if __name__ == '__main__':
    print("s01: Agent Loop")
    print("输入问题，回车发送。输入 q 退出。\n")

    # 消息历史
    history = []

    while True:
        try:
            query = input("\033[36ms01 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break

        # 用户消息加入对话历史
        history.append({"role": "user", "content": query})

        # 执行 Agent Loop
        agent_loop(history)

        # 打印模型的最后一个文本消息
        # 模型会生成内容块列表，例如
        # TextBlock(
        #    type='text'
        #    text="xxxxxx"
        # )
        response_content = history[-1]["content"]
        if isinstance(response_content, list):
            for block in response_content:
                if getattr(block, "type", None) == "text":
                    print(block.text)

        print()
```

这里 `history` 贯穿整个 REPL 循环，每次用户输入都追加到同一个历史里：

```python
history.append({"role": "user", "content": query})
agent_loop(history)
```

这意味着同一进程内的多轮输入共享上下文。用户上一轮让模型创建的文件、查询过的信息、模型回答过的内容，都可能影响下一轮。`agent_loop` 结束后，再用 `history[-1]["content"]` 取出模型最后一轮回复，遍历其中的文本块打印给用户。

# 六、观察现象

运行时重点看两个现象：

1. 模型何时选择调用 `bash`。
2. 工具输出回来后，模型如何决定下一步。

例如：

```text
创建一个名为 hello.py 的文件并打印 Hello, world!
```

模型通常会先调用 bash 创建文件，可能再读取或运行它验证，然后才停止。

再比如：

```text
当前的 Git 分支是什么？
```

模型会调用类似 `git branch --show-current` 的命令，拿到结果后用自然语言回答。

# 七、回顾问题

学完本课后，应该能回答：

1. 为什么只让模型输出命令还不算 agent？

   因为模型输出完命令就停了——它不会自己执行，也看不到结果后继续推理。你必须手动跑命令、再把输出粘贴回对话框，每一轮都充当"中间层"。==把这个"输出命令 → 执行 → 结果喂回去 → 继续推理"的来回自动化，才形成闭环。== 所以"只输出命令"只是单次生成，缺少让模型根据工具结果持续行动的循环，不算 agent。

2. `tool_use` 和 `tool_result` 分别表示什么？

   - `tool_use`：模型回复中的一个工具调用块（`type='tool_use'`），包含 `name` 和 `input`，表示模型"举手说我要用工具"。
   - `tool_result`：`harness` 执行工具后，把输出包装成的结果块（`type='tool_result'`），通过 `tool_use_id` 对应回模型刚才发出的那个工具调用，作为新的 `user` 消息回传。

3. 为什么工具结果要追加回 `messages`？

   因为==工具结果不是直接打印给模型，而是作为对话历史的一部分回传。== 只有追加到 `messages`，模型才能在下一轮看到命令执行后的真实结果，并据此继续推理。这是闭环成立的关键——没有这一步，模型就无法感知自己行动的后果。

4. `stop_reason` 在这个教学实现里起什么作用？

   它是循环的退出信号：`stop_reason == "tool_use"` 表示模型还要继续调工具，循环继续执行；`stop_reason != "tool_use"` 表示模型"做完了"，`return` 退出循环。==整个循环只靠这一个信号决定继续还是停止。==

5. `harness` 和模型的职责边界是什么？

   - **模型**：负责决策——要不要调工具、调哪个、传什么参数。
   - **harness**：负责执行——调了就跑、把结果喂回去、维护消息历史、提供工具/知识/权限。

   `harness` 没有让模型变聪明，模型本身已经很智能；`harness` 只是给了模型手、眼睛和一个可工作的空间。真正的判断在模型，环境在 `harness`。

6. 为什么本课的 bash 工具需要后续权限系统补强？

   本课的危险命令拦截只是==教学版的轻量保护==，靠字符串匹配 `rm -rf /`、`sudo`、`shutdown` 等片段，既不完整也无法覆盖所有危险操作。而 `bash` 能执行任意 shell 命令，真实场景需要细粒度权限治理：哪些文件能改、哪些命令要确认、哪些操作要禁止。所以必须用后续的权限系统补强。

> [!note] 本课定位
> 后面 18 个章节都在这个循环上叠加机制，循环本身始终不变。
