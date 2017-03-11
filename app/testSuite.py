#!/usr/bin/env python
"""
@author: Vincent Roy [DTP]

Script that contains the entire test suite for HomeBakedPi. The script allows the configuration of testing blocks.
A testing block is a set of unit tests that are grouped together because they have a common environmental testing
parameter, such as testing on the internet or testing with a live sensor network.

"""

import unittest


# parameters of the test
off = 1         # testing off the internet and off the sensor network
net = 1         # testing on the internet
local = 1       # testing on the local network (i.e. physical nodes active on the local server)




# perform test that are off line (off the internet and the sensor network)
if (off == 1):

    from testParamReader import *

    from testHubOFF import  *
    from testHubFactoryOFF import*

    from testNodeOFF import *

    from testSensorOFF import *
    from testEnvSensorOFF import *
    from testOccpSensorOFF import *

    from testActuatorOFF import *

    from testDateTimeConversion import *
    from testTimeConvertToDays import *

    from testEventQOFF import *
    from testEventOFF import *
    from testActionsOFF import *
    from testLogOFF import *

    from testHomeBakedPiActuatorSchedulerOFF import *


# perform tests that are on the internet
if (net == 1):

    from testEventQueueONNetwork import *

    from testCommUtilONNetwork import *

    from testActionsON import *


# perform the test that are on the local network (i.e. physical nodes active on the local server)
if (local == 1):


    from testEnvSensorONLocalNetwork import *

    from testHomeBakedPiONLocalNetwork import *



if __name__ == '__main__':
    
    unittest.main()