# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

result1 = run_python_file("calculator", "main.py")
result2 = run_python_file("calculator", "tests.py")
result3 = run_python_file("calculator", "../main.py")
result4 = run_python_file("calculator", "nonexistent.py")

print(result1)
print(result2)
print(result3)
print(result4)