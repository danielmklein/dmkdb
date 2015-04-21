'''
Class that performs loading of data from file.
For CS 457 Final Project, Spring 2015.

Daniel Klein
'''

import os, os.path
import re

from Table import Table
from Database import Database

class DataLoader(object):
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        print("data loader initialized. data_dir is: {0}".format(data_dir))


    '''
    Parses data files, builds tables and builds and returns database.
    '''
    def load(self):
        print("load() was called. cool.")
        
        db = Database()
        
        for file_name in os.listdir(self.data_dir):
            table_name = re.match('[^\.]+', file_name).group()

            new_table = Table(table_name)

            print("table name is: {0}".format(table_name))
            
            full_path = os.path.join(self.data_dir, file_name)
            with open(full_path, 'r') as data_file:
                first_line = True

                for line in data_file:
                    elems = line.split()
                    
                    if (first_line): # name the columns from the filename plus numbering
                        num_columns = len(elems)
                        for i in range(1, num_columns+1):
                            new_table.add_column_name(table_name + str(i))
                        print(new_table.column_names)
                        first_line = False

                    #print(elems)

                    new_table.add_key(elems[0]) # first column value is pk
 
                    for elem_num in range(1, len(elems)):
                        col_name = table_name + str(elem_num+1)
                        new_table.add_value(col_name, elems[0], elems[elem_num])                    
                
            print(new_table.columns)

            db.add_table(new_table)

                    

        '''
        TODO:
        get table name from filename
        create column names from table name + numbers 1-n
        read each line of file, put key value in keys list of table,
        put other vals in columns dict under proper column and key
        '''


        return 5
