import re

class QueryExecutor(object):

    def __init__(self, db):
        self.db = db

    def parse_query(self, query):
        pass

    def perform_query(self, query):
        #print("QueryExecutor.perform_query() called with query: {0}".format(query))

        ''' okay, what do we do here?
        uppercase entire query
        make sure it has select and from
        get list of columns from after select (or *) -- it might be agg func
        get table from after "from" 
        get and parse "where" clause, if present
        get and parse "order by" clause, if present
        '''

        query = query.upper()

        if (not re.search(r"SELECT.+FROM.+", query)):
            print("invalid query: {0}".format(query))
            return None

        columns = re.search(r"SELECT\s+(.+)\s+FROM", query).group(1).trim()
        print("columns to fetch are: {0}".format(columns))
        
        table = re.search(r"FROM\s+([A-Z])\s+", query).group(1).trim()
        print("table to query is: {0}".format(table))

        conditions_match = re.search(r"WHERE\s+([^O;]+)", query)
        
        if (conditions_match):
            conditions = conditions_match.group(1).trim()
            print("conditions are: {0}".format(conditions))

        order_by_match = re.search(r"ORDER\s+BY\s+(.*)\s*;", query)
        if (order_by_match):
            order_by = order_by_match.group(1).trim()
            print("order by: {0}".format(order_by))

        print()


