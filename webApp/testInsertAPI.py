#!/usr/bin/env python
"""
@author: Vincent Roy [DTP]

Module with Unit test class for testing the api of the homeBakedPiWebApp

"""


import unittest
import urllib2
from subprocess import call
import time



class TestSensorOFF(unittest.TestCase):
    """
    Unit test class for testing the
    """

    def setUp(self):
        """
        Setup the testing
        """

        time.sleep(2)


    def test_insertTempSensorValue(self):
        """
        Testing the insertSensorValue api with a valid node and instrument
        """

        response = urllib2.urlopen('http://127.0.0.1:5000/insertSensorValue/KITCHEN;TMP-1;99')

        self.assertEqual(response.read(),'1')


    def test_insertTempSensorValue_nonValidNodeInst(self):
        """
        Testing the insertSensorValue api with a non valid node and instrument
        """

        response = urllib2.urlopen('http://127.0.0.1:5000/insertSensorValue/KITCHEN;bla-1;99')

        self.assertEqual(response.read(),'0')


    def test_insertDoorSwitchSensorValue(self):
        """
        Testing the insertSensorValue api with a valid node and instrument
        """

        response = urllib2.urlopen('http://127.0.0.1:5000/insertSensorValue/ENTRANCE;SW-1;1')

        self.assertEqual(response.read(),'1')


    def test_insertMotionDetectionSensorValue(self):
        """
        Testing the insertSensorValue api with a valid node and instrument
        """

        response = urllib2.urlopen('http://127.0.0.1:5000/insertSensorValue/ENTRANCE;MD-1;1')

        self.assertEqual(response.read(),'1')

