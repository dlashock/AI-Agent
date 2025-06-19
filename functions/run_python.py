import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file, args=None):
    try:
       working_path = os.path.abspath(working_directory)
    except Exception:
        return f'Error: Invalid working directory "{working_directory}"'

    try:
        file_path = os.path.abspath(os.path.join(working_path, file))
    except Exception:
        return f'Error: Invalid file path "{file}"'

    if not file_path.startswith(working_path):
        return f'Error: Cannot execute "{file}" as it is outside the permitted working directory'
    
    if not os.path.exists(file_path):
        return f'Error: File "{file}" not found'
    
    if not file_path.endswith(".py"):
        return f'Error: File "{file}" is not a Python file'
        
    try:
        commands = ["python", file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_path,
        )

        if not result.stdout:
            print("No output produced")
        else:
            print(f'STDOUT: {result.stdout.decode("utf-8")}')
        print(f"STDERR: {result.stderr}")
        if result.returncode != 0:
            return f'Process exited with code {result.returncode}'
    except Exception as e:
            return f"Error: executing Python file: {e}"
    
schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments to provide when running the Python file. These are not required, but can be used to pass commands to the Python script (e.g., '--verbose' or '--help').",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to run, relative to the working directory.",
            ),
        },
    ),
)