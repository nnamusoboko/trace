import os
from openai.types.chat import ChatCompletionToolParam

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_abs_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_abs_dir, directory))

        valid_target_dir = os.path.commonpath([working_abs_dir, target_dir]) == working_abs_dir

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_in_dir = os.listdir(target_dir)
        files_info: list[str] = []
        for file in files_in_dir:
            full_filepath = os.path.join(target_dir, file)
            files_info.append(
                f"- {file}: file_size={os.path.getsize(full_filepath)} bytes, is_dir={os.path.isdir(full_filepath)}"
            )
        return "\n".join(files_info)

    except Exception as e:
        return f"Error: {e}"

schema_get_files_info: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


if __name__ == "__main__":
    print(get_files_info(".venv", "bin"))
