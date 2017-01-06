#!/usr/bin/env python
"""
@author: Vincent Roy [not in use]

Module with Unit test class for testing the Pi_WebCamera class and the HomeBakedPiWebCamera app on the home network

"""


import unittest
from occpSensor import *
from node import *
from hub import *
import sqlite3
import time


class TestPiWebCameraONNetwork(unittest.TestCase):
    """
    Unit test class for testing the PiWebCamera online (i.e. attached to a physical camera node)
    """

    def setUp(self):
        """
        Setup the testing
        """

        # create a node and add a mock temperature amd camera sensor
        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KitchenNode',self.myHub,'','http://192.168.0.39','OCC')
        self.testPiWebCamera = Pi_WebCamera('CAM1',self.myNode,'LOW')



    def test_takeReading_PiWebCamera(self):
        """
        Testing the takeReading method using a mock temperature sensor. Must return a value between -20 and 50
        """

        self.testPiWebCamera.takeReading()





if __name__ == '__main__':
    unittest.main()

