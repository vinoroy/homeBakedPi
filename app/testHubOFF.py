#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the Hub class offline (i.e. off the internet and not connected to a sensor network)

"""

import unittest
from node import *
from hub import *
from envSensor import *
from occpSensor import *
from sensorEvent import *
import time
from actuator import *
from hubFactory import *
from imageSensor import *



class TestHubOFF(unittest.TestCase):
    """
    Test class for testing the Hub class offline (i.e. off the network and not connected to a sensor network)
    """

    def setUp(self):
        """
        Setup the testing
        """


        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KitchenNode',self.myHub,'','','ENV')

        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-2',[12,32],self.myNode,'LOW'))
        self.myNode.addSensor(MOCK_TempSensor('MOCK-TMP-3',[12,32],self.myNode,'HIGH'))
        self.myNode.addSensor(MOCK_Camera('MOCK-CAM-1',self.myNode,'HIGH'))
        self.myNode.addSensor(MOCK_Camera('MOCK-CAM-2',self.myNode,'HIGH'))
        self.myHub.addNode(self.myNode)


        self.myAct1 = MOCK_V110Switch('MOCK-SW-1','MOCK-SW-1',self.myHub)
        self.myAct2 = MOCK_V110Switch('MOCK-SW-2','MOCK-SW-2',self.myHub)

        self.myAct1.updateDBState()
        self.myAct2.updateDBState()



    def test_addNode(self):
        """
        Testing the addNode method of the Hub by verifiying that the number of nodes is greater after a new node has been
        added
        """

        initLen = self.myHub.getNumberNodes()

        self.myHub.addNode(self.myNode)

        newLen = self.myHub.getNumberNodes()

        self.assertGreater(newLen,initLen)


    def test_addNode_nonNode(self):
        """
        Test that a non node type object cannot be added to the nodes list of the hub by verifying that the list length
        has not been increased
        """

        initLen = self.myHub.getNumberNodes()
        self.myHub.addNode(SensorEvent('Temp', 'Temp12', 45,self.myNode.getNodeID(),'Temp alarm'))
        newLen = self.myHub.getNumberNodes()

        self.assertEqual(initLen,newLen)


    def test_getNodeIdx_trueNode(self):
        """
        Test to confirm that it is possibile to get the index of a node that is
        actually in the node list of the hub
        """

        self.myHub.addNode(self.myNode)
        idx = self.myHub.getNodeIdx('KitchenNode')

        self.assertEqual(idx,0)


    def test_getNodeIdx_falseNode(self):
        """
        Test to confirm that a node that is not in the list of the hub will return a result
        of -1
        """

        idx = self.myHub.getNodeIdx('TMP1')

        self.assertEqual(idx,-1)


    def test_getNode_trueNode(self):
        """
        Test to confirm that it is possibile to get the reference of a node that is
        actually in the node list of the hub
        """

        self.myHub.addNode(self.myNode)
        nodeRef = self.myHub.getNode(self.myNode.getNodeID())

        self.assertIsInstance(nodeRef,Node)
        self.assertEqual(nodeRef.nodeID,self.myNode.getNodeID())


    def test_getNode_falseNode(self):
        """
        Test to confirm that a node that is not in the list of nodes of the hub will return a result
        of -1
        """

        nodeRef = self.myHub.getNode('TMP1')

        self.assertEqual(nodeRef,-1)


    def test_HubIDFromNode(self):
        """
        Test to make sure that node object can communicate back with the hub to which it belongs
        """

        self.myHub.addNode(self.myNode)

        fstNode = self.myHub.getNodeAtIdx(0)

        self.assertEqual(fstNode.hub.getHubID(),'Main')


    def test_lowFreqUpDate(self):
        """
        Test to make sure that the lowFreqUpDate (ie scan) is performed

        """

        self.myHub.addActuator(self.myAct1)
        self.myHub.addActuator(self.myAct2)

        lenBeforeScanLow = len(self.myNode.getSensorAtIdx(0).getSensorValuesFrmDB())

        lenBeforeScanHigh = len(self.myNode.getSensorAtIdx(1).getSensorValuesFrmDB())

        dateTimeNumUpdateStateBefore = self.myHub.actuators[0].getLastStateFrmDB()[1]

        # wait 3 seconds since last scan to avoid a unique data constraint in the db
        time.sleep(3)

        self.myHub.lowFreqUpDate()

        lenAfterScanLow = len(self.myNode.getSensorAtIdx(0).getSensorValuesFrmDB())

        lenAfterScanHigh = len(self.myNode.getSensorAtIdx(1).getSensorValuesFrmDB())

        dateTimeNumUpdateStateAfter =  self.myHub.actuators[0].getLastStateFrmDB()[1]

        self.assertGreater(lenAfterScanLow,lenBeforeScanLow)

        self.assertEqual(lenBeforeScanHigh,lenAfterScanHigh)

        self.assertGreater(dateTimeNumUpdateStateAfter,dateTimeNumUpdateStateBefore)



    def test_highFreqUpDate(self):
        """
        Test to make sure that the highFreqUpDate (ie scan) is performed

        """

        lenBeforeScanLow = len(self.myNode.getSensorAtIdx(0).getSensorValuesFrmDB())

        lenBeforeScanHigh = len(self.myNode.getSensorAtIdx(1).getSensorValuesFrmDB())

        # wait 3 seconds since last scan to avoid a unique data constraint in the db
        time.sleep(3)

        self.myHub.highFreqUpDate()

        lenAfterScanLow = len(self.myNode.getSensorAtIdx(0).getSensorValuesFrmDB())

        lenAfterScanHigh = len(self.myNode.getSensorAtIdx(1).getSensorValuesFrmDB())

        self.assertEqual(lenAfterScanLow,lenBeforeScanLow)

        self.assertGreater(lenAfterScanHigh, lenBeforeScanHigh)


    def test_getListOfNodes(self):
        """
        Test to verify that the getListOfNodes methods returns the number of nodes in the unittest

        """

        self.assertEqual(len(self.myHub.getListOfNodes()),1)


    def test_getAllLastValues(self):
        """
        Test to verify that the getAllValuesDict will create a dictionary for each node of all the last values for each sensor

        """
        self.myHub.lowFreqUpDate()

        time.sleep(3)

        self.myHub.lowFreqUpDate()

        self.assertEqual(len(self.myHub.getAllLastValues()),1)


    def test_getListOfNodesWithCamera(self):
        """
        Test to verify that the getListOfNodesWithCamera will return a list of the cameras on the network

        """

        listOfCams = self.myHub.getListOfNodesWithCamera()

        self.assertEqual(len(listOfCams),2)



    def test_getHubID(self):
        """
        Test to verify that the getHubID will return a valid hub ID

        """

        self.assertEqual(self.myHub.getHubID(),'Main')


    def test_getDBFile(self):
        """
        Test to verify that the getDBFile will return a valid database file

        """

        self.assertEqual(self.myHub.getDBFile(),'bakedPiDB')


    def test_getEventQ(self):
        """
        Test to verify that the getEventQ will return a valid event queue that is of the right type

        """

        self.assertEqual(isinstance(self.myHub.getEventQ(),EventQueue),1)


    def test_getNumberNodes(self):
        """
        Test to verify that the getNumberNodes will return a valid number of nodes associated to the hub

        """

        self.assertEqual(self.myHub.getNumberNodes(),1)


    def test_getNodeAtIdx(self):
        """
        Test to verify that the getNodeAtIdx will return the valid node at index x

        """

        self.assertEqual(self.myHub.getNodeAtIdx(0).getNodeID(),'KitchenNode')


    def test_getHubMailAgt(self):
        """
        Test to verify that the getHubMailAgt will return the valid email agent object

        """

        self.assertTrue(isinstance(self.myHub.getHubMailAgt(),EmailAgent))




    def test_addActuator(self):
        """
        Testing the addActuator method of the Hub
        """

        initLen = self.myHub.getNumberActuators()

        self.myHub.addActuator(self.myAct1)

        newLen = self.myHub.getNumberActuators()

        self.assertGreater(newLen,initLen)


    def test_addActuator_nonActuator(self):
        """
        Test that a non actuator type object cannot be added to the actuators list of the hub
        """

        initLen = self.myHub.getNumberActuators()

        self.myHub.addActuator(SensorEvent('Temp', 'Temp12', 45,self.myNode.getNodeID(),'Temp alarm'))

        newLen = self.myHub.getNumberActuators()

        self.assertEqual(initLen,newLen)


    def test_getActuatorIdx_trueActuator(self):
        """
        Test to confirm that it is possibile to get the index of an actuator that is
        actually in the actuator list of the hub
        """

        self.myHub.addActuator(self.myAct1)
        self.myHub.addActuator(self.myAct2)
        idx = self.myHub.getActuatorIdx('MOCK-SW-1')

        self.assertEqual(idx,0)


    def test_getActuatorIdx_falseActuator(self):
        """
        Test to confirm that an actuator that is not in the list of the hub will return a result
        of -1
        """

        idx = self.myHub.getActuatorIdx('TMP1')

        self.assertEqual(idx,-1)


    def test_getActuator_trueActuator(self):
        """
        Test to confirm that it is possibile to get the reference of a node that is
        actually in the node list of the hub
        """

        self.myHub.addActuator(self.myAct1)
        self.myHub.addActuator(self.myAct2)
        actRef = self.myHub.getActuator(self.myAct1.getActuatorID())

        self.assertIsInstance(actRef,Actuator)
        self.assertEqual(actRef.actuatorID,self.myAct1.getActuatorID())


    def test_getActuator_falseActuator(self):
        """
        Test to confirm that an actuator that is not in the list of actuators of the hub will return a result
        of -1
        """

        actRef = self.myHub.getActuator('TMP1')
        self.assertEqual(actRef,-1)


    def test_getListActuatorsWithState(self):
        """
        Test to confirm that getListActuatorsWithState is correct
        """

        self.myHub.addActuator(self.myAct1)
        self.myHub.addActuator(self.myAct2)

        result = self.myHub.getListActuatorsWithState()

        # verify that the list contains two elements
        self.assertEqual(len(result),2)

        # verify that the states of the actuators are closed = 0
        self.assertEqual(result[0][1],0)
        self.assertEqual(result[1][1],0)


        self.myAct1.setOpen()
        self.myAct2.setOpen()

        # get the list and verify the the actuators are now open
        result = self.myHub.getListActuatorsWithState()
        self.assertEqual(result[0][1],1)
        self.assertEqual(result[1][1],1)


    def test_getListNodesInstruments(self):
        """
        Test to confirm that getListNodesInstruments is correct
        """

        self.assertEqual(len(self.myHub.getListNodesInstruments('ENV')),4)


    def test_getInstAtNode_validNodeValidInst(self):
        """
        Test to confirm that getInstAtNode function is ok for a valid noe and a valid instrument
        """

        theInst = self.myHub.getInstAtNode('KitchenNode','MOCK-TMP-2')

        self.assertEqual(theInst.getInstID(),'MOCK-TMP-2','getInstID error')



    def test_getInstAtNode_nonValidNode(self):
        """
        Test to confirm that getInstAtNode function is ok for a valid noe and a valid instrument
        """

        theInst = self.myHub.getInstAtNode('KitchenNodeBla','MOCK-TMP2')

        self.assertEqual(theInst,-1,'getInstID error')





if __name__ == '__main__':
    unittest.main()