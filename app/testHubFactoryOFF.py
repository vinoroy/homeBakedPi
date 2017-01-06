#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the HubFactory class off line (i.e. not connected to the internet and not connected
to a sensor network)

"""

import unittest
from hubFactory import *




class TestHubFactorOFF(unittest.TestCase):
    """
    Test class for testing the HubFactory class off line (i.e. not connected to the network and not connected
    to an Arduino)
    """

    def setUp(self):
        """
        Setup the testing
        """

        # one hub factory with mock mode off
        self.myFac = HubFactory('bakedPiDB',0)

        # one hub factory with no db and mock mode off
        self.myFacNoDBFile = HubFactory('',0)



    def test_createHub(self):
        """
        Test the creation of the hub, node, sensors and actuators from the test database file. In the test data base there
        are four nodes, one of the has four sensors and there are three actuators. The test will verify this assertion.
        """


        aHub = self.myFac.createHub()

        numNode = aHub.getNumberNodes()
        self.assertEqual(numNode,2)

        # get a reference to the one and only node and count the number of sensors created, this should be 4
        theNode = aHub.getNodeAtIdx(0)
        numSensors = theNode.getNumberSensors()
        self.assertEqual(numSensors,3)

        # count the number of actuators created, this should be 0
        numActuators = aHub.getNumberActuators()
        self.assertEqual(numActuators,0)


    def test_createHub_noDBFile(self):
        """
        Test the creation of the hub with a db file that does not exist. The hub should be created void of any sensors
        """

        aHub = self.myFacNoDBFile.createHub()

        self.assertEqual(aHub.getNumberNodes(),0)




if __name__ == '__main__':
    unittest.main()