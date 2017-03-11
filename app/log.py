#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module logs all of the homeBakedPi events, actions and scheduled tasks
"""

from dateTimeConversion import *
import sqlite3
import math


class Log:
    """
    This class is used to log all of the homeBakedPi events, actions and scheduled tasks


    Attributes :

        - aaa : (aaa) description of attribute (ex aaa)

    """


    def __init__(self,hub):
        self.hub = hub
        self.dbTable = 'LOG'


    def getHub(self):
        """
        Returns the ref to the hub

        Args :
            - none


        Return :
            - (Hub) reference to the hub object
        """

        return self.hub



    def insertLogEntry(self,numDate,type,decription):
        """
        Inserts an entry into the log database with a timestamp

        Args :
            - numDate : (float) date number of the log entry
            - type : (string) event, action or task
            - description : (string) textual description (may include nodeID, instID etc)


        Return :
            - none
        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        dateStr = conNumToDateTime(numDate).strftime("%Y-%m-%d %H:%M:%S")


        # insert value into the appropriate table and commit
        conn.execute("INSERT INTO LOG VALUES ('%s','%f','%s','%s')" % (type,numDate,dateStr,decription))
        conn.commit()


        conn.close()


    def getLogEntriesFrmDB(self, strDate=None, endDate=None, last=0):
        """
        This function gets from the database historic entries for the log.

        Args :
            - strDate : (float) datenum of the start date of the search
            - endDate : (float) datenum of the end date of the search
            - last : (int) 1 = get the last value

        Return :
            - logDateMatrix : (list of list) array of date and log entries (datenumber, date str, description, days frm most recent)
            - if no values the return will be an empty list

        """

        logDateMatrix = []

        conn = sqlite3.connect(self.getHub().getDBFile())


        # get the lastest log entry in the db. This will serve the purpose of the latest entry stored in the db
        tmpResult = conn.execute("SELECT * FROM LOG ORDER BY DATE DESC LIMIT 1")
        row = tmpResult.fetchone()

        # only execute if there is something in the database
        if row != None :

            # get the latest date
            mostRecent = row[1]
            conn.close()

            conn = sqlite3.connect(self.getHub().getDBFile())

            # if only the last value for the sensor is required
            if last == 1:

                # get the last row
                tmpResult = conn.execute("SELECT * FROM LOG ORDER BY DATE DESC LIMIT 1")
                row = tmpResult.fetchone()
                logDateMatrix.append([row[0],conNumToDateTime(row[2]).strftime("%Y-%m-%d %H:%M:%S"),row[3],row[2]-mostRecent])

            else :

                # query for no start and end dates
                if strDate == None and endDate == None:


                    result = conn.execute("SELECT * FROM LOG ORDER BY DATE")


                # query for a start but no end date
                if strDate != None and endDate == None:

                    result = conn.execute("SELECT * FROM LOG WHERE DATE >= '%f' ORDER BY DATE" % (strDate))


                # query between two dates
                if strDate != None and endDate != None:

                    result = conn.execute("SELECT * FROM LOG WHERE DATE >= '%f' AND DATE <= '%f' ORDER BY DATE" % (strDate,endDate))


                # put the date number, string date, event type, log decsription and number of days from most recent date
                # in the matrix
                for row in result:

                    logDateMatrix.append([row[1],row[2],row[0],row[3],row[1]-mostRecent])

            conn.close()

        return logDateMatrix



    def getLastDayLogEntries(self):
        """
        This function gets from the database the log entries for the last day.

        Args :
            - none

        Return :
            - logDateMatrix : (list of list) array of date and sensor values (datenumber, date str, value, days frm most recent)
            - if no values the return will be an empty array

        """

        # get the current date number and subtract one day to get the date number of the day yesterday
        curDateNum = conDateTimeToNum(datetime.now())
        lastDayDateNum = math.floor(curDateNum) - 1


        return self.getLogEntriesFrmDB(lastDayDateNum)




    def getLastWeekLogEntries(self):
        """
        This function gets from the database the values for the last week.

        Args :
            - none

        Return :
            - sensorDateMatrix : (list of list) array of date and sensor values (datenumber, date str, value, days frm most recent)
            - if no values the return will be an empty array

        """

        # get the current date number and subtract seven days to get the date number of the day one week ago
        curDateNum = conDateTimeToNum(datetime.now())
        lastWeekDateNum = math.floor(curDateNum) - 7

        return self.getLogEntriesFrmDB(lastWeekDateNum)




    def getLastMonthLogEntries(self):
        """
        This function gets from the database the values for the last month.

        Args :
            - none

        Return :
            - sensorDateMatrix : (list of list) array of date and sensor values (datenumber, date str, value, days frm most recent)
            - if no values the return will be an empty array

        """

        # get the current date number and subtract 30 days to get the date number of the day one month ago
        curDateNum = conDateTimeToNum(datetime.now())
        lastMonthDateNum = math.floor(curDateNum) - 30

        return self.getLogEntriesFrmDB(lastMonthDateNum)



    def clearAllLogEntries(self):
        """
        This function clears from the db all log entries

        Args :
            - none

        Return :
            - none

        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        conn.execute("DELETE FROM LOG")
        conn.commit()

        conn.close()



