#!/usr/bin/env python
"""
@author: Vincent Roy []

Module with Unit test class for testing the Action class online

"""

import unittest

import time

from hub import *
from eventQ import *
from actions import *
from datetime import datetime
import time


class TestAction(unittest.TestCase):
    """
    Test class for testing the Action class online
    """

    def setUp(self):
        """
        Setup the testing
        """

        self.myHub = Hub('Main','bakedPiDB',smsGateway='@sms.rogers.com',cellNumber='5147945869')
        self.myQueue = EventQ(self.myHub)


    def tearDown(self):
        """
        Cleanup the testing
        """

        self.myHub.getLog().clearAllLogEntries()


    def test_doAction_SendEmail(self):
        """
        Testing the doAction method of the SendEmail

        """

        self.myEvent = DoorOpening(self.myQueue,'ENTRANCE','SW-1',1)

        self.myAction = SendEmail(self.myEvent)

        self.myAction.doAction()

        self.assertEqual(self.myAction.getActionDoneState(),1)


    def test_doAction_SendSMS(self):
        """
        Testing the doAction method of the SendSMS

        """

        self.myEvent = DoorOpening(self.myQueue,'ENTRANCE','SW-1',1)

        self.myAction = SendSMS(self.myEvent)

        self.myAction.doAction()

        self.assertEqual(self.myAction.getActionDoneState(),1)
