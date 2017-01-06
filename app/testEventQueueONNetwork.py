#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the eventQueue class on the network (ie connected to the internet)

"""


import unittest
from sensorEvent import *
from hub import *
from node import *
from envSensor import *
import time
from commUtil import *


class TestEventQueueONNetwork(unittest.TestCase):
    """
    Unit test class for testing the eventQueue class on network (ie connected to the internet)
    """

    def setUp(self):
        """
        Setup the testing
        """

        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KitchenNode',self.myHub,'','','ENV')
        
        
    def test_handleTempThrshEvent(self):
        """
        Test to verify that an event will be generated from a sensor threshold verification. A mock temperature sensor
        is created with very small thresholds, hence the random temperature reading will exceed the threshold value. This
        will result in an email msg.
        """


        emailsBefore = numberOfEmailsInbox('vinoroy70@gmail.com','miller12')

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[0,1],self.myNode,'LOW'))
        self.myNode.scanSensors('LOW') # scan once all sensors
        self.myNode.getHub().getEventQ().handleEvents()

        self.assertEqual(self.myNode.getHub().getEventQ().getEventQLength(),0)

        emailsAfter = numberOfEmailsInbox('vinoroy70@gmail.com','miller12')

        self.assertGreater(emailsAfter,emailsBefore)


    
if __name__ == '__main__':
    
    unittest.main()