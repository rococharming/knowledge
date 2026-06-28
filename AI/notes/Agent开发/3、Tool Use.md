# 一、核心理念

> "加一个工具，只加一个 handler" — 循环不用动，新工具注册进 dispatch map 就行。

[[2、Agent Loop]] 的 `while True` 循环已经让模型能持续行动，但它只配了一个 `bash` 工具：读文件要 `cat`，写文件要 `echo "..." > file.py`，改文件要 `sed`。模型想的是"读这个文件"，却要拼出 `cat path/to/file` —— 多了一层翻译，浪费 token，还容易拼错。

本课要做的事是：在循环完全不动的前提下，把工具数量从 1 扩到 5。==循环是固定的，会变化的是工具、知识、权限。== 这正是 [[1、Agent Harness]] 里那张拆解图的第二行——"工具（bash、read、write、edit、glob、grep、browser...）"。

`harness` 层在这一节的核心是**工具分发**：扩展模型能触达的边界。给 Agent 加一个工具只需要做两件事：

1. **定义工具**：在 `tools` 列表里加一条描述（告诉模型"我能做什么"）
2. **注册处理函数**：在 `tools_handlers` 字典里加一个映射（告诉 harness"该怎么跑"）

# 二、为什么需要专用工具

只有 bash 一个工具时，每个操作都要模型先把意图翻译成 shell 命令：

| 模型的意图 | bash 里的翻译 | 问题 |
| --- | --- | --- |
| 读文件 | `cat path/to/file` | 多一层翻译，浪费 token |
| 写文件 | `echo "..." > file.py` | 引号、转义、换行容易拼错 |
| 改文件 | `sed -i 's/old/new/' file` | 语法晦涩，跨平台行为不一 |
| 找文件 | `find . -name "*.py"` | 参数多，模型可能记错 |

问题不在于"bash 做不到"，而在于**让模型直接表达意图更省 token、更不易出错**。`read_file` 直接告诉模型"你给路径，我给你内容"，模型不用再考虑怎么拼命令。

专用工具的另一个价值是**安全边界可控**。bash 能跑任意 shell 命令，而 `read_file` / `write_file` 这种受限工具可以在 handler 里做路径校验（见 `safe_path`），把"能做什么"收窄到"读/写工作区内的文件"。

# 三、解决方案

循环完全保留（LLM 调用、`stop_reason` 判断、消息追加）。唯一的变动在工具执行那几行：硬编码的 `run_bash()` 替换为 `tools_handlers[block.name](**block.input)` 查表分发。

```python
# 之前（硬编码）
output = run_bash(block.input["command"])

# 现在（查表）
handler = tools_handlers.get(block.name)    # 根据工具名映射要调用的工具函数
output = handler(**block.input) if handler else f"Unknown tool: {block.name}"
```

`**block.input` 是关键：模型在 `tool_use` 里返回的 `input` 字典，正好是 handler 函数的参数。`read_file` 的 handler 签名是 `run_read(path, limit=None)`，模型返回 `{"path": "README.md", "limit": 10}`，`**block.input` 就把它展开成 `run_read(path="README.md", limit=10)`。==工具名 → handler 的映射让分发变成一次查表，参数传递靠 `**` 解包自动完成。==

# 四、完整代码

以下是本课的完整实现。它等于 Agent Loop 那一课的全部代码，再叠加：4 个新工具函数、`tools_handlers` 分发映射、`safe_path` 路径安全校验。==循环本身（`agent_loop`）与上一课完全一致，只改了工具执行那几行。==

