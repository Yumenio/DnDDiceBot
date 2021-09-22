from grammar.lexer import DiceLexer
from grammar.lexer import _tokens
from grammar.ast import *
import ply.yacc as yacc
import ply.lex as lt
tokens = _tokens

precedence = (
    ( 'left', 'plus', 'minus'),
    ( 'nonassoc', 'adv', 'disadv'),
)
errors = []
class DiceParser:
    def parse(self, lexer, program):
        self.tokens = _tokens
        self.lexer = lexer
        self.lexer.build()
        ast = self.parser.parse(program)
        self.errors = errors
        return ast
    
    def find_column(input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1  
    
    def p_command(p):
        '''command : roll_list
                        | mod_list
                        |
        '''
        if len(p) == 1:
            p[0] = CommandNode( [RollNode('d20', [])])
        elif isinstance(p[1][0], RollNode):
            p[0] = CommandNode(p[1])
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = CommandNode( [RollNode('d20', p[1])])

    def p_roll_list(p):
        '''roll_list : roll
                    | roll roll_list
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_roll(p):
        ''' roll : number dice mod_list
                    | number dice
                    | dice mod_list
                    | dice
        '''
        if len(p) == 4:
            p[0] = RollNode(p[2], p[3], p[1])
        elif len(p) == 3:
            if not isinstance(p[1], int):
                p[0] = RollNode(p[1], p[2])
            else:
                p[0] = RollNode(p[2], [], p[1])
        else:
            p[0] = RollNode(p[1], [])
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_mod_list(p):
        ''' mod_list : mod
                        | mod mod_list
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_mod(p):
        ''' mod : plus number
                        | minus number
                        | star number
                        | adv
                        | disadv
        '''
        if len(p) == 1:
            p[0] = []
            return
        elif p[1] == '+':
            p[0] = PlusNode(p[2])
        elif p[1] == '-':
            p[0] = MinusNode(p[2])
        elif p[1] == '*':
            p[0] = StarNode(p[2])
        elif p[1] == '!':
            p[0] = AdvantageNode()
        elif p[1] == '?':
            p[0] = DisadvantageNode()

        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
            

    # Compute column.
    #   input is the input text string
    #   token is a token instance
    #parentesis?

    def p_error(p):
        global errors
        def find_column(input, token):
            line_start = input.rfind('\n', 0, token.lexpos) + 1
            return (token.lexpos - line_start) + 1  #parentesis?

        if not p:
            errors.append(SyntacticError % (0,0,'EOF'))
            return

        token_column = find_column(p.lexer.lexdata, p)
        # errors.append(_SyntacticError % (p.lineno, token_column, p.value))
        SyntacticError = '(%d, %d) - SyntacticError: ERROR at or near "%s"'
        print(SyntacticError % (p.lineno, token_column, p.value))
        # print(f'({p.lineno}, {token_column}) - SyntacticError: ERROR at or near "{p.value}"')
        

    parser = yacc.yacc(debug = True)
