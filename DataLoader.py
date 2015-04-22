'''
Class that performs loading of data from file.
For CS 457 Final Project, Spring 2015.

Daniel Klein
'''

import os, os.path
import re

from Table import Table
from Database import Database

TIMESTAMP_COL_NAME = 'TS'

class DataLoader(object):
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        print("data loader initialized. data_dir is: {0}".format(data_dir))


    '''
    Parses data files, builds tables and builds and returns database.
    '''
    def load(self):
        print("loading data from files into db")
        timestamp = 0
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
                        num_columns = len(elems) + 1
                        for i in range(1, num_columns):
                            new_table.add_column_name(table_name + str(i))

                        new_table.add_column_name(TIMESTAMP_COL_NAME)

                        print(new_table.column_names)
                        first_line = False

                    #print(elems)

                    # add the primary key
                    new_table.add_key(elems[0]) # first column value is pk
 
                    # add the new row
                    for elem_num in range(1, len(elems)):
                        col_name = table_name + str(elem_num+1)
                        print("adding col {0} with key {1} and value {2}"
                              .format(col_name, elems[0], elems[elem_num]))

                        new_table.add_value(col_name, elems[0], elems[elem_num])
                      
                    # add the timestamp for the new row  
                    print("adding col {0} with key {1} and value {2}"
                          .format(TIMESTAMP_COL_NAME, elems[0], timestamp))

                    new_table.add_value(TIMESTAMP_COL_NAME, elems[0], timestamp)
                    timestamp += 1
                                      
                
            #print(new_table.columns)

            db.add_table(new_table)

        return db