```python
#!/usr/bin/env python3

import os
import subprocess
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

try:
    import readline
    # macOS 的 libedit 在处理中文输入时有退格问题，这四行修复它
    readline.parse_and_bind('set bind-tty-special-chars off')
    readline.parse_and_bind('set input-meta on')
    readline.parse_and_bind('set output-meta on')
    readline.parse_and_bind('set convert-meta off')
except ImportError:
    pass


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

# 当前工作目录
work_dir = Path.cwd()

# 构造一个客户端对象
client = Anthropic(
            base_url = base_url,
            auth_token = auth_token
       )

# 定义系统提示词
system = f"你是一个工作在 {work_dir} 的编码 Agent。使用 bash 来处理任务。执行，不做解释"

# 定义工具列表
tools = [
    {
        "name": "bash",
        "description": "Run a shell command.",
        "input_schema": {
            "type": "object",
            "properties": { "command": { "type": "string" } },
            "required": ["command"]
        }
    },
    {
        "name": "read_file",
        "description": "Read file content.",
        "input_schema": {
            "type": "object",
            "properties": { "path": { "type": "string" }, "limit": { "type": "integer" } },
            "required": ["path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file.",
        "input_schema": {
            "type": "object",
            "properties": { "path": {"type": "string"}, "content": {"type": "string"} },
            "required": ["path", "content"]
        }
    },
    {
        "name": "edit_file",
        "description": "Replace exact text in a file once.",
        "input_schema": {
            "type": "object",
            "properties": { "path": {"type": "string"}, "old_text": {"type": "string"}, "new_text": { "type": "string" } },
            "required": ["path", "old_text", "new_text"]
        }
    },
    {
        "name": "glob",
        "description": "Find files matching a glob pattern.",
        "input_schema": {
            "type": "object",
            "properties": { "pattern": {"type": "string" } },
            "required": ["pattern"]
        }
    }
]



# Bash 工具函数
def run_bash(command: str) -> str:
    # 危险命令拦截
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"

    # 启动子进程执行命令，阻塞等待它结束
    # 返回一个 CompletedProcess 对象，里面封装了退出码、标准输出、标准错误
    try:
        r = subprocess.run(command, shell=True, cwd=work_dir, capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout(120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"

# 确保传入路径位于工作目录下，挡住一切越界访问
def safe_path(p: str) -> Path:
    path = (work_dir / p).resolve()  # 拼接并解析成绝对路径
    if not path.is_relative_to(work_dir):
        raise ValueError(f"Path escapes workspace: {p}")
    return path

# Read 工具函数
def run_read(path: str, limit: int | None = None) -> str:
    try:
        lines = safe_path(path).read_text().splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"...({len(lines) - limit} more lines)"]
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


# Write 工具函数
def run_write(path: str, content: str) -> str:
    try:
        file_path = safe_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True) # 自动创建父目录
        file_path.write_text(content)  # 覆盖写入内容
        return f"Wrote {len(content.encode())} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"

# Edit 工具函数
def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        file_path = safe_path(path)
        text = file_path.read_text()
        if old_text not in text:
            return f"Error: text not found in {path}"
        file_path.write_text(text.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"

# Glob 工具函数
def run_glob(pattern: str) -> str:
    import glob as g
    try:
        results = []
        # 将工作目录作为根目录匹配 pattern，但 glob 函数本身不做越界防护:pattern 里若含 .. 或绝对路径片段,glob 仍可能返回工作区之外的路径。
        # 因此这里需要校验
        for match in g.glob(pattern, root_dir=work_dir):
            if (work_dir / match).resolve().is_relative_to(work_dir):
                results.append(match)
        return "\n".join(results) if results else "(no matches)"
    except Exception as e:
        return f"Error: {e}"

# 工具分发映射
tools_handlers = {
    "bash": run_bash,
    "read_file": run_read,
    "write_file": run_write,
    "edit_file": run_edit,
    "glob": run_glob,
}


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
                print(f"\033[33m$ {block.name}\033[0m")
                handler = tools_handlers.get(block.name)    # 根据工具名映射要调用的工具函数
                output = handler(**block.input) if handler else f"Unknown tool: {block.name}"
                print(str(output)[:200])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,   # tool_result 的 id 与 tool_use 的 id 一一对应
                    "content": output
                })

        # 将工具调用结果作为 user 信息追加到消息列表回送到模型
        messages.append( {"role": "user", "content": results} )

if __name__ == '__main__':
    print("s02: Tool Use — 在 s01 的基础上加了 4 个工具")
    print("输入问题，回车发送。输入 q 退出。\n")

    # 消息历史
    history = []

    while True:
        try:
            query = input("\033[36ms02 >> \033[0m")
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

# 五、逐段理解

## 1、环境与客户端

本课复用 [[2、Agent Loop#1、环境与客户端]] 的全部配置，只在它之上叠加新工具。要点回顾：

```python
load_dotenv(override=True)

