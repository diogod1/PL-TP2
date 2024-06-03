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
    
    # Declarações gerais dentro das funcoes
    def p_declaracao_corpo_funcao(self, p):
        """declaracao_corpo_funcao : declaracao_atribuicao
                                   | declaracao_escrever
                                   | declaracao_comentario
                                   | expressao ';'"""
        p[0] = p[1]

    # Lista de declarações, que pode ser uma única declaração ou várias declarações
    def p_lista_declaracoes_corpo_funcao(self, p):
        """lista_declaracoes_corpo_funcao : declaracao_corpo_funcao
                                          | lista_declaracoes_corpo_funcao declaracao_corpo_funcao"""
        if len(p) == 2:
            p[0] = {'op': 'seq', 'args': [p[1]]}  # uma única declaração
        else:
            p[1]['args'].append(p[2])  # Adiciona a declaração à lista existente
            p[0] = p[1]    

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
        """declaracao_funcao : FUNCAO ID '(' expressao_funcao ')' ',' ':' expressao ';'
                             | FUNCAO ID '(' expressao_funcao ')' ':' lista_declaracoes_corpo_funcao FIM """
        if len(p) == 10:
            p[0] = {'op': 'funcao', 'args': [p[2],p[4],p[8]]}  # uma única declaração
        else:
            p[0] = {'op': 'funcao', 'args': [p[2],p[4],p[7]]}
            
    def p_expressao_number(self, p):
        """expressao : NUMBER"""
        p[0] = {'op': 'number', 'args': [p[1]]}

    def p_expressao_id(self,p):
        """expressao : ID """
        p[0] = {'var': p[1]}
        
    def p_expressao_parentises(self,p):
        """expressao : '(' expressao ')' """
        p[0] = p[2]

    def p_expressao_string(self, p):
        """expressao : STRING """
        resultado = re.findall(r"\#\{(.*?)\}", p[1])
        if len(resultado) == 0:
            p[0] = {'op': 'string', 'args': [p[1]]}
        else:
            p[0] = {'op': 'string_interpol', 'args': [p[1]]}
            #Limpar o valor
            p[0]['args'] = []

            last_pos = 0
            #loop aos resultados
            for match in resultado:
                start_index = p[1].find('#{' + match + '}', last_pos)
                if start_index > last_pos:
                    #Adiciona a string antes da variavel
                    p[0]['args'].append({'op': 'string', 'args': [p[1][last_pos:start_index]]})
                #Adiciona a variavel
                p[0]['args'].append({'var': match})
                #Atualizar a posição
                last_pos = start_index + len(match) + 3  

            if last_pos < len(p[1]):
                # Adicionar o resto da string
                p[0]['args'].append({'op': 'string', 'args': [p[1][last_pos:]]})

    def p_expressao_concat(self,p):
        """expressao : expressao CONCAT expressao"""
        p[0] = {'op': 'concat', 'args': [p[1],p[3]]}

    def p_expressao(self,p):
        """expressao : expressao '+' expressao
                     | expressao '-' expressao
                     | expressao '/' expressao
                     | expressao '*' expressao """
        p[0] = {'op': p[2], 'args': [p[1], p[3]]}
    
    def p_expressao_array(self,p):
        """expressao : '[' lista_expressao_array ']'
                     | '[' ']' """
        if len(p) == 3:
            p[0] = {'op': 'array', 'args': []} 
        else:
            p[0] = {'op': 'array', 'args': [p[2]]}
        
    def p_map_array(self,p):
        """ expressao : MAP '(' ID ',' expressao ')' """
        p[0] = {'op': 'map', 'args': [p[3],p[5]]}
        
    def p_fold_array(self,p):
        """ expressao : FOLD '(' ID ',' expressao ')' """
        p[0] = {'op': 'array', 'args': [p[3],p[5]]}    
        
    # Lista de declarações, que pode ser uma única declaração ou várias declarações
    def p_lista_expressao_array(self, p):
        """lista_expressao_array : expressao
                                 | lista_expressao_array ',' expressao"""
        if len(p) == 2:
            p[0] = {'op': 'expressao_array', 'args': [p[1]]}  # uma única declaração
        else:
            p[1]['args'].append(p[3])  # Adiciona a declaração à lista existente
            p[0] = p[1]    

    
    def p_expressao_aleatorio(self,p):
        """expressao : ALEATORIO '(' NUMBER ')'"""
        p[0] = {'op': 'aleatorio', 'args': [p[3]]} 

    def p_expressao_entrada(self,p):
        """expressao : ENTRADA '(' ')'"""
        p[0] = {'op': 'entrada', 'args': []}

    def p_expressao_funcao(self, p):
        """expressao_funcao : expressao_parametro
                            | expressao_funcao ',' expressao_parametro"""
        if len(p) == 2:
            p[0] = {'op': 'expressao_funcao', 'args': [p[1]]}
        else:
            p[1]['args'].append(p[3])
            p[0] = p[1]
            
    def p_expressao_parametro_id(self,p):
        """expressao_parametro : ID"""
        p[0] = {'op': 'parametro_id', 'args': [p[1]]} 
    
    def p_expressao_parametro_number(self,p):
        """expressao_parametro : NUMBER"""
        p[0] = {'op': 'parametro_number', 'args': [p[1]]} 
    
    def p_chama_funcao(self, p):
        """ expressao : ID '(' expressao_funcao ')'"""
        p[0] = {'op': 'chama_funcao', 'args': [p[1],p[3]]}
        
    # Fim da especificação da gramática 		
    def p_error(self, p):
        if p:
            print(f"Syntax error: unexpected '{p.type}'")
        else:
            print("Syntax error: unexpected end of file")
        exit(1)
  
    # def p_declaracao_funcao(self, p):
    #     """declaracao_funcao: FUNCAO ID'('lista_atribuicao')' = lista_expressoes ';'"""

    #def p_lista_atribuicao(self, p):