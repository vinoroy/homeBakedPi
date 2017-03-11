#!/usr/bin/env python
"""
@author: Vincent Roy []

Module with Unit test class for testing the Event class offline (i.e. off the internet and not connected to a sensor network)

"""

import unittest

import time
from eventQ import *
from events import *
from hub import *


class TestEventOFF(unittest.TestCase):
    """
    Test class for testing the Event class offline
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



    def test_performAssociatedActions_correctNumberofActionsDone(self):
        """
        Testing the performAssociatedActions method for the correct number of actions done

        """

        myEvent = MOCK_DoorOpening(self.myQueue,'ENTRANCE','SW-1',1)

        myEvent.performAssociatedActions()

        self.assertEqual(myEvent.getNumberOfActionsDone(),myEvent.getNumberOfActions())


    def test_logEvent_onEventCreation(self):
        """
        Testing the logEvent method will insert one new event in the log when an event is created

        """

        logLenBefore = len(self.myHub.getLog().getLogEntriesFrmDB())

        myEvent = MOCK_DoorOpening(self.myQueue,'ENTRANCE','SW-1',1)

        logLenAfter = len(self.myHub.getLog().getLogEntriesFrmDB())

        self.assertEqual(logLenAfter - logLenBefore,1)