base_url = os.getenv("ANTHROPIC_BASE_URL")
auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
model = os.getenv("MODEL")

# 用 auth_token 认证时，必须清除可能残留的 ANTHROPIC_API_KEY
# 否则 SDK 会同时发送 x-api-key 和 Authorization: Bearer，API 返回 401
os.environ.pop("ANTHROPIC_API_KEY", None)

work_dir = Path.cwd()

client = Anthropic(
            base_url = base_url,
            auth_token = auth_token
       )

system = f"你是一个工作在 {work_dir} 的编码 Agent。使用 bash 来处理任务。执行，不做解释"
```

两点与上一课一致、本课仍成立：

- 客户端用 `auth_token`（走 `Authorization: Bearer`）而非 `api_key`（走 `x-api-key`）。==用 `auth_token` 认证时必须 `os.environ.pop("ANTHROPIC_API_KEY", None)` 清掉残留的 `ANTHROPIC_API_KEY`，否则两个头同时发，API 校验冲突返回 401。==
- `work_dir = Path.cwd()` 把当前工作目录固化下来，后续所有 file tools 都以它为根做路径校验。

## 2、工具定义

`tools` 列表从 1 条扩到 5 条，每条都是同一个结构：

```python
tools = [
    { "name": "bash",       "description": "Run a shell command.",            "input_schema": {...} },
    { "name": "read_file",  "description": "Read file content.",              "input_schema": {...} },
    { "name": "write_file", "description": "Write content to a file.",        "input_schema": {...} },
    { "name": "edit_file",  "description": "Replace exact text in a file once.", "input_schema": {...} },
    { "name": "glob",       "description": "Find files matching a glob pattern.", "input_schema": {...} },
]
```

每条定义都在回答两个问题，与 [[2、Agent Loop#3、工具定义]] 的约定一致：

- **`name` + `description`**：给模型看的"工具说明书"。模型据此判断什么时候该用哪个工具。
- **`input_schema`**：定义工具参数的结构。`required` 标出必填字段。

对比只有 bash 时，这里多出来的只是 4 条同结构的描述——==加一个工具 = 在 `tools` 列表加一条==，循环、消息流、`stop_reason` 判断都没动。

## 3、Bash 工具函数

`run_bash` 与上一课完全一致——危险命令拦截 + `subprocess.run` 执行 + 兜底，此处不再展开。详见 [[2、Agent Loop#4、工具执行]]。

```python
def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        r = subprocess.run(command, shell=True, cwd=work_dir, capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout(120s)"
    except (FileNotFoundError, OSError) as e:
        return f"Error: {e}"
```

## 4、路径安全：safe_path

file tools（`read` / `write` / `edit` / `glob`）都经过 `safe_path` 校验，它是本课新引入的防线：

```python
def safe_path(p: str) -> Path:
    path = (work_dir / p).resolve()  # 拼接并解析成绝对路径
    if not path.is_relative_to(work_dir):
        raise ValueError(f"Path escapes workspace: {p}")
    return path
```

它做了两件事：

1. 把相对路径解析成绝对路径：`work_dir / p` 再 `.resolve()`，处理掉 `..` 和软链接。
2. 校验结果仍在工作区内：`is_relative_to(work_dir)`。如果模型传 `../../etc/passwd`，解析后会跳出 `work_dir`，直接抛错。

==这是把"能做什么"收窄到"只能动工作区内的文件"的最小实现。== 注意它只保护 file tools，`bash` 不受此限制——这正是本课留给下一课的缺口。

## 5、Read 工具函数

```python
def run_read(path: str, limit: int | None = None) -> str:
    try:
        lines = safe_path(path).read_text().splitlines()
        if limit and limit < len(lines):
            lines = lines[:limit] + [f"...({len(lines) - limit} more lines)"]
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
```

`limit` 超出时追加 `...(N more lines)` 提示，让模型知道文件被截断了——否则模型可能以为读到的是完整文件，基于不完整内容下结论。

## 6、Write 工具函数

```python
def run_write(path: str, content: str) -> str:
    try:
        file_path = safe_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True) # 自动创建父目录
        file_path.write_text(content)  # 覆盖写入内容
        return f"Wrote {len(content.encode())} bytes to {path}"
    except Exception as e:
        return f"Error: {e}"
