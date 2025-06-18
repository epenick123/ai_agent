import os, subprocess, time, sys

def run_python_file(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not (abs_file_path == abs_working or abs_file_path.startswith(abs_working + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result_string = ""
        result = subprocess.run([sys.executable, file_path], timeout=30, cwd = abs_working, capture_output = True)
        if result.stdout == b"" and result.stderr == b"":
            return "No output produced."
        if result.stdout != b"":
            result_string += f"STDOUT: {result.stdout.decode().strip()}\n"
        if result.stderr != b"":
            result_string += f"STDERR: {result.stderr.decode().strip()}\n"
        if result.returncode != 0:
            result_string += f"Process exited with code {result.returncode}\n"
        return result_string.strip()

    except Exception as e:
        return f"Error: executing Python file: {e}"