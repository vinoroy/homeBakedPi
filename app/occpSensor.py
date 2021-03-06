#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module contains all of the occupation sensor classes

"""


import random
from subprocess import call
from datetime import datetime
from datetime import timedelta
from dateTimeConversion import *
import platform
import random
import sqlite3
import urllib,re
from sensor import *
from events import *


class OccpSensor(Sensor):
    """
    Abstract class for the occupational type sensors.
    """


    def __init__(self,node,freq,instID):
        Sensor.__init__(self,node,freq,instID)


    def verifyThresholds(self):
        """
        Verify thresholds for occupational type sensors. Verify if the new reading exceeds the threshold.
        If a threshold is exceeded an event is added to the event pool.

        Args :
            - return

        Return :
            - none
        """


        if self.getHub().getMonitoringParam('OCCP') == True :

            if self.getLastReadingInBuffer() == self.thrsh:
                
                self.getHub().getEventQ().addEventToQueue(self.createEvent())




class DoorSwitchSensor(OccpSensor):
    """
    Abstract class for the door contact switch family of sensors. Here only some specific
    attributes are specified, no method implementation
    """

    def __init__(self,node,freq,instID):
        OccpSensor.__init__(self,node,freq,instID)
        self.mesureType = 'Contact switch'
        self.mesureUnit ='binary'
        self.instType = ''
        self.dbTable = 'DOOROPENINGS'
        self.alarmMsg = 'Door open'



class IPDoorSwitch(DoorSwitchSensor):


    def __init__(self, instID, limit,node,freq):
        DoorSwitchSensor.__init__(self,node,freq,instID)
        self.instType = 'IPDOORSWITCH'
        self.thrsh = limit
        self.urlSensorExtension = 'door'



    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        sensorValue = self.sendUrlRequestToNode(self.urlSensorExtension)


        return sensorValue


    def createEvent(self):
        """
        Create the event based on the specific sensor type.

        Args :
            - none

        Return :
            - (Event) specific event object based on the concrete sensor class

        """


        return DoorOpening(self.getHub().getEventQ(),self.getNode().getNodeID(),self.getInstID(),self.getLastReadingInBuffer())




class MOCK_DoorSwitch(DoorSwitchSensor):
    """
    Mock door contact switch class used for integration and unit tests when
    sensors are offline
    """


    def __init__(self,instID,limit,node,freq):
        DoorSwitchSensor.__init__(self,node,freq,instID)
        self.instType ='MOCKDOORSWITCH'
        self.thrsh = limit


    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # generate a random int number for the light value
        idxRnd = random.randint(0, 4)
        mockValues = [1, 1, 1, 1, 1]
        mockValue = mockValues[idxRnd]

        return mockValue


    def createEvent(self):
        """
        Create the event based on the specific sensor type.

        Args :
            - none

        Return :
            - (Event) specific event object based on the concrete sensor class

        """

        return MOCK_DoorOpening(self.getHub().getEventQ(),self.getNode().getNodeID(),self.getInstID(),self.getLastReadingInBuffer())




class MotionDetectionSensor(OccpSensor):
    """
    Abstract class for the motion detection family of sensors. Here only some specific
    attributes are specified, no method implementation
    """

    def __init__(self,node,freq,instID):
        OccpSensor.__init__(self,node,freq,instID)
        self.mesureType = 'Motion detection'
        self.mesureUnit ='binary'
        self.instType = ''
        self.dbTable = 'MOTION'
        self.alarmMsg = 'Motion detection'


class IPMotionDetection(MotionDetectionSensor):

    def __init__(self, instID, limit,node,freq):
        MotionDetectionSensor.__init__(self,node,freq,instID)
        self.instType = 'IPMOTION'
        self.thrsh = limit
        self.urlSensorExtension = 'motion'




    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        sensorValue = self.sendUrlRequestToNode(self.urlSensorExtension)


        return sensorValue


    def createEvent(self):
        """
        Create the event based on the specific sensor type.

        Args :
            - none

        Return :
            - (Event) specific event object based on the concrete sensor class

        """

        return MotionDetection(self.getHub().getEventQ(),self.getNode().getNodeID(),self.getInstID(),self.getLastReadingInBuffer())




class MOCK_MotionDetection(MotionDetectionSensor):
    """
    Mock door contact switch class used for integration and unit tests when
    sensors are offline
    """


    def __init__(self,instID,limit,node,freq):
        MotionDetectionSensor.__init__(self,node,freq,instID)
        self.instType ='MOCKMOTION'
        self.thrsh = limit


    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # generate a random int number for the light value
        idxRnd = random.randint(0, 4)
        mockValues = [1, 1, 1, 1, 1]
        mockValue = mockValues[idxRnd]

        return mockValue


    def createEvent(self):
        """
        Create the event based on the specific sensor type.

        Args :
            - none

        Return :
            - (Event) specific event object based on the concrete sensor class

        """

        return MOCK_MotionDetection(self.getHub().getEventQ(),self.getNode().getNodeID(),self.getInstID(),self.getLastReadingInBuffer())



class RFIDSensor(Sensor):
    """
    Abstract class for the RFID family of sensors. Here only some specific
    attributes are specified, no method implementation
    """
    
    def __init__(self,node,freq,instID):
        Sensor.__init__(self,node,freq,instID)
        self.mesureType = 'RFIDReader'
        self.mesureUnit ='tag'
        self.thrsh = [0,1]    
        self.dbTable = 'RFIDREADINGS'
    
    def takeReading(self):
        """
        Not implemented in the base class but must be in the concrete
        classes
        """

        raise NotImplementedError( "Should have implemented this" )
        
        
    def storeReading(self,date,value):
        """
        Stores the reading for the RFID class of sensors. Overides the base class store method

        Args :

            - date
            - value

        Return :
            - none

        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        conn.execute("INSERT INTO '%s' VALUES ('%s','%f','%d',0)" % (self.dbTable,self.instID,date,value))
        conn.commit()

        conn.close()
        

