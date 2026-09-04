import os
from typing import cast

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessageParam,
)

import config
import prompts
from call_function import available_functions, call_function
from cli import get_args

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

    completted_successfuly = False
    for _ in range(config.MAX_AGENT_ITERATIONS):

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions
        )
        if not response.usage:
            raise RuntimeError("Failed request to API")

        is_verbose = args.verbose
        if is_verbose:
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
            assistant_message = cast(
                ChatCompletionAssistantMessageParam,
                message.model_dump(exclude_none=True)
            )
            messages.append(assistant_message)

            for tool_call in message.tool_calls:
                if tool_call.type == "function":
                    result = call_function(tool_call, is_verbose)
                    if not result["content"]:
                        raise Exception("Tool function call didnt produce any result")

                    if is_verbose:
                        print(f"-> {result['content']}")

                    messages.append(result)
        else:
            messages.append({
                "role": "assistant",
                "content": message.content
            })
            completted_successfuly = True
            break

    if not completted_successfuly:
        print(f"\nError: Agent failed to reach a solution within {config.MAX_AGENT_ITERATIONS} iterations.")
        if messages:
            print(f"Last system state: {messages[-1]}")
        exit(1)


if __name__ == "__main__":
    main()
