import ply.lex as lex

class FCALexer:
    tokens = (
        'ID', 'NUMBER', 'PLUS', 'TIMES', 'MINUS', 'LPAREN', 'RPAREN', 'EQUALS', 'SEMICOLON', 
        'ESCREVER', 'FUNCAO', 'FIM', 'COLON', 'COMMA'
    )
    literals = ['+', '*', '-', '(', ')', '=', ';', ':', ',']

    t_ignore = ' \t\n'  # Ignore whitespace and tabs

    def t_ESCREVER(self, t):
        r'ESCREVER'
        return t

    def t_FUNCAO(self, t):
        r'FUNCAO'
        return t
    
    def t_FIM(self, t):
        r'FIM'
        return t

    def t_COLON(self, t):
        r':'
        return t

    def t_COMMA(self, t):
        r','
        return t

    def t_LPAREN(self, t):
        r'\('
        return t

    def t_RPAREN(self, t):
        r'\)'
        return t

    def t_EQUALS(self, t):
        r'='
        return t

    def t_SEMICOLON(self, t):
        r';'
        return t

    def t_PLUS(self, t):
        r'\+'
        return t

    def t_MINUS(self, t):
        r'-'
        return t

    def t_TIMES(self, t):
        r'\*'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
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