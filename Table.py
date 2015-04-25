'''
Class representing a database table for 
CS 457 Final Project

Daniel Klein
Spring 2015
'''

class Table(object):


    def __init__(self, table_name):
        self.name = table_name
        self.column_names = []
    
        # each row is keyed on TS, contains dict containing
        # col name-data val pairs
        self.rows = {} 

   
    def add_column_name(self, col):
        if (col not in self.column_names):
            self.column_names.append(col)

        return


    def add_value(self, key, col_name, value):
        # if column name dict not in column_names, add it
        # then, add val at columns[key]
        
        if (col_name not in self.column_names):
            raise Exception("invalid column name.")

        if (key not in self.rows):
            self.rows[key] = {}
        
        self.rows[key][col_name] = value

        
        
