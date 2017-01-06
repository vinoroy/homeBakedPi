#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the SensorEvent class offline (i.e. not connected to the sensor network and the internet)

"""


import unittest
from sensorEvent import *
from node import *
from hub import *
from envSensor import *
import time


class TestSensorEventOFF(unittest.TestCase):
    """
    Test class for testing the SensorEvent class offline (i.e. not connected to the sensor network and the internet)
    """
    
    def setUp(self):
        """
        Setup the testing
        """

        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KitchenNode',self.myHub,'','','ENV')

        self.myEvt = SensorEvent('Temp', 'Temp12', 45,self.myNode.getNodeID(),'Temp alarm')


    def test_getEventMsg(self):
        """
        Testing the  getEventMsgStr method
        """

        msg = self.myEvt.getEventMsg()
        self.assertGreater(len(msg),0)
        
        

    

if __name__ == '__main__':
    
    unittest.main()