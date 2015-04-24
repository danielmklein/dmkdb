'''
Main program for CS 457 Final Project
Spring 2015

Daniel Klein

'''

from DataLoader import DataLoader
from Table import Table
from Database import Database
from QueryExecutor import QueryExecutor
from ResultWriter import ResultWriter

DATA_DIR = "data"
INPUT_FILENAME = "input.txt"
OUTPUT_FILENAME = "results.txt"

def main():
    database = DataLoader(DATA_DIR).load()

    print("num tables: {0}".format(len(database.tables)))

    with open(INPUT_FILENAME, 'r') as input_file:
        file_text = input_file.read().strip()
    
    queries = file_text.split(';')

    executor = QueryExecutor(database)
    
    with open(OUTPUT_FILENAME, 'w') as output_file:
        writer = ResultWriter(output_file)
        for query in queries:
            clean_query = query.replace('\n', ' ').strip() + ";"
            print("QUERY: {0}".format(clean_query))
            
            result = executor.perform_query(clean_query)

            writer.write_result(result)

    return 0;



main()
