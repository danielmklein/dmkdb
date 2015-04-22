
class QueryExecutor(object):

    def __init__(self, db):
        self.db = db

    def parse_query(self, query):
        pass

    def perform_query(self, query):
        print("QueryExecutor.perform_query() called with query: {0}".format(query))

        ''' okay, what do we do here?
        uppercase entire query
        make sure it has select and from
        get list of columns from after select (or *) -- it might be agg func
        get table from after "from" 
        get and parse "where" clause, if present
        get and parse "order by" clause, if present
        '''
