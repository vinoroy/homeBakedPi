#!/usr/bin/env python
"""
@author: Vincent Roy []

Module with Unit test class for testing the Log class offline

"""

import unittest

import time
from log import *
from hub import *
from datetime import datetime


class TestLog(unittest.TestCase):
    """
    Test class for testing the eventQueue class
    """

    def setUp(self):
        """
        Setup the testing
        """

        self.myHub = Hub('Main','bakedPiDB')
        self.myLog = Log(self.myHub)


    def tearDown(self):
        """
        Cleanup the testing
        """

        self.myLog.clearAllLogEntries()


    def test_insertLogEntry_oneEntry(self):
        """
        Testing the insertLogEntry method

        """

        curDate = conDateTimeToNum(datetime.now())

        lenBeforeInsert = len(self.myLog.getLogEntriesFrmDB())

        self.myLog.insertLogEntry(curDate,'TEST','bla bla bla')

        lenAfterInsert = len(self.myLog.getLogEntriesFrmDB())

        self.assertGreater(lenAfterInsert,lenBeforeInsert)


    def test_clearAllLogEntries(self):
        """
        Testing the clearAllLogEntries method

        """

        curDate = conDateTimeToNum(datetime.now())

        lenBeforeInsert = len(self.myLog.getLogEntriesFrmDB())

        self.myLog.insertLogEntry(curDate,'TEST','bla bla bla')

        lenAfterInsert = len(self.myLog.getLogEntriesFrmDB())

        self.myLog.clearAllLogEntries()

        self.assertGreater(lenAfterInsert,lenBeforeInsert)

        lenAfterClearCmd = len(self.myLog.getLogEntriesFrmDB())

        self.assertEqual(lenAfterClearCmd,0)






    def test_getLastDayLogEntries(self):
        """
        Testing the getLastDayLogEntries method

        """

        curDate = conDateTimeToNum(datetime.now())
        date0 = curDate
        date1 = curDate - .5
        date2 = curDate - 2
        date3 = curDate - 3
        date4 = curDate - 5
        date5 = curDate - 8


        self.myLog.insertLogEntry(date0,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date1,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date2,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date3,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date4,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date5,'TEST','bla bla bla')


        self.assertLess(len(self.myLog.getLastDayLogEntries()),3)



    def test_getLastWeekLogEntries(self):
        """
        Testing the getLastWeekLogEntries method

        """

        curDate = conDateTimeToNum(datetime.now())
        date0 = curDate
        date1 = curDate - .5
        date2 = curDate - 2
        date3 = curDate - 3
        date4 = curDate - 5
        date5 = curDate - 8

        self.myLog.insertLogEntry(date0,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date1,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date2,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date3,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date4,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date5,'TEST','bla bla bla')

        self.assertEqual(len(self.myLog.getLastWeekLogEntries()),5)


    def test_getLastMonthLogEntries(self):
        """
        Testing the getLastMonthLogEntries method

        """

        curDate = conDateTimeToNum(datetime.now())
        date0 = curDate
        date1 = curDate - .5
        date2 = curDate - 2
        date3 = curDate - 3
        date4 = curDate - 5
        date5 = curDate - 8
        date6 = curDate - 40

        self.myLog.insertLogEntry(date0,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date1,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date2,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date3,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date4,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date5,'TEST','bla bla bla')
        self.myLog.insertLogEntry(date6,'TEST','bla bla bla')

        self.assertEqual(len(self.myLog.getLastMonthLogEntries()),6)