class ParallaxRFIDReader_ArduinoSensor(RFIDSensor):
    """
    RFID sensor connected to an Arduino microcontroller. Note that the communication to the Arduino is serial
    """

    
    def __init__(self,instID,node,freq):
        RFIDSensor.__init__(self,node,freq,instID)
        self.instType ='Parallax RFID Reader'

        
    def takeReading(self):
        """
        Take a reading from the RFID sensor that is connected to the Arduino microcontroller

        Return :
            - none

        """

        # only perform if the serial connection is active
        if (self.node.serLinkActive == 1):

            # prepare the message and send the message to the Arduino
            cmdMsg = self.node.nodeMsgID + "1"                  
            sensResp = self.node.hub.ser.sendCmdNReadResp(cmdMsg)            

            # parse the incoming message
            resultList = sensResp.split(";")
            command = int(resultList[0])
            RFIDid = resultList[1]
            state = int(resultList[2])
            
            if (RFIDid == self.instID and command == 1):        
            
                # get current date and convert to date num
                currDate = datetime.today()
                numCurrDate = conDateTimeToNum(currDate)
            
                # append date and temp to the sensor data vector
                self.data.append([numCurrDate,state])
                
                # store the last result in the database
                self.storeReading(numCurrDate,state)
                                                  
                self.verifyThresholds()
        
        
    def verifyThresholds(self):
        """
        Verifies if there has been a change in the state of the sensor

        Args :
            - none

        Return :
            - none

        """
        
        if (len(self.data) > 1):
            RFIDDiff = self.data[-1][1] - self.data[-2][1]

            if (RFIDDiff != 0):      
                self.node.eventQ.addEventToPool(SensorEvent(self.mesureType,self.instID, RFIDDiff))
        
    
          
class MOCK_RFIDReader(RFIDSensor):
    """
    Mock RFID class used for integration and unit tests when
    sensors are offline
    """


    def __init__(self,instID,node,freq):
        RFIDSensor.__init__(self,node,freq,instID)
        self.instType ='MOCK RFID Reader'

     
     
    def takeReading(self):
        """
        Take a reading from the mock RFID sensor.

        Return :
            - none
        """

        idxRnd = random.randint(0, 5)
        testValues = [1, 0, 1, 0, 1, 0]
        testValue = testValues[idxRnd]

        currDate = datetime.today()
        numCurrDate = conDateTimeToNum(currDate)

        self.storeReading(numCurrDate,testValue)

        self.data.append([numCurrDate,testValue])
