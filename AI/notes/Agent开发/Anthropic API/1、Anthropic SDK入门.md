---
title: Anthropic SDK入门
date: 2026-06-11
tags: [AI, Agent, Anthropic]
aliases:
  - Anthropic SDK入门
  - AnthropicSDK入门
---

# 一、Anthropic SDK简介

Anthropic API 是 Anthropic 提供给开发者的 HTTP 接口，用来在程序中调用 Claude 模型。开发者可以通过 API 发送请求，将用户消息、模型名称、可用工具、最大输出长度等参数传给模型，然后获取模型生成的响应。

Anthropic 提供了 Python 实现的 Anthropic SDK 客户端库，用来在程序中调用 Anthropic Messages API。它封装了底层 HTTP 请求、鉴权、请求参数、响应对象等细节，使得开发者不需要手动拼接请求地址、请求头和 JSON 数据。

如果某个第三方模型服务兼容 Anthropic 的 Messages API 格式，也可以继续使用该 SDK，只需要将`base_url`和`api_key`改成对应服务商提供的地址和密钥即可。

# 二、环境准备

## 1、Python 版本要求

先确认本地 Python 版本：

```shell
python3 --version
```

建议使用 Python `3.7.1` 及以上版本。

## 2、安装依赖包

本次示例需要安装两个依赖：

```shell
pip install anthropic
pip install python-dotenv
```

| 依赖              | 作用                                           |
| --------------- | -------------------------------------------- |
| `anthropic`     | Anthropic Python SDK，用来创建客户端并调用 Messages API |
| `python-dotenv` | 读取 `.env` 文件，把其中的配置加载到环境变量中                  |

# 三、API Key与环境变量配置

## 1、获取API Key

本示例使用第三方平台 Kimi 为例，从 Kimi 开发者平台复制 API Key 备用。

密钥属于敏感信息，不能直接写死在代码里，也不要提交到 Git 仓库。更合适的方式是放入 `.env` 文件，再通过环境变量读取。


## 2、创建.env文件

在项目根目录创建`.env`文件：

```env
ANTHROPIC_BASE_URL=https://api.kimi.com/coding/
ANTHROPIC_API_KEY=你的kimi-api-key
MODEL_ID=kimi-for-coding
```

| 配置项                  | 说明                                           |
| -------------------- | -------------------------------------------- |
| `ANTHROPIC_BASE_URL` | API 请求的基础地址，用来把 Anthropic SDK 的请求发送到 Kimi 接口 |
| `ANTHROPIC_API_KEY`  | Kimi 或第三方服务商提供的 API Key                      |
| `MODEL_ID`           | 要调用的模型名称，例如 `kimi-for-coding`，具体以服务商文档为准     |

`ANTHROPIC_BASE_URL` 是关键配置。没有显式设置 `base_url` 时，`anthropic` SDK 会默认请求 Anthropic 官方接口；这里需要把请求地址改成 Kimi 的兼容接口地址。


# 四、加载配置并创建客户端

```python
from dotenv import load_dotenv
from anthropic import Anthropic
import os

# 读取项目根目录下的 `.env` 文件，并把配置加载到环境变量中
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")   # 从环境变量中读取 API Key
base_url = os.getenv("ANTHROPIC_BASE_URL")   # 从环境变量中读取 API 请求地址
model = os.getenv("MODEL_ID")                # 从环境变量中读取模型名称


# 创建 Anthropic SDK 客户端
client = Anthropic(
    base_url=base_url,
    api_key=api_key,
)
```

`Anthropic` 构造函数中的两个参数需要特别注意：

```python
client = Anthropic(
    base_url=base_url,
    api_key=api_key,
)
```

|参数|说明|
|---|---|
|`base_url`|请求发送到哪里。这里传入 Kimi 的接口地址|
|`api_key`|请求使用哪个密钥鉴权。这里传入 Kimi 的 API Key|

`anthropic` SDK 可以从环境变量中自动读取 `ANTHROPIC_API_KEY`，但 `base_url` 建议显式传入，否则容易把请求发到默认服务地址。

# 五、发送第一条消息

```python
response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "你好"}
    ]
)

print(response.content[0].text)
```

`client.messages.create()` 用来创建一次 Messages API 请求。它会把用户消息发送给指定模型，并返回模型生成的响应对象。

常用参数如下：

| 参数           | 说明                            |
| ------------ | ----------------------------- |
| `model`      | 要调用的模型名称，例如 `kimi-for-coding` |
| `max_tokens` | 限制本次响应最多生成多少 token            |
| `messages`   | 对话消息列表，用来描述用户输入和历史上下文         |

`messages` 是一个列表，每个元素表示一条消息：

```python
{"role": "user", "content": "你好"}
```

| 字段        | 说明                             |
| --------- | ------------------------------ |
| `role`    | 消息角色，常见值是 `user` 和 `assistant` |
| `content` | 消息内容，可以是一段文本，也可以在更复杂场景中使用结构化内容 |

返回值 `response` 是 SDK 封装后的响应对象。普通文本响应通常可以这样读取：

```python
print(response.content[0].text)
```

其中：

|表达式|含义|
|---|---|
|`response.content`|模型返回的内容块列表|
|`response.content[0]`|第一个内容块|
|`response.content[0].text`|第一个文本内容块中的文本|

# 六、完整示例

```python
from dotenv import load_dotenv
from anthropic import Anthropic
import os

load_dotenv()

client = Anthropic(
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

MODEL = os.getenv("MODEL_ID")

response = client.messages.create(
    model=MODEL,
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "给我讲个笑话，并打印结果"}
    ]
)

print(response.content[0].text)

```