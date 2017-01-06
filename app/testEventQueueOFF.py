#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the eventQueue class off line (ie not connected to the internet and not connected
to a sensor network)

"""



import unittest
from sensorEvent import *
from hub import *
from node import *
from envSensor import *
import time


class TestEventQueueOFF(unittest.TestCase):
    """
    Unit test class for testing the eventQueue class off line (ie not attached to a sensor)
    """

    def setUp(self):
        """
        Setup the testing
        """
        

        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KitchenNode',self.myHub,'','','ENV')
        

        self.myEvt = SensorEvent('Temp', 'Temp12', 45, self.myNode.getNodeID(),'Temp alarm')


    
    def test_addEventToPool(self):
        """
        Test to see that we can register one event (add) to the pool
        """

        self.myNode.getHub().getEventQ().addEventToPool(self.myEvt)

        self.assertEqual(self.myNode.getHub().getEventQ().getEventQLength(),1)


    def test_addEventToPool_nonSensorEvent(self):
        """
        Test that it is impossible to add a non sensor event to the event queue. Hence the queue length will not be longer
        """
    
        self.myNode.hub.eventQ.addEventToPool(MOCK_TempSensor('MOCK-TMP-1',[12,32],self.myNode,'LOW'))

        self.assertEqual(self.myNode.getHub().getEventQ().getEventQLength(),0)


    def test_rmEventFrmPool(self):
        """
        Test to see that we can register one event to the pool and then remove it.
        """

        self.myNode.getHub().getEventQ().addEventToPool(self.myEvt)
        self.myNode.getHub().getEventQ().rmEventFrmPool()

        self.assertEqual(self.myNode.getHub().getEventQ().getEventQLength(),0)


    def test_rmEventFrmPool_noEventsInPool(self):
        """
        Test to see that the code will not break if one tries to remove an event from an empty queue
        """

        self.myNode.getHub().getEventQ().rmEventFrmPool()

        self.assertEqual(self.myNode.getHub().getEventQ().getEventQLength(),0)


    def test_handleEvents_noEventsInPool(self):
        """
        Test to see that the code will not break if one tries to handle an event from an empty pool
        """

        self.myNode.getHub().getEventQ().handleEvents()


    def test_forceTempThrshEvent(self):
        """
        Test that it is possible to force a threshold of a mock temperature sensor and then get a SensorEvent in the queue
        """

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-1',[0,1],self.myNode,'LOW'))
        self.myNode.scanSensors('LOW') # scan once all sensors

        self.assertEqual(self.myNode.getHub().getEventQ().getEventQLength(),1)


    def test_getEventQLength(self):
        """
        Test that if we add one event the event queue length will be exactly one
        """

        self.myHub.getEventQ().addEventToPool(self.myEvt)


        self.assertEqual(self.myHub.getEventQ().getEventQLength(),1)


        
if __name__ == '__main__':
    
    unittest.main()