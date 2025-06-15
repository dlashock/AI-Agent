import os

def get_files_info(working_directory, directory=None):
    working_path = os.path.abspath(working_directory)

    if directory is None or directory == ".":
        dir_path = working_path
    else:
        dir_path = os.path.abspath(os.path.join(working_path, directory))
    
    if not dir_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(dir_path):
        return f'Error: "{directory}" is not a directory'



    try:
        dir_contents = os.listdir(dir_path)
    except Exception as e:
         return f"Error: Unable to list contents of directory '{directory}'."

    # Initialize variables to store file information         
    is_dir = False
    file_size = 0
    filename = None

    # List to store the formatted strings for each item in the directory
    dir_strings = []

    for item in dir_contents:
        try:
            item_path = os.path.join(dir_path, item)
        except Exception as e:
            return f"Error: Unable to construct path for item '{item}' in directory '{directory}'."
        
        if os.path.isdir(item_path):
            is_dir = True
        else:
            is_dir = False
        
        try:
            file_size = os.path.getsize(item_path)
        except Exception as e:
            return f"Error: Unable to get size for item '{item}' in directory '{directory}'."
        filename = item
        dir_strings.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")
    
    return "\n".join(dir_strings)