```

两点：

- `file_path.parent.mkdir(parents=True, exist_ok=True)` 自动创建父目录——模型写 `src/new/mod.py` 时不用先 `mkdir`。
- 返回字节数用 `len(content.encode())` 而不是 `len(content)`。==中文字符串里 `len` 数的是字符数，`encode()` 后才是真实写入的字节数==。这是给模型一个准确的反馈，避免它对文件大小产生误判。

## 7、Edit 工具函数

```python
def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        file_path = safe_path(path)
        text = file_path.read_text()
        if old_text not in text:
            return f"Error: text not found in {path}"
        file_path.write_text(text.replace(old_text, new_text, 1))
        return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"
```

两个设计：

- `old_text not in text` 先做存在性检查，找不到时返回明确的 `text not found`，==而不是静默地什么都不改==。这让模型能立刻发现"我想改的片段不在文件里"，重新读取文件确认。
- `str.replace(old_text, new_text, 1)`，==第三个参数 `1` 表示只替换第一处==。这避免了一个 `old_text` 在文件里多次出现时被批量改掉——精确编辑是 `edit_file` 区别于 `sed` 的核心价值。

## 8、Glob 工具函数

```python
def run_glob(pattern: str) -> str:
    import glob as g
    try:
        results = []
        # 将工作目录作为根目录匹配 pattern，但 glob 函数本身不做越界防护:pattern 里若含 .. 或绝对路径片段,glob 仍可能返回工作区之外的路径。
        # 因此这里需要校验
        for match in g.glob(pattern, root_dir=work_dir):
            if (work_dir / match).resolve().is_relative_to(work_dir):
                results.append(match)
        return "\n".join(results) if results else "(no matches)"
    except Exception as e:
        return f"Error: {e}"
```

这里的注释点出一个容易被忽略的细节：`g.glob(pattern, root_dir=work_dir)` 虽然以 `work_dir` 为根，但==`pattern` 里若含 `..` 或绝对路径片段，`glob` 仍可能返回工作区之外的路径==。所以拿到每个 `match` 后还要再 `resolve()` + `is_relative_to` 校验一次，把越界结果过滤掉。

## 9、工具出错的处理方式

每个函数都用 `try/except` 兜底，把异常转成字符串返回。==工具出错不是抛异常打断循环，而是作为 `tool_result` 喂回模型，让模型自己决定下一步==——读不到就换路径，找不到文本就先读文件确认。这与 [[2、Agent Loop]] 的消息流一致：循环只看 `stop_reason`，不被工具异常干扰。

## 10、工具分发

`tools_handlers` 是工具名 → 处理函数的字典：

```python
tools_handlers = {
    "bash": run_bash,
    "read_file": run_read,
    "write_file": run_write,
    "edit_file": run_edit,
    "glob": run_glob,
}
```

循环里只改了一行——从硬编码 `run_bash` 变成查表：

```python
for block in response.content:
    if block.type == "tool_use":
        print(f"\033[33m$ {block.name}\033[0m")
        handler = tools_handlers.get(block.name)    # 根据工具名映射要调用的工具函数
        output = handler(**block.input) if handler else f"Unknown tool: {block.name}"
        print(str(output)[:200])
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,   # tool_result 的 id 与 tool_use 的 id 一一对应
            "content": output
        })
