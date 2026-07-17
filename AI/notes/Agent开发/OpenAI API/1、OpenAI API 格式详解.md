---
title: OpenAI API 格式详解
date: 2026-06-24
tags: [AI, Agent, OpenAI]
aliases:
  - OpenAI API 格式详解
  - OpenAIAPI格式详解
---

# 一、前置准备

安装 [Hoppscotch](https://docs.hoppscotch.io/documentation/clients/desktop/overview)。

Hoppscotch 是一款轻量级的 API 调试与请求测试工具，适合学习和调试 HTTP / Web API。


# 二、快速开始：OpenAI API 请求与响应

要使用兼容 OpenAI API 请求的模型完成对话，首先需要指定大模型服务的**BASE_URL**和**API_KEY**：

- BASE_URL：API 请求的服务器地址，例如 OpenAI 官方的 `https//api.openai.com/v1` ，或者兼容 OpenAI 的第三方模型 `https://xxx.com/v1`。
- API_KEY：相当于身份凭证，标识是否有权限使用该模型，以及用于计费和限流。通常放在 Header 里：`Authorization: Bearer YOUR_API_KEY`。

在完成 BASE_URL 和 API_KEY 配置之后，就可以通过 `/chat/completions` 发起一次对话请求。

`/chat/completions`是 OpenAI 兼容接口中 **对话式生成（Chat Completion）** 的核心路径，它表示基于聊天上下文生成（补全）下一条回复。

一个完整请求的通常由三部分组成：请求地址（URL）、请求头（Header）和请求体（Body）。

其中完整的请求方法和请求地址格式：

```
POST {BASE_URL}/v1/chat/completions
```

例如，Deepseek 的请求地址：

```
https://api.deepseek.com/v1/chat/completions
```

表示在 Deepseek 大语言服务中，调用对话生成接口。

请求头用于声明请求类型以及身份确认信息。

```
Content-Type: application/json  
Authorization: Bearer YOUR_API_KEY
```

其中：

- `Content-Type: application/json`表示请求体使用 JSON 格式
- `Authorization: Bearer YOUR_API_KEY`携带 API Key，用于身份验证

请求体为 JSON 格式，用于指定具体的模型以及想让模型做什么等。

打开 Hoppscotch，以 Deepseek 为例，一次 request 请求如下：

![[assets/Pasted image 20260624004902.png]]

注：需要指定请求头的内容类型`Content_Type`和授权`Authorization`。

点击发送后，得到如下的 JSON 响应体：

![[assets/Pasted image 20260624005243.png]]

# 三、请求体字段

这里介绍一下 OpenAI API 请求体中几个重要的字段。

## 1、model

必须提供的 string 类型的模型 ID，例如上述的`deepseek-v4-flash`。


## 2、messages

必须提供的 array 类型的消息列表，包含完整的对话历史，每个消息是一个 JSON 对象。

消息角色（role）有四种类型：`system`、`user`、`assistant`、`tool`。

### （1）system message

system message 是系统提示词，包含以下字段：

- role：值固定为`system`
- content：系统提示词内容
- name：对话参与者的名称（可选）

### （2）user message

user message 是用户消息，即一次提问，包含以下字段：

- role：值固定为`user`
- content：值类型为 string 或 array 二选一。
	- string 类型：表示消息的文本内容
	- array 类型：一般用于调用**多模态模型**，用来包含多个内容部分的数组，一般是一个文本内容的 json 对象和一个或多个图片内容的 json 对象。
		- 文本内容：`type` 字段值为 `text`，`text`字段值为消息内容。
		- 图像内容：`type`字段值是`image_url`，`image_url`字段的值又是一个 JSON 对象，字段有`url`和`detail`。`url`必填，为图像的 URL 或 Base64 编码的图像数据，`detail`一般默认是`auto`。
-  name：对话参与者的名称（可选）

这里举一个请求多模态，包含图像信息的消息：让AI识别下图中的内容。

![[assets/Pikachu.png]]

因为涉及多模态，这里使用 kimi 模型，不过，kimi 模型不支持外链图片，也就是不允许直接抓公网 URL 图片，因此这里采用 base64 的方式。

可以先执行：

```shell
base64 -i Pikachu.png
```

将得到一大段 base64 文本字符串。

然后拼成 data URL：

```
data:image/png;base64,xxx
```

xxx就是上面生成的base64 文本字符串。


![[assets/Pasted image 20260624014411.png|600]]

### （3）assistant message

assistant message 是模型生成的回复，它包含以下字段：

- role：值固定为`assistant`
- content：模型生成的回复
- tool_calls：可选的 array 类型，大模型生成的工具调用，例如函数调用。tools_calls 数组的每个元素是一个 JSON 对象，代表一个函数调用，包含字段：
	- id：函数调用的 id
	- type：工具调用的类型，目前仅支持 function
	- function: 模型针对工具调用生成的函数说明（使用哪一个函数以及函数参数是什么）
		- name：要调用的函数名称
		- arguments：调用函数所用的参数，由模型以 JSON 格式生成
- function_calls：已弃用（由tool_calls替代）

### （4）tool message

用户根据 assistant 的 tool_calls 内容调用了某个函数，还需要将函数调用结果反馈给大模型，让大模型根据函数调用结果生成最终回复。字段：

-  role：值固定为`role`
- tool_call_id：表示本地消息是对哪个函数调用的结果反馈，与 assistant message -> tool_calls -> id 对应
- content：工具调用的结果

> 原先还有 function message，已废弃并由 tool message 替代


## 3、tools

用户可选的字段，是 array 类型，表示可供模型选择的一个工具列表。目前仅支持函数 function 作为工具。该列表最多支持 128 个 tool。

每个 tool 包含的字段：

- type：工具类型，目前仅支持 function
- function：表示函数的一些描述信息
	- description：函数功能描述，模型根据描述获知何时该调用该函数
	- name：函数名称
	- parameters：函数接收的参数，描述为 JSON Schema 对象。若不含 parameters 字段，表示定义了一个不带参数的函数

## 4、tool_choice

可选的 string 或 JSON 对象类型，控制模型调用哪个函数（如果有）。

- "none"表示模型不会调用函数而是生成信息，"auto" 意味着模型可以在生成消息或调用函数之间进行选择。当不存在函数时，"none"是默认值，当存在函数时，"auto"是默认值
- 还可以设置 tool_choice 的值为 `{"type": "function", "function": {"name": "my_function"}}`指定特定函数来强制模型调用该函数

这里举一个大模型使用工具的例子，给模型提供工具列表，在让模型回答对应的问题是，查看模型生成的回复。

场景：问某个地方的天气怎么样？提供 get_current_weather 工具。

```json
{
    "model": "deepseek-v4-flash",
    "messages": [
      {
          "role": "system",
          "content": "你是一个乐于助人的助手"
      },
      {
          "role": "user",
          "content": "今天深圳的天气怎么样？"
      }
    ],
    "tools": [
      {
        "type": "function",
        "function": {
		  "name": "get_current_weather",
          "description": "获取给定位置的当前天气",
          "parameters": {
            "type": "object",
            "properties": {
              "location": {
                "type": "string",
                "description": "城市地点，例如北京"
              },
            	"unit": {
              	  "type": "string",
                  "enum": ["celsius", "fahrenheit"]
            }	
            },
            "required": ["location"]
          }
        }
      }
    ]
    ]
  }
```

大模型回答：

```json
{
  "id": "4e9f1ae6-1cd9-40d3-9cfe-bd523f1abba2",
  "object": "chat.completion",
  "created": 1782239084,
  "model": "deepseek-v4-flash",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "深圳今天的天气情况我来帮你查询一下！",
        "reasoning_content": "用户想知道今天深圳的天气。我需要调用 get_current_weather 函数来获取深圳的天气信息。让我查询一下。",
        "tool_calls": [
          {
            "index": 0,
            "id": "call_00_j9DA1goVLsSrqpyuwMfR0413",
            "type": "function",
            "function": {
              "name": "get_current_weather",
              "arguments": "{\"location\": \"深圳\", \"unit\": \"celsius\"}"
            }
          }
        ]
      },
      "logprobs": null,
      "finish_reason": "tool_calls"
    }
  ],
  "usage": {
    "prompt_tokens": 316,
    "completion_tokens": 97,
    "total_tokens": 413,
    "prompt_tokens_details": {
      "cached_tokens": 0
    },
    "completion_tokens_details": {
      "reasoning_tokens": 26
    },
    "prompt_cache_hit_tokens": 0,
    "prompt_cache_miss_tokens": 316
  },
  "system_fingerprint": "fp_8b330d02d0_prod0820_fp8_kvcache_20260402"
}
```

## 5、stream

可选的 stream 值，如果设置了 `true`，将会流式的返回消息，会流式的返回消息，就像在 ChatGPT 中一样。token将在可用时作为data-only的SSE事件发送给用户，http的chunk流由 data: [DONE] 消息终止。这一点常用于实现实时聊天agent，以快速响应用户。



# 四、响应体字段

API 返回的 响应体中也包几个非常重要 JSON 字段。 

如果采用非流式，则有如下一些重要字段：

## 1、id
聊天的唯一标识符。

## 2、created
创建聊天完成消息时的 Unix 时间戳（以秒为单位）。

## 3、模型

用于聊天完成的模型。

## 4、choices

包含一个或多个聊天响应的列表。如果请求的参数n 大于1，请求模型生成多个答复，列表的元素将是多个。一般情况下 choices 只包含一个元素，每个元素是一个 JSON 对象，包含的字段有：

- index：整数类型，表示该元素在choices中的索引，一般是0
- finish_reason：模型停止生成的原因。例如`stop`表示自然停止，`length`表示达到请求指定最大 token 数、`tool_calls`表示模型要调用工具。
- message：表示模型生成的聊天信息。
	- role：固定为 assistent
	- content：消息内容
	- tool_calls：数组类型，表示模型生成的工具调用。包含name、arguments字段。


## 5、usage

完成请求的使用统计信息。是一个json对象，字段有：

- completion_tokens，模型生成的新token数
- prompt_tokens，用户输入的prompt的token数
- total_tokens，对话的总token数，prompt_tokens + completion_tokens