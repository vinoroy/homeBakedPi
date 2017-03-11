#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the eventQueue class on the network (ie connected to the internet)

"""


import unittest
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

        
        
    def test_handleEvents_TempEnvThreshold_Event(self):
        """
        Test to verify that an event will be generated from a sensor threshold verification. A temperature sensor
        is created with very small thresholds, hence the normal temperature reading will exceed the threshold value. This
        will result in an email msg.
        """


        self.myNode = Node('KITCHEN',self.myHub,'','http://192.168.0.119','ENV')


        emailsBefore = numberOfEmailsInbox('vinoroy70@gmail.com','miller12')

        self.myNode.addSensor(IPTempSensor('TMP-1',[0,1],self.myNode,'LOW'))
        self.myNode.scanSensors('LOW') # scan once all sensors
        self.myNode.getHub().getEventQ().handleEvents()

        self.assertEqual(self.myNode.getHub().getEventQ().getEventQLength(),0)

        emailsAfter = numberOfEmailsInbox('vinoroy70@gmail.com','miller12')

        self.assertGreater(emailsAfter,emailsBefore)

        time.sleep(4)


    def test_handleEvents_DoorOpening_Event(self):
        """
        Test to verify that an event will be generated from a sensor. A door contact switch sensor
        is created and the door is manually opened and hence will result in an exceeded threshold value. This
        will result in an email msg.
        """


        self.myNode = Node('ENTRANCE',self.myHub,'','http://192.168.0.167','ENV')

        emailsBefore = numberOfEmailsInbox('vinoroy70@gmail.com','miller12')

        self.myNode.addSensor(IPDoorSwitch('SW-1',1,self.myNode,'LOW'))
        self.myNode.scanSensors('LOW') # scan once all sensors
        self.myNode.getHub().getEventQ().handleEvents()

        self.assertEqual(self.myNode.getHub().getEventQ().getEventQLength(),0)

        emailsAfter = numberOfEmailsInbox('vinoroy70@gmail.com','miller12')

        self.assertGreater(emailsAfter,emailsBefore)



    
if __name__ == '__main__':
    
    unittest.main()