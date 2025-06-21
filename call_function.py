from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python
from functions.write_file import write_file, schema_write_file
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_call_part.args["working_directory"] = "./calculator"

    match function_call_part.name:
        case "get_files_info":
            result = get_files_info(**function_call_part.args)
        case "get_file_content":
            result = get_file_content(**function_call_part.args)
        case "run_python_file":
            result = run_python_file(**function_call_part.args)
        case "write_file":
            result = write_file(**function_call_part.args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                        )
                    ],
                )
        
    return types.Content(
        role="tool",
        parts=[
        types.Part.from_function_response(
        name=function_call_part.name,
        response={"result": result},
                )
            ],
        ) 
