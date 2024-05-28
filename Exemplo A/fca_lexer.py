import ply.lex as lex

class FCALexer:
    tokens = (
        'VAR_ID', 'NUM', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'EQUALS', 'LPAREN', 'RPAREN', 'SEMICOLON'
    )

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_EQUALS = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_SEMICOLON = r';'
    t_ignore = ' \t'

    def t_VAR_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*[\?\!]?'
        return t

    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()