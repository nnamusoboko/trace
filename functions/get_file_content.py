import os
import config


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_abs_dir = os.path.abspath(working_directory)
        target_filepath = os.path.normpath(os.path.join(working_abs_dir, file_path))

        valid_target_dir = os.path.commonpath([working_abs_dir, target_filepath]) == working_abs_dir
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_filepath):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_filepath, "r", encoding="utf-8") as f:
            content =  f.read(config.MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'

            return content

    except Exception as e:
        return f"Error: {e}"
