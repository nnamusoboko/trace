import os

from openai.types.chat import ChatCompletionToolParam

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_abs_dir = os.path.abspath(working_directory)
        target_filepath = os.path.normpath(os.path.join(working_abs_dir, file_path))

        valid_target_dir = os.path.commonpath([working_abs_dir, target_filepath]) == working_abs_dir
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_filepath):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(target_filepath)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_filepath, "w") as f:
            _ = f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"


schema_write_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file to write to, relative to the working directory"
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file"
                }
            }
        }
    }
}
