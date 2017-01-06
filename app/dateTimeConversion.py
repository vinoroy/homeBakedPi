#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module contains functions to convert a datetime object into a
datenumber and back to a datetime object. The datenumber system is based on the Excel
datenumber system which sets datenumber 0 equivalent to 1900\01\00

"""

from __future__ import division
from datetime import datetime
from datetime import timedelta


def conDateTimeToNum(dateToBeConv):
    """
    Converts date object into a datenumber of the Excel datenumber system (1900/01/00)

    Args :
        - dateToBeConv : (datetime) date to be converted

    Returns :
        - dateNum : (float)

    """

    dateOrigin = datetime(1899, 12, 31)

    delta = dateToBeConv - dateOrigin

    dateNum = float(delta.days) + (float(delta.seconds) / 86400)

    return dateNum


def conNumToDateTime(dateNum):
    """
    Converts a date number back to a date object

    Args :
        - dateNum : (float) date number to be converted to a date object

    Return :
        - dateObj : (datetime) date time object of the date number
    """

    dateOrigin = datetime(1899, 12, 31)

    delta = timedelta(days=dateNum)

    dateObj = dateOrigin + delta

    return dateObj


def conNumToNumDateGregorian(dateNum):
    """
    Converts a date number of the excel datenumber system (1900-01-01) to the Gregorian date (0000-01-01)

    Args :
        - dateNum : (float) date number to be converted to Gregorian date number

    Return :
        - dateNum : (float) date number to be converted to Gregorian date number
    """

    # add the number of days since the birth of christ 0000 01 01
    dateNum = dateNum +693594

    return dateNum


def conDateNumToDateStr(dateNum):
    """
    Converts a date number to a date in string format

    Args :
        - dateNum (float) date number to be converted to a string representation of the date

    Return :
        - (string) string representation of the date
    """

    return conNumToDateTime(dateNum).strftime("%Y-%m-%d %H:%M:%S")


def nowInHours():
        """
        Helper function to get the current time in decimal hours
        """

        curDateTime = datetime.now()

        curHr = curDateTime.hour
        curMin = curDateTime.minute
        curSec = curDateTime.second

        curTimeDecimalHours = curHr + curMin/60 + curSec/3600

        return curTimeDecimalHours


if __name__ == "__main__":
    print 'Decimal hrs : ' + str(nowInHours())
    print 'Decimal days : ' + str(conDateTimeToNum(datetime.now()))



