#!/usr/bin/env python
"""
@author: Vincent Roy []

Module with Unit test class for testing the Hub class offline (i.e. off the internet and not connected to a sensor network)

"""

import unittest

import time
from eventQueue import *
from events import *


class TestIntegration(unittest.TestCase):
    """
    Test class for testing the eventQueue class
    """

    def setUp(self):
        """
        Setup the testing
        """


        self.myQueue = EventQueue()



    def test_addEvent(self):
        """
        Testing the addEvent method

        """

        initLen = self.myQueue.getEventQLength()

        self.myQueue.addEventToQueue(DoorOpening(self.myQueue,'ENTRANCE','SW-1',1))

        newLen = self.myQueue.getEventQLength()

        self.assertGreater(newLen,initLen)


    def test_handleEvents_DoorAndRFIDEvent(self):
        """
        Testing the handle events for a door opening and RFID event
        """

        self.myQueue.addEventToQueue(DoorOpening(self.myQueue,'ENTRANCE','SW-1',1))

        self.myQueue.handleEvents()

        print 'adding a new event'

        self.myQueue.addEventToQueue(RFIDDetection(self.myQueue,'ENTRANCE','RF-1',1))

        time.sleep(30)

        self.assertEqual(self.myQueue.queue[0].getNumberOfActionsPerformed(),3)


    def test_handleEvents_DoorAndNonRFIDEvent(self):
        """
        Testing the handle events for a door opening and RFID event
        """

        self.myQueue.addEventToQueue(DoorOpening(self.myQueue,'ENTRANCE','SW-1',1))

        self.myQueue.handleEvents()

        print 'adding a new event'

        self.myQueue.addEventToQueue(MotionDetection(self.myQueue,'ENTRANCE','MD-1',1))

        time.sleep(30)

        self.assertEqual(self.myQueue.queue[0].getNumberOfActionsPerformed(),2)


    def test_getEvent_realEvent_DoorOpening(self):
        """
        Test the getEvent for a real DoorOpening event that has been inserted into the queue
        """

        self.myQueue.addEventToQueue(DoorOpening(self,'ENTRANCE','SW-1',1))

        evt = self.myQueue.getEvent('doorOpening','ENTRANCE','SW-1')

        self.assertEqual(evt,self.myQueue.queue[0])


    def test_getEvent_realEvent_MotionDetection(self):
        """
        Test the getEvent for a real MotionDetection event that has been inserted into the queue
        """

        self.myQueue.addEventToQueue(MotionDetection(self,'ENTRANCE','MD-1',1))

        evt = self.myQueue.getEvent('motionDetection','ENTRANCE','MD-1')

        self.assertEqual(evt,self.myQueue.queue[0])





    def test_getEvent_notRealEvent(self):
        """
        Test the getEvent for a DoorEvent event that has not been inserted into the queue
        """

        self.myQueue.addEventToQueue(DoorOpening(self,'ENTRANCE','SW-1',1))

        evt = self.myQueue.getEvent('doorOpening','ENTRANCE','SW-2')

        self.assertNotEqual(evt,self.myQueue.queue[0])

        self.assertEqual(evt,None)








