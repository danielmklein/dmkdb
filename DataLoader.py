'''
Class that performs loading of data from data files.
For CS 457 Final Project, Spring 2015.

Daniel Klein
'''

import os, os.path
import re

from Table import Table
from Database import Database

TIMESTAMP_COL_NAME = 'TS'
DATA_FILE_NAMES = ['A.txt', 'B.txt', 'C.txt']

class DataLoader(object):
    
    def __init__(self, data_dir):
        self.data_dir = data_dir


    '''
    Parses data files, builds tables, and builds and returns database.
    '''
    def load(self):
        timestamp = 0
        db = Database()
        
        for file_name in DATA_FILE_NAMES:
            # generate the name of the table from the filename
            table_name = re.match('[^\.]+', file_name).group()
            new_table = Table(table_name)
            
            full_path = os.path.join(self.data_dir, file_name)
            with open(full_path, 'r') as data_file:
                first_line = True

                for line in data_file:
                    elems = line.split()
                    
                    if (first_line): 
                        # generate col names from the filename plus col num
                        # starting with timestamp
                        new_table.add_column_name(TIMESTAMP_COL_NAME)
                        num_columns = len(elems) + 1
                        for col_num in range(1, num_columns):
                            new_table.add_column_name(table_name + str(col_num))

                        first_line = False
 
                    # add vals for each new row, starting with timestamp
                    new_table.add_value(timestamp, TIMESTAMP_COL_NAME, timestamp)
                    for elem_num in range(len(elems)):
                        col_name = table_name + str(elem_num+1)
                        new_table.add_value(timestamp, col_name, elems[elem_num])

                    timestamp += 1
            # finally, add the table we just built to the db
            db.add_table(new_table)

        return db
    # end load


