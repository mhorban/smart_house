# Copyright (C) Marian Horban - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Marian Horban <m.horban@gmail.com>

from pyparsing import Literal, CaselessLiteral, Word, Combine, Group, Optional, \
    ZeroOrMore, Forward, nums, alphas
import math
import operator


class RuleParser(object):
    # map operator symbols to corresponding arithmetic operations
    opn = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "^": operator.pow,
        "OR": operator.or_,
        "AND": operator.and_,
        "NOT": operator.not_,
        "==": operator.eq,
        "!=": operator.ne,
        ">=": operator.ge,
        ">": operator.gt,
        "<=": operator.le,
        "<": operator.lt,
    }
    fn = {"sin": math.sin,
          "cos": math.cos,
          "tan": math.tan,
          "abs": abs,
          "trunc": lambda a: int(a),
          "round": round}

    def __init__(self, get_sensor_value_func):
        self.exprStack = []
        self.bnf = None
        self.get_sensor_value_func = get_sensor_value_func

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def get_sensor_value(self, strg, loc, toks):
        #get sensor value by sensor name toks[0]
        print "get sensor value for ", toks[0]
        val = self.get_sensor_value_func(toks[0])
        return str(val)

    def BNF(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        #global bnf
        if not self.bnf:
            point = Literal(".")
            fnumber = Combine(Word("+-" + nums, nums) +
                              Optional(point + Optional(Word(nums))))
            ident = Word(alphas, alphas + nums + "_$")
            sensor_ident = (CaselessLiteral('GET_SENSOR_VAL:').suppress() +
                            Word(alphas + nums + "_$")).setParseAction(self.get_sensor_value)

            and_ = CaselessLiteral('AND')
            or_ = CaselessLiteral('OR')
            not_ = CaselessLiteral('NOT')
            neq = CaselessLiteral('!=')
            lt = Literal('<')
            eqlt = CaselessLiteral('<=')
            gt = Literal('>')
            eqgt = CaselessLiteral('>=')
            eq = CaselessLiteral('==')

            plus = Literal("+")
            minus = Literal("-")
            mult = Literal("*")
            div = Literal("/")
            lpar = Literal("(").suppress()
            rpar = Literal(")").suppress()
            add_op = plus | minus
            mult_op = mult | div
            cmp_op = eqlt | eqgt | eq | neq | lt | gt

            expr = Forward()
            atom = (Optional("-") + (fnumber | sensor_ident | ident + lpar + expr + rpar).setParseAction(self.pushFirst) | (
                    lpar + expr.suppress() + rpar)).setParseAction(self.pushUMinus)

            term = atom + ZeroOrMore((mult_op + atom).setParseAction(self.pushFirst))
            add_exp = term + ZeroOrMore((add_op + term).setParseAction(self.pushFirst))
            cmp_exp = add_exp + ZeroOrMore((cmp_op + add_exp).setParseAction(self.pushFirst))
            cmp_not_exp = cmp_exp + ZeroOrMore((not_ + cmp_exp).setParseAction(self.pushFirst))
            cmp_not_and_exp = cmp_not_exp + ZeroOrMore((and_ + cmp_not_exp).setParseAction(self.pushFirst))
            cmp_not_and_or_exp = cmp_not_and_exp + ZeroOrMore((or_ + cmp_not_and_exp).setParseAction(self.pushFirst))
            expr << cmp_not_and_or_exp
            self.bnf = expr
        return self.bnf

    def evaluateStack(self, s):
        op = s.pop()
        #print "OP = ", op
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op == "NOT":
            return self.opn[op](self.evaluateStack(s))
        if op in self.opn:#"+-*/^<>":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def compute(self, string):
        self.exprStack = []
        results = self.BNF().parseString(string)
        val = self.evaluateStack(self.exprStack[:])
        return val




