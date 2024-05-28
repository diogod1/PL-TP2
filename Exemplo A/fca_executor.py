class Executor:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}

    def execute(self):
        self.visit(self.ast)
        print("Variables:", self.variables)

    def visit(self, node):
        if node[0] == 'seq':
            for stmt in node[1]:
                self.visit(stmt)
        elif node[0] == 'assign':
            self.variables[node[1]] = self.visit(node[2])
        elif node[0] == 'binop':
            left = self.visit(node[2])
            right = self.visit(node[3])
            if node[1] == '+':
                return left + right
            elif node[1] == '-':
                return left - right
            elif node[1] == '*':
                return left * right
        elif node[0] == 'num':
            return node[1]
        elif node[0] == 'var':
            return self.variables[node[1]]

if __name__ == '__main__':
    ast = ('seq', [
        ('assign', 'tmp_01', ('binop', '+', ('binop', '*', ('num', 2), ('num', 3)), ('num', 4))),
        ('assign', 'a1_', ('binop', '-', ('num', 12345), ('binop', '*', ('num', 5191), ('num', 15)))),
        ('assign', 'idade_valida?', ('num', 1)),
        ('assign', 'mult_3!', ('binop', '*', ('var', 'a1_'), ('num', 3)))
    ])
    executor = Executor(ast)
    executor.execute()