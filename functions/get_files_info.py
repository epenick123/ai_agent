import os

def get_files_info(working_directory, directory=None):
    result = ""
    if directory is None:
        directory = working_directory
    
       # If directory is a relative path, join with working_directory
    if not os.path.isabs(directory):
        directory = os.path.join(working_directory, directory)
    
    abs_working = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(directory)

    if not (abs_dir == abs_working or abs_dir.startswith(abs_working + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isdir(directory) == False: 
        return (f'Error: "{directory}" is not a directory')
        
    try: content_list = os.listdir(directory)
    except Exception as e: 
        return f"Error: {e}"

    for entry in content_list:
        entry_path = os.path.join(directory, entry)
        try: file_size = os.path.getsize(entry_path)
        except Exception as e:
            result += f"Error: {e}"
        entrydir = os.path.isdir(entry_path)
        result += (f"- {entry}: file_size={file_size} bytes, is_dir={entrydir}\n")
    
    return result
    
