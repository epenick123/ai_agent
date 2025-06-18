import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

if len(sys.argv)<2:
    print("Error:No prompt provided"),
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=sys.argv[1])]),
]
model_name = "gemini-2.0-flash-001"

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


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

schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description="Returns contents of specified file truncated to value of max characters",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the requested file, relative to the working directory. If not provided or is not a file, returns an error."
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description="Executes a python file with optional arguments",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the requested file, relative to the working directory. If not provided, is not a proper file, or is unexecutable, returns an error."
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description="Writes or overwrites file at specified location",
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the requested file, relative to the working directory. If not provided or is not a file, returns an error."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The actual data to be stored into the file at the file_path."
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt,)
)
for call in response.function_calls:
    function_call_result = call_function(call, verbose="--verbose" in sys.argv)
for call in response.function_calls:
    function_call_result = call_function(call, verbose="--verbose" in sys.argv)
    # Print the result if verbose
    if (function_call_result.parts 
        and hasattr(function_call_result.parts[0], "function_response") 
        and function_call_result.parts[0].function_response.response is not None 
        and "--verbose" in sys.argv):
        print(f"-> {function_call_result.parts[0].function_response.response}")
    elif not (function_call_result.parts 
        and hasattr(function_call_result.parts[0], "function_response") 
        and function_call_result.parts[0].function_response.response is not None):
        raise Exception("Fatal: Missing function response in Content")

if len(response.function_calls) == 0:
    if len(sys.argv)==2: 
        print(response.text)

    elif sys.argv[2] == "--verbose":
        print("User prompt:", sys.argv[1])
        print("Prompt tokens:",response.usage_metadata.prompt_token_count)
        print("Response tokens:",response.usage_metadata.candidates_token_count)
        print(response.text)

    else:
        print(response.text)


