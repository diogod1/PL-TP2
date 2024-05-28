import re

class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.c_code = "#include <stdio.h>\n\nint main() {\n"

    def sanitize_variable_name(self, name):
        return re.sub(r'\W|^(?=\d)', '_', name)

    def generate_code(self):
        if self.ast:
            self.visit(self.ast)
            self.c_code += "    return 0;\n}\n"
        else:
            print("No AST to generate code from")
        return self.c_code

    def visit(self, node):
        if node[0] == 'seq':
            for stmt in node[1]:
                self.visit(stmt)
        elif node[0] == 'assign':
            sanitized_var = self.sanitize_variable_name(node[1])
            self.c_code += f"    char {sanitized_var}[100] = "
            self.visit(node[2])
            self.c_code += ";\n"
        elif node[0] == 'escrever':
            self.c_code += "    printf(\"%s\\n\", "
            self.visit(node[1])
            self.c_code += ");\n"
        elif node[0] == 'binop':
            self.c_code += "("
            self.visit(node[2])
            self.c_code += f" {node[1]} "
            self.visit(node[3])
            self.c_code += ")"
        elif node[0] == 'num':
            self.c_code += str(node[1])
        elif node[0] == 'string':
            self.c_code += f"\"{node[1]}\""
        elif node[0] == 'var':
            sanitized_var = self.sanitize_variable_name(node[1])
            self.c_code += sanitized_var

if __name__ == '__main__':
    ast = ('seq', [
        ('escrever', ('var', 'valor')),
        ('escrever', ('binop', '*', ('num', 365), ('num', 2))),
        ('escrever', ('string', 'Ola Mundo')),
        ('assign', 'curso', ('string', 'ESI')),
        ('escrever', ('binop', '+', ('string', 'Olá, '), ('var', 'curso')))
    ])
    generator = CodeGenerator(ast)
    c_code = generator.generate_code()
    print(c_code)