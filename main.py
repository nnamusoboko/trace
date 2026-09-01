import os
from dotenv import load_dotenv
from openai import OpenAI

_ = load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Empty api key")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def main():
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Describe an ai agent? Use one paragraph maximum."
            }
        ]
    )
    if not response.usage:
        raise RuntimeError("Failed request to API")

    print(
         f"""
            Prompt tokens: {response.usage.prompt_tokens}
            Response tokens: {response.usage.completion_tokens}
            total tokens: {response.usage.total_tokens}
         """
     )

    print(f"response: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
