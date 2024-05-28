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
        if isinstance(node, dict):
            op = node['op']
            if op == 'seq':
                for stmt in node['args']:
                    self.visit(stmt)
            elif op == 'assign':
                var_name = self.sanitize_variable_name(node['args'][0])
                self.c_code += f"    int {var_name} = "
                self.visit(node['args'][1])
                self.c_code += ";\n"
            elif op == 'binop':
                self.c_code += "("
                self.visit(node['args'][1])
                self.c_code += f" {node['args'][0]} "
                self.visit(node['args'][2])
                self.c_code += ")"
            elif op == 'uminus':
                self.c_code += "-("
                self.visit(node['args'][0])
                self.c_code += ")"
            elif op == 'num':
                self.c_code += str(node['args'][0])
            elif op == 'var':
                var_name = self.sanitize_variable_name(node['args'][0])
                self.c_code += var_name
        elif isinstance(node, tuple):
            if node[0] == 'binop':
                self.c_code += "("
                self.visit(node[2])
                self.c_code += f" {node[1]} "
                self.visit(node[3])
                self.c_code += ")"
            elif node[0] == 'num':
                self.c_code += str(node[1])
            elif node[0] == 'var':
                var_name = self.sanitize_variable_name(node[1])
                self.c_code += var_name
            elif node[0] == 'uminus':
                self.c_code += "-("
                self.visit(node[1])
                self.c_code += ")"
            else:
                raise TypeError(f"Invalid node type: {node[0]}")
        else:
            raise TypeError("Invalid node type, expected dict or tuple")

if __name__ == '__main__':
    ast = {
        'op': 'seq',
        'args': [
            {'op': 'assign', 'args': ['tmp_01', {'op': 'binop', 'args': ['+', {'op': 'num', 'args': [2]}, {'op': 'binop', 'args': ['+', {'op': 'num', 'args': [3]}, {'op': 'num', 'args': [4]}]}]}]},
            {'op': 'assign', 'args': ['a1_', {'op': 'binop', 'args': ['-', {'op': 'num', 'args': [12345]}, {'op': 'binop', 'args': ['*', {'op': 'num', 'args': [5191]}, {'op': 'num', 'args': [15]}]}]}]},
            {'op': 'assign', 'args': ['idade_valida?', {'op': 'num', 'args': [1]}]},
            {'op': 'assign', 'args': ['mult_3!', {'op': 'binop', 'args': ['*', {'op': 'var', 'args': ['a1_']}, {'op': 'num', 'args': [3]}]}]}
        ]
    }
    generator = CodeGenerator(ast)
    c_code = generator.generate_code()
    print(c_code)