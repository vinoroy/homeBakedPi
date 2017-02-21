#!/usr/bin/env python
"""
@author: Vincent Roy []

This module contains all of the classes for the actions in response to an event

"""

from datetime import datetime, timedelta
import time
import os
from events import *
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig()



def verifyRFIDEvent(event):

    from events import *

    print 'verifying event queue for RFID event'

    event.getEventQueue().printEvents()

    if isinstance(event.getEventQueue().getEvent('rfidDetection','ENTRANCE','RF-1'),RFIDDetection):

        print 'ok found the RFID event'

        event.incrementPerformedAction()



class Action:
    """
    This class is action class. It serves as a base class for all actions that are associated to an event

    Attributes :

        - event : (Event) reference to the event object that holds the action
        - actionType : (string) type of action

    """

    def __init__(self,event = ''):
        self.event = event
        self.actionType = ''


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



class DelayAndVerifyRFIDEvent(Action):
    """
    This class is responsible for performing a background delay of a certain duration and then to launch a task to
    verify the event queue for the presence of an RFID event

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'delayAndRFIDEvent'


    def doAction(self):
        """
        This function schedules a background task to verify the event queue for an RFID event in xx seconds

        """

        print 'scheduling a verification of the event queue for an RFID event in 12 seconds '

        scheduler = BackgroundScheduler()

        now = datetime.now()
        now_plus_12s = now + timedelta(minutes=0.2)

        scheduler.add_job(verifyRFIDEvent, 'date', run_date=now_plus_12s,args=[self.event])
        scheduler.start()


class OpenLight(Action):
    """
    This class is class is responsible for opening a light

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'openLight'

    def doAction(self):
        """
        This function opens a light

        """

        print 'opening light'

        self.event.incrementPerformedAction()


class SendSMS(Action):
    """
    This class is responsible for sending an sms

    """

    def __init__(self,event):
        Action.__init__(self,event)
        self.actionType = 'sendSMS'

    def doAction(self):
        """
        This functions sends an sms

        """

        print 'sending sms'

        self.event.incrementPerformedAction()



