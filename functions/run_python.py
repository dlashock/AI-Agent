import os
import subprocess

def run_python_file(working_directory, file):
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
    
    print(file_path)
    
    try:
        result = subprocess.run(f"python3 {file_path}", timeout=30, capture_output=True, shell=True, cwd=working_path)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    if not result.stdout:
        print("No output produced")
    else:
        print(f'STDOUT: {result.stdout.decode("utf-8")}')
    print(f"STDERR: {result.stderr}")
    if result.returncode != 0:
        return f'Process exited with code {result.returncode}'