#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module contains a factory class designed for the creation of a Hub.

"""


import unittest
from envSensor import *
from occpSensor import *
from node import *
from hub import *


class HubFactory:
    """
    The HubFactory is a factory class that is responsible for the creation of a hub. Hub creation can be linked
    to a database, hence all of the hub attibutes and nodes can be loaded from a database.

    Attributes :
        - dbFile : (string) name of data base file that contains the node and sensor attributes as well as the tables for the readings
        - fromDB : (int) 0  - do not create hub and sensors from database file (for testing purposes)
                         1  - create the hub from the attributes stored in the database file
        - email : (string) email address where the notifications will be sent
        - emailPass : (string) password for the email account where the notifications will be sent.
        - smsGateway : (string) root address of the email to sms gateway
        - cellNumber : (string) cell number to be used to send sms using the email to sms gateway
        - mockMode : (int) flag to indicate if the application hub is in test mode (1 = test mode)

    """

    def __init__(self, dbFile, mockMode, email = 'vinoroy70@gmail.com', emailPass = 'miller12',smsGateway='',cellNumber=''):
        self.dbFile = dbFile
        self.email = email
        self.emailPass = emailPass
        self.smsGateway = smsGateway
        self.cellNumber = cellNumber
        self.mockMode = mockMode



    def createHub(self):
        """
        Creates a hub and returns it to the requester.

        Args :
            - none

        Return :
            - hub object

        """

        self.myHub = Hub('Main',self.dbFile,self.email, self.emailPass,self.smsGateway,self.cellNumber)

        ######################################################################################################
        # create the nodes and the sensors
        ######################################################################################################

        conn = sqlite3.connect(self.dbFile)

        try:

            nodesInDB = conn.execute("SELECT * FROM NODES")

            for currNode in nodesInDB:

                currNodeName = currNode[0]
                nodeName = currNode[0]
                nodeMsgID = currNode[1]
                active = currNode[2]
                urlStr = currNode[3]
                nodeType = currNode[4]
                mockFlag = currNode[5]


                # if the node is active and verify if the mode of the app corresponds to the test flag (1 == test mode)
                if active == 1 and mockFlag == self.mockMode:


                    self.myNode = Node(nodeName,self.myHub,nodeMsgID,urlStr,nodeType)

                    sensorsInDBForNodeX = conn.execute("SELECT * FROM SENSORS WHERE NODEID ='%s'" % (currNodeName))

                    for currSensor in sensorsInDBForNodeX:

                        instID = currSensor[1]
                        active = currSensor[2]
                        instType = currSensor[3]
                        lowLimit = currSensor[4]
                        upperLimit = currSensor[5]
                        freq = currSensor[6]

                        # create a sensor based on the appropriate sensor type. This section will need to be changed for each new
                        # sensor type
                        if active == 1 and instType == 'IPTEMP':

                            self.myNode.addSensor(IPTempSensor(instID,[lowLimit,upperLimit],self.myNode,freq))

                        elif active == 1 and instType == 'IPLDR':

                            self.myNode.addSensor(IPLDRSensor(instID,[lowLimit,upperLimit],self.myNode,freq))

                        elif active == 1 and instType == 'IPHUMID':

                            self.myNode.addSensor(IPHumiditySensor(instID,[lowLimit,upperLimit],self.myNode,freq))

                        elif active == 1 and instType == 'IPDOORSWITCH':

                            self.myNode.addSensor(IPDoorSwitch(instID,lowLimit,self.myNode,freq))

                        elif active == 1 and instType == 'IPMOTION':

                            self.myNode.addSensor(IPMotionDetection(instID,lowLimit,self.myNode,freq))

                        elif active == 1 and instType == 'MOCKTEMP':

                            self.myNode.addSensor(MOCK_TempSensor(instID,[lowLimit,upperLimit],self.myNode,freq))

                        elif active == 1 and instType == 'MOCKLDR':

                            self.myNode.addSensor(MOCK_LDRSensor(instID,[lowLimit,upperLimit],self.myNode,freq))

                        elif active == 1 and instType == 'MOCKBARO':

                            self.myNode.addSensor(MOCK_BarometricPressureSensor(instID,[lowLimit,upperLimit],self.myNode,freq))

                        elif active == 1 and instType == 'MOCKHUMIDITY':

                            self.myNode.addSensor(MOCK_HumiditySensor(instID,[lowLimit,upperLimit],self.myNode,freq))

                        elif active == 1 and instType =='MOCKDOOR':

                            self.myNode.addSensor(MOCK_DoorSwitch(instID,lowLimit,self.myNode,freq))

                    sensorsInDBForNodeX.close()

                    self.myHub.addNode(self.myNode)


            nodesInDB.close()
            conn.close()

            print 'Hub created on : ' + str(datetime.today())

        except sqlite3.OperationalError, msg:

            print msg


        ##############################################################################################################
        # create the actuators
        ##############################################################################################################

        conn = sqlite3.connect(self.dbFile)

        try:

            actuatorsInDB = conn.execute("SELECT * FROM ACTUATORS")

            for currAct in actuatorsInDB:

                actID = currAct[0]
                actType = currAct[1]
                actAddress = currAct[2]
                actOpenTime = currAct[3]
                actCloseTime = currAct[4]
                mockFlag = currAct[9]

                if mockFlag == self.mockMode:

                    if actType == 'MOCK_V110Switch':

                        self.myHub.addActuator(MOCK_V110Switch(actID,actAddress,self.myHub,actOpenTime,actCloseTime))

            actuatorsInDB.close()
            conn.close()


        except sqlite3.OperationalError, msg:

            print msg


        return self.myHub




