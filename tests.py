# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

result1 = get_file_content("calculator", "calculator/main.py")
result2 = get_file_content("calculator", "calculator/pkg/calculator.py")
result3 = get_file_content("calculator", "calculator/bin/cat")

print(result1)
print(result2)
print(result3)