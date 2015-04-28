'''
Main program for CS 457 Final Project
Spring 2015

Daniel Klein

'''
import re

from DataLoader import DataLoader
from Table import Table
from Database import Database
from QueryExecutor import QueryExecutor
from ResultWriter import ResultWriter

DATA_DIR = ""
INPUT_FILENAME = "input.txt"
OUTPUT_FILENAME = "results.txt"

def main():
    print("**************************************************")
    print("**************************************************")
    print("****             Daniel Klein                 ****")
    print("****                CS 457                    ****")
    print("****             Final Project                ****")
    print("**************************************************")
    print("**************************************************")
    print("**** Initializing database from data files... ****")
    database = DataLoader(DATA_DIR).load()
    print("****         Database initialized.            ****")
    print("****                                          ****")

    with open(INPUT_FILENAME, 'r') as input_file:
        print("****           Reading input file...          ****")
        file_text = input_file.read().strip()
        print("****           Input file loaded.             ****")
        print("****                                          ****")
    
    queries = file_text.split(';')

    executor = QueryExecutor(database)
    
    with open(OUTPUT_FILENAME, 'w') as output_file:
        writer = ResultWriter(output_file)
        for query in queries:
            # get the entire query on one line, remove excess whitespace,
            # and add back the semicolon
            clean_query = query.replace('\n', ' ').strip() + ";" 
            if not re.search(r"\w", clean_query): # the blank line at the end...
                continue
            print("**** Executing query: {}".format(clean_query))
            print("****                                          ****")

            (col_names, rows) = executor.perform_query(clean_query)

            writer.write_result(col_names, rows)
            print("****          Result saved to file.           ****")
            print("****                                          ****")

    print("****          All queries completed.          ****")  
    print("****        Results are in {}        ****".format(OUTPUT_FILENAME))
    print("**************************************************")

    return 0;



main()
