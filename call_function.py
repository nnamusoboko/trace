from openai.types.chat import ChatCompletionToolParam
from functions.get_files_info import schema_get_files_info

available_functions: list[ChatCompletionToolParam] = [
    schema_get_files_info,
]
