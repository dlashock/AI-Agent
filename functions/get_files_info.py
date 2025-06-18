import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    working_path = os.path.abspath(working_directory)
    dir_path = os.path.abspath(os.path.join(working_path, directory or "."))

    if not dir_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(dir_path):
        return f'Error: "{directory}" is not a directory'

    try:
        dir_contents = os.listdir(dir_path)
    except Exception:
        return f"Error: Unable to list contents of directory '{directory}'."

    dir_strings = []

    for item in dir_contents:
        item_path = os.path.join(dir_path, item)

        is_dir = os.path.isdir(item_path)
        try:
            file_size = os.path.getsize(item_path)
        except Exception:
            return f"Error: Unable to get size for item '{item}' in directory '{directory}'."

        dir_strings.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(dir_strings)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)