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
        self.empty_res = True


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
            condition = condition.replace(expr, result)
        print("condition is now {}".format(condition))
        return self.nested_bool_eval(condition)

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
        



    def create_token_lst(self, s):
        """create token list:
        'True or False' -> [True, lambda..., False]"""
        s = s.replace('(', ' ( ')
        s = s.replace(')', ' ) ')

        return [self.str_to_token[it] for it in s.split()]


    def find(self, lst, what, start=0):
        return [i for i,it in enumerate(lst) if it == what and i >= start]


    def parens(self, token_lst):
        """returns:
        (bool)parens_exist, left_paren_pos, right_paren_pos
        """
        left_lst = self.find(token_lst, '(')

        if not left_lst:
            return False, -1, -1

        left = left_lst[-1]

        #can not occur earlier, hence there are args and op.
        right = self.find(token_lst, ')', left + 4)[0]

        return True, left, right


    def bool_eval(self, token_lst):
        """token_lst has length 3 and format: [left_arg, operator, right_arg]
        operator(left_arg, right_arg) is returned"""
        return token_lst[1](token_lst[0], token_lst[2])


    def formatted_bool_eval(self, token_lst):
        """eval a formatted (i.e. of the form 'ToFa(ToF)') string"""
        if not token_lst:
            return self.empty_res

        if len(token_lst) == 1:
            return token_lst[0]

        has_parens, l_paren, r_paren = self.parens(token_lst)

        if not has_parens:
            return self.bool_eval(token_lst)

        token_lst[l_paren:r_paren + 1] = [self.bool_eval(token_lst[l_paren+1:r_paren])]

        return self.formatted_bool_eval(token_lst, bool_eval)


    def nested_bool_eval(self, s):
        """The actual 'eval' routine,
        if 's' is empty, 'True' is returned,
        otherwise 's' is evaluated according to parentheses nesting.
        The format assumed:
        [1] 'LEFT OPERATOR RIGHT',
        where LEFT and RIGHT are either:
                True or False or '(' [1] ')' (subexpression in parentheses)
        """
        return self.formatted_bool_eval(self.create_token_lst(s))
