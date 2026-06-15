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

BLUE = "\033[34m"
GREEN= "\033[32m"
RESET = "\033[0m"


def chat_with_model():
    print("Welcome to Chatbot!")
    print("Type 'quit' to exit chat.")

    conversation = []

    while True:
        user_input = input(f"{GREEN}You:{RESET}")

        if user_input.lower() == "quit":
            print("Goodbye")
            break

        conversation.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        stream = client.messages.create(
            model=model,
            max_tokens=800,
            temperature=0,
            messages=conversation,
            stream=True
        )

        print(f"{BLUE}Model:{RESET}", end='', flush=True)

        assistant_response = ""
        for event in stream:
            if event.type == "content_block_delta":
                content = event.delta.text
                print(f"{BLUE}{content}{RESET}", flush=True, end="")
                assistant_response += content

        print()  # New Line

        conversation.append(
            {
                "role": "assistant",
                "content": assistant_response
            }
        )



if __name__ == "__main__":
    chat_with_model()



