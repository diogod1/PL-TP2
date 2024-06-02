from fca_lexer import FCALexer
import re
import ply.yacc as pyacc
 
class ArithGrammar:
    # Define a precedência dos operadores para resolver questões na gramatica
    precedence = (
        ('left', '+', '-'),  # Operadores de adição e subtração com associatividade à esquerda
        ('left', '*', '/'),  # Operadores de multiplicação e divisão com associatividade à esquerda
        # ('right', 'UMINUS'),  # Operadores unários como '-' (negativo) e 'NEG' têm associatividade à direita
    )
 
    # Constructor
    def __init__(self):
        self.yacc = None
        self.lexer = None
        self.tokens = None
 
    # Construir o analisador sintatico, pega no lexer e configura-o
    def build(self, **kwargs):
        self.lexer = FCALexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self, **kwargs)
 
    # Realiza a analise sintatica do Input fornecido
    def parse(self, string):
        self.lexer.input(string)
        return self.yacc.parse(lexer=self.lexer.lexer)
 
    # Regras Producao da Gramatica:
 
    # Lista de declarações, que pode ser uma única declaração ou várias declarações
    def p_lista_declaracoes(self, p):
        """lista_declaracoes : declaracao
                             | lista_declaracoes declaracao"""
        if len(p) == 2:
            p[0] = {'op': 'seq', 'args': [p[1]]}  # uma única declaração
        else:
            p[1]['args'].append(p[2])  # Adiciona a declaração à lista existente
            p[0] = p[1]
 
    # Declarações gerais dentro do programa
    def p_declaracao(self, p):
        """declaracao : declaracao_atribuicao
                      | declaracao_escrever
                      | declaracao_funcao
                      | declaracao_comentario"""
        p[0] = p[1]
 
    #| declaracao_expressao 
    #| declaracao_funcao
    # | declaracao_se
    # | declaracao_comentario

    # Declaração com atribuição
    def p_declaracao_atribuicao(self, p):
        """declaracao_atribuicao : ID '=' expressao ';'"""
        p[0] = {'op': 'atribuicao', 'args': [p[1], p[3]]}
    
    def p_declaracao_escrever(self,p):
        """declaracao_escrever : ESCREVER '(' expressao ')' ';'"""
        p[0] = {'op': 'escrever', 'args': [p[3]]}

    def p_declaracao_comentario(self,p):
        """declaracao_comentario : COMENTARIOS"""
        p[0] = {'op': 'comentario', 'args': [p[1]]}
        
    def p_declaracao_funcao(self, p):
        """declaracao_funcao : FUNCAO ID '(' expressao_funcao ')' ':' expressao ';' """
        p[0] = {'op': 'funcao', 'args': [p[2],p[4],p[7]]}
            
    def p_expressao_number(self, p):
        """expressao : NUMBER"""
        p[0] = {'op': 'number', 'args': p[1]}

    def p_expressao_id(self,p):
        """expressao : ID """
        p[0] = {'op': 'id', 'args': p[1]}

    def p_expressao_string(self,p):
        """expressao : STRING """
        resultado = re.findall(r"\#{(.*?)}", p[1])
        if resultado is any:
            p[0] = {'op': 'string', 'args': p[1]}
        else:
            for substring in resultado:
                p[0] = {'op': 'string', 'args': p[1]}

    def p_expressao_concat(self,p):
        """expressao : expressao CONCAT expressao"""
        p[0] = {'op': 'concat', 'args': [p[1],p[3]]}

    def p_expressao(self,p):
        """expressao : expressao '+' expressao
                     | expressao '-' expressao
                     | expressao '/' expressao
                     | expressao '*' expressao"""
        p[0] = {'op': p[2], 'args': [p[1], p[3]]}
    
    def p_expressao_funcao(self, p):
        """expressao_funcao : expressao
                            | expressao_funcao ',' expressao"""
        if len(p) == 2:
            p[0] = {'op': 'expressao_funcao', 'args': [p[1]]}
        else:
            p[1]['args'].append(p[3])
            p[0] = p[1]
    
    
    # def p_declaracao_funcao(self, p):
    #     """declaracao_funcao: FUNCAO ID'('lista_atribuicao')' = lista_expressoes ';'"""

    #def p_lista_atribuicao(self, p):