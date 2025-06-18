import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
       working_path = os.path.abspath(working_directory)
    except Exception:
        return f'Error: Invalid working directory "{working_directory}"'

    try:
        file_path = os.path.abspath(os.path.join(working_path, file_path))
    except Exception:
        return f'Error: Invalid file path "{file_path}"'

    if not file_path.startswith(working_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)

    if len(file_content_string) == MAX_CHARS:
        file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

    return file_content_string