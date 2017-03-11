#!/usr/bin/env python
"""
@author: Vincent Roy []

Module with Unit test class for testing the Action class offline

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
    Test class for testing the Action class offline
    """

    def setUp(self):
        """
        Setup the testing
        """

        self.myHub = Hub('Main','bakedPiDB')
        self.myQueue = EventQ(self.myHub)


    def tearDown(self):
        """
        Cleanup the testing
        """

        self.myHub.getLog().clearAllLogEntries()


    def test_doAction(self):
        """
        Testing the doAction method

        """

        self.myEvent = DoorOpening(self.myQueue,'ENTRANCE','SW-1',1)

        self.myAction = MOCK_OpenLight(self.myEvent)

        self.myAction.doAction()

        self.assertEqual(self.myAction.getActionDoneState(),1)




    def test_logActionDone(self):
        """
        Testing the logActionDone method

        """

        self.myEvent = DoorOpening(self.myQueue,'ENTRANCE','SW-1',1)

        self.myAction = MOCK_OpenLight(self.myEvent)

        lenLogBeforeInsert = len(self.myHub.getLog().getLogEntriesFrmDB())

        self.myAction.doAction()

        lenLogAfterInsert = len(self.myHub.getLog().getLogEntriesFrmDB())

        self.assertGreater(lenLogAfterInsert,lenLogBeforeInsert)

