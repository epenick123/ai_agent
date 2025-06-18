import os
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python_file import run_python_file
from .write_file import write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    # (1) Create your functions dictionary here, e.g. {"list_dir": list_dir, ...}
    functions = {
        "get_files_info":get_files_info,
        "get_file_content":get_file_content,
        "run_python_file":run_python_file,
        "write_file":write_file,
    }


    # (2) Copy args and add working_directory
    args = function_call_part.args.copy()
    args["working_directory"] = "./calculator"
    
    function_name = function_call_part.name

    # (3) Verbose output
    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    # (4) Check if function exists in functions
    if function_name in functions:
        func = functions[function_name]
        function_result = func(**args)  # <--- notice the ** here!
        
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)
    else:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)