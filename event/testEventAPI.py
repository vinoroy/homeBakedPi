#!/usr/bin/env python
"""
@author: Vincent Roy []

Module with Unit test class for testing the api for the event queue

"""


import unittest
import urllib2
import time



class TestSensorOFF(unittest.TestCase):
    """
    Unit test class for testing the web api for the event queue
    """

    def setUp(self):
        """
        Setup the testing
        """

        pass


    def test_insert_MotionEvent(self):
        """
        Testing the insertion of a motion detection event
        """

        response = urllib2.urlopen('http://127.0.0.1:5000/insertEvent/motion;ENTRANCE;MD-1;1')

        self.assertEqual(response.read(),'1')


    def test_insert_DoorAndRfid(self):
        """
        Testing the the insertion of a door opening and then a RFID event
        """

        response = urllib2.urlopen('http://127.0.0.1:5000/insertEvent/door;ENTRANCE;SW-1;1')

        self.assertEqual(response.read(),'1')

        time.sleep(3)

        response = urllib2.urlopen('http://127.0.0.1:5000/insertEvent/rfid;ENTRANCE;RF-1;1')

        self.assertEqual(response.read(),'1')

        time.sleep(20)

