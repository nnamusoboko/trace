import os
import subprocess

from openai.types.chat import ChatCompletionToolParam
import config

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_abs_dir = os.path.abspath(working_directory)
        target_filepath = os.path.normpath(os.path.join(working_abs_dir, file_path))

        valid_target_dir = os.path.commonpath([working_abs_dir, target_filepath]) == working_abs_dir
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_filepath):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        _, extension = os.path.splitext(target_filepath)
        if not (extension == ".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python3", target_filepath]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_abs_dir,
            capture_output=True,
            text=True,
            timeout=config.PROCESS_TIME
        )

        output_str = build_output_string(result)
        return output_str

    except Exception as e:
        return f"Error: executing Python file: {e}"

def build_output_string(result: subprocess.CompletedProcess[str]) -> str:
    output_strs: list[str] = []

    if result.returncode != 0:
        output_strs.append(f"Process exited with code {result.returncode}")
    if not result.stdout and not result.stderr:
        output_strs.append("No output produced")
    else:
        if result.stdout:
            output_strs.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output_strs.append(f"STDERR: {result.stderr}")

    return "\n".join(output_strs)

schema_run_python_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a python script in a sub-process and produce output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Filepath of file to execute relative to working directory"
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of commands to run to execute python file",
                }
            }
        }
    }
}
