#!/usr/bin/env python
"""
@author: Vincent Roy []

This module contains all of the classes for the actions in response to an event

"""

from datetime import datetime, timedelta
import time
import os
from events import *
from dateTimeConversion import *




class Action:
    """
    This class is action class. It serves as a base class for all actions that are associated to an event

    Attributes :

        - event : (Event) reference to the event object that holds the action
        - actionType : (string) type of action
        - actionDone : (int) 0 not done 1 done

    """

    def __init__(self,event):
        self.event = event
        self.actionType = ''
        self.actionDone = 0


    def doAction(self):
        """
        Not implemented in the base class but must be implemented in the concrete
        classes

        Args :
            - none


        Return :
            - none
        """

        raise NotImplementedError("Should have implemented this" )


    def getEvent(self):
        """
        Returns the reference to the event object associated to the action

        Args :
            - none

        Return :
            - (Event) reference to the associated event
        """

        return self.event


    def logActionDone(self):
        """
        Method that registers to the log the action performed. Also updates the state of the action

        Args :
            - none

        Return :
            - none
        """

        curDate = conDateTimeToNum(datetime.now())

        msg = 'Action associated to :' + self.getEvent().getBasicEventMsg()

        self.getEvent().getEventQ().getHub().getLog().insertLogEntry(curDate,self.actionType,msg)

        self.actionDone = 1



    def getActionDoneState(self):
        """
        Returns the state of the action

        Args :
            - none

        Return :
            - (int) state of the action
        """

        return self.actionDone




class DelayAndVerifyRFIDEvent(Action):
    """
    This class is responsible for performing a background delay of a certain duration and then to launch a task to
    verify RFID reader for the latest TAG entry

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'DELAY_AND_RFIDEVENT'


    def doAction(self):
        """
        This function waits for 30 seconds and then verify if a new RFID tag has been registered

        """

        print 'Sleeping for 30 seconds and then verifying new RFID tags'

        self.logActionDone()



class MOCK_DelayAndVerifyRFIDEvent(Action):
    """
    Mock class responsible for performing a mock background delay of a certain duration and then to launch a task to
    verify RFID reader for the latest TAG entry

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'MOCK_DELAY_AND_RFIDEVENT'


    def doAction(self):
        """
        Mock function waits for 30 seconds and then verify if a new RFID tag has been registered

        """

        print 'Mock sleeping for 30 seconds and then verifying new RFID tags'

        self.logActionDone()


class OpenLight(Action):
    """
    This class is class is responsible for opening a light

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'OPEN_LIGHT'

    def doAction(self):
        """
        This function opens a light

        """

        print 'opening light'

        self.logActionDone()


class MOCK_OpenLight(Action):
    """
    Mock class class responsible for opening a mock light

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'OPEN_LIGHT'

    def doAction(self):
        """
        Mock function opens a mock light

        """

        print 'Mock opening light'

        self.logActionDone()



class SendSMS(Action):
    """
    This class is responsible for sending an sms

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'SEND_SMS'

    def doAction(self):
        """
        This functions sends an sms

        """

        emailAgent = self.getEvent().getEventQ().getHub().getHubMailAgt()

        subject = self.getEvent().getEventType() + ' EVENT'
        msg = self.getEvent().getBasicEventMsg()

        emailAgent.sendSMS(subject,msg)

        self.logActionDone()


class MOCK_SendSMS(Action):
    """
    Mock class responsible for sending a mock sms

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'SEND_SMS'

    def doAction(self):
        """
        Mock functions sends a mock sms

        """

        print 'Mock sending sms'

        self.logActionDone()



class SendEmail(Action):
    """
    This class is responsible for sending an email to the registered client

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'SEND_EMAIL'


    def doAction(self):
        """
        This functions sends an email

        """

        emailAgent = self.getEvent().getEventQ().getHub().getHubMailAgt()

        subject = self.getEvent().getEventType() + ' EVENT'
        msg = self.getEvent().getBasicEventMsg()

        emailAgent.sendEmail(subject,msg)

        self.logActionDone()



class MOCK_SendEmail(Action):
    """
    Mock class is responsible for sending a mock email to the registered client

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'SEND_EMAIL'


    def doAction(self):
        """
        Mock functions sends a mock email

        """

        emailAgent = self.getEvent().getEventQ().getHub().getHubMailAgt()

        subject = self.getEvent().getEventType() + ' EVENT'
        msg = self.getEvent().getBasicEventMsg()

        emailAgent.sendEmail(subject,msg)

        self.logActionDone()
