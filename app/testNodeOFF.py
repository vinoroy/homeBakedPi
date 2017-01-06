#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the Node class offline (i.e. not connected to the internet and the sensor network)

"""

import unittest
from node import *
from hub import *
from envSensor import *
from occpSensor import *
from imageSensor import *
from sensorEvent import *
import time



class TestNodeOFF(unittest.TestCase):
    """
    Test class for testing the Node class offline (i.e. not connected to the network and the sensor network)

    """

    def setUp(self):
        """
        Setup the testing
        """

        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KitchenNode',self.myHub,'','','ENV')



    def test_addSensor(self):
        """
        Testing the addSensor method to the node by verifying that the number of sensors attached to the node is greater
        after adding an instrument
        """

        initLen = self.myNode.getNumberSensors()

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[12,32],self.myNode,'LOW'))
        self.myNode.addSensor(MOCK_Camera('MOCK-CAM-1',self.myNode,'LOW'))

        newLen = self.myNode.getNumberSensors()

        self.assertGreater(newLen,initLen)


    def test_addSensor_nonSensor(self):
        """
        Test that a non sensor type object cannot be added to the sensor list of the node by verifying the number of
        sensors before and after
        """

        initLen = self.myNode.getNumberSensors()

        self.myNode.addSensor(SensorEvent('Temp', 'Temp12', 45,self.myNode.getNodeID(),'Temp alarm'))

        newLen = self.myNode.getNumberSensors()

        self.assertEqual(initLen,newLen)


    def test_getSensorIdx_trueSensor(self):
        """
        Test to confirm that it is possible to get the index of a sensor that is
        actually in the sensor list
        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[12,32],self.myNode,'LOW'))

        idx = self.myNode.getSensorIdx('MOCK-TMP-1')

        self.assertEqual(idx,0)


    def test_getSensorIdx_falseSensor(self):
        """
        Test to confirm that a sensor that is not in the list will return a result
        of -1
        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[12,32],self.myNode,'LOW'))

        idx = self.myNode.getSensorIdx('TMP-1')

        self.assertEqual(idx,-1)    


    def test_getSensor_trueSensor(self):
        """
        Test to confirm that it is possible to get the reference of a sensor that is
        actually in the sensor list
        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[12,32],self.myNode,'LOW'))

        senRef = self.myNode.getSensor('MOCK-TMP-1')

        self.assertIsInstance(senRef,Sensor)


    def test_getSensor_falseSensor(self):
        """
        Test to confirm that a sensor that is not in the list will return a result
        of -1
        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[12,32],self.myNode,'LOW'))

        senRef = self.myNode.getSensor('TMP-1')

        self.assertEqual(senRef,-1)

        

    def test_scanSensors_LOWFreq(self):
        """
        Test the scanSensor method by passing in the LOW freq scan parameter. All of the instruments must be
        updated. This is verified by comparing the length of the data set before and after
        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[-10,100],self.myNode,'LOW'))
        self.myNode.addSensor(MOCK_Camera('MOCK-CAM-1',self.myNode,'LOW'))

        self.myNode.scanSensors('LOW') # scan once all sensors
        time.sleep(2)

        fstSensor = self.myNode.sensors[0]
        lstScanTime = fstSensor.data[0][0] # get the date number of the last scan
        lstScanLen = len(fstSensor.data) # get length of data values

        self.myNode.scanSensors('LOW') # scan once more all sensors

        newScanTime = fstSensor.data[0][0] # get the date number of the new scan
        newScanLen = len(fstSensor.data) # get length of data values

        self.assertGreaterEqual(newScanTime,lstScanTime)
        self.assertGreaterEqual(newScanLen,lstScanLen)
        

    def test_scanSensors_HIGHFreq_noHIGHFreqSensors(self):
        """
        Test the scanSensors method by passing in the HIGH freq scan parameter, but no sensors that are
        set with a HIGH scan freq. All of the instruments must not be updated.
        This is verified by comparing the length of the data set before and after
        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[-10,100],self.myNode,'LOW'))
        self.myNode.addSensor(MOCK_Camera('MOCK-CAM-1',self.myNode,'LOW'))

        self.myNode.scanSensors('LOW') # scan once all sensors
        time.sleep(2)

        fstSensor = self.myNode.sensors[0]
        lstScanLen = len(fstSensor.data) # get length of data values


        self.myNode.scanSensors('HIGH') # try to scan all sensors
        time.sleep(2)

        newScanLen = len(fstSensor.data) # get length of data values

        self.assertEqual(newScanLen,lstScanLen)



    def test_NodeIDFromSensor(self):
        """
        Test to make sure that sensor can communicate with the node that it is associated to.
        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[12,32],self.myNode,'LOW'))
        self.myNode.addSensor(MOCK_Camera('MOCK-CAM-1',self.myNode,'LOW'))

        time.sleep(2)

        fstSensor = self.myNode.getSensorAtIdx(0)

        self.assertEqual(fstSensor.getNode().getNodeID(),'KitchenNode')


    def test_getSensorsValuesMatrix(self):
        """
        Test to verify that the getSensorsValuesMatrix will return a valid matrix of sensor values

        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[-10,100],self.myNode,'LOW'))

        self.myNode.scanSensors('LOW') # scan once all sensors

        time.sleep(2)

        self.assertGreater(len(self.myNode.getSensorsValuesMatrix()),0)


    def test_getListSensorsID(self):
        """
        Test to verify that the getListSensorsID will the exact list of sensors associated to the node

        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[-10,100],self.myNode,'LOW'))
        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-2',[-10,100],self.myNode,'LOW'))

        self.assertEqual(len(self.myNode.getListSensorsID()),2)


    def test_getHub(self):
        """
        Test to verify that the getHub will return the valid hub object

        """

        self.assertTrue(isinstance(self.myNode.getHub(),Hub))


    def test_getNodeID(self):
        """
        Test to verify that the getNodeID will return the valid node ID

        """

        self.assertEqual(self.myNode.getNodeID(),'KitchenNode')


    def test_getNodeMsgID(self):
        """
        Test to verify that the getNodeMsgID will return the valid message

        """

        self.assertEqual(self.myNode.getNodeMsgID(),'')



    def test_getNumberSensors(self):
        """
        Test to verify that the getNumberSensors will return the valid number of sensors associated to the node

        """

        self.assertEqual(self.myNode.getNumberSensors(),0)


    def test_getSensorAtIdx(self):
        """
        Testing the getSensorAtIdx method to verify that it will return the valid sensor at index x
        """

        s1 = MOCK_TempSensor('MOCK-TMP-1',[12,32],self.myNode,'LOW')
        s2 = MOCK_TempSensor('MOCK-TMP-2',[12,32],self.myNode,'LOW')

        self.myNode.addSensor(s1)
        self.myNode.addSensor(s2)

        self.assertEqual(self.myNode.getSensorAtIdx(1),s2)

        
if __name__ == '__main__':
    unittest.main()