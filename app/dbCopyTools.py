#!/usr/bin/env python
"""
@author: Vincent Roy [not in use]

This module implements functions to copy data of one data base to a new database with a different schema

"""



import sqlite3
import sys




def createDB(dbFileName):
    """
    This function creates a db file based for the homeBakedPi framework

    Args :
            - dbFileName : (string) file name of the database to be created

        Return :
            - none

    """

    # create a connection to a new db file
    con = sqlite3.connect(dbFileName)
    cur = con.cursor()

    # create all of the required tables
    cur.executescript("""
        DROP TABLE IF EXISTS BAROREADINGS;
        CREATE TABLE "BAROREADINGS" ("NODEID" CHAR NOT NULL , "INSTID" CHAR NOT NULL , "DATE" DOUBLE NOT NULL , "VALUE" DOUBLE, "UPLOAD" INTEGER NOT NULL  DEFAULT 0, PRIMARY KEY ("NODEID", "INSTID", "DATE"));

        DROP TABLE IF EXISTS CAMREADINGS;
        CREATE TABLE "CAMREADINGS" ("NODEID" CHAR NOT NULL , "INSTID" CHAR NOT NULL , "DATE" FLOAT NOT NULL , "VALUE" CHAR, "UPLOAD" INTEGER, PRIMARY KEY ("NODEID", "INSTID", "DATE"));

        DROP TABLE IF EXISTS HUMIDITYREADINGS;
        CREATE TABLE "HUMIDITYREADINGS" ("NODEID" CHAR NOT NULL , "INSTID" CHAR NOT NULL , "DATE" DOUBLE NOT NULL , "VALUE" DOUBLE, "UPLOAD" INTEGER NOT NULL  DEFAULT 0, PRIMARY KEY ("NODEID", "INSTID", "DATE"));

        DROP TABLE IF EXISTS LDRREADINGS;
        CREATE TABLE "LDRREADINGS" ("NODEID" TEXT NOT NULL , "INSTID" TEXT NOT NULL , "DATE" DOUBLE NOT NULL , "VALUE" DOUBLE, "UPLOAD" INTEGER NOT NULL  DEFAULT 0, PRIMARY KEY ("NODEID", "INSTID", "DATE"));

        DROP TABLE IF EXISTS NODES;
        CREATE TABLE "NODES" ("NODEID" CHAR PRIMARY KEY  NOT NULL , "NODEMSGID" CHAR, "ACTIVE" INTEGER, "URL" CHAR, "NODETYPE" CHAR);

        DROP TABLE IF EXISTS RFIDREADINGS;
        CREATE TABLE "RFIDREADINGS" ("INSTID" TEXT NOT NULL,"DATE" REAL NOT NULL,"STATE" INTEGER NOT NULL, "UPLOAD" INTEGER NOT NULL  DEFAULT 0);

        DROP TABLE IF EXISTS SENSORS;
        CREATE TABLE "SENSORS" ("NODEID" CHAR NOT NULL , "INSTID" CHAR NOT NULL , "ACTIVE" INTEGER, "INSTTYPE" CHAR, "LOWLIMIT" DOUBLE, "UPPERLIMIT" DOUBLE, "FREQ" CHAR, PRIMARY KEY ("NODEID", "INSTID"));

        DROP TABLE IF EXISTS TEMPREADINGS;
        CREATE TABLE "TEMPREADINGS" ("NODEID" CHAR NOT NULL , "INSTID" CHAR NOT NULL , "DATE" DOUBLE NOT NULL , "VALUE" DOUBLE, "UPLOAD" INTEGER NOT NULL  DEFAULT 0, PRIMARY KEY ("NODEID", "INSTID", "DATE"));

        """)

    # commit the creation of the tables to the file and close the connection
    con.commit()
    con.close()


def copyDB(sourceDB,destDB):
    """
    This function copies the data from the source database to  the destination database for each table

    Args :
            - sourceDB : (string) file name of the source database
            - destDB : (string) file name of the destination database

        Return :
            - none

    """

    # dictionary of the instrument tables and columns to be copied
    tables = {'BAROREADINGS':[0,1,2,3,4],'CAMREADINGS':[4,0,1,2,3],'HUMIDITYREADINGS':[0,1,2,3,4], 'LDRREADINGS':[0,1,2,3,4],'RFIDREADINGS':[4,0,1,2,3],'TEMPREADINGS':[0,1,2,3,4]}

    # create the new destination db where all the records are to be copied
    createDB(destDB)

    # open a connection to the source database
    connSrc = sqlite3.connect(sourceDB)

    # open a connection to the destination database
    connDest = sqlite3.connect(destDB)


    # copy all of the data for the instrument tables
    for table in tables:

        print 'copying' + table
    
        # extract all results from the source database for the concerned table
        result = connSrc.execute("SELECT * FROM '%s' ORDER BY DATE" % (table))

        # get the column indexes
        idx = tables[table]

        # for each entry in the the table
        for row in result:

            # extract the values
            node = row[idx[0]]
            inst = row[idx[1]]
            date = row[idx[2]]
            value = row[idx[3]]
            upload = row[idx[4]]

            # print to the console the values
            print 'node' + str(node)
            print 'inst' + str(inst)
            print 'date' + str(date)
            print 'value' + str(value)
            print 'upload' + str(upload)


            # insert the data in the appropriate destination database table
            if table == 'CAMREADINGS':

                connDest.execute("INSERT INTO '%s' VALUES('%s','%s','%f','%s','%f')" % (table,node,inst,date,value,upload))

            else:
                connDest.execute("INSERT INTO '%s' VALUES('%s','%s','%f','%f','%f')" % (table,node,inst,date,value,upload))

        # commit the changes
        connDest.commit()


    # copy the data of the nodes table, extract all of the rows from the node table
    result = connSrc.execute("SELECT * FROM NODES")

    # iterate over each row
    for row in result:

        # extract the values
        NODEID = row[0]
        NODEMSGID = row[1]
        ACTIVE = row[2]
        URL = ''
        NODETYPE = ''

        # insert the values in the destination node table
        connDest.execute("INSERT INTO NODES VALUES('%s','%s','%f','%s','%s')" % (NODEID,NODEMSGID,ACTIVE,URL,NODETYPE))


    # commit the changes
    connDest.commit()


    # copy the data of the sensors table, extract all of the rows
    result = connSrc.execute("SELECT * FROM SENSORS")

    # iterate over each row
    for row in result:

        # extract the values
        NODEID = row[0]
        INSTID = row[1]
        ACTIVE = row[2]
        INSTTYPE = row[3]
        LOWLIMIT = row[4]
        UPPERLIMIT = row[5]
        FREQ = row[6]

        # insert into the sensor destination table
        connDest.execute("INSERT INTO SENSORS VALUES('%s','%s','%f','%s','%f','%f','%s')" % (NODEID,INSTID,ACTIVE,INSTTYPE,LOWLIMIT,UPPERLIMIT,FREQ))

    # commit the changes
    connDest.commit()


    # close the source and the destination database
    connSrc.close()
    connDest.close()



if __name__ == "__main__":

    # get the source DB
    sourceDB = sys.argv[1]

    # get the destination DB
    destDB = sys.argv[2]


    copyDB(sourceDB,destDB)