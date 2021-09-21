from grammar.ast import *
import grammar.visitor as visitor
from random import randint

class SemanticError(Exception):
    pass

class Executor:
    def __init__(self):
        self.rolls = ''

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(CommandNode)
    def visit(self, node):
        for roll in node.roll_list:
            self.rolls += ' ['
            self.visit(roll)
            self.rolls += '] '

    @visitor.when(RollNode)
    def visit(self, node):
        num_dices = node.num_dices
        adv = sum([1 if isinstance(i, AdvantageNode) else 0 for i in node.mod_list])
        disadv = sum([1 if isinstance(i, DisadvantageNode) else 0 for i in node.mod_list])

        if adv and disadv:
            raise SemanticError('Advantage and disadvantage cancel each other')
        if adv > 1:
            raise SemanticError('Advantage modiffiers aren\'t cummulative')
        if disadv > 1:
            raise SemanticError('Disadvantage modiffiers aren\'t cummulative')

        for i in range(num_dices):
            self.rolls += format( randint(0,20) if not adv + disadv else (randint(0,20), randint(0,20)) )
            self.rolls += ', '
        else:
            self.rolls = self.rolls[:-2]

    @visitor.when(PlusNode)
    def visit(self, node):
        return int(node.number)
        
    @visitor.when(MinusNode)
    def visit(self, node):
        return int(node.number)

def format(roll):
    if isinstance(roll, int):
        # tg doesn't support colored font :"D
        # if roll == 1:
        #     return color.RED + str(roll) + color.END
        # elif roll == 20:
        #     return color.GREEN + str(roll) + color.END

        if roll == 1:
            return color.BOLD + str(roll) + color.END
        elif roll == 20:
            return color.BOLD + str(roll) + color.END
        else:
            return str(roll)
    
    else:   #[dis]advantageous case
        l_roll = format(roll[0])
        r_roll = format(roll[1])
        return '(' + l_roll + ',' + r_roll + ')'

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'