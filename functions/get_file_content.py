import os

def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(file_path)
    
    if not (abs_file_path == abs_working or abs_file_path.startswith(abs_working + os.sep)):
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

    if os.path.isfile(abs_file_path) == False:
        return(f'Error: File not found or is not a regular file: "{file_path}"')

    MAX_CHARS = 10000
    extra = ""
    try: 
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            extra = f.read(1)
    except Exception as e:
        return f"Error: {e}"
        
    
    if len(extra) > 0:
        file_content_string += (f'\n[...File "{file_path}" truncated at 10000 characters]')

    return file_content_string