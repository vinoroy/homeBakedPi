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
    Base event class used to register all of the information and actions with regards to an event (ie door opening,
    motion detection, sensor threshold exceeded, etc)

    Attributes :
        - eventType : (string) type of the event
        - nodeID : (string) identification of the node from which the event was generated
        - instID : (string) identification of the instrument from which theevent was generated
        - value : (float) value of the instrument associated with the event
        - eventQ : (EventQ) reference to the eventQueue object
        - numDate : (float) date number of the event
        - actions : (list Actions) list of the registered actions with the event
        - numberOfActions : (int) number of actions that are to be performed with the event
        - numberOfActionsDone : (int) number of actions that have been succescfully done


    """

    def __init__(self, eventQ, nodeID='', instID='', value=''):

        currDate = datetime.today()
        numCurrDate = conDateTimeToNum(currDate)

        self.eventType = ''
        self.nodeID = nodeID
        self.instID = instID
        self.value = value
        self.eventQ = eventQ
        self.numDate = numCurrDate
        self.actions = []
        self.numberOfActions = None
        self.numberOfActionsDone = 0


    def getEventQ(self):
        """
        Returns the reference to the eventQueue that holds the event

        Args :
            - none

        Return :
            - (EventQ) event queue tht holds the event

        """

        return self.eventQ


    def getNumberOfActions(self):
        """
        Returns the number of actions that must be done in response to the event

        Args :
            - none

        Return :
            - (int) number of actions that must be done in response to the event

        """

        return self.numberOfActions


    def getNumberOfActionsDone(self):
        """
        Returns the number of actions that have been done in response to the event

        Args :
            - none

        Return :
            - (int) number of actions that have been done in response to the event

        """

        return self.numberOfActionsDone



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

            if action.actionDone == 1:

                self.numberOfActionsDone += 1


    def printEventInfo(self):
        """
        Prints to console the info about the event

        Args :
            - none

        Return :
            - none

        """

        print self.eventType + ' - ' + conDateNumToDateStr(self.numDate)


    def logEvent(self):
        """
        Inserts into the log the event

        Args :
            - none

        Return :
            - none

        """

        curDate = conDateTimeToNum(datetime.now())

        msg = self.getBasicEventMsg()

        self.getEventQ().getHub().getLog().insertLogEntry(curDate,self.eventType,msg)


    def getBasicEventMsg(self):
        """
        Build a message from the event data

        Args :
            - none

        Return :
            - (string) message from the event data

        """

        msg = self.eventType + ' event from ' + self.nodeID + ' node and ' + self.instID + ' sensor with a value of : ' + str(self.value) + ' at ' + conDateNumToDateStr(self.numDate)

        return msg


    def getEventType(self):
        """
        Returns the event type

        Args :
            - none

        Return :
            - (string) event type

        """

        return self.eventType



class EnvThreshold(Event):
    """
    Environmental threshold event class

    """

    def __init__(self, eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'ENV_THRESHOLD'

        self.actions.append(SendEmail(self))
        self.actions.append(SendSMS(self))

        self.numberOfActions = len(self.actions)

        self.logEvent()



class MOCK_EnvThreshold(Event):
    """
    Mock environmental threshold event class

    """

    def __init__(self, eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'MOCK_ENV_THRESHOLD'

        self.actions.append(MOCK_SendEmail(self))

        self.numberOfActions = len(self.actions)

        self.logEvent()


class DoorOpening(Event):
    """
    Door opening event class

    """

    def __init__(self, eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'DOOR_OPENING'

        #self.actions.append(DelayAndVerifyRFIDEvent(self))
        self.actions.append(SendEmail(self))
        self.actions.append(SendSMS(self))
        #self.actions.append(OpenLight(self))

        self.numberOfActions = len(self.actions)

        self.logEvent()



class MOCK_DoorOpening(Event):
    """
    Mock door opening event class

    """

    def __init__(self, eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'MOCK_DOOR_OPENING'

        self.actions.append(MOCK_DelayAndVerifyRFIDEvent(self))
        self.actions.append(MOCK_SendSMS(self))
        self.actions.append(MOCK_OpenLight(self))

        self.numberOfActions = len(self.actions)

        self.logEvent()



class MotionDetection(Event):
    """
    Motion detection event class

    """

    def __init__(self,eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'MOTION_DETECTION'

        self.actions.append(SendSMS(self))
        self.actions.append(OpenLight(self))

        self.numberOfActions = len(self.actions)

        self.logEvent()




class MOCK_MotionDetection(Event):
    """
    Mock motion detection event class

    """

    def __init__(self,eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'MOCK_MOTION_DETECTION'

        self.actions.append(MOCK_SendSMS(self))
        self.actions.append(MOCK_OpenLight(self))

        self.numberOfActions = len(self.actions)

        self.logEvent()



class RFIDDetection(Event):
    """
    RFID detection event class

    """

    def __init__(self,eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'RFID_IDENTIFICATION'

        self.actions.append(SendSMS(self))

        self.numberOfActions = len(self.actions)

        self.logEvent()


class MOCK_RFIDDetection(Event):
    """
    Mock RFID detection event class

    """

    def __init__(self,eventQueue, nodeID, instID, value):
        Event.__init__(self,eventQueue, nodeID, instID, value)

        self.eventType = 'MOCK_RFID_IDENTIFICATION'

        self.actions.append(MOCK_SendSMS(self))

        self.numberOfActions = len(self.actions)

        self.logEvent()