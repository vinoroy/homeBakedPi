#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the dateTimeConversion class

"""

import unittest
from datetime import datetime
from dateTimeConversion import *


class TestDateTimeConversion(unittest.TestCase):
    """
    Unit test class for testing the dateTimeConversion class
    """

    def setUp(self):
        """
        Setup the testing
        """
        pass
    
    def test_conVersion(self):
        """
        Testing the conDateTimeToNum & conNumToDateTime methods
        """
        # get the date object for the 1 jan 2004 and convert it to a date number
        # then back again to a date object, the test make sure that the original
        # date object is equal to the converted    
        testDate = datetime(2004,1,1)
        numTestDate = conDateTimeToNum(testDate)
        backTestDate = conNumToDateTime(numTestDate)
        self.assertEqual(testDate,backTestDate)


    def test_conDateTimeToNum(self):
        """
        Testing the conDateTimeToNum with a known datenumber value

        """
        testDate = datetime(1900,1,30)
        numTestDate = conDateTimeToNum(testDate)
        knownDateNum = 30
        self.assertEqual(numTestDate,knownDateNum)


    def test_conNumToDateTime(self):
        """
        Testing the conNumToDateTime with a known date object

        """

        testDateNum = 30
        testDate = conNumToDateTime(testDateNum)
        knownDate = datetime(1900,1,30)
        self.assertEqual(testDate,knownDate)



    def test_conNumToNumDateGregorian(self):
        """
        Testing the conNumToNumDateGregorian with a known Gregorian date number

        """

        testDateNum = 30
        testDateGreg = conNumToNumDateGregorian(testDateNum)
        knownDateNumGreg = 30 + 693594
        self.assertEqual(testDateGreg,knownDateNumGreg)



    def test_conDateNumToDateStr(self):
        """
        Testing the conDateNumToDateStr with a know date string

        """

        testDate = datetime(1900,1,30)
        testDateStr = testDate.strftime("%Y-%m-%d %H:%M:%S")
        testDateNum = conDateTimeToNum(testDate)

        self.assertEqual(conDateNumToDateStr(testDateNum),testDateStr)



 
if __name__ == '__main__':
    unittest.main()