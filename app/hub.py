#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module contains the Hub class. The hub is the central governing component of the homeBakedPi system.

"""


import pickle
from commUtil import *
from dateTimeConversion import *
import time
from numbers import Number
from eventQ import *
from node import *
import sqlite3
from occpSensor import *
from actuator import *
from imageSensor import *
from log import *


    
class Hub():
    """

    The hub is the central governing component of the homeBakedPi system. It is composed of one or more nodes. Each node contains
    one or more sensors. The hub contains several methods to manage the nodes (add, remove a node, get index of a node, etc)

    Attributes :
        - nodes : (list Nodes) list of all the nodes that compose the hub
        - actuators : (list Actuators) list of all the actuators that compose the hub
        - hubMailAgt : (EmailAgent) reference to the EmailAgent object of the hub
        - hubID : (string) name of the hub
        - eventQ : (EventQ) reference to the event queue object that is part of the hub
        - log : (Log) refernce to the log object of the hub
        - dbFile : (string) name of the database file associated to the hub

    """

    def __init__(self,hubID, dbFile, email = 'vinoroy70@gmail.com', emailPass = 'miller12',smsGateway='@sms.rogers.com',cellNumber='5147945869'):
        self.nodes = []
        self.node = Node('mock',self,'','','') # mock node for uml association
        self.actuators = []
        self.actuator = Actuator('mock','',self) # mock actuator for uml association
        self.hubMailAgt = EmailAgent(email,emailPass,smsGateway,cellNumber)
        self.hubID = hubID
        self.eventQ = EventQ(self)
        self.log = Log(self)
        self.dbFile = dbFile


    def getHubID(self):
        """
        Returns the hub id

        Args :
            - none

        Return :
            - (string) hub id

        """

        return  self.hubID


    def getDBFile(self):
        """
        Returns the database file name

        Args :
            - none

        Return :
            - (string) name of the database file

        """

        return self.dbFile



    def getEventQ(self):
        """
        Returns the event queue object of the hub

        Args :
            - none

        Return :
            - (EventQueue) event queue of the hub

        """

        return self.eventQ



    def getLog(self):
        """
        Returns the log object of the hub

        Args :
            - none

        Return :
            - (Log) log of the hub

        """

        return self.log


    def getNumberNodes(self):
        """
        Returns the number of nodes associated to the hub

        Args :
            - none

        Return :
            - (int) number of nodes associated to the hub

        """

        return len(self.nodes)



    def getNodeAtIdx(self,idx):
        """
        Returns the node at index

        Args :
            - (int) index of node to be returned

        Return :
            - (Node) node at index

        """

        return self.nodes[idx]



    def getHubMailAgt(self):
        """
        Returns the EmailAgent object associated to the hub

        Args :
            - none

        Return :
            - (EmailAgent) email agent object associated to the hub

        """

        return self.hubMailAgt



    def addNode(self,node):
        """
        Appends a node to the list of nodes associated to the hub

        Args :
            - node : (node object) a node that we wish to add to the node list

        Return :
            - none

        """

        if isinstance(node, Node ):
            self.nodes.append(node)


    def getNodeIdx(self,nodeID):
        """
        Gets the index for the corresponding node. Returns -1 if the node is
        not found

        Args :
            - nodeID : (string) name of the node

        Return :
            - (int) index of the node 0 to n (-1 if the node is not found)

        """

        # set the return value to -1 in case the node is not found
        nodeIdx = -1

        for i in range(0,len(self.nodes)):

            if (self.nodes[i].getNodeID() == nodeID):

                nodeIdx = i

                return nodeIdx

        return nodeIdx

        
    def getNode(self,nodeID):
        """
        Gets the reference for the corresponding node. Returns -1 if the node is
        not found

        Args :
            - nodeID : (string) name of the node

        Return :
            - (object ref)  reference to the node (-1 if the node is not found)

        """

        # set the return value to -1 in case the node is not found
        node = -1

        for i in range(0,len(self.nodes)):

            if (self.nodes[i].getNodeID() == nodeID):

                node = self.nodes[i]

                return node

        return node
                


    def addActuator(self,act):
        """
        Appends an actuator to the list of actuators associated to the hub

        Args :
            - actuator : (Actuator object) an actuator that we wish to add to the actuators list

        Return :
            - none

        """

        if isinstance(act, Actuator):
            self.actuators.append(act)



    def getActuator(self,actuatorID):
        """
        Gets the reference for the corresponding actuator. Returns -1 if the actuator is
        not found

        Args :
            - actuatorID : (string) name of the actuator

        Return :
            - (object ref)  reference to the actuator (-1 if the actuator is not found)

        """

        # set the return value to -1 in case the actuator is not found
        actuator = -1

        for curAct in self.actuators:

            if (curAct.getActuatorID() == actuatorID):

                actuator = curAct

                return actuator

        return actuator



    def getActuatorIdx(self,actuatorID):
        """
        Gets the index for the corresponding actuator. Returns -1 if the actuator is
        not found

        Args :
            - actuatorID : (string) name of the actuator

        Return :
            - (int) index of the actuator 0 to n (-1 if the actuator is not found)

        """

        # set the return value to -1 in case the actuator is not found
        actuatorIdx = -1

        for i in range(0,len(self.actuators)):

            if (self.actuators[i].getActuatorID() == actuatorID):

                actuatorIdx = i

                return actuatorIdx

        return actuatorIdx


    def getNumberActuators(self):
        """
        Returns the number of actuators associated to the hub

        Args :
            - none

        Return :
            - (int) number of actuators associated to the hub

        """

        return len(self.actuators)



    def lowFreqUpDate(self):
        """
        Requests all of the registered nodes to scan the low frequency sensors

        Args :
            - none

        Return :
            - none
        """

        print 'LOW frequency scan of all sensors :' + str(datetime.today())

        for aNode in self.nodes:
            aNode.scanSensors('LOW')

        print 'LOW frequency update state of all actuators :' + str(datetime.today())

        for aAct in self.actuators:
            aAct.updateDBState()



    def highFreqUpDate(self):
        """
        Requests all of the registered nodes to scan the high frequency sensors

        Args :
            - none

        Return :
            - none
        """

        print 'HIGH frequency scan sensors of each node :' + str(datetime.today()) + ' DateNum : ' + str(conDateTimeToNum(datetime.today()))

        for aNode in self.nodes:
            aNode.scanSensors('HIGH')


    def checkSchedulesOfActuators(self):
        """
        Requests all of the registered actuators to check their scheduling

        Args :
            - none

        Return :
            - none
        """

        for aActuator in self.actuators:

            aActuator.checkSchedule()


    def resetSchedulesOfActuators(self):
        """
        Reset the schedules of all of the registered actuators

        Args :
            - none

        Return :
            - none
        """

        for aActuator in self.actuators:

            aActuator.resetScheduleFlags()


    def prtHubAttributes(self):
        """
        Prints to the console the attributes of the hub. Used for debugging purposes

        Args :
            - none

        Return :
            - none
        """

        print '-----------------Hub attributes----------------'
        print 'Hub id :' + self.hubID
        print 'DB file :' + self.dbFile


        for node in self.nodes:

            node.prtNodeAttributes()


    def prtHubLastValuesFromDB(self):
        """
        Prints to the console the last values from DB (ie not buffer) of all the sensors of the attached to the hub.
        Used for debugging purposes

        Args :
            - none

        Return :
            - none
        """

        print 'Hub id :' + self.hubID
        print ""

        for node in self.nodes:

            node.prtNodeLastValuesFromDB()



    def getListOfNodes(self,nodeType = ''):
        """
        This method returns a list of all the node IDs attached to the hub that corrspond to the node type.
        If the node type is not specified all nodes attached to the hub will be returned.

        Args :
            - node type : (string) node type to for the list creation

        Return :
            - list of all the nodes that correspond to the node type
        """

        listOfNodes = []

        for node in self.nodes:

            if node.nodeType == nodeType or nodeType == '':
                listOfNodes.append(node.getNodeID())


        return listOfNodes


    def getListNodesInstruments(self,nodeType=''):
        """
        This method returns a list of all the node IDs - instruments attached to the hub.

        Args :
            - nodeType : (string) filter for the type of node

        Return :
            - list of all the nodes - instruments attached to the hub
        """

        listOfNodesInstruments= []

        for node in self.nodes:

            if node.nodeType == nodeType or node.nodeType == '':

                for inst in node.sensors:

                    listOfNodesInstruments.append(node.nodeID+':'+inst.instID)

        return listOfNodesInstruments



    def getInstAtNode(self,nodeID,instID):
        """
        This method

        Args :
            - nodeID : (string) ID of the node
            - instID : (string) ID of the instrument

        Return :
            - inst (ref Sensor) instrument object, -1 if not found
        """

        theNode = self.getNode(nodeID)

        if theNode != -1 :

            theInst = theNode.getSensor(instID)

            return theInst

        return -1



    def getAllLastValues(self):
        """
        This method returns a dictionary with the sensor values for each node

        Args :
            - none

        Return :
            - dict of all the nodes, each node contains list of all the last values for each sensor
        """

        lastValuesOfSensors = dict()

        listOfNodes = self.getListOfNodes()

        for node in listOfNodes:

            nodeRef = self.getNode(node)

            lastValuesOfSensors[node] = nodeRef.getSensorsValuesMatrix()

        return lastValuesOfSensors



    def getListOfNodesWithCamera(self):
        """
        This method returns a list of all the nodeID instID pairs that correspond to cameras

        Args :
            - none

        Return :
            - list of all the nodeID instID pairs that correspond to cameras
        """

        listOfNodesWithCam = []

        for node in self.nodes:

            for sensor in node.sensors:

                if isinstance(sensor,Camera) == 1:

                    insertStr = node.getNodeID() + ':' + sensor.getInstID()

                    listOfNodesWithCam.append(insertStr)

        return listOfNodesWithCam


    def getListActuatorsWithState(self):
        """
        This method returns a list of all the actuators with the present state (on  or off)

        Args :
            - none

        Return :
            - list of all actuator ids with the state (on or off) tagged at the end of the actuator id
        """

        listActuatorsWithState = []

        for actuator in self.actuators:

            curState = ''

            if actuator.getLastStateFrmDB()[0] == 0:

                curState = '(OFF)'

            else:

                curState = '(ON)'

            listActuatorsWithState.append([actuator.actuatorID+':'+curState,actuator.getState()])

        return listActuatorsWithState



    def getListActuators(self):
        """
        This method returns a list of all the actuators attached to the hub

        Args :
            - none

        Return :
            - list of all actuator ids
        """

        listActuators = []

        for actuator in self.actuators:

            listActuators.append(actuator.actuatorID)

        return listActuators
