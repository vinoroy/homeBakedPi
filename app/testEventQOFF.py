#!/usr/bin/env python
"""
@author: Vincent Roy []

Module with Unit test class for testing the EventQ class offline (i.e. off the internet and not connected to a sensor network)

"""

import unittest

import time
from eventQ import *
from events import *
from hub import *


class TestEventQOFF(unittest.TestCase):
    """
    Test class for testing the eventQ class offline
    """

    def setUp(self):
        """
        Setup the testing
        """

        self.myHub = Hub('Main','bakedPiDB')
        self.myQueue = EventQ(self.myHub)


    def tearDown(self):
        """
        Setup the testing
        """

        self.myHub.getLog().clearAllLogEntries()



    def test_addEvent_validEventType(self):
        """
        Testing the addEvent method with a valid event

        """

        initLen = self.myQueue.getEventQLength()

        self.myQueue.addEventToQueue(DoorOpening(self.myQueue,'ENTRANCE','SW-1',1))

        newLen = self.myQueue.getEventQLength()

        self.assertGreater(newLen,initLen)



    def test_addEvent_nonValidEventType(self):
        """
        Testing the addEvent method with a non valid event type

        """

        self.myQueue.addEventToQueue(Hub('Main','bakedPiDB'))

        qLen = self.myQueue.getEventQLength()

        self.assertEqual(qLen,0)



    def test_rmEventFrmQueue(self):
        """
        Testing the rmEventFrmQueue method

        """

        self.myQueue.addEventToQueue(DoorOpening(self.myQueue,'ENTRANCE','SW-1',1))

        removedElement = self.myQueue.rmEventFrmQueue()

        self.assertEqual(isinstance(removedElement, Event),True)

        self.assertEqual(self.myQueue.getEventQLength(),0)



    def test_getEventQLength(self):
        """
        Testing the getEventQLength method

        """

        self.myQueue.addEventToQueue(DoorOpening(self.myQueue,'ENTRANCE','SW-1',1))

        self.assertEqual(self.myQueue.getEventQLength(),1)



    def test_handleEvents_DoorOpening(self):
        """
        Testing the handle events for a mock door opening event
        """

        self.myQueue.addEventToQueue(MOCK_DoorOpening(self.myQueue,'ENTRANCE','SW-1',1))

        self.myQueue.handleEvents()

        self.assertEqual(self.myQueue.getEventQLength(),0)







