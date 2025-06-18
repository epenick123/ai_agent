import os

def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not (abs_file_path == abs_working or abs_file_path.startswith(abs_working + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        dir1 = os.path.dirname(abs_file_path)
        os.makedirs(dir1, exist_ok=True)
      
    except Exception as e:
        return f'Error: Error creating file path {abs_file_path}'
    
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Error writing content to {abs_file_path}'
    
