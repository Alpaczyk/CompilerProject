from lark import Lark, Transformer

grammar = r"""
string: ESCAPED_STRING
%import common.ESCAPED_STRING
"""
parser = Lark(grammar, start = "string")
print(parser.parse(text='"Hello World"'))
def parse(text):
    print(parser.parse(text).pretty())

parse('"Hello World"')
grammarInt = r"""
expr: LB? expr ADD expr RB?
    | LB? expr MUL expr RB?
    | LB? expr DIV expr RB?
    | LB? expr SUB expr RB?
    | num
num: SIGNED_NUMBER
%import common.SIGNED_NUMBER
%ignore " "
LB: "("
RB: ")"
MUL: "*"
ADD: "+"
DIV: "/"
SUB: "-"
"""
parserInt = Lark(grammarInt, start = 'expr')
def parse_int(integer):
    print(parserInt.parse(integer).pretty())

parse_int('42 + 1')
parse_int('42 + 1 * 2')
parse_int('42 - 1 + 2')
parse_int('42 + 4 / 2')
parse_int('42 - (1 + 2)')




