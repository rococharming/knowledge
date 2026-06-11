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

MODEL = os.getenv("MODEL_ID")

conversation_history = []

while True:
    user_input = input("用户：")

    if user_input.lower() == "quit":
        print("对话结束")
        break

    conversation_history.append({
        "role": "user", "content": user_input
    })

    response = client.messages.create(
        system="每次回复我都以 Kamen Rider 开头",
        model=MODEL,
        max_tokens=1000,
        messages=conversation_history,
    )

    assistant_response = response.content[0].text
    print(f"助手：{assistant_response}")

    conversation_history.append({
        "role": "assistant", "content": assistant_response
    })
