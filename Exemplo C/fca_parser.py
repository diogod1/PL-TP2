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
            p[0] = ('seq', p[1] + [p[2]])

    def p_statement_assign(self, p):
        'statement : ID EQUALS expressao SEMICOLON'
        p[0] = ('assign', p[1], p[3])

    def p_statement_escrever(self, p):
        'statement : ESCREVER LPAREN expressao RPAREN SEMICOLON'
        p[0] = ('escrever', p[3])

    def p_statement_funcao(self, p):
        'statement : FUNCAO ID LPAREN lista_atribuicao RPAREN COLON statements FIM'
        p[0] = ('func', p[2], p[4], p[7])

    def p_statement_call(self, p):
        'statement : ID LPAREN lista_expressoes RPAREN SEMICOLON'
        p[0] = ('call', p[1], p[3])

    def p_expressao_binop(self, p):
        '''expressao : expressao PLUS termo
                     | expressao MINUS termo
                     | termo'''
        if len(p) == 4:
            p[0] = ('binop', p[2], p[1], p[3])
        else:
            p[0] = p[1]

    def p_termo_binop(self, p):
        '''termo : termo TIMES fator
                 | fator'''
        if len(p) == 4:
            p[0] = ('binop', p[2], p[1], p[3])
        else:
            p[0] = p[1]

    def p_fator_num(self, p):
        'fator : NUMBER'
        p[0] = ('num', p[1])

    def p_fator_var(self, p):
        'fator : ID'
        p[0] = ('var', p[1])

    def p_fator_expr(self, p):
        'fator : LPAREN expressao RPAREN'
        p[0] = p[2]

    def p_lista_atribuicao(self, p):
        '''lista_atribuicao : ID
                            | lista_atribuicao COMMA ID'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_lista_expressoes(self, p):
        '''lista_expressoes : expressao
                            | lista_expressoes COMMA expressao'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)