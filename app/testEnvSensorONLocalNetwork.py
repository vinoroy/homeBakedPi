#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the envSensor class online

"""


import unittest
from envSensor import *
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
        self.myNode = Node('KITCHEN',self.myHub,'','http://192.168.0.119','ENV')

        self.testSenTemp = IPTempSensor('TMP-1',[0,100000],self.myNode,'LOW')
        self.testSenHumid = IPHumiditySensor('HUMID-1',[0,100000],self.myNode,'LOW')
        self.testSenLDR = IPLDRSensor('LDR-1',[0,100000],self.myNode,'LOW')



    def test_takeReading_IPTempSensor(self):
        """
        Testing the takeReading method using a esp temperature sensor.
        """

        self.testSenTemp.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testSenTemp.getLastReadingInBuffer()
        self.assertTrue(isinstance(newReading, float))


    def test_takeReading_IPTempSensor_wrongURLExtension(self):
        """
        Testing the takeReading method using a esp temperature sensor but with wrong url extension.
        Must return an empty value
        """

        # purposely modify the url extension to be bad !!!
        self.testSenTemp.urlSensorExtension = 'tempp'

        self.testSenTemp.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testSenTemp.getLastReadingInBuffer()

        self.assertEqual(newReading,None)


    def test_takeReading_IPHumiditySensor(self):
        """
        Testing the takeReading method using a esp humidity sensor.
        """

        self.testSenHumid.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testSenHumid.getLastReadingInBuffer()

        self.assertTrue(isinstance(newReading, float))


    def test_takeReading_IPLDRSensor(self):
        """
        Testing the takeReading method using a esp ldr sensor.
        """

        self.testSenLDR.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testSenLDR.getLastReadingInBuffer()

        self.assertTrue(isinstance(newReading, float))
