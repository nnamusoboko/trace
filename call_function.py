import json
from collections.abc import Callable
from typing import TypedDict

from openai.types.chat import (
    ChatCompletionMessageFunctionToolCall,
    ChatCompletionToolParam,
)

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_code import run_python_file, schema_run_python_file
from functions.write_to_file import schema_write_file, write_file
import config

class ToolCallResultMessage(TypedDict):
    role: str
    tool_call_id: str
    content: str


available_functions: list[ChatCompletionToolParam] = [
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
    schema_get_file_content,
]

function_map: dict[str, Callable] = {
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
    "get_file_content": get_file_content
}

def call_function(tool_call: ChatCompletionMessageFunctionToolCall, verbose: bool = False) -> ToolCallResultMessage:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    function_args["working_directory"] = config.WORKING_DIR

    result = function_map[function_name](**function_args)
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }
