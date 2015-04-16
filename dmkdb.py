'''
Main program for CS 457 Final Project
Spring 2015

Daniel Klein

'''

from DataLoader import DataLoader
from Table import Table
from Database import Database

def main():
    data_dir = "data"

    database = DataLoader(data_dir).load()




main()
