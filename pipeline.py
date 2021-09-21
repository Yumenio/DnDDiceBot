from grammar.lexer import DiceLexer
from grammar.parser import DiceParser
from grammar.executor import Executor

class Pipeline:
    def __init__(self, data : str, verbose=False):
        self.data = data
        self.lexer = DiceLexer()
        self.parser = DiceParser()
        self.verbose = verbose


        if self.verbose:
            self.lexer.build()
            self.tokens = self.lexer.input(self.data)
            self.lexer = DiceLexer()

        self.ast = self.parser.parse(self.lexer, self.data)
        self.executor = Executor()
        self.executor.visit(self.ast)
        a = 0

    def getAnswer(self):
        return self.executor.rolls

if __name__ == '__main__':
    # data = 'd4+3! 3d20!+6'
    data = '20d8!'
    verbose = True

    pipeline = Pipeline(data, verbose)
    print(pipeline.getAnswer())