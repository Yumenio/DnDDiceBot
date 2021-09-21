class Node:
    pass

class CommandNode(Node):
    def __init__(self, roll_list):
        self.roll_list = roll_list

class DeclarationNode(Node):
    pass
class ExpressionNode(Node):
    pass

class RollNode(Node):
    def __init__(self, dice, mod_list, num_dices=1):
        self.dice = dice
        self.mod_list = mod_list
        self.num_dices = num_dices

class AdvantageNode(Node):
    pass
class DisadvantageNode(Node):
    pass

class PlusNode(Node):
    def __init__(self, num):
        self.num = num
class MinusNode(Node):
    def __init__(self, num):
        self.num = num

class NumNode(Node):
    pass