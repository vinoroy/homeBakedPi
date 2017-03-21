#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module contains the base class for all of the sensor types that can be used in a homeBakedPi
network

"""


import random
from subprocess import call
from datetime import datetime
from datetime import timedelta
from dateTimeConversion import *
import platform
import sqlite3
import numpy as np
import math
import urllib2

    

 
class Sensor:
    """
    This class is an abstract class of sensor type. No concrete objects can be logically
    instantiated from this class. Furthermore not all methods are implemented

    Attributes :

        - mesureType : (string) measurement type of the sensor (ex Temperature)
        - mesureUnit : (string) unit for the measurement (ex deg C)
        - instType : (string) model type of the sensor (TMP36)
        - instID : (string) identification of the sensor
        - dbTable : (string) name of the database table that will store sensor values
        - data : (list) data struct to hold sensor values since the application is live
        - thrsh : (list) lower and upper threshold values for the sensor
        - alarmMsg : (string) message that is to be relayed with the alarm
        - node : (Node) reference to the node that is composed of sensor objects
        - scanFreq : (string) LOW or HIGH, default is LOW. The actual time is set in the hub object
        - urlSensorExtension : (string) identifies the url extension for the sensor to be read

    """


    def __init__(self, node = [],freq = 'LOW',instID = ''):
        self.mesureType = ''
        self.mesureUnit =''
        self.instType =''
        self.instID = instID
        self.dbTable = ''
        self.data = []
        self.thrsh = []
        self.alarmMsg = ''
        self.node = node
        self.scanFreq = freq
        self.urlSensorExtension = ''


    def getInstID(self):
        """
        Returns the inst id

        Args :
            - none

        Return :
            - (string) inst id

        """

        return  self.instID


    def getNode(self):
        """
        Returns the node object associated to the sensor

        Args :
            - none

        Return :
            - (Node) Node object associated to the sensor

        """

        return self.node



    def getHub(self):
        """
        Returns the hub object associated to the node that is associated to the sensor

        Args :
            - none

        Return :
            - (Hub) hub object associated to the node that is associated to the sensor

        """

        return self.getNode().getHub()


    def getHighThreshhold(self):
        """
        Returns the high threshold value

        Args :
            - none

        Return :
            - (float) high threshold value

        """

        return self.thrsh[1]


    def getLowThreshhold(self):
        """
        Returns the low threshold value

        Args :
            - none

        Return :
            - (float) low threshold value

        """

        return self.thrsh[0]


    def getThresholds(self):
        """
        Returns the low and high threshold values

        Args :
            - none

        Return :
            - (list float) low and high threshold values

        """

        return self.thrsh


    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        raise NotImplementedError( "Should have implemented this" )


    def setThresholds(self,low, high):
        """
        Function to set the low and high threshold values of the sensor

        Args :
            - low : (float) value of the low threshold
            - high : (float) value  of the low threshold

        Return :
            - none

        """

        self.thrsh[0] = low

        self.thrsh[1] = high

        conn = sqlite3.connect(self.getHub().getDBFile())

        # update the state data for the current actuator
        conn.execute("UPDATE SENSORS SET LOWLIMIT = '%f', UPPERLIMIT = '%f' WHERE NODEID = '%s' AND INSTID = '%s'" % (low,high,self.getNode().nodeID,self.instID))
        conn.commit()

        conn.close()


    def takeReading(self):
        """
        Take a reading for the sensor, store the value in the db and validate the thresholds

        Args :
            - none

        Return :
            - none

        """

        currDate = datetime.today()
        numCurrDate = conDateTimeToNum(currDate)

        sensorValue = self.getValueFrmSensor()

        self.data.append([numCurrDate,sensorValue])

        self.storeReading(numCurrDate,sensorValue)

        self.verifyThresholds()

        
    
    def prtSensorAttributes(self):
        """
        Prints to the console the attributes of the sensor. Used for debugging purposes

        Args :
            - return

        Return :
            - none
        """

        print '\t\t----------Inst ID : '+ self.instID + ' attributes------------'
        print '\t\tMesure type : ' + self.mesureType
        print '\t\tMesure unit : ' + self.mesureUnit
        print '\t\tInstrument type : ' + self.instType

        # only print if threshold have been added
        if type(self.thrsh) is list:
            print '\t\tLower threshold : ' + str(self.thrsh[0])
            print '\t\tUpper threshold : ' + str(self.thrsh[1])
        else:
            print '\t\tTheshold : ' + str(self.thrsh)
        
        
    def prtSensorValuesInBuffer(self):
        """
        Prints all the measurement values of a sensor. Used for debugging

        Args :
            - return

        Return :
            - none
        """

        for i in self.data:
            print i


    def prtSensorLastValueFromDBB(self):
        """
        Prints the last value of a sensor in the DB. Used for debugging

        Args :
            - return

        Return :
            - none
        """

        #extract the last measurement for the sensor
        tmp = self.getSensorValuesFrmDB(last=1)

        # if there are values for the sensor, then add them
        if len(tmp) > 0:

            dateNum = tmp[0][0]
            dateStr = conNumToDateTime(dateNum).strftime("%Y-%m-%d %H:%M:%S")
            value = tmp[0][2]

            print "\t\t" + self.getInstID() + "\t" + str(value) + "\t" + dateStr

         
    def getLastReadingStrInBuffer(self):
        """
        String representation of the last reading. Can be used
        for html output in between tags

        Args :
            - return

        Return :
            - none

        """

        if len(self.data) > 0:        
            outStr = str(conNumToDateTime(self.data[-1][0]))+' - '+self.mesureType + ' : '+str(self.data[-1][1])+'  '+ self.mesureUnit
            return outStr
        else:
            return "No data"
        
        
    def getLastReadingInBuffer(self):
        """
        Get the last reading of the instrument

        Args :
            - none

        Return :
            - (float) numerical value of the last reading
        """

        if len(self.data) > 0:        
            return self.data[-1][1]

        else:
            return []

            
    def verifyThresholds(self):
        """
        Verify if the new reading exceeds the thresholds. If a threshold is exceeded an event is added to the event pool.
        This is an abstract method, it is implemented by lower level classes

        Args :
            - none

        Return :
            - none

        """

        raise NotImplementedError( "Should have implemented this" )


    def createEvent(self):
        """
        Create the event based on the specific sensor type. This is an abstract class, Hence it must be implements bu the concrete
        clas

        Args :
            - none

        Return :
            - (Event) specific event object based on the concrete sensor class

        """

        raise NotImplementedError( "Should have implemented this" )




    def insertEventValue(self,value):
        """
        Store the reading and verify the thresholds. This function is used when the value is generated by the sensor as
        result of an event.

        Args :
            - value : (float) value of the sensor

        Return :
            - none

        """

        currDate = datetime.today()
        numCurrDate = conDateTimeToNum(currDate)

        self.data.append([numCurrDate,value])

        self.storeReading(numCurrDate,value)

        self.verifyThresholds()



    def storeReading(self,date,value):
        """
        Stores the reading into the associated database table

        Args:
            - date : (float) date of the measurement
            - value : (float) value of the measurement

        Return :
            - none
        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        dateStr = conNumToDateTime(date).strftime("%Y-%m-%d %H:%M:%S")

        # if the value is a valid float value
        if value !=None:

            # insert value into the appropriate table and commit
            conn.execute("INSERT INTO '%s' VALUES ('%s','%s','%f','%f','%s')" % (self.dbTable,self.node.getNodeID(),self.instID,date,value,dateStr))
            conn.commit()

        else:

            pass

        conn.close()


    def getSensorValuesFrmDB(self, strDate=None, endDate=None, last=0):
        """
        This function gets from the database historic values for the sensors.

        Args :
            - strDate : (float) datenum of the start date of the search
            - endDate : (float) datenum of the end date of the search
            - last : (int) 1 = get the last value

        Return :
            - sensorDateMatrix : (list of list) array of date and sensor values (datenumber, date str, value, days frm most recent)
            - if no values the return will be an empty list

        """

        sensorDateMatrix = []

        conn = sqlite3.connect(self.getHub().getDBFile())


        # get the lastest date in the db for the sensor. This will serve the purpose of the latest date stored in the db
        tmpResult = conn.execute("SELECT * FROM '%s' WHERE INSTID = '%s' ORDER BY DATE DESC LIMIT 1" % (self.dbTable,self.instID))
        row = tmpResult.fetchone()

        # only execute if there is something in the database
        if row != None :

            # get the latest date
            mostRecent = row[2]
            conn.close()

            conn = sqlite3.connect(self.getHub().getDBFile())

            # if only the last value for the sensor is required
            if last == 1:

                # get the last row
                tmpResult = conn.execute("SELECT * FROM '%s' WHERE INSTID = '%s' ORDER BY DATE DESC LIMIT 1" % (self.dbTable,self.instID))
                row = tmpResult.fetchone()
                sensorDateMatrix.append([row[2],conNumToDateTime(row[2]).strftime("%Y-%m-%d %H:%M:%S"),row[3],row[2]-mostRecent])

            else :

                # query for no start and end dates
                if strDate == None and endDate == None:


                    result = conn.execute("SELECT * FROM '%s' WHERE INSTID = '%s' ORDER BY DATE" % (self.dbTable,self.instID))


                # query for a start but no end date
                if strDate != None and endDate == None:

                    result = conn.execute("SELECT * FROM '%s' WHERE INSTID = '%s' AND DATE >= '%f' ORDER BY DATE" % (self.dbTable,self.instID,strDate))


                # query between two dates
                if strDate != None and endDate != None:

                    result = conn.execute("SELECT * FROM '%s' WHERE INSTID = '%s' AND DATE >= '%f' AND DATE <= '%f' ORDER BY DATE" % (self.dbTable,self.instID,strDate,endDate))


                # put the date number, string date, value and number of days from most recent date in the matrix
                for row in result:

                    sensorDateMatrix.append([row[2],conNumToDateTime(row[2]).strftime("%Y-%m-%d %H:%M:%S"),row[3],row[2]-mostRecent])

            conn.close()

        return sensorDateMatrix



    def getLastDayValuesFrmDB(self):
        """
        This function gets from the database the values for the last day.

        Args :
            - none

        Return :
            - sensorDateMatrix : (list of list) array of date and sensor values (datenumber, date str, value, days frm most recent)
            - if no values the return will be an empty array

        """

        # get the current date number and subtract one day to get the date number of the day yesterday
        curDateNum = conDateTimeToNum(datetime.now())
        lastDayDateNum = math.floor(curDateNum) - 1


        return self.getSensorValuesFrmDB(lastDayDateNum)




    def getLastWeekValuesFrmDB(self):
        """
        This function gets from the database the values for the last week.

        Args :
            - none

        Return :
            - sensorDateMatrix : (list of list) array of date and sensor values (datenumber, date str, value, days frm most recent)
            - -1 if unsuccessful

        """

        # get the current date number and subtract seven days to get the date number of the day one week ago
        curDateNum = conDateTimeToNum(datetime.now())
        lastWeekDateNum = math.floor(curDateNum) - 7

        return self.getSensorValuesFrmDB(lastWeekDateNum)




    def getLastMonthValuesFrmDB(self):
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

        return self.getSensorValuesFrmDB(lastMonthDateNum)




    def clearSensorValuesInDB(self):
        """
        This function clears all the values for the given sensor in the database table

        Args :
            - none

        Return :
            - 1 if successful storage in price db
            - -1 if unsuccessful storage in price db

        """

        conn = sqlite3.connect(self.getHub().getDBFile())


        try:

            conn.execute("DELETE FROM '%s' WHERE instID = '%s'" % (self.dbTable, self.instID))
            conn.commit()

            return 1

        except sqlite3.IntegrityError:

            print 'Could not delete entries for asset'

            return -1

        conn.close()




    def setScanFreq(self,newFreq):
        """
        Set the scan frequency of the sensor

        Args :
            - newFreq : (string) LOW or HIGH. The actual time is set in the hub object

        Return :
            - none

        """
        if newFreq == 'LOW':

            self.scanFreq = newFreq

        elif newFreq == 'MEDIUM':

            self.scanFreq = newFreq

        elif newFreq == 'HIGH':

            self.scanFreq = newFreq


    def sendUrlRequestToNode(self,requestedSensor):
        """
        This method sends a url request to a node. The response is then returned to the caller

        Args :
            - requestedSensor : (string) sensor value that is requested

        Return :
            - (float) value of the sensor

        """

        urlString = self.getNode().getNodeUrl() + '/' + requestedSensor


        try:

            response = urllib2.urlopen(urlString,timeout=4)

            responseStr = response.read()

            response.close()

            splitResponseStr = responseStr.split(';')
            nodeID = splitResponseStr[0]
            instID = splitResponseStr[1]
            value = splitResponseStr[2]

            if nodeID == self.getNode().getNodeID():

                if instID == self.getInstID():

                    floatOfSensorValue = float(value)

                    return floatOfSensorValue

        except:

            print 'URL timed out'

            return None

