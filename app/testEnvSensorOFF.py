#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the envSensor class offline (i.e. not connected to a sensor network)

"""


import unittest
from envSensor import *
from node import *
from hub import *
import sqlite3
import time

# test list
# make a test to verify if the verify thresholds is done when take reading is performed

class TestEnvSensorOFF(unittest.TestCase):
    """
    Unit test class for testing the envSensor class offline (i.e. not attached to a physical sensing node)
    """

    def setUp(self):
        """
        Setup the testing
        """


        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KitchenNode',self.myHub,'','','ENV')

        self.testSenTemp = MOCK_TempSensor('MOCK-TMP-1',[0,100],self.myNode,'LOW')
        self.testSenLDR = MOCK_LDRSensor('MOCK-LDR-1',[0,1025],self.myNode,'LOW')
        self.testSenBaro = MOCK_BarometricPressureSensor('MOCK-BARO-1',[70,120],self.myNode,'LOW')
        self.testSenHumidity = MOCK_HumiditySensor('MOCK-HUMID-1',[0,101],self.myNode,'LOW')

        self.myHub.setMonitoringParam('ENV',True)


    def tearDown(self):
        """
        Cleanup after tests
        """

        self.myHub.setMonitoringParam('ENV',False)



    def test_takeReading_Mock_TempSensor(self):
        """
        Testing the takeReading method using a mock temperature sensor. Must return a value between -20 and 50
        """

        self.testSenTemp.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testSenTemp.getLastReadingInBuffer()
        self.assertTrue(newReading >= -20 & newReading <= 50)



    def test_takeReading_MOCK_LDRSensor(self):
        """
        Testing the takeReading method using a mock ldr sensor. Must return a value between 0 and 1250
        """

        self.testSenLDR.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testSenLDR.getLastReadingInBuffer()
        self.assertTrue(newReading >= 0 & newReading <= 1025)



    def test_takeReading_MOCK_BaroSensor(self):
        """
        Testing the takeReading method using a mock barometric sensor. Must return a value between 0 and 200
        """

        self.testSenBaro.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testSenBaro.getLastReadingInBuffer()
        self.assertTrue(newReading >= 0 & newReading <= 200)




    def test_takeReading_MOCK_HumiditySensor(self):
        """
        Testing the takeReading method using a mock humidity sensor. Must return a value between 0 and 101
        """

        self.testSenHumidity.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)
        newReading = self.testSenHumidity.getLastReadingInBuffer()
        self.assertTrue(newReading >= 0 & newReading <= 101)


    def test_forceTempThrshEvent(self):
        """
        Test that it is possible to force a threshold of a mock temperature sensor and then get an event in the queue
        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[0,1],self.myNode,'LOW'))
        self.myNode.scanSensors('LOW') # scan once all sensors

        self.assertEqual(self.myNode.getHub().getEventQ().getEventQLength(),1)



if __name__ == '__main__':
    unittest.main()

