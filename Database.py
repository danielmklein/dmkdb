'''
Class representing database for
CS 457 Final Project

Daniel Klein
Spring 2015
'''


class Database(object):

    def __init__(self):
        self.tables = {} # tables is a dict of tablename:table key-val pairs

    def add_table(self, table):
        self.tables[table.name] = table

        return
