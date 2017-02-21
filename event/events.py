#!/usr/bin/env python
"""
@author: Vincent Roy []

Module contains the Event class responsible for registering the information and actions with regards to a
sensor event.
"""

from datetime import datetime
from dateTimeConversion import *
from actions import *


class Event:
    """
    Base event class used to register all of the information and actions with regards to an event

    Attributes :
        - eventType : (string) type of the event
        - nodeID : (string) identification of the node from which the event was generated
        - instID : (string) identification of the instrument from which theevent was generated
        - value : (float) value of the instrument associated with the event
        - eventQueue : (EventQueue) reference to the eventQueue object
        - numDate : (float) date number of the event
        - actions : (list Actions) list of the registered actions with the event
        - actionsPerformed : (int) number of actions performed so far
        - numActionsToPerform : (int) total number of actions to be performed

    """

    def __init__(self, eventQueue='', nodeID='', instID='', value=''):

        currDate = datetime.today()
        numCurrDate = conDateTimeToNum(currDate)

        self.eventType = ''
        self.nodeID = nodeID
        self.instID = instID
        self.value = value
        self.eventQueue = eventQueue
        self.numDate = numCurrDate
        self.actions = []
        self.actionsPerformed = None
        self.numActionsToPerform = None


    def performAssociatedActions(self):
        """
        Walks through the registered actions and requests for the action to be performed

        Args :
            - none

        Return :
            - none

        """

        for action in self.actions:

            action.doAction()



    def setActionStats(self):
        """
        Sets the stats of the event when the event is created

        Args :
            - none

        Return :
            - none

        """

        self.actionsPerformed = 0
        self.numActionsToPerform = len(self.actions)


    def incrementPerformedAction(self):
        """
        Increments the number of actions performed

        Args :
            - none

        Return :
            - none

        """

        self.actionsPerformed += 1


    def getNumberOfActionsPerformed(self):
        """
        Get the number of performed actions

        Args :
            - none

        Return :
            - (int) the number of performed actions so far

        """

        return self.actionsPerformed


    def getEventQueue(self):
        """
        Returns the reference to the eventQueue that holds the event

        Args :
            - none

        Return :
            - (EventQueue) event queue tht holds the event

        """

        return self.eventQueue


    def printEventInfo(self):
        """
        Prints to console the info abount the event

        Args :
            - none

        Return :
            - none

        """

        print self.eventType + ' - ' + conDateNumToDateStr(self.numDate)





class DoorOpening(Event):
    """
    Door opening event class

    """

    def __init__(self, eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'doorOpening'

        self.actions.append(DelayAndVerifyRFIDEvent(self))
        self.actions.append(SendSMS(self))
        self.actions.append(OpenLight(self))

        self.setActionStats()


class MotionDetection(Event):
    """
    Motion detection event class

    """

    def __init__(self,eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'motionDetection'

        self.actions.append(SendSMS(self))
        self.actions.append(OpenLight(self))

        self.setActionStats()


class RFIDDetection(Event):
    """
    RFID detection event class

    """

    def __init__(self,eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'rfidDetection'

        self.actions.append(SendSMS(self))

        self.setActionStats()


    

