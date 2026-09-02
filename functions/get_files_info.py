import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_abs_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_abs_dir, directory))

        valid_target_dir = os.path.commonpath([working_abs_dir, target_dir]) == working_abs_dir

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        return f'Success: "{directory}" is within the working directory'
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print(get_files_info("/calculator", "/calculator"))
