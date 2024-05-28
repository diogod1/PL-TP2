class Executor:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}
        self.functions = {}

    def execute(self):
        if self.ast:
            self.visit(self.ast)
            print("Variables:", self.variables)
        else:
            print("No AST to execute")

    def visit(self, node):
        if node[0] == 'seq':
            for stmt in node[1]:
                self.visit(stmt)
        elif node[0] == 'assign':
            self.variables[node[1]] = self.visit(node[2])
        elif node[0] == 'escrever':
            print(self.visit(node[1]))
        elif node[0] == 'binop':
            left = self.visit(node[2])
            right = self.visit(node[3])
            if node[1] == '+':
                return str(left) + str(right) if isinstance(left, str) or isinstance(right, str) else left + right
            elif node[1] == '-':
                return left - right
            elif node[1] == '*':
                return left * right
        elif node[0] == 'num':
            return node[1]
        elif node[0] == 'string':
            return node[1]
        elif node[0] == 'var':
            return self.variables.get(node[1], f"Undefined variable '{node[1]}'")
        elif node[0] == 'func':
            self.functions[node[1]] = (node[2], node[3])
        elif node[0] == 'call':
            func_name = node[1]
            if func_name in self.functions:
                params, body = self.functions[func_name]
                local_vars = self.variables.copy()
                for param, arg in zip(params, node[2]):
                    local_vars[param] = self.visit(arg)
                executor = Executor(body)
                executor.variables = local_vars
                executor.functions = self.functions
                executor.execute()
                self.variables.update(executor.variables)
            else:
                print(f"Undefined function '{func_name}'")

if __name__ == '__main__':
    ast = ('seq', [
        ('func', 'soma', ['a', 'b'], ('seq', [('assign', 'c', ('binop', '+', ('var', 'a'), ('var', 'b')))])),
        ('call', 'soma', [('num', 4), ('num', 2)])
    ])
    executor = Executor(ast)
    executor.execute()