from fca_lexer import FCALexer
import ply.yacc as pyacc

class ArithGrammar:
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS', 'UNARY_NEG'),
    )

    def __init__(self):
        self.yacc = None
        self.lexer = None
        self.tokens = None

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
        """declaracao : declaracao_atribuicao
                      | declaracao_expressao
                      | declaracao_funcao
                      | declaracao_escrever"""
        p[0] = p[1]

    def p_declaracao_atribuicao(self, p):
        """declaracao_atribuicao : VAR_ID '=' lista_expressoes ';'"""
        p[0] = {'op': 'atribuicao', 'args': [p[1], p[3]]}

    def p_declaracao_escrever(self, p):
        """declaracao_escrever : ESCREVER '(' expressao ')' ';'"""
        p[0] = {'op': 'escrever', 'args': [p[3]]}

    def p_declaracao_funcao(self, p):
        """declaracao_funcao : FUNCAO VAR_ID '(' lista_atribuicao ')' ':' lista_declaracoes FIM"""
        p[0] = {'op': 'funcao', 'args': [p[2], p[4], p[7]]}

    def p_lista_atribuicao(self, p):
        """lista_atribuicao : VAR_ID
                            | lista_atribuicao ',' VAR_ID"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_expressao_binop(self, p):
        '''expressao : expressao '+' termo
                     | expressao '-' termo
                     | termo'''
        if len(p) == 4:
            p[0] = {'op': 'binop', 'args': [p[2], p[1], p[3]]}
        else:
            p[0] = p[1]

    def p_termo_binop(self, p):
        '''termo : termo '*' fator
                 | fator'''
        if len(p) == 4:
            p[0] = {'op': 'binop', 'args': [p[2], p[1], p[3]]}
        else:
            p[0] = p[1]

    def p_fator_num(self, p):
        'fator : NUMBER'
        p[0] = {'op': 'num', 'args': [p[1]]}

    def p_fator_string(self, p):
        'fator : STRING'
        p[0] = {'op': 'string', 'args': [p[1]]}

    def p_fator_var(self, p):
        'fator : VAR_ID'
        p[0] = {'op': 'var', 'args': [p[1]]}

    def p_fator_expr(self, p):
        'fator : ( expressao )'
        p[0] = p[2]

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
        else:
            print("Syntax error at EOF")