#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the envSensor class online

"""


import unittest
from occpSensor import *
from node import *
from hub import *
import sqlite3
import time


class TestEnvSensorONLocalNetwork(unittest.TestCase):
    """
    Unit test class for testing the envSensor class on the local network (i.e. onthe local network where the physical nodes
    are connected)
    """

    def setUp(self):
        """
        Setup the testing
        """


        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('ENTRANCE',self.myHub,'','http://192.168.0.181','ENV')


        self.testDoorSwitch = IPDoorSwitch('SW-1',1,self.myNode,'NONE')
        self.testMotion = IPMotionDetection('MD-1',1,self.myNode,'NONE')



    def test_takeReading_IPDoorSwitch(self):
        """
        Testing the takeReading method using an ip door switch sensor.
        """

        self.testDoorSwitch.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testDoorSwitch.getLastReadingInBuffer()

        if newReading == 0 or newReading == 1:
            test = True
        else:
            test = False

        self.assertTrue(test)


    def test_takeReading_IPMotion(self):
        """
        Testing the takeReading method using an ip door switch sensor.
        """

        self.testMotion.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testMotion.getLastReadingInBuffer()

        if newReading == 0 or newReading == 1:
            test = True
        else:
            test = False

        self.assertTrue(test)
