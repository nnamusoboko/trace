from openai.types.chat import ChatCompletionToolParam
from functions.get_files_info import schema_get_files_info
from functions.run_code import schema_run_python_file
from functions.write_to_file import schema_write_file
from functions.get_file_content import schema_get_file_content


available_functions: list[ChatCompletionToolParam] = [
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
    schema_get_file_content,
]
