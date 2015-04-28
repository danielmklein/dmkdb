'''
This class takes care of parsing and executing database queries.
For CS 457 Final Project.

Daniel Klein
Spring 2015
'''

import re

from ConditionEvaluator import ConditionEvaluator

class QueryExecutor(object):

    def __init__(self, db):
        self.db = db

    '''
    Parse the given query to determine what table, columns, conditions, and sort condition.
    '''
    def parse_query(self, query):

        query = query.upper() # upper case for safety!

        # query must at least have a SELECT and a FROM
        if (not re.search(r"SELECT.+FROM.+", query)):
            print("INVALID QUERY: {0}".format(query))
            return None

        # what columns is the query asking for?
        columns = re.search(r"SELECT\s+(.+)\s+FROM", query).group(1).strip()
        columns = [col.strip() for col in columns.split(",")]
        
        # what table are we querying?
        table = re.search(r"FROM\s+([A-Z])\s*", query).group(1).strip()

        # what logical conditions do we want to select on?
        conditions_match = re.search(r"WHERE\s+([ABCDNOR()=<>0-9 ]+)(ORDER BY.*)?;", query)
        conditions = None
        if (conditions_match):
            conditions = conditions_match.group(1).strip()

        # how do we order the results?
        order_by = None
        order_by_match = re.search(r"ORDER\s+BY\s+(.*)\s*;", query)
        if (order_by_match):
            order_by = order_by_match.group(1).strip()

        return (columns, table, conditions, order_by)
    # end parse_query
    

    '''
    Perform the given query on the database.
    '''
    def perform_query(self, query):
        query_params = self.parse_query(query) # (columns, table, conditions, order_by)

        if (query_params is None):
            return None, None # represents Null column names and Null result
        else:
            (col_names, table_name, conditions, order_by) = query_params

        if (table_name in self.db.tables.keys()):
            # set the name of the table to use
            data_table = self.db.tables[table_name]
        else:
            raise Exception("Invalid table name in query: {0}".format(query))

        # if it's 'SELECT *' we use all of the columns
        if (len(col_names) == 1 and col_names[0] == "*"):
            col_names = data_table.column_names

        # select returns a dictionary, structured just like the original data_table,
        # containing only the rows that match the select conditions
        selected_tuples = self.select(conditions, data_table) 

        # sort converts the dictionary into a list of row lists
        # sorted on whatever the order by column is
        sorted_tuples = self.sort(data_table.column_names, selected_tuples, order_by) 

        # we might have an aggregate function in the query      
        if (len(col_names) == 1 and re.search(r"[A-Z]+\([A-Z0-9]+\)", col_names[0])):
            agg_match = re.search(r"([A-Z]+)\(([A-Z0-9]+)\)", col_names[0])
            agg_func = agg_match.group(1).strip()
            agg_col = agg_match.group(2).strip()

            result = self.perform_aggregate(agg_func, agg_col, data_table.column_names, sorted_tuples)
        else:
            # check listed column names for validity
            for col in col_names:
                if (col not in data_table.column_names):
                    raise Exception("Invalid column name: {0}".format(col))

            # project gives us only the columns we asked for
            result = self.project(col_names, data_table.column_names, sorted_tuples)

        return col_names, result
    # end perform_query

    
    '''
    select the tuples that match the WHERE conditions
    '''
    def select(self, conditions, data_table):
        selected_tuples = {}
        if (conditions):
            # evaluate the conditional expression -- filter out tuples
            evaluator = ConditionEvaluator()
            
            for key in data_table.rows.keys():
                cur_row = data_table.rows[key]
                # if the row matches the condition, add it to the result set
                if (evaluator.evaluate_condition(cur_row, conditions)):
                    selected_tuples[key] = cur_row
        else: # if no conditions, just return all rows
            selected_tuples = data_table.rows

        return selected_tuples
    # end select

    
    '''
    project the columns specified in the SELECT clause
    '''
    def project(self, proj_cols, all_col_names, tuples):
        
        # since we're dealing with lists, we need to find the
        # indices of the columns we want
        col_indexes = []
        for col in proj_cols:
            col_indexes.append(all_col_names.index(col))
   
        projected = []
        for row in tuples:
            projected_row = []
            for col_idx in col_indexes:
                projected_row.append(row[col_idx])
            projected.append(projected_row)

        return projected
    # end project
            
    '''
    sort the given rows by the given 'ORDER BY' column
    '''
    def sort(self, col_names, unordered_tuples, order_by):
        # first we convert dictionary to list of lists in order to sort
        sorted_tuples = self.data_dict_to_row_list(col_names, unordered_tuples)

        if (order_by):
            if (order_by not in col_names):
                raise Exception("Invalid column name in ORDER BY clause")
            else:
                sort_idx = col_names.index(order_by)
                sorted_tuples.sort(key = lambda tup: tup[sort_idx])
        
        return sorted_tuples
    # end sort


    '''
    Just walk through the dict, plopping each entry into a list,
    and plop each new list a big list representing the db table.
    '''
    def data_dict_to_row_list(self, col_names, data_dict):
        rows = []
        for key in data_dict.keys():
            row = []
            for col in col_names:
                row.append(int(data_dict[key][col]))
            rows.append(row)
        
        return rows
    # end data_dict_to_row_list

  
    def perform_aggregate(self, func_name, col, col_names, tuples,):
        
        if func_name != "AVG": # yep, only AVG. 
            raise Exception("Aggregate function: {} is not supported.".format(func_name))

        if col not in col_names:
            raise Exception("Invalid column name in AVG function.")
        else:
            col_index = col_names.index(col)
        
        sum = 0
        for row in tuples:
            sum += row[col_index]

        if len(tuples) == 0: # no divide by zero here, no sir!
            result = []
        else:
            # stick the result in a string because whatever
            result = [["{0:.2f}".format(sum/len(tuples))]]

        return result
    # end perform_aggregate



