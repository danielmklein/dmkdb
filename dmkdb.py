'''
Main program for CS 457 Final Project
Spring 2015

Daniel Klein

'''

from DataLoader import DataLoader
from Table import Table
from Database import Database

DATA_DIR = "data"
INPUT_FILENAME = "input.txt"
OUTPUT_FILENAME = "results.txt"

def main():
    database = DataLoader(DATA_DIR).load()

    print("num tables: {0}".format(len(database.tables)))

    return 0;



main()
