#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the OccpSensor module offline (i.e. not connected to the sensor network and the internet)

"""


import unittest
from occpSensor import *
from node import *
from hub import *
import sqlite3
import time




class TestOccpSensorOFF(unittest.TestCase):
    """
    Test class for testing the OccpSensor module offline (i.e. not connected to the sensor network and the internet)
    """

    def setUp(self):


        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KitchenNode',self.myHub,'','','ENV')

        self.testDoorSwitch_wideThresholds = MOCK_DoorSwitch('MOCK-SW-1',2,self.myNode,'NONE')
        self.testDoorSwitch_narrowThresholds = MOCK_DoorSwitch('MOCK-SW-2',1,self.myNode,'NONE')

        self.testMotionDetection = MOCK_MotionDetection('MOCK-MD-1',1,self.myNode,'NONE')

        self.myHub.setMonitoringParam('OCCP',True)


    def tearDown(self):
        """
        Cleanup after tests
        """

        self.myHub.setMonitoringParam('OCCP',False)


    def test_takeReading_MOCK_DoorSwitch(self):
        """
        Test the take reading method of the door contact switch with a mock switch. Verify be making sure the table
        length is longer
        """

        conn = sqlite3.connect(self.myHub.dbFile)

        cursor = conn.execute("SELECT Count(*) FROM DOOROPENINGS")
        lenTableBefore = cursor.next()[0]

        self.testDoorSwitch_wideThresholds.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)

        cursor = conn.execute("SELECT Count(*) FROM DOOROPENINGS")
        lenTableAfter = cursor.next()[0]

        cursor.close()
        conn.close()

        self.assertGreater(lenTableAfter,lenTableBefore)


    def test_verifyThresholds_Mock_DoorSwitch_generatedEvent(self):
        """
        Test to verify the verifyThresholds method of the door contact switch with thresholds that will generate an event
        """

        lenQBefore = self.myHub.getEventQ().getEventQLength()

        self.testDoorSwitch_narrowThresholds.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)

        lenQAfter = self.myHub.getEventQ().getEventQLength()

        self.assertGreater(lenQAfter,lenQBefore)



    def test_verifyThresholds_Mock_DoorSwitch_noGeneratedEvent(self):
        """
        Test to verify the verifyThresholds method of the door contact switch with thresholds that will not generate an event
        """

        lenQBefore = self.myHub.getEventQ().getEventQLength()

        self.testDoorSwitch_wideThresholds.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)

        lenQAfter = self.myHub.getEventQ().getEventQLength()

        self.assertEqual(lenQAfter,lenQBefore)


    def test_takeReading_MOCK_MotionDetection(self):

        """
        Test the take reading method of the motion detection sensor with a mock sensor. Verify be making sure the table
        length is longer
        """

        conn = sqlite3.connect(self.myHub.dbFile)

        cursor = conn.execute("SELECT Count(*) FROM MOTION")
        lenTableBefore = cursor.next()[0]

        self.testMotionDetection.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)

        cursor = conn.execute("SELECT Count(*) FROM MOTION")
        lenTableAfter = cursor.next()[0]

        cursor.close()
        conn.close()

        self.assertGreater(lenTableAfter,lenTableBefore)





if __name__ == '__main__':
    unittest.main()




