'''
Class that performs loading of data from file.
For CS 457 Final Project, Spring 2015.

Daniel Klein
'''

from Table import Table
from Database import Database

class DataLoader(object):
    
    def __init__(self, data_dir):
        print("data loader initialized. data_dir is: {0}".format(data_dir))


    '''
    Parses data files, builds tables and builds and returns database.
    '''
    def load(self):
        print("load() was called. cool.")
        return 5
