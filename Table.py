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
        self.keys = []
    
        # columns consists of dicts, each dict has key of a column name,
        # value of dict of pk-columnvalue key-value pairs.
        # for example: columns = {a1:{1:5, 4:67, 54, 99}, a2:{1:90, 6:75}}.
        self.columns = {}

   
    def add_column_name(self, col):
        if (col not in self.column_names):
            self.column_names.append(col)

        return


    def add_key(self, key):
        if (key not in self.keys):
            self.keys.append(key)
        
        return


    def add_value(self, col_name, key, value):
        # if column name dict not in column_names, add it
        # then, add val at columns[key]
        if (col_name not in self.column_names):
            raise Exception("invalid column name")

        if (col_name not in self.columns):
            self.columns[col_name] = {}

        self.columns[col_name][key] = value
        
        
