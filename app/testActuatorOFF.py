#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the Actuator type classes offline (i.e. not connected to a network). More
specifically the unit test are for testing the functions that are common to all actuator classes

"""

from __future__ import division
import unittest
from actuator import *
from hub import *
import time
from dateTimeConversion import *
from datetime import datetime
from hbpApp import *




class TestActuatorOFF(unittest.TestCase):
    """
    Unit test class for testing the Actuator type classes offline. More
    specifically the unit test are for testing the functions that are common to all actuator classes. All tests are done
    with a Mock 110V actuator switch.
    """

    def setUp(self):
        """
        Setup the testing
        """

        self.myHub = Hub('Main','bakedPiDB')

        self.testSwitch = MOCK_V110Switch('MOCK-SW-1','MOCK-SW-1',self.myHub)



    def test_1(self):

        self.testSwitch.resetScheduleFlags()


    def test_getState_MOCK_V110Switch(self):
        """
        Testing the getState method of the MOCK_V110Switch actuator class
        """

        self.assertEqual(self.testSwitch.getState(),0)


    def test_setOpen_MOCK_V110Switch(self):
        """
        Testing the setOpen method of the MOCK_V110Switch actuator class
        """

        self.testSwitch.setOpen()
        self.assertEqual(self.testSwitch.getState(),1)


    def test_setClose_MOCK_V110Switch(self):
        """
        Testing the setClose method of the MOCK_V110Switch actuator class
        """

        self.testSwitch.setClose()
        self.assertEqual(self.testSwitch.getState(),0)



    def test_setScheduleTimes(self):
        """
        Testing the setScheduleTimes method of the V110Switch actuator class
        """


        self.testSwitch.setScheduleTimes(1,2)


        self.assertEqual(self.testSwitch.openTime,1)
        self.assertEqual(self.testSwitch.closeTime,2)


    def test_getScheduleTimes(self):
        """
        Testing the getScheduleTimes method of the V110Switch actuator class
        """


        self.testSwitch.setScheduleTimes(1,2)


        self.assertEqual(self.testSwitch.getScheduleTimes()[0],1)
        self.assertEqual(self.testSwitch.getScheduleTimes()[1],2)


    def test_checkSchedule1_beforePeriod(self):
        """
        #Testing the checkSchedule method of the V110 Switch class before the scheduled period. The result should be
        #closed
        """


        curTime = self.nowInHours()


        onTime = curTime + 2/60
        offTime = curTime + 4/60
        self.testSwitch.setScheduleTimes(onTime,offTime)


        self.testSwitch.checkSchedule()
        self.assertEqual(self.testSwitch.getState(),0)
        self.assertEqual(self.testSwitch.getOpenFlag(),0)
        self.assertEqual(self.testSwitch.getCloseFlag(),0)


    def test_checkSchedule2_inbetweenPeriod(self):
        """
        Testing the checkSchedule method of the V110 Switch class in between the period. The result should be
        open
        """


        curTime = self.nowInHours()


        onTime = curTime - 2/60
        offTime = curTime + 3/60
        self.testSwitch.setScheduleTimes(onTime,offTime)


        self.testSwitch.checkSchedule()
        self.assertEqual(self.testSwitch.getState(),1)
        self.assertEqual(self.testSwitch.getOpenFlag(),1)
        self.assertEqual(self.testSwitch.getCloseFlag(),0)


    def test_checkSchedule3_inbetweenPeriodManualOpen(self):
        """
        Testing the checkSchedule method of the V110 Switch class in between the period for a switch that was manually turned
        on. The result should be open with the openFlag set to 1 even though the switch was manually turned on.
        """


        curTime = self.nowInHours()


        onTime = curTime - 2/60
        offTime = curTime + 3/60
        self.testSwitch.setScheduleTimes(onTime,offTime)


        self.testSwitch.setOpen()


        self.testSwitch.checkSchedule()
        self.assertEqual(self.testSwitch.getState(),1)
        self.assertEqual(self.testSwitch.getOpenFlag(),1)
        self.assertEqual(self.testSwitch.getCloseFlag(),0)



    def test_checkSchedule4_afterPeriod(self):
        """
        Testing the checkSchedule method of the V110 Switch class after the  period. The result should be closed
        """

        curTime = self.nowInHours()


        onTime = curTime - 3/60
        offTime = curTime - 2/60
        self.testSwitch.setScheduleTimes(onTime,offTime)
        self.testSwitch.setOpenFlag(1) # to indicate that the switch was already set to open automatically


        self.testSwitch.checkSchedule()
        self.assertEqual(self.testSwitch.getState(),0)
        self.assertEqual(self.testSwitch.getOpenFlag(),1)
        self.assertEqual(self.testSwitch.getCloseFlag(),1)



    def test_checkSchedule5_afterPeriodManualClose(self):
        """
        Testing the checkSchedule method of the V110 Switch class after the  period and where the switch has been manually closed
        . The result should be closed with the close flag set to 1.
        """

        curTime = self.nowInHours()


        onTime = curTime - 3/60
        offTime = curTime - 2/60
        self.testSwitch.setScheduleTimes(onTime,offTime)
        self.testSwitch.setOpenFlag(1) # to indicate that the switch was already set to open automatically


        self.testSwitch.setClose()


        self.testSwitch.checkSchedule()
        self.assertEqual(self.testSwitch.getState(),0)
        self.assertEqual(self.testSwitch.getOpenFlag(),1)
        self.assertEqual(self.testSwitch.getCloseFlag(),1)



    def test_1setOpenFlag(self):
        """
        Testing the setOpenFlag method of the V110 Switch class. The flag is set to 1 and the db is verified to make
        sure the flag is at 1
        """

        self.testSwitch.setOpenFlag(1)


        result = self.testSwitch.getOpenFlag()


        self.assertEqual(result,1)



    def test_2setOpenFlag(self):
        """
        Testing the setOpenFlag method of the V110 Switch class. The flag is set to 0 and the db is verified to make
        sure the flag is at 0
        """

        self.testSwitch.setOpenFlag(0)


        result = self.testSwitch.getOpenFlag()


        self.assertEqual(result,0)


    def test_1setCloseFlag(self):
        """
        Testing the setCloseFlag method of the V110 Switch class. The flag is set to 1 and the db is verified to make
        sure the flag is at 1
        """

        self.testSwitch.setCloseFlag(1)


        result = self.testSwitch.getCloseFlag()


        self.assertEqual(result,1)



    def test_2setCloseFlag(self):
        """
        Testing the setCloseFlag method of the V110 Switch class. The flag is set to 0 and the db is verified to make
        sure the flag is at 0
        """

        self.testSwitch.setCloseFlag(0)


        result = self.testSwitch.getCloseFlag()


        self.assertEqual(result,0)


    def test_toggleSwitch(self):
        """
        Testing the toggleSwitch method of the V110 Switch class
        """


        self.testSwitch.toggleSwitch()
        self.assertEqual(self.testSwitch.getState(),1)


        self.testSwitch.toggleSwitch()
        self.assertEqual(self.testSwitch.getState(),0)



    def test_getLastStateFrmDB_open(self):
        """
        Testing the getLastStateFrmDB method of the actuator class after the switch has been opened
        """


        self.testSwitch.setOpen()


        curState = self.testSwitch.getState()


        dbState = self.testSwitch.getLastStateFrmDB()[0]


        self.assertEqual(curState,dbState,'getLastStateFrmDB error')



    def nowInHours(self):
        """
        Helper function to get the current time in decimal hours
        """


        curDateTime = datetime.now()


        curHr = curDateTime.hour
        curMin = curDateTime.minute
        curSec = curDateTime.second


        return curHr + curMin/60 + curSec/3600






