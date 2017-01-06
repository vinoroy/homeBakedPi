#!/usr/bin/env python
"""
@author: Vincent Roy [not in use]

Module with Unit test class for testing the Pi_WebCamera class amd the HomeBakedPiWebCamera app off the home network but
rather on the local machine Flask server

"""


import unittest
from occpSensor import *
from node import *
from hub import *
import sqlite3
import time


class TestPiWebCameraONLocalServer(unittest.TestCase):
    """
    Unit test class for testing the PiWebCamera class offline (i.e. not attached to a physical camera )
    """

    def setUp(self):
        """
        Setup the testing
        """

        # create a node and add a mock temperature amd camera sensor
        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KitchenNode',self.myHub,'','http://127.0.0.1:5000','OCC')
        self.testPiWebCamera = Pi_WebCamera('CAM1',self.myNode,'LOW')



    def test_takeReading_PiWebCamera(self):
        """
        Testing the takeReading method using a mock pi web camera sensor.
        """

        self.testPiWebCamera.takeReading()






if __name__ == '__main__':
    unittest.main()

