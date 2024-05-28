import sys
from fca_parser import FCAParser
from fca_code_generator import CodeGenerator
from fca_executor import Executor

def read_input_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if len(sys.argv) < 2:
    print("Usage: python main.py <input_file.fca>")
    sys.exit(1)

input_file = sys.argv[1]
input_data = read_input_file(input_file)

parser = FCAParser()
result = parser.parse(input_data)
print("AST:", result)

executor = Executor(result)
executor.execute()

generator = CodeGenerator(result)
c_code = generator.generate_code()

output_file = "output.c"
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(c_code)

print(f"Generated C code written to {output_file}")