import argparse

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()
    return args
