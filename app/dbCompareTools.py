#!/usr/bin/env python
"""
@author: Vincent Roy [not in use]

This module implements functions to compare the tables of a database with respect to another database

"""



import sqlite3
import sys
from pprint import pprint
 


def getColumnNames(dbName,tableName):
    """
    This function extracts the column names for a given table of a given database

    Args :
            - dbName : (string) file name of the database
            - tableName : (string) table name to be examined

        Return :
            - list of the column names of the given table

    """


    # open a connection to the database file
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()

    # get all of the info about the given table
    cursor.execute("PRAGMA table_info('%s')" % (tableName))

    # create a list to hold the column names
    columnNames = []

    # iterate through the column info to extract the name
    for row in cursor:

        columnNames.append([row[1],row[2]])


    # close the db connection
    connection.close()

    # return the column names
    return columnNames


def getTableNames(dbName):
    """
    This function extracts the table names of a given database

    Args :
            - dbName : (string) file name of the database

        Return :
            - list of the table names

    """


    # create an empty list for the table names
    tableNames = []

    # open a connection to the database file
    connection = sqlite3.connect(dbName)
    cursor = connection.cursor()

    # get all of the tables of the database file
    cursor.execute('select name from sqlite_master where type=\'table\'')
    for table in cursor:
        tableNames.append(table[0])

    # close the connection
    connection.close()

    # return the table names
    return tableNames



def compareDBTables(newDB,oldDB):
    """
    This function compares the names of the database tables of the new database with the names of the old. If the name of
    the new table is present in the old (1) or not (0)

    Args :
            - dbName : (string) file name of the database

        Return :
            - list of the table names

    """


    # get the tableNames for the dev db
    newTableNames = getTableNames(newDB)

    # get the tableNames for the prod db
    oldTableNames = getTableNames(oldDB)

    # create an output matrix
    compResult = []

    for newTable in newTableNames:

        curTable = [newTable,0]

        for oldTable in oldTableNames:

            if oldTable == newTable:

                curTable[1] = 1

        compResult.append(curTable)

    return compResult


def compareTableColumns(devDB,prodDB,tableName):

    devColNamesTypes = getColumnNames(devDB,tableName)

    prodColNamesTypes = getColumnNames(prodDB,tableName)

    compResult = []

    for devCol in devColNamesTypes:

        curCol = [devCol[0],0,0]

        for prodCol in prodColNamesTypes:

            if prodCol[0] == devCol[0]:

                curCol[1] = 1

                if prodCol[1] == devCol[1]:
                    curCol[2] = 1


        compResult.append(curCol)

    return compResult



def compare(devDB,prodDB):

    tablesNames = compareDBTables(devDB,prodDB)

    for table in tablesNames:

        if table[1] == 1:

            print ''
            print 'Comparing the :' + table[0] + ' table '

            colNames = compareTableColumns(devDB,prodDB,table[0])


            for col in colNames:

                print(col)



if __name__ == "__main__":

    # get the dev db file
    devDB = sys.argv[1]

    # get the prod db file
    prodDB = sys.argv[2]



    compare(devDB,prodDB)






