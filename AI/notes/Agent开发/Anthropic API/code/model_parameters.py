
from dotenv import load_dotenv
from anthropic import Anthropic
import os


load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")
if not api_key:
    raise RuntimeError("请设置 ANTHROPIC_AUTH_TOKEN 或 ANTHROPIC_API_KEY 环境变量")

client = Anthropic(
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    api_key=api_key,
)

model = os.getenv("MODEL_ID")


def max_tokens_demo():
    truncate_response = client.messages.create(
        max_tokens=10,
        model=model,
        messages=[
            {"role": "user", "content": "讲一个笑话"}
        ]
    )

    print(truncate_response.content[0].text)
    print(truncate_response.usage.completion_tokens)
    print(truncate_response.stop_reason)

def stop_sequences_demo():
    response = client.messages.create(
        max_tokens=500,
        model=model,
        messages=[
            {
                "role": "user",
                "content": "生成一个 JSON 对象，表示一个用户，包含姓名、性别和电话"
            }
        ],
        stop_sequences=["}"]
    )

    print(response.content[0].text)
    print(response.stop_reason)
    print(response.stop_sequence)

def temperature_demo():

    temperatures = [0.0, 1.0]

    for temperature in temperatures:
        print(f"使用 temperature={temperature}，让模型生成十次结果")
        print("=================")
        for i in range(10):
            response = client.messages.create(
                max_tokens=500,
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": "想一个富有想象力的外星星球名字。只用一个英文单词回答。"
                    }
                ],
                temperature=temperature,
            )
            print(f"第 {i+1} 次响应： {response.content[0].text}")


if __name__ == "__main__":
    # max_tokens_demo()
    # stop_sequences_demo()
    temperature_demo()