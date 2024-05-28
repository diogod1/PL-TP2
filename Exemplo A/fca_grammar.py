from fca_lexer import FCALexer
import ply.yacc as pyacc

class ArithGrammar:
    tokens = FCALexer.tokens
    
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.yacc = None
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = FCALexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self, **kwargs)

    def parse(self, string):
        self.lexer.input(string)
        return self.yacc.parse(lexer=self.lexer.lexer)

    def p_lista_declaracoes(self, p):
        """lista_declaracoes : declaracao
                             | lista_declaracoes declaracao"""
        if len(p) == 2:
            p[0] = {'op': 'seq', 'args': [p[1]]}
        else:
            p[1]['args'].append(p[2])
            p[0] = p[1]

    def p_declaracao(self, p):
        """declaracao : declaracao_atribuicao"""
        p[0] = p[1]

    def p_declaracao_atribuicao(self, p):
        """declaracao_atribuicao : VAR_ID EQUALS expressao SEMICOLON"""
        p[0] = {'op': 'assign', 'args': [p[1], p[3]]}

    def p_expressao_binaria(self, p):
        """expressao : expressao PLUS expressao
                     | expressao MINUS expressao
                     | expressao TIMES expressao
                     | expressao DIVIDE expressao"""
        p[0] = ('binop', p[2], p[1], p[3])

    def p_expressao_uminus(self, p):
        """expressao : MINUS expressao %prec UMINUS"""
        p[0] = ('uminus', p[2])

    def p_expressao_numero(self, p):
        """expressao : NUM"""
        p[0] = ('num', p[1])

    def p_expressao_variavel(self, p):
        """expressao : VAR_ID"""
        p[0] = ('var', p[1])

    def p_expressao_paren(self, p):
        """expressao : LPAREN expressao RPAREN"""
        p[0] = p[2]

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")

if __name__ == '__main__':
    data = '''
    tmp_01 = 2 + 3 + 4 ;
    a1_ = 12345 - (5191 * 15) ;
    idade_valida? = 1;
    mult_3! = a1_ * 3 ;
    '''
    parser = ArithGrammar()
    parser.build()
    result = parser.parse(data)
    print(result)