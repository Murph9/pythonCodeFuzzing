from __future__ import annotations # using self type hint doens't work
import random
import ast
import operator as op

BASE_STRING = "{0} {4} {1} {5} {2} {6} {3}"
OPERATORS = '+*-/'

operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}

class Subject:
    def __init__(self, args = None):
        self.args = args
        if not self.args:
            self.args = [
                random.randint(0, 100),
                random.randint(0, 100),
                random.randint(0, 100),
                random.randint(0, 100),
                random.choice(OPERATORS),
                random.choice(OPERATORS),
                random.choice(OPERATORS)
            ]

    @property
    def count(self):
        return len(self.args)

    def mutate(self, other: Subject, mut_rate: float) -> Subject:
        result = _mix_lists(self.args, other.args)
        for x in range(len(result)):
            if random.uniform(0, 1) < mut_rate:
                if isinstance(result[x], int):
                    result[x] = random.randint(0, 100)
                else:
                    result[x] = random.choice(OPERATORS)

        return Subject(args=result)

    def evaluate(self):
        _str = BASE_STRING.format(*self.args)
        try:
            return self._eval(ast.parse(_str, mode='eval').body)
        except ZeroDivisionError:
            return None

    def _eval(self, node):
        if isinstance(node, ast.Num): # <number>
            return node.n
        elif isinstance(node, ast.BinOp): # <left> <operator> <right>
            return operators[type(node.op)](self._eval(node.left), self._eval(node.right))
        elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
            return operators[type(node.op)](self._eval(node.operand))
        else:
            raise TypeError(node)

    def __str__(self):
        return f"'{BASE_STRING.format(*self.args)}' -> {self.evaluate()}"

def _mix_lists(list1, list2, ratio = 0.5):
    if len(list1) != len(list2):
        print("ERROR, lists not the same size")
        return None
    out = []
    for i in range(len(list1)):
        if ratio < random.uniform(0, 1):
            out.append(list1[i])
        else:
            out.append(list2[i])
    return out