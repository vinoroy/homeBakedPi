#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This modules contains a function and a simple script that creates a hub from a database file using the hubFactory based
on the passed in arguments. This module is used to create the homeBakedPi network in a script context

"""


from hubFactory import *
from paramReader import *
from paramReader import *
import sys


def createHub(argv):
    """
    Function that creates a hub from a database file using the hubFactory based
    on the passed in arguments.

    Args :
        - pos 0 : (string) file name containing the environmental parameters
        - pos 1 : (string) environment type (prod, dev, flaskServer, etc)

    Returns :
        - aHub : (ref Hub) a populated Hub object

    """


    # read the environment variables from the files passed in the first paramter
    envParams = paramReader(argv[0])

    # get the environment type (prod or dev) from the passed in environment parameters
    envType = argv[1]

    # get the environement params for the given environment type
    params = envParams[envType]

    # extract the environment parameters
    dbPath = params['dbPath']
    email = params['email']
    emailPass = params['emailPass']
    mockMode = params['mockMode']

    #print '-------------Env Params-------------------'
    #print 'Environment parameters from file %s' % argv[0]
    #print 'Environment type : %s' % envType
    #print 'Database path : %s' % dbPath
    #print 'Email : %s' % email
    #print 'Email password : %s' % emailPass

    myFac = HubFactory(dbPath,mockMode,email,emailPass)

    aHub = myFac.createHub()

    return aHub




if __name__ == "__main__":

    # create a Hub and use the second and thrird passed in argument
    theHub = createHub(sys.argv[1:3])

    theHub.prtHubAttributes()

    # execute command if user passed a third argument [low,high,node:sensor](low scan, high scan or output all values
    # for a sensor)
    if len(sys.argv) >= 4 :
        cmd = sys.argv[3]

        if cmd == 'low' :

            theHub.lowFreqUpDate()

        elif cmd == 'high' :

            theHub.highFreqUpDate()

        elif cmd == 'chkSchedules':

            theHub.checkSchedulesOfActuators()


        elif cmd == 'resetSchedules':

            # reset the schedules of each registered actuator with the hub
            theHub.resetSchedulesOfActuators()

        # get the values of a specific node for a specific sensor (ex KITCHEN:TMP-1)
        else:


            splitParamStr = cmd.split(':')

            nodeStr = splitParamStr[0]
            sensorStr = splitParamStr[1]
            theNode = theHub.getNode(nodeStr)
            theSensor = theNode.getSensor(sensorStr)

            print theSensor.getSensorValuesFrmDB()


    print theHub.getAllLastValues()