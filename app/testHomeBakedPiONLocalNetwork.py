#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the homeBakedPi module functions on the local network (i.e. network where the
physical devices are connected)

"""
from __future__ import division
import unittest
from hbpApp import *
from envSensor import *
from node import *
from hub import *
import sqlite3
import time
from dateTimeConversion import *
import datetime




class TestHomeBakedPi(unittest.TestCase):
    """
    Test class for testing the homeBakedPi module functions
    """

    def setUp(self):
        """
        Setup the testing
        """

        pass



    def test_0_createHub(self):
        """
        Testing the createHub with a know number of nodes
        """

        theHub = createHub(['parameters.xml','dev'])


        theHub.prtHubLastValuesFromDB()

        self.assertEqual(len(theHub.getListOfNodes()),2)




    def test_1_lowParamScan(self):
        """
        Testing the low param scan. This should create one more reading in the temperature table
        """


        conn = sqlite3.connect('bakedPiDB')


        cursor = conn.execute("SELECT Count(*) FROM TEMPREADINGS")
        lenBefore = cursor.next()[0]


        # command line string
        cmd = './hbpApp.py parameters.xml dev low'

        # call
        call(cmd, shell=True)

        time.sleep(3)


        cursor = conn.execute("SELECT Count(*) FROM TEMPREADINGS")
        lenAfter = cursor.next()[0]


        cursor.close()
        conn.close()

        self.assertGreater(lenAfter,lenBefore)

