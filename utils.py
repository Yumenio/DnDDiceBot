help_message ='''
Usage: /d [num]d[faces] [+num, -num, *num, /num, !, ?]

+num, - num: modify the final result accordingly
*num: adds num to all the corresponding rolls, and shows them modified
/num: same as *num but substracting num instead of adding num
!: advantage modifier
?: disadvantage modifier

e.g.:    /d d20!+5 [(<u>19</u>,18)] = 24, 
            /d 6d6+6 [1,2,5,2,4,6] = 26, 
            /d 3d20!*6-1 [(<u>16</u>,<b>7</b>), (<u><b>7</b></u>,<u><b>7</b></u>), (<u><b>26</b></u>,5)] = 48, 
            /d ?+1 [(<u><b>1</b></u>, 16)] = 2
'''

WHITELIST = [
    -533675535,
    564213106,
    -1001454846017,
    -704972513
]

class SyntacticError(Exception):
    pass

class SemanticError(Exception):
    pass