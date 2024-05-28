import ply.lex as lex

class FCALexer:
    tokens = (
        'ID', 'NUMBER', 'STRING', 'PLUS', 'TIMES', 'MINUS', 'LPAREN', 'RPAREN', 'EQUALS', 'SEMICOLON', 
        # Novas adições
        'ESCREVER', 'COMENTARIOS', "CONCAT", "FUNCAO", "FIM", "MAP", "FOLD"
    )
    literals = ['+', '*', '-', '(', ')', '=', ';', ',',':']

    # t_PLUS = r'\+'
    # t_TIMES = r'\*'
    # t_MINUS = r'-'
    # t_LPAREN = r'\('
    # t_RPAREN = r'\)'
    # t_EQUALS = r'='
    # t_SEMICOLON = r';'
    # Remover

    t_ignore = ' \n'

    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        t.value = t.value[1:-1]  # remove aspas
        return t

    #Novas adições
    def t_ESCREVER(self, t):
        r'[Ee]SC(REVER)?'
        return t
    
    def t_COMENTARIOS(self, t):
        r'--.*|{-.*\n*-}'
        return t
    
    def t_CONCAT(self, t):
        r'<>'
        return t
    
    def t_FUNCAO(self, t):
        r'FUNCAO'
        return t
    
    def t_FIM(self, t):
        r'FIM'
        return t
    
    def t_MAP(self, t):
        r'[Mm]ap'
        return t
    
    def t_FOLD(self, t):
        r'[Ff]OLD'
        return t
    #---------------------------------------------------

    def t_ID(self, t):
        r'[a-z_][a-zA-Z_0-9]*[!?]?'
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        token = self.lexer.token()
        return token if token is None else token.type