```

两处细节：

- `tools_handlers.get(block.name)` 用 `.get` 而不是 `[]`：模型可能返回一个没注册的工具名，`.get` 返回 `None`，落到 `else` 分支返回 `Unknown tool: ...`，循环不会因 `KeyError` 崩掉。
- `handler(**block.input)`：模型返回的 `input` 字典直接解包成函数参数，==前提是 handler 的签名与 `input_schema` 的字段名严格对齐==。这就是为什么前面强调"签名与 schema 一一对应"。

> [!note] 加工具的代价
> ==加一个工具 = 在 `tools` 列表加一条 + 在 `tools_handlers` 字典加一行映射。== 循环不变，`agent_loop` 一行都没改。这种"定义与实现分离 + 查表分发"的结构，是后续叠加权限、钩子、并发的前提——分发点只有一个，所有机制都挂在这个点上。

## 11、多个工具调用

模型经常一次返回多个 `tool_use`，例如"读一下 `a.py` 和 `b.py`，然后列出所有 `.py` 文件"。`response.content` 是一个列表，模型一轮回复可以包含多个工具调用块，按原始顺序逐个执行：

```python
for block in response.content:
    if block.type == "tool_use":
        handler = tools_handlers.get(block.name)    # 根据工具名映射要调用的工具函数
        output = handler(**block.input) if handler else f"Unknown tool: {block.name}"
        ...
        results.append({
            "type": "tool_result",
            "tool_use_id": block.id,   # tool_result 的 id 与 tool_use 的 id 一一对应
            "content": output
        })
