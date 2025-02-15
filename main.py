from lark import Lark, Transformer

grammar = r"""
?expr: sum 

?sum: sum "+" product -> add
    | sum "-" product -> sub
    | product
    
?product: product "*" atom -> mul
    | product "/" atom -> div
    | atom
    
?atom: num
    | "(" sum ")"
    
?num: SIGNED_NUMBER -> num
%import common.SIGNED_NUMBER
%ignore " "
"""

class MyTransformer(Transformer):

    def num(self, value):
        (value, ) = value
        return int(value)

    def expr(self, value):
        return value

    def mul(self, items):
        if len(items) == 1:
            return items[0]
        return items[0] * items[1]

    def add(self, items):
        if len(items) == 1:
            return items[0]
        return items[0] + items[1]

    def div(self, items):
        if len(items) == 1:
            return items[0]
        return items[0] / items[1]

    def sub(self, items):
        if len(items) == 1:
            return items[0]
        return items[0] - items[1]


def parse(notation):
    transformer = MyTransformer()
    parser = Lark(grammar=grammar, start='expr')
    tree = parser.parse(notation)
    return transformer.transform(tree)

import unittest

class CalculatorTests(unittest.TestCase):

    def test_simple_adding(self):
        self.assertEqual(41 + 1, parse('41+1'))

    def test_simple_sub(self):
        self.assertEqual(41 - 1, parse('41-1'))

    def test_simple_mul(self):
        self.assertEqual(41 * 1, parse('41*1'))

    def test_simple_div(self):
        self.assertEqual(41 / 1, parse('41/1'))

    def test_all_operation_in_order(self):
        self.assertEqual(41 * 3 / 4 + 5 - 6, parse('41*3/4+5-6'))

    def test_all_operations_with_wrong_order(self):
        self.assertEqual(41 + 1 * 4 - 7 / 2, parse('41+1*4-7/2'))

    def test_ignoring_whitespace(self):
        self.assertEqual(41 +     1, parse('41+     1'))

    def test_with_brackets(self):
        self.assertEqual(41 * 3 / ((4 + 5) - 6), parse('41*3/((4+5)-6)'))

    def test_with_brackets_2(self):
        self.assertEqual((41 + 1) * (4 - 7) / 2, parse('(41+1)*(4-7)/2'))

    def test_big_adding(self):
        self.assertEqual(4100000 + 100000, parse('4100000+100000'))

    def test_big_sub(self):
        self.assertEqual(4100000 - 100000, parse('4100000-100000'))

    def test_big_mul(self):
        self.assertEqual(4100000 * 100000, parse('4100000*100000'))

    def test_big_div(self):
        self.assertEqual(4100000 / 100000, parse('4100000/100000'))

    def test_literal(self):
        self.assertEqual(42, parse('42'))

    def test_literal_minus(self):
        self.assertEqual(-42, parse('-42'))





