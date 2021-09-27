from grammar.ast import *
import grammar.visitor as visitor
from random import randint
from utils import SemanticError

class Executor:
    def __init__(self):
        self.rolls = ''
        self.data = []

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(CommandNode)
    def visit(self, node):
        for roll in node.roll_list:
            dice_value = int(roll.dice[1:])
            if roll.num_dices < 1 or roll.num_dices > 100 or dice_value < 2 or dice_value > 100:
                continue
            self.rolls += (str(roll.num_dices) if roll.num_dices>1 else '') + roll.dice +':['
            self.visit(roll)
            self.rolls += '] \n'

    @visitor.when(RollNode)
    def visit(self, node):
        num_dices = node.num_dices
        dice_value = int(node.dice[1:])
        adv = sum([1 if isinstance(i, AdvantageNode) else 0 for i in node.mod_list])
        disadv = sum([1 if isinstance(i, DisadvantageNode) else 0 for i in node.mod_list])
        global_modifier = sum([ i.num for i in node.mod_list if isinstance(i, StarNode) and i.num<21])
        global_modifier -= sum([ j.num for j in node.mod_list if isinstance(j, DivNode) and j.num<21])

        if adv and disadv:
            raise SemanticError('Advantage and disadvantage cancel each other')
        if adv > 1:
            raise SemanticError('Advantage modiffiers aren\'t cumulative')
        if disadv > 1:
            raise SemanticError('Disadvantage modiffiers aren\'t cumulative')

        self.data.append([])
        current_roll_list = self.data[-1]
        for i in range(num_dices):
            roll = randint(1,dice_value)+global_modifier if not adv + disadv else (randint(1,dice_value)+global_modifier, randint(1,dice_value)+global_modifier, '!' if adv else '?')
            current_roll_list.append(roll)
            self.rolls += format(roll, dice_value, global_modifier )
            self.rolls += ', '
        else:
            self.rolls = self.rolls[:-2]
        
        plain_modifiers = [ i for i in node.mod_list if isinstance(i, PlusNode) or isinstance(i, MinusNode)]

        for mod in plain_modifiers:
            current_roll_list.append(mod.num if isinstance(mod, PlusNode) else -mod.num)

    @visitor.when(PlusNode)
    def visit(self, node):
        return int(node.number)
        
    @visitor.when(MinusNode)
    def visit(self, node):
        return int(node.number)

def format(roll, maxvalue = 20, global_mod = 0):
    if isinstance(roll, int):
        # natural one
        if roll == 1 + global_mod:
            return '<b>' + str(roll) + '</b>'
        
        # natural twenty
        elif roll == maxvalue+global_mod:
            return '<b>' + str(roll) + '</b>'
        
        else:
            return str(roll)
    
    else:   #[dis]advantageous case
        l_roll = format(roll[0], maxvalue, global_mod)
        r_roll = format(roll[1], maxvalue, global_mod)
        # return '(' + l_roll + ',' + r_roll + ')'
        case = roll[2]
        if case == '!':
            greater = max(roll[0], roll[1])
            x = '(' + ('<u>' if roll[0] == greater else '') + l_roll + ('</u>' if roll[0] == greater else '') + ',' + ('<u>' if roll[1] == greater else '') + r_roll + ('</u>' if roll[1] == greater else '') +')'
            return x
        elif case == '?':
            lesser = min(roll[0], roll[1])
            x = '(' + ('<u>' if roll[0] == lesser else '') + l_roll + ('</u>' if roll[0] == lesser else '') + ',' + ('<u>' if roll[1] == lesser else '') + r_roll + ('</u>' if roll[1] == lesser else '') +')'
            return x
