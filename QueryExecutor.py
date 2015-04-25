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
        
        table = re.search(r"FROM\s+([A-Z])\s+", query).group(1).strip()
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


    def perform_query(self, query):
        query_params = self.parse_query(query) # (columns, table, conditions, order_by)

        if (query_params is None):
            return None, None

        col_names = query_params[0]
        table_name = query_params[1]
        conditions = query_params[2]
        order_by = query_params[3]

        result = []

        if (table_name not in self.db.tables.keys()):
            raise Exception("invalid table name in query: {0}".format(query))

        # set the name of the table to use
        data_table = self.db.tables[table_name]

        # set the columns we are gonna use
        if (len(col_names) == 1 and col_names[0] == "*"):
            col_names = data_table.column_names

        if (conditions):
            # evaluate the conditional expression -- filter out tuples
            evaluator = ConditionEvaluator()
            selected_tuples = {}
       
            for key in data_table.rows.keys():
                cur_row = data_table.rows[key]
                if (evaluator.evaluate_condition(cur_row, conditions)):
                    print("column {0} matches condition, added to result".format(cur_row))
                    selected_tuples[key] = cur_row

        # sort by the column we wish to order by
        sorted_tuples = []
        for key in selected_tuples.keys():
            row = []
            for col in data_table.column_names:
                row.append(int(selected_tuples[key][col]))
            sorted_tuples.append(row)
        
        if (order_by):
            sort_idx = data_table.column_names.index(order_by)
            sorted_tuples.sort(key = lambda tup: tup[sort_idx])

        # project the columns we want
        print("we want columns: {0}".format(col_names))
        for col in col_names:
            if (col not in data_table.column_names):
                raise Exception("invalid column name: {0}".format(col))

        projected = []
        col_indexes = []
        for col in col_names:
            col_indexes.append(data_table.column_names.index(col))

        for row in sorted_tuples:
            projected_row = []
            for col_idx in col_indexes:
                projected_row.append(row[col_idx])
            projected.append(projected_row)

        print("results: {0}".format(projected))

        return col_names, projected
            
        



