from grammar.lexer import DiceLexer
from grammar.parser import DiceParser
from grammar.executor import Executor

class Pipeline:
    def __init__(self, verbose=False):
        self.lexer = DiceLexer()
        self.parser = DiceParser()
        self.verbose = verbose


        if self.verbose:
            self.lexer.build()
            self.tokens = self.lexer.input(self.data)
            self.lexer = DiceLexer()

        # self.ast = self.parser.parse(self.lexer, self.data)
        # self.executor = Executor()
        # self.executor.visit(self.ast)

    def execute(self, data: str):
        self.ast = self.parser.parse(self.lexer, data)
        self.executor = Executor()
        self.executor.visit(self.ast)
        return self.getString(), self.getResult()

    def getString(self):
        return self.executor.rolls
    def getDices(self):
        return self.executor.data
    def getResult(self):
        data = self.getDices()
        acc = 0
        for rolls in data:
            for roll in rolls:
                if not isinstance(roll, int):
                    l,r,case = roll
                    acc += max(l,r) if case=='!' else min(l,r)
                else:
                    acc += roll
        return max(0,acc)

if __name__ == '__main__':
    data = '10!+3 d20?-1'
    # data = '2d8 + 3 - 4! 2d20?+6'
    verbose = False

    pipeline = Pipeline(verbose)
    pipeline.execute(data)
    print(pipeline.getString() + '  =   ' + str(pipeline.getResult()))