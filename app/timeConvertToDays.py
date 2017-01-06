#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module that contains functions for the conversion of time units (seconds, minutes & hours) into days

"""

from __future__ import division

def conSecondsToDays(sec):
    """
    Converts seconds into days unit

    Args :
        - sec : (float) number of seconds to be converted into days unit

    Return :
        - (float) number of days
    """

    days = sec/(60*60*24)

    return days


def conMinutesToDays(min):
    """
    Converts minutes into days unit

    Args :
        - min : (float) number of minutes to be converted into days unit

    Return :
        - (float) number of days

    """

    days = min/(60*24)

    return days

def conHoursToDays(hrs):
    """
    Converts hours into days unit

    Args :
        - hrs : (float) number of hours to be converted into days unit

    Return :
        - (float) number of days
    """

    days = hrs/24

    return  days


