#!/usr/bin/env python
"""
@author: Vincent Roy []

This module contains the node class. A node can contain one or more sensors. And a hub can contain one or more nodes.
"""


from sensor import *
from dateTimeConversion import *
import time
from numbers import Number
import urllib
import urllib2
    
    
class Node():
    """
    A node is the backbone of the sensening array of a given location. It holds
    all of the sensing instruments and provides the basic logic of the node.

    Attributes :
        - sensors : (Sensor list) list of sensor objects attached to the node
        - nodeID : (string) name of the node
        - nodeMsgID : (character) character used in prefixing a message to be sent to the physical node by serial comm.
                                  The character enables a node to recognize if the message is destined for it. Must
                                  set empty if to disable serial com activity
        - nodeURL : (string) URL of the node
        - hub : (Hub) reference to the hub object to which the node belongs


    """
    
    def __init__(self,nodeID,hub,nodeMsgID,nodeUrl,nodeType):
        self.sensors = []
        self.sensor = Sensor(self) # mock sensor for UML association
        self.nodeID = nodeID
        self.nodeMsgID = nodeMsgID
        self.nodeURL = nodeUrl
        self.nodeType = nodeType
        self.hub = hub



    def getNodeID(self):
        """
        Returns the node id

        Args :
            - none

        Return :
            - (string) node id

        """

        return self.nodeID


    def getHub(self):
        """
        Returns the hub object associated to the node

        Args :
            - none

        Return :
            - (Hub) hub object associated to the node

        """

        return self.hub


    def getNodeMsgID(self):
        """
        Returns the node message id

        Args :
            - none

        Return :
            - (string) node message id

        """

        return self.nodeMsgID




    def getNumberSensors(self):
        """
        Returns the number of sensors associated to the node

        Args :
            - none

        Return :
            - (int) number of sensors associated to the node

        """

        return len(self.sensors)


    def getSensorAtIdx(self,idx):
        """
        Returns the sensor at index x

        Args :
            - (int) index of the sensor to be returned

        Return :
            - (Sensor) sensor at index x

        """

        return self.sensors[idx]


    def addSensor(self,sen):
        """
        Appends a sensor to the list of sensors for the node

        Args :
            - sen : (obj ref) sensor object to add to the list

        Return :
            - none

        """
        if isinstance( sen, Sensor ):        
            self.sensors.append(sen)


    def getSensorIdx(self,instID):
        """
        Gets the index for the corresponding sensor. Returns -1 if the sensor is
        not found

        Args :
            - instID : (string) name of the sensor

        Return :
            - (int) index of  the sensor list that contains the desired sensor object. Retruns -1 if the desired sensor
              has not been identified
        """
        retVal = -1        

        # iterate through the list of sensors and id the desired sensor
        for i in range(0,len(self.sensors)):
            if (self.sensors[i].instID == instID):
                retVal = i
                return retVal
        return retVal

        
    def getSensor(self,instID):
        """
        Gets the reference for the corresponding sensor. Returns -1 if the sensor is
        not found

        Args :
            - instID : (string) name of the sensor

        Return :
            - obj reference to the sensor with the corresponding identification. Returns -1 if the sensor is
              not found
        """

        retVal = -1        

        # iterate through the list of sensors and id the desired sensor
        for i in range(0,len(self.sensors)):
            if (self.sensors[i].instID == instID):
                retVal = self.sensors[i]
                return retVal
        return retVal



    def getNodeUrl(self):
        """
        Returns the node url

        Args :
            - none

        Return :
            - (String) url of the node

        """

        return self.nodeURL


    def prtLastValueOfAllSensorsInBuffer(self):
        """
        Loop through each sensor and print to standard out the last value of the sensor tht is in the buffer

        Args :
            - none

        Return :
            - none
        """

        for i in self.sensors:
            print i.getLastReadingStrInBuffer()


    def prtNodeLastValuesFromDB(self):
        """
        Loop through each sensor and print to standard out the last value of the sensor tht is in the DB

        Args :
            - none

        Return :
            - none
        """

        print "\tNode ID : " + self.getNodeID()

        for i in self.sensors:
            i.prtSensorLastValueFromDBB()

        print ""


    
    def prtAllValuesOfSensorsInBuffer(self):
        """
        Loop through each sensor output the attributes and then all of its measurements to standard out

        Args :
            - none

        Return :
            - none
        """

        for i in self.sensors:
            i.prtSensorAttributes()
            i.prtSensorValuesInBuffer()



    def prtNodeAttributes(self):
        """
        Prints to the console the attributes of the node. Used for debugging purposes

        Args :
            - none

        Return :
            - none
        """

        print '\t--------- Node ID : ' + self.nodeID + ' attributes-------------'
        print '\tNode msg ID : ' + str(self.nodeMsgID)
        print '\tNumber of sensors : ' + str(len(self.sensors))

        # iterate over each sensor and print the sensors attributes
        for sensor in self.sensors:

            sensor.prtSensorAttributes()



    
    def scanSensors(self,scanFreq):
        """
        Loops through all of the sensors associated to a certain frequency and takes a reading

        Args :
            - scanFreq : (string) frequency (low or high) that must be used to filter the sensors associated with the
                                  node that will be read

        Return :
            - none
        """

        # iterate each sensor and take a reading
        for i in self.sensors:
            if i.scanFreq == scanFreq:
                i.takeReading()
    

    def getSensorsValuesMatrix(self):
        """
        Create a matrix with the instID, inst type, date, value and unit type for each sensor

        Args :
            - none

        Return :
            - none
        """

        # create the resultMatrix
        resMatrix = []

        # for each sensor of the node
        for sensor in self.sensors:

            # extract the last measurement for the sensor
            tmp = sensor.getSensorValuesFrmDB(last=1)

            # if there are values for the sensor, then add them
            if len(tmp) > 0:

                dateNum = tmp[0][0]
                dateStr = conNumToDateTime(dateNum).strftime("%Y-%m-%d %H:%M:%S")
                value = tmp[0][2]

            # insert the values for the sensor into the matrix
            resMatrix.append([sensor.instID,sensor.instType,dateNum,dateStr,value,sensor.mesureUnit])

        return resMatrix


    def getListSensorsID(self):
        """
        Get the list of all the sesnor IDs attached to the node

        Args :
            - none

        Return :
            - (string list) list of all the sensor IDs


        """

        # create a list to store the results
        listOfSensorsID = []

        # iterate through the object list of sensor and put the ID in the list
        for sensor in self.sensors:
            listOfSensorsID.append(sensor.instID)


        return listOfSensorsID



