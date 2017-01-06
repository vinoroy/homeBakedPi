#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the timeConvertToDays module offline (i.e. not connected to the sensor network and the internet)

"""

import unittest
from timeConvertToDays import *


class TestTimeConvertToDays(unittest.TestCase):
    """
    Test class for testing the timeConvertToDays module offline (i.e. not connected to the sensor network and the internet)
    """

    def setUp(self):
        """
        Setup the testing
        """

        pass

    def test_conversionSecToDays(self):
        """
        Testing the conversion of seconds to days unit
        """

        self.assertEqual(conSecondsToDays(43200),0.5)


    def test_conversionMinToDays(self):
        """
        Testing the conversion of minutes to days unit
        """

        self.assertEqual(conMinutesToDays(720),0.5)


    def test_conversionHrsToDays(self):
        """
        Testing the conversion of hours to days unit
        """

        self.assertEqual(conHoursToDays(12),0.5)



if __name__ == '__main__':
    unittest.main()