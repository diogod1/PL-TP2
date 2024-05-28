class Executor:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}

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

if __name__ == '__main__':
    ast = ('seq', [
        ('escrever', ('var', 'valor')),
        ('escrever', ('binop', '*', ('num', 365), ('num', 2))),
        ('escrever', ('string', 'Ola Mundo')),
        ('assign', 'curso', ('string', 'ESI')),
        ('escrever', ('binop', '+', ('string', 'Olá, '), ('var', 'curso')))
    ])
    executor = Executor(ast)
    executor.execute()