import ply.lex as lex

reserved = {}

_tokens = [
    'space',
    'number',
    'plus',
    'minus',
    'star',
    'div',
    'tab',
    'newline',
    'adv',
    'disadv',
    'dice'
]
_tokens += list(reserved.values())

def find_all(s):
    b = [] 
    a = s.find('a')
    while a != -1:
        b.append(a)
        a = s.find('a', a + 1)
    return b

def find_last(text, row, col):
    first = text.find("\n")
    temp_text = text
    add_col= first
    add_row = 0
    loop = True
    while loop:
        if first > 0:
            if temp_text[first-1] == "\\":
                temp_text = temp_text[first+1: ]
                add_col = first
                first = temp_text.find("\n")
                add_row += 1
                loop = True
            else:
                loop = False
                if first + 1 == len(temp_text):
                    eof = True
                else:
                    eof = False
        else:
            # cuando no hay newline
            if first == -1:
                add_col = len(temp_text) + 1
                eof = True
            # cuando hay newline pero al inicio :)
            else:
                add_col = 0
                eof = False
            break
                
    if add_row == 0:
        add_col += col
    add_row += row
    return (add_row, add_col, eof)

class DiceLexer:
    tokens = _tokens
    col = 0
    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.col = 0

    # Compute column.
    #   input is the input text string
    #   token is a token instance
    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1  #parentesis?

    t_ignore_space = r'[ ]+'

    def t_number(self, t):
        r'\d+'
        t.value = int(t.value)
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    def t_opar(self, t):
        r'\('
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    
    def t_cpar(self, t):
        r'\)'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    def t_plus(self,t):
        r'\+'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    def t_minus(self,t):
        r'\-'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
    
    def t_star(self,t):
        r'\*'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    def t_div(self,t):
        r'/'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    def t_adv(self,t):
        r'\!'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t
        
    def t_disadv(self,t):
        r'\?'
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    # t_ignore_tab = r'\t+'
    def t_tab(self, t):
        r'\t+'
        self.col += 4*len(t.value)
        # t.lexer.skip(len(t.value))

    def t_dice(self, t):
        r'd\d+'
        if t.value.lower() in reserved:
            t.type = reserved[t.value.lower()]
        t.col = self.find_column(t.lexer.lexdata,t) + (self.col - self.col//4)
        return t

    def t_eof(self, t):
        a = 0
    
    # Error handling rule
    def t_error(self,t):
        # errores del string
        # if t.value[0] == '"':
        #     row, col, eof = find_last(t.value, t.lexer.lineno, self.find_column(t.lexer.lexdata,t))
        #     if eof:
        #         self.errors.append(LexicographicError % (row, col, f'EOF in string constant'))
        #         t.lexer.skip(len(t.value))
        #     else:
        #         self.errors.append(LexicographicError % (row, col, f'Unterminated string constant'))
        # else:
        # self.errors.append(_LexicographicError % (t.lexer.lineno, self.find_column(t.lexer.lexdata,t), f'ERROR "{t.value[0]}"'))
        # print(LexicographicError % (t.lexer.lineno, self.find_column(t.lexer.lexdata,t), f'ERROR "{t.value[0]}"'))
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.errors = []
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)
        self.tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            self.tokens.append(tok)
        
        return self.tokens