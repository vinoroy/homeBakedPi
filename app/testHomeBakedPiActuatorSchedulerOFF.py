#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the homeBakedPi module functions offline (i.e. not connected to any kind of network)

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



class TestHomeBakedPiActuatorSchedulerOFF(unittest.TestCase):
    """
    Test class for testing the homeBakedPi module functions
    """

    def setUp(self):
        """
        Setup the testing
        """

        # create a hub and then a node for the tests
        pass


    def test_3_setupBefore_chkSchedulesParamTest_before(self):

        theHub = createHub(['parameters.xml','dev-m'])

        theAct = theHub.getActuator('MOCK-SW-1')

        curTime = nowInHours()

        onTime = curTime + .5/60
        offTime = curTime + 2/60

        theAct.setScheduleTimes(onTime,offTime)



    def test_4_chkSchedulesParamTest_before(self):
        """
        # Testing the checkSchedule method of the V110 Switch class before the scheduled period. The result should be
        #closed
        """

        # command line string
        cmd = './hbpApp.py parameters.xml dev-m chkSchedules'

        # call
        call(cmd, shell=True)

        # allow a 3 second sleep interval to set the results on the db
        time.sleep(3)

        theHub = createHub(['parameters.xml','dev-m'])

        theAct = theHub.getActuator('MOCK-SW-1')

        openFlag = theAct.getOpenFlag()
        closeFlag = theAct.getCloseFlag()
        lastState = theAct.getLastStateFrmDB()

        # verify that the open and close flag are still at 0 and that the last state is still closed
        self.assertEqual(openFlag,0)
        self.assertEqual(closeFlag,0)
        self.assertEqual(lastState[0],0)



    def test_5_setupBefore_chkSchedulesParamTest_inbetween(self):

        theHub = createHub(['parameters.xml','dev-m'])

        theAct = theHub.getActuator('MOCK-SW-1')

        curTime = nowInHours()

        onTime = curTime - 50/60
        offTime = curTime + 50/60
        theAct.setScheduleTimes(onTime,offTime)


    def test_6_chkSchedulesParamTest_inbetween(self):
        """
        # Testing the checkSchedule method of the V110 Switch class before the scheduled period. The result should be
        #closed
        """

        # command line string
        cmd = './hbpApp.py parameters.xml dev-m chkSchedules'

        # call
        call(cmd, shell=True)

        # allow a 3 second sleep interval to set the results on the db
        time.sleep(3)

        theHub = createHub(['parameters.xml','dev-m'])

        theAct = theHub.getActuator('MOCK-SW-1')

        openFlag = theAct.getOpenFlag()
        closeFlag = theAct.getCloseFlag()
        lastState = theAct.getLastStateFrmDB()

        # verify that the open and close flag are still at 0 and that the last state is still closed
        self.assertEqual(openFlag,1)
        self.assertEqual(closeFlag,0)
        self.assertEqual(lastState[0],1)


    def test_7_setupBefore_chkSchedulesParamTest_after(self):

        theHub = createHub(['parameters.xml','dev-m'])

        theAct = theHub.getActuator('MOCK-SW-1')

        curTime = nowInHours()

        onTime = curTime - 50/60
        offTime = curTime - 40/60
        theAct.setScheduleTimes(onTime,offTime)
        theAct.setOpenFlag(1)


    def test_8_chkSchedulesParamTest_after(self):
        """
        # Testing the checkSchedule method of the V110 Switch class before the scheduled period. The result should be
        #closed
        """

        # command line string
        cmd = './hbpApp.py parameters.xml dev-m chkSchedules'

        # call
        call(cmd, shell=True)

        # allow a 3 second sleep interval to set the results on the db
        time.sleep(3)

        theHub = createHub(['parameters.xml','dev-m'])

        theAct = theHub.getActuator('MOCK-SW-1')

        openFlag = theAct.getOpenFlag()
        closeFlag = theAct.getCloseFlag()
        lastState = theAct.getLastStateFrmDB()

        # verify that the open and close flag are still at 0 and that the last state is still closed
        self.assertEqual(openFlag,1)
        self.assertEqual(closeFlag,1)
        self.assertEqual(lastState[0],0)
