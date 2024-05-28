import ply.yacc as yacc
from fca_lexer import FCALexer

class FCAParser:
    tokens = FCALexer.tokens

    def __init__(self):
        self.lexer = FCALexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

    def p_statements(self, p):
        '''statements : statement
                      | statements statement'''
        if len(p) == 2:
            p[0] = ('seq', [p[1]])
        else:
            p[0] = ('seq', p[1][1] + [p[2]])

    def p_statement_assign(self, p):
        'statement : ID EQUALS expression SEMICOLON'
        p[0] = ('assign', p[1], p[3])

    def p_statement_escrever(self, p):
        'statement : ESCREVER LPAREN expression RPAREN SEMICOLON'
        p[0] = ('escrever', p[3])

    def p_expression_binop(self, p):
        '''expression : expression PLUS term
                      | expression MINUS term
                      | term'''
        if len(p) == 4:
            p[0] = ('binop', p[2], p[1], p[3])
        else:
            p[0] = p[1]

    def p_term_binop(self, p):
        '''term : term TIMES factor
                | factor'''
        if len(p) == 4:
            p[0] = ('binop', p[2], p[1], p[3])
        else:
            p[0] = p[1]

    def p_factor_num(self, p):
        'factor : NUMBER'
        p[0] = ('num', p[1])

    def p_factor_string(self, p):
        'factor : STRING'
        p[0] = ('string', p[1])

    def p_factor_var(self, p):
        'factor : ID'
        p[0] = ('var', p[1])

    def p_factor_expr(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

if __name__ == '__main__':
    parser = FCAParser()
    result = parser.parse('ESCREVER(valor); ESCREVER(365 * 2); ESCREVER("Ola Mundo"); curso = "ESI"; ESCREVER("Olá, " + curso);')
    print("AST:", result)