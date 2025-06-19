import os
from google.genai import types

def write_file(working_directory, file_path, content=None):
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
    
    if not os.path.exists(file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        except Exception:
            return f'Error: Could not create directory for "{file_path}"'
        
    with open(file_path, "w") as f:
        try:
            f.write(content)
        except Exception:
            return f'Error: Could not write to file "{file_path}"'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If not provided, the file will be created empty.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the files to be writtin/overwritten, relative to the working directory. If not provided, write file in the working directory itself.",
            ),
        },
    ),
)