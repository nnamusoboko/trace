import argparse

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument("user_prompt", type=str, help="User prompt")
    _ = parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()
    return args
