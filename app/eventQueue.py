#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module contains an event pool class that is responsible for storing and handling untreated events as they are
generated by the homeBakedPi sensor network.

"""


from sensorEvent import *


class EventQueue():
    """
    This class is responsible for storing and handling untreated events as they are generated by the homeBakedPi sensor network.

    Attributes :
        - pool : (SensorEvent list) array list of all the untreated events generated by the homeBakdedPi network
        - hub : (Hub) reference to the hub object that is composed of an eventQueue object

    """
  
    def __init__(self,hub):
        self.pool = []
        self.hub = hub

    
    def addEventToPool(self,evt):
        """
        Appends a sensor event to the event queue if it is of the right type

        Args :
            - evt : (event object) event generated by one of the sensors in the network

        Return :
            - none

        """

        if isinstance( evt, SensorEvent ):
            self.pool.append(evt)

        
    def rmEventFrmPool(self):
        """
        Remove the oldest event in the event queue (FIFO)

        Args :
            - none

        Return :
            - (event object) the oldest event object

        """

        if len(self.pool) > 0:
            return self.pool.remove(self.pool[0])


    def getEventQLength(self):
        """
        Returns the length of the event queue

        Args :
            - none

        Return :
            - (int) length of the event queue

        """

        return len(self.pool)


    def handleEvents(self):
        """
        Based on the event type an action is undertaken (email is sent, etc)

        Args :
            - none

        Return :
            - none

        """
        # iterate through all the events in the pool
        for e in self.pool:

            msg = e.getEventMsg()
            subject = e.getEventDesc()
            self.hub.hubMailAgt.sendMsg('vinoroy70@gmail.com',subject,msg)
            self.rmEventFrmPool()
