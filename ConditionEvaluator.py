'''
This class takes care of evaluating logical expressions from database queries.
Given a row and a condition, evaluate_condition will return whether or not that
row meets the condition. This is for the CS 457 Final Project.

Daniel Klein
Spring 2015
'''
import re

class ConditionEvaluator(object):

    def __init__(self):
        self.str_to_token = {'True':True,
                'False':False,
                'AND':lambda left, right: left and right,
                'OR':lambda left, right: left or right,
                '=':lambda left, right: left == right,
                '<>':lambda left, right: left != right,
                '<':lambda left, right: left < right,
                '>':lambda left, right: left > right,
                '<=':lambda left, right: left <= right,
                '>=':lambda left, right: left >= right,
                '(':'(',
                ')':')'}
    # end __init__


    def evaluate_condition(self, row, condition):
        '''
        use regex to find all simple expressions and evaluate them on the row in question
        replace each one with 'True' or 'False' STRINGS, then evaluate resulting string 
        with nested_bool_eval
        '''
        simple_exprs = re.findall(r"\(?\w+\s?[=<>]+\s?\d+\)?", condition)

        for expr in simple_exprs:
            if "(" in expr:
                trimmed_expr = expr.replace("(", "")
                trimmed_expr = trimmed_expr.replace(")", "")
            else:
                trimmed_expr = expr

            if ("(" in expr) and not (")" in expr):
                expr = expr.replace("(", "")
            if (")" in expr) and not ("(" in expr):
                expr = expr.replace(")", "")

            result = self.simple_eval(row, trimmed_expr)

            condition = condition.replace(expr, result)

        return self.eval_bool_expr(condition)
    # end evaluate_condition


    def simple_eval(self, row, expression):
        '''
        given a simple expression of the form COLNAME OPERATOR VALUE,
        we return a string 'True'/'False' result
        '''

        match = re.search(r"(\w+)\s?([=<>]+)\s?(\d+)", expression)

        if not match:
            raise Exception("found unexpected expression: {0}".format(match.group()))
  
        col_name = match.group(1).strip()
        op = match.group(2).strip()
        val = int(match.group(3).strip())

        if (col_name not in row.keys()):
            raise Exception("Invalid column name in: {}".format(expression))

        # convert the string operator into a real Python operator
        real_op = self.str_to_token[op]
        col_val = int(row[col_name])

        # since we converted the operator to a Python operator,
        # we can call it like a function to evaluate the condition now
        if (real_op(col_val, val)):
            return 'True'
        else:
            return 'False'
    # end simple_eval


    def build_token_list(self, expr_string):
        '''
        space things out nicely, then convert plain old strings
        into real Python tokens (True, False, or, and, etc)
        '''
        expr_string = expr_string.replace('(', ' ( ')
        expr_string = expr_string.replace(')', ' ) ')
        token_list = [self.str_to_token[item] for item in expr_string.split()]

        return token_list
   # end build_token_list


    def find(self, token_list, token, start=0):
        '''
        given a token, return the indices at which that 
        token first appears in the given token list
        '''
        return [i for i, item in enumerate(token_list) if item == token and i >= start]
    # end find


    def find_parens(self, token_list):
        '''
        returns:
        (bool)parens_exist, left_paren_pos, right_paren_pos
        '''
        left_list = self.find(token_list, '(')

        if not left_list:
            return False, -1, -1

        # take the last open paren
        left = left_list[-1]

        # find the corresponding close paren
        # cannot occur earlier, hence there are args and op.
        right = self.find(token_list, ')', left + 2)[0]

        return True, left, right
    # end find_parens


    def eval_simple_expr(self, token_list):
        '''
        token_list[1] will be either AND or OR, which we can evaluate
        as a function on the two operands, which will each be either True or False
        '''
        return token_list[1](token_list[0], token_list[2])
    # end eval_simple_expr


    def eval_formatted_expr(self, token_list, emp_res=True):
        '''
        this recursively evaluates an expression that has been properly formatted
        '''
        if not token_list:
            return emp_res

        if len(token_list) == 1:
            return token_list[0]

        has_parens, l_paren, r_paren = self.find_parens(token_list)

        if not has_parens:
            return self.eval_simple_expr(token_list)

        token_list[l_paren:r_paren + 1] = [self.eval_simple_expr(token_list[l_paren+1:r_paren])]

        return self.eval_formatted_expr(token_list, self.eval_simple_expr)
    # end formatted_bool_eval


    def eval_bool_expr(self, s):
        '''
        the function that evaluates a logical expression string
        '''
        return self.eval_formatted_expr(self.build_token_list(s))
    # end nested_bool_eval


