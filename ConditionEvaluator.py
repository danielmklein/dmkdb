# http://stackoverflow.com/questions/2467590/dynamically-evaluating-simple-boolean-logic-in-python
# adapt this for evaluating these expressions
# given a row, loop through it, replacing each inequality/equality with 'True' or 'False'
# then evaluate it with the code from above.
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
        simple_exprs = re.findall(r"\w+\s?[=<>]+\s?\d+", condition)
        print("condition starts out as: {}".format(condition))

        for expr in simple_exprs:
            result = self.simple_eval(row, expr)
            if "(" in condition:
                condition = condition.replace("(" + expr + ")", result)
            else:
                condition = condition.replace(expr, result)
        print("condition is now {}".format(condition))
        return self.eval_bool_expr(condition)
    # end evaluate_condition


    def simple_eval(self, row, expression):
        match = re.search(r"(\w+)\s?([=<>]+)\s?(\d+)", expression)

        if not match:
            raise Exception("found unexpected expression: {0}".format(match.group()))
  
        col_name = match.group(1).strip()
        op = match.group(2).strip()
        val = int(match.group(3).strip())
        #print ("col, op, val: {}, {}, {}".format(col_name, op, val))

        real_op = self.str_to_token[op]
        col_val = int(row[col_name])

        if (real_op(col_val, val)):
            print("{} {} {} is TRUE".format(col_val, op, val))
            return 'True'
        else:
            print("{} {} {} is FALSE".format(col_val, op, val))
            return 'False'
    # end simple_eval


    def build_token_list(self, expr_string):
        '''
        space things out nicely, then convert plain old strings
        into real Python tokens (True, False, or, and, etc)
        '''
        expr_string = expr_string.replace('(', ' ( ')
        expr_string = expr_string.replace(')', ' ) ')
        print("expr string is now: {}".format(expr_string))
        token_list = [self.str_to_token[item] for item in expr_string.split()]
        print("token string is: {}".format(expr_string.split()))

        return token_list
   # end build_token_list


    def find(self, token_list, token, start=0):
        '''
        given a token, return the indices at which that 
        token appears in the given token list
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

        left = left_list[-1]

        # cannot occur earlier, hence there are args and op.
        right = self.find(token_list, ')', left + 2)[0]

        return True, left, right
    # end find_parens


    def eval_simple_expr(self, token_list):
        '''
        token_list has length 3 and format: [left_arg, operator, right_arg]
        operator(left_arg, right_arg) is returned
        '''
        return token_list[1](token_list[0], token_list[2])
    # end eval_simple_expr


    def eval_formatted_expr(self, token_list, emp_res=True):
        '''
        eval a formatted (i.e. of the form 'ToFa(ToF)') string
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