```

每个 `tool_use` 块都有自己的 `block.id`，对应的 `tool_result` 用同一个 `tool_use_id` 回传。==模型一次可能请求多个工具调用，结果需要靠 `tool_use_id` 准确匹配回去。== 这一点和 [[2、Agent Loop#tool_result 字段含义]] 完全一致——本课只是工具多了，匹配机制没变。

教学版按 `response.content` 原始顺序逐个执行，不做并发。CC 的做法更复杂，见下文「深入 CC 源码」。

## 12、入口交互

主程序维护一个 `history`，与上一课的 REPL 结构一致：

```python
if __name__ == '__main__':
    print("s02: Tool Use — 在 s01 的基础上加了 4 个工具")
    print("输入问题，回车发送。输入 q 退出。\n")

    history = []

    while True:
        try:
            query = input("\033[36ms02 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break

        history.append({"role": "user", "content": query})
        agent_loop(history)

        response_content = history[-1]["content"]
        if isinstance(response_content, list):
            for block in response_content:
                if getattr(block, "type", None) == "text":
                    print(block.text)

        print()
```

`history` 贯穿整个 REPL 循环，同一进程内的多轮输入共享上下文。`agent_loop` 结束后，用 `history[-1]["content"]` 取出模型最后一轮回复，遍历其中的文本块打印给用户。详见 [[2、Agent Loop#6、入口交互]]。

# 六、相对上一课的变更

| 组件 | 之前 | 之后 |
| --- | --- | --- |
| 工具数量 | 1（bash） | 5（+read、write、edit、glob） |
| 工具执行 | 硬编码 `run_bash()` | `tools_handlers` 查表分发 |
| 路径安全 | 无 | `safe_path` 校验（仅 file tools） |
| 多工具调用 | 单工具 | 模型可一次返回多个 `tool_use`，按原始顺序逐个执行 |
| 循环 | `while True` + `stop_reason` | 完全一致 |

# 七、观察现象

运行：

```bash
cd learn-claude-code
python s02_tool_use/code.py
```

试试这些 prompt：

```text
Read the file README.md and tell me what this project is about
Create a file called test.py that prints "hello", then read it back
Find all Python files in this directory
Read both README.md and requirements.txt, then create a summary file
```

观察重点：

1. **模型什么时候只调一个工具，什么时候一次调多个？** 像"读 A 和读 B"这种独立操作，模型倾向于一轮里塞多个 `tool_use`；而"创建后读回"这种有依赖的，会分多轮。
2. **多个工具调用的顺序和结果是否正确？** 每个 `tool_result` 是否对应到正确的 `tool_use_id`。
3. **专用工具 vs bash 的选择：** 模型更愿意用 `read_file` 还是 `bash cat`？专用工具是否让响应更短、更准。
4. **`safe_path` 的拦截：** 让模型读 `../xxx` 看它是否被挡在工作区外。

# 八、回顾问题

学完本课后，应该能回答：

1. 为什么本课加工具时"循环不用动"？

   因为循环只做三件事：调模型、判断 `stop_reason`、追加消息。工具执行只是循环里的一行 `output = ...`。本课把这一行从硬编码 `run_bash()` 换成 `tools_handlers[block.name](**block.input)` 查表分发，==分发点只有一个，新工具只要进 `tools` + `tools_handlers` 两张表就能被调用，循环结构本身一行没改。==

2. `tools_handlers` 和 `tools` 各自的职责是什么？

   - **`tools`**：给模型看的"工具说明书"——告诉模型有哪些工具、各自的参数 schema。模型据此生成 `tool_use`。
   - **`tools_handlers`**：给 harness 用的"实现映射"——工具名 → 处理函数。模型生成 `tool_use` 后，harness 用它查出该跑哪个函数。

   ==定义（`tools`）与实现（`tools_handlers`）分离，加工具就是两边各加一条。==

3. `handler(**block.input)` 为什么能自动完成参数传递？

   因为 handler 函数的签名与 `input_schema` 的字段名严格对齐。`run_read(path, limit=None)` 对应 schema 里的 `path` / `limit`；模型返回 `input = {"path": "...", "limit": 10}`，`**block.input` 把字典展开成关键字参数 `run_read(path="...", limit=10)`。==前提是名字对得上，否则会 `TypeError`。==

4. `safe_path` 防的是什么？为什么 bash 不受它保护？

   `safe_path` 防的是路径穿越——模型传 `../../etc/passwd` 这类相对路径，`resolve()` 后跳出 `work_dir`，`is_relative_to` 校验失败抛错。它把 file tools 的能力收窄到"工作区内"。bash 不受保护是因为它执行的是任意 shell 命令，路径校验对 `cat /etc/passwd` 这种命令无能为力——==bash 的安全治理要靠下一课的权限系统，不是路径校验。==

5. 模型一次返回多个 `tool_use` 时，结果怎么对应回去？

   每个 `tool_use` 块带唯一的 `block.id`，harness 把每个工具的输出包装成 `tool_result`，用同一个 `tool_use_id` 标记。模型下一轮通过 `tool_use_id` 把结果和调用一一对应，==即使一轮里调了 5 个工具也不会串台。==

6. 为什么本课仍需要后续权限系统补强？

   file tools 受 `safe_path` 保护，但 bash 能执行任意 shell 命令，`rm -rf /` 在危险命令字符串黑名单漏网时仍能跑。==`safe_path` 是工具内的自我约束，bash 没有这种约束==。真实场景需要在工具执行之前加一道统一的门：哪些操作安全、哪些要用户批准、哪些禁止——这就是 Permission 要做的事。

> [!note] 本课定位
> 工具分发点建立后，后续所有机制（权限、钩子、并发、流式执行）都挂在这个分发点上。下一课 Permission → 在工具执行之前加一道门：这个操作安全吗？需要用户批准吗？

# 九、深入 CC 源码

> 以下基于 CC 源码 `Tool.ts`、`tools.ts`、`toolOrchestration.ts`、`toolExecution.ts`、`StreamingToolExecutor.ts` 的核查。教学版为了概念清晰做了简化，这里对照生产级实现，看清省略了什么。

## 1、工具定义方式

| | 教学版 | CC |
| --- | --- | --- |
| 定义 | `tools` 列表（JSON Schema） | `buildTool()` 创建的独立对象 |
| 实现 | `tools_handlers` 字典（函数） | 工具对象内含 schema + 验证 + 权限 + 执行 |
| 汇总 | 手写列表 | `getAllBaseTools()` 自动汇总 |

教学版的"定义与实现分开"对教学更清晰——读者一眼看到"加一个工具 = 两条定义"。CC 把它们揉进一个对象，代价是单个工具更重，好处是 schema、验证、权限、执行在同一个地方声明，不会漏掉某一项。

## 2、并发安全判断：isConcurrencySafe()

教学版按原始顺序逐个执行，不做并发。CC 用 `isConcurrencySafe(input)` 判断能否并发——==注意这不是简单的"只读 vs 写"，而是按具体输入判断==：

| | isReadOnly | isConcurrencySafe |
| --- | --- | --- |
| FileRead | true | true |
| Glob | true | true |
| Bash `ls` | true | **true** ← 关键差异 |
| Bash `rm` | false | false |
| TaskCreate | false | **true** ← 改状态但可并发 |

CC 的 Bash tool 的 `isConcurrencySafe` 等于 `isReadOnly`——只读命令可并发，写命令不可。TaskCreate 虽然改了任务文件，但每次都写不同的文件，所以可以并发。=="是否改状态"和"能否并发"是两回事，CC 按输入精细判断。==

## 3、分区算法

CC 的 `partitionToolCalls()`（`toolOrchestration.ts:91-115`）不是简单分两组，而是把工具调用**按连续块分批**：

```text
[read A, read B, glob *.py, bash "rm x", read C]
  → batch1(并发): [read A, read B, glob *.py]
  → batch2(串行): [bash "rm x"]
  → batch3(并发): [read C]
```

并发安全的连续块编入同一个 batch，batch 内真正并发执行（`toolOrchestration.ts:152-176`，有并发上限）。遇到非并发安全的就开新 batch 串行执行。==batch 之间严格顺序，batch 内尽量并发。== 教学版省略了这一切，逐个串行执行——目标是先讲清楚分发，不追求性能。

## 4、验证管线

CC 的每个工具调用经过严格的 5 步验证（`toolExecution.ts`）：

1. **Zod schema 验证**（`614-680`，教学版用 JSON Schema 替代）：参数类型/结构检查
2. **工具级 `validateInput()`**（`682-733`）：参数值验证（如路径是否在工作区内）
3. **PreToolUse hooks**（`800-862`）：钩子可以返回消息、修改输入、阻止执行
4. **权限检查**（`921-931`，下一课的核心内容）：`canUseTool` + `checkPermissions` → allow/deny/ask
5. **执行 `tool.call()`**（`1207-1222`）

教学版省略了 Zod（用 JSON Schema）、省略了 `validateInput`（用 `safe_path` 安全函数）、保留了权限检查和钩子的概念。==教学版的 `safe_path` 大致对应第 2 步的简化版，但 CC 的验证是分层管线，每一层都能拦截。==

## 5、流式工具执行

CC 的 `StreamingToolExecutor`（`StreamingToolExecutor.ts`）让工具在模型还在生成时就启动——不等模型说完。`read_file` 可能在模型还在输出"我来分析"的时候就跑完了。教学版不实现这个，目标与上一课一致——概念清晰，不追求性能极致。

> [!tip] 速查
>
> | 概念 | 一句话 |
> | --- | --- |
> | `tools_handlers` | 工具名 → 处理函数的字典。加工具 = 加一行映射 |
> | 工具定义 | 告诉模型"我能做什么"的 JSON schema |
> | 多工具调用 | 模型可一次返回多个 `tool_use`，按原始顺序逐个执行 |
> | 循环不变 | `while True` 循环一行都没改 |
> | `safe_path` | file tools 的路径穿越防线；bash 不受其保护 |
> | `isConcurrencySafe` | CC 按具体输入判断能否并发，不是简单的只读 vs 写 |
> | 分区算法 | 连续并发安全块编入同一 batch，batch 内并发、batch 间串行 |
