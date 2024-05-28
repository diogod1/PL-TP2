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
        if node['op'] == 'seq':
            for stmt in node['args']:
                self.visit(stmt)
        elif node['op'] == 'assign':
            var_name = self.sanitize_variable_name(node['args'][0])
            self.c_code += f"    int {var_name} = "
            self.visit(node['args'][1])
            self.c_code += ";\n"
        elif node['op'] == 'binop':
            self.c_code += "("
            self.visit(node['left'])
            self.c_code += f" {node['op']} "
            self.visit(node['right'])
            self.c_code += ")"
        elif node['op'] == 'num':
            self.c_code += str(node['value'])
        elif node['op'] == 'var':
            var_name = self.sanitize_variable_name(node['name'])
            self.c_code += var_name
        elif node['op'] == 'func':
            func_name = self.sanitize_variable_name(node['name'])
            params = ", ".join([self.sanitize_variable_name(p) for p in node['params']])
            self.c_code += f"\nint {func_name}({params}) {{\n"
            self.visit(node['body'])
            self.c_code += "}\n"
        elif node['op'] == 'call':
            func_name = self.sanitize_variable_name(node['name'])
            args = ", ".join([self.sanitize_variable_name(a) for a in node['args']])
            self.c_code += f"    {func_name}({args});\n"

if __name__ == '__main__':
    ast = {
        'op': 'seq',
        'args': [
            {'op': 'func', 'name': 'soma', 'params': ['a', 'b'], 'body': {'op': 'seq', 'args': [{'op': 'assign', 'args': ['c', {'op': 'binop', 'op': '+', 'left': {'op': 'var', 'name': 'a'}, 'right': {'op': 'var', 'name': 'b'}}]}]}},
            {'op': 'call', 'name': 'soma', 'args': [{'op': 'num', 'value': 4}, {'op': 'num', 'value': 2}]}
        ]
    }
    generator = CodeGenerator(ast)
    c_code = generator.generate_code()
    print(c_code)