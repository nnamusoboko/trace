import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from cli import get_args
import prompts
from call_function import available_functions

_ = load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Empty api key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def main():
    args = get_args()
    user_prompt = args.user_prompt

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": prompts.system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions
    )
    if not response.usage:
        raise RuntimeError("Failed request to API")

    if args.verbose:
        print(
            f"""
                User prompt: {user_prompt}
                Prompt tokens: {response.usage.prompt_tokens}
                Response tokens: {response.usage.completion_tokens}
                total tokens: {response.usage.total_tokens}
            """
        )

    message = response.choices[0].message
    print(f"response: {message.content}")
    print(f"tools: {message.tool_calls}")

    if message.tool_calls:
        for tool_call in message.tool_calls:
            if tool_call.type == "function":
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")



if __name__ == "__main__":
    main()
