import re

from ConditionEvaluator import ConditionEvaluator

class QueryExecutor(object):

    def __init__(self, db):
        self.db = db

    def parse_query(self, query):
        #print("QueryExecutor.perform_query() called with query: {0}".format(query))

        query = query.upper()

        if (not re.search(r"SELECT.+FROM.+", query)):
            print("invalid query: {0}".format(query))
            return None

        columns = re.search(r"SELECT\s+(.+)\s+FROM", query).group(1).strip()
        columns = [col.strip() for col in columns.split(",")]
        print("columns to fetch are: {0}".format(columns))
        
        table = re.search(r"FROM\s+([A-Z])\s*", query).group(1).strip()
        print("table to query is: {0}".format(table))

        conditions_match = re.search(r"WHERE\s+([ABCDNOR()=<>0-9 ]+)(ORDER BY.*)?;", query)
        
        conditions = None
        if (conditions_match):
            conditions = conditions_match.group(1).strip()
            print("conditions are: {0}".format(conditions))

        order_by = None
        order_by_match = re.search(r"ORDER\s+BY\s+(.*)\s*;", query)
        if (order_by_match):
            order_by = order_by_match.group(1).strip()
            print("order by: {0}".format(order_by))

        print()

        return (columns, table, conditions, order_by)
    # end parse_query
    


    def perform_query(self, query):
        query_params = self.parse_query(query) # (columns, table, conditions, order_by)

        if (query_params is None):
            return None, None

        col_names = query_params[0]
        table_name = query_params[1]
        conditions = query_params[2]
        order_by = query_params[3]

        if (table_name not in self.db.tables.keys()):
            raise Exception("invalid table name in query: {0}".format(query))

        # set the name of the table to use
        data_table = self.db.tables[table_name]

        # this is a dict
        selected_tuples = self.select(conditions, data_table) 

        # this is a list of lists
        sorted_tuples = self.sort(data_table.column_names, selected_tuples, order_by) 

        # set the columns we are gonna use
        if (len(col_names) == 1 and col_names[0] == "*"):
            col_names = data_table.column_names

        # project the columns we want
        print("we want columns: {0}".format(col_names))
        
        if (len(col_names) == 1 and re.search(r"[A-Z]+\([A-Z0-9]+\)", col_names[0])):
            agg_match = re.search(r"([A-Z]+)\(([A-Z0-9]+)\)", col_names[0])
            agg_func = agg_match.group(1).strip()
            agg_col = agg_match.group(2).strip()
            print("we want to find the {} of column {}".format(agg_func, agg_col))
            result = self.perform_aggregate(agg_func, agg_col, data_table.column_names, sorted_tuples)
        else:

            for col in col_names: # TODO: MAKE SURE WE DO AVG!!
                if (col not in data_table.column_names):
                    raise Exception("invalid column name: {0}".format(col))

            result = self.project(col_names, data_table.column_names, sorted_tuples)
 
        print("results: {0}".format(result))

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
                if (evaluator.evaluate_condition(cur_row, conditions)):
                    print("column {0} matches condition, added to result".format(cur_row))
                    selected_tuples[key] = cur_row
        else:
            selected_tuples = data_table.rows

        return selected_tuples
    # end select

    
    '''
    project the columns specified in the SELECT clause
    '''
    def project(self, proj_cols, all_col_names, tuples):
        projected = []
        col_indexes = []
        for col in proj_cols:
            col_indexes.append(all_col_names.index(col))

        for row in tuples:
            projected_row = []
            for col_idx in col_indexes:
                projected_row.append(row[col_idx])
            projected.append(projected_row)

        return projected
    # end project
            
    
    def sort(self, col_names, unordered_tuples, order_by):
        # sort by the column we wish to order by
        sorted_tuples = []
        for key in unordered_tuples.keys():
            row = []
            for col in col_names:
                row.append(int(unordered_tuples[key][col]))
            sorted_tuples.append(row)
        
        if (order_by):
            sort_idx = col_names.index(order_by)
            sorted_tuples.sort(key = lambda tup: tup[sort_idx])
        
        return sorted_tuples
    # end sort

  
    def perform_aggregate(self, func_name, col, col_names, tuples,):
        
        if func_name != "AVG":
            raise Exception("aggregate function: {} is not supported.".format(func_name))

        col_index = col_names.index(col)
        sum = 0

        for row in tuples:
            sum += row[col_index]

        if len(tuples) == 0:
            result = []
        else:
            result = [["{0:.2f}".format(sum/len(tuples))]]
            for num in result:
                print("avg: {}".format(num))

        return result
    # end perform_aggregate



