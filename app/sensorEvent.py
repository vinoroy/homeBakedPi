#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module contains the SensorEvent class responsible for registering the information with regards to a
sensor event.
"""

from datetime import datetime
from dateTimeConversion import *


class SensorEvent:
    """
    Used to register all of the information with regards to a
    an event associated with a sensor (ex threshold alarm, intrusion, etc)

    Attributes :
        - eventType : (string) description of the event type
        - date : (float) automatically generated date number
        - instID : (string) name of the instrument
        - value : (float) value of the sensor at the time the event was generated
        - nodeID : (string) name of the node associated with the sensor that generated the event
    """

    def __init__(self, eventType, instID, value, nodeID, eventDesc):

        currDate = datetime.today()
        numCurrDate = conDateTimeToNum(currDate)        
        
        self.eventType = eventType # this is the mesuremnt type
        self.date = numCurrDate
        self.instID = instID
        self.nodeID = nodeID
        self.sensorValue = value
        self.eventDesc = eventDesc
        
    def getEventMsg(self):
        """
        Returns a message string with the details of the event

        Args :
            - none

        Return :
            - message string with the details of the event
        """

        msgStr = str(self.date)+' - '+self.eventType + ' On sensor : '+self.instID +' at value '+str(self.sensorValue)
        
        return msgStr


    def getEventDesc(self):
        """
        Returns the event description

        Args :
            - none

        Return :
            - string description of the event
        """

        return self.eventDesc
        
        
        
        
        

