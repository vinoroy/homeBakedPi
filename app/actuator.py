#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module contains the base class and derived classes of the actuator types that can be used in a homeBakedPi
network.


"""


from __future__ import division
from datetime import datetime
from datetime import timedelta
from dateTimeConversion import *
import sqlite3
import time
import sys
from datetime import datetime






class Actuator:
    """
    This class is an abstract class of the actuator type. No concrete objects can be logically
    instantiated from this class. Furthermore not all methods are implemented

    Attributes :

        - actuatorType : (string) actuator type (ex WEMO 110V switch)
        - actuatorID : (string) identification for the sensor
        - address : (string) address to localize the actuator
        - dbTable : (string) name of the table that stores the actuator data

    """


    def __init__(self, actuatorID, address, hub):
        self.actuatorType = ''
        self.actuatorID = actuatorID
        self.address = address
        self.dbTable = 'ACTUATORS'
        self.hub = hub




    def getState(self):
        """
        Not implemented in the base class but must be implemented in the concrete
        classes

        Args :
            - none

        Return :
            - none
        """

        raise NotImplementedError( "Should have implemented this" )


    def setOpen(self):
        """
        Not implemented in the base class but must be implemented in the concrete
        classes

        Args :
            - none

        Return :
            - none
        """

        raise NotImplementedError( "Should have implemented this" )


    def setClose(self):
        """
        Not implemented in the base class but must be implemented in the concrete
        classes

        Args :
            - none

        Return :
            - none
        """
        raise NotImplementedError( "Should have implemented this" )


    def getHub(self):
        """
        Returns the hub object associated to the actuator

        Args :
            - none

        Return :
            - (Hub) hub object associated to the node

        """

        return self.hub


    def getAddress(self):
        """
        Returns the network address of the actuator

        Args :
            - none

        Return :
            - (string) network address of the actuator

        """

        return self.address


    def getActuatorID(self):
        """
        Returns the ID of the actuator

        Args :
            - none

        Return :
            - (string) ID of the actuator

        """

        return self.actuatorID


    def updateDBState(self):
        """
        Updates the state of the actuator in the database

        Args :
            - none

        Return :
            - none

        """

        curState = self.getState()

        curDateTime = datetime.now()
        curDateTimeNum = conDateTimeToNum(curDateTime)


        conn = sqlite3.connect(self.getHub().getDBFile())


        # update the state data for the current actuator
        conn.execute("UPDATE '%s' SET LASTSTATE = '%i', LASTSTATETIME = '%f' WHERE ACTUATORID = '%s'" % (self.dbTable,curState,curDateTimeNum,self.actuatorID))
        conn.commit()

        conn.close()


    def getLastStateFrmDB(self):
        """
        Get the last state of the actuator from the database

        Args :
            - none

        Return :
            - (list) last state (int : 0 for closed & 1 for open) and the last date time number (double)

        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        # get the last db state for the current actuator
        result = conn.execute("SELECT * FROM '%s' WHERE ACTUATORID = '%s' LIMIT 1" % (self.dbTable,self.actuatorID))
        row = result.fetchone()
        lastDBState = [row[7],row[8]]

        conn.close()

        return lastDBState



class V110Switch(Actuator):
    """
    Abstract class for the 110V family of switches. Here only some specific
    attributes are specified and added to the actuator base class.

    Attributes :

        - actuatorType : (string) actuator type (ex WEMO 110V switch)
        - actuatorID : (string) identification for the sensor
        - address : (string) address to localize the actuator
        - openTimes : (float list) list that contains the ON times in hours
        - closeTimes : (string) list that contains the OFF times in hours

    """


    def __init__(self,actuatorID,address,hub,openTime,closeTime):
        Actuator.__init__(self,actuatorID,address,hub)
        self.openTime = openTime
        self.closeTime = closeTime



    def setScheduleTimes(self,openTime,closeTime):
        """
        Function to set the open and close time schedule of the actuator

        Args :
            - openTime : (float) value of the open time
            - closeTime : (float) value  of the close time

        Return :
            - none

        """

        self.openTime = openTime

        self.closeTime = closeTime

        conn = sqlite3.connect(self.getHub().getDBFile())

        # set the new open and close time and reset the open and close flags
        conn.execute("UPDATE ACTUATORS SET OPENTIME = '%f', CLOSETIME = '%f', OPENFLAG = 0, CLOSEFLAG = 0 WHERE ACTUATORID = '%s'" % (openTime,closeTime,self.actuatorID))
        conn.commit()

        conn.close()



    def getScheduleTimes(self):
        """
        Function to return the open and close time schedule of the actuator

        Args :
            - none

        Return :
            - (float list) openTime and closeTime

        """

        return [self.openTime, self.closeTime]


    def checkSchedule(self):
        """
        Checks the scheduled open and close times programmed for the actuator and consequently opens or closes the switch

        Args :
            - none

        Return :
            - none

        """

        # get the current decimal time
        curDateTime = datetime.now()
        curHr = curDateTime.hour
        curMin = curDateTime.minute
        curTime = curHr + curMin/60



        # if the switch is closed and the curTime is greater than the scheduled open time and the switch flag has not been set to done
        # for the given schedule time then open and set the flag to done
        if self.getState() == 0 and curTime >= self.openTime and curTime <= self.closeTime and self.getOpenFlag() == 0:


            self.setOpen()

            # if the switch was succesfully opened then set the open flag to 0 ... meaning that it has been done
            if self.getState() == 1:

                self.setOpenFlag(1)


        # if the switch is already open and the curTime is greater than the scheduled open time and the switch flag has not been set to done
        # for the given schedule time then set the flag to done
        elif self.getState() == 1 and curTime >= self.openTime and curTime <= self.closeTime and self.getOpenFlag() == 0:

            self.setOpenFlag(1)



        # if the switch is open and the curTime is greater than the scheduled close time and the switch has not been closed for
        # for the given schedule time then close
        elif self.getState() == 1 and curTime > self.closeTime and self.getCloseFlag() == 0:


            self.setClose()

            # if the switch was succesfully closed then set the close time check to 0 ... meaning that it has been done
            if self.getState() == 1:

                self.setCloseFlag(1)


        # if the switch is already closed and the curTime is greater than the scheduled close time and the switch flag has not been set to done
        # for the given schedule time then set the flag to done
        elif self.getState() == 0 and curTime > self.closeTime and self.getCloseFlag() == 0:

            self.setCloseFlag(1)



    def setOpenFlag(self,openFlag):
        """
        Sets to the db the state of the open flag

        Args :
            - openFlag : (int) state of the flag to set

        Return :
            - none

        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        # update the open flag
        conn.execute("UPDATE ACTUATORS SET OPENFLAG = '%d' WHERE ACTUATORID = '%s'" % (openFlag,self.actuatorID))
        conn.commit()

        conn.close()


    def setCloseFlag(self,closeFlag):
        """
        Sets to the db the state of the close flag

        Args :
            - closeFlag : (int) state of the flag to set

        Return :
            - none

        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        conn.execute("UPDATE ACTUATORS SET CLOSEFLAG = '%d' WHERE ACTUATORID = '%s'" % (closeFlag,self.actuatorID))
        conn.commit()

        conn.close()


    def resetScheduleFlags(self):
        """
        Resets to the db the state of the open and close flags to 0

        Args :
            - none

        Return :
            - none

        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        # update the close flag
        conn.execute("UPDATE ACTUATORS SET OPENFLAG = 0 AND CLOSEFLAG = 0 WHERE ACTUATORID = '%s'" % (self.actuatorID))
        conn.commit()

        conn.close()



    def getOpenFlag(self):
        """
        Gets from the db the state of the open flag

        Args :
            - none

        Return :
            - (int) state of the open flag to set

        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        result = conn.execute("SELECT OPENFLAG FROM ACTUATORS WHERE ACTUATORID = '%s'" % (self.actuatorID))
        openFlag = result.fetchone()[0]

        conn.close()

        return openFlag



    def getCloseFlag(self):
        """
        Gets from the db the state of the close flag

        Args :
            - none

        Return :
            - (int) state of the close flag to set

        """

        conn = sqlite3.connect(self.getHub().getDBFile())

        result = conn.execute("SELECT CLOSEFLAG FROM ACTUATORS WHERE ACTUATORID = '%s'" % (self.actuatorID))
        closeFlag = result.fetchone()[0]

        conn.close()

        return closeFlag




    def toggleSwitch(self):
        """
        Checks the current state of the switch and toggles the state

        Args :
            - none

        Return :
            - none

        """

        curState = self.getState()

        if curState == 0:

            self.setOpen()

        if curState == 1:

            self.setClose()



class MOCK_V110Switch(V110Switch):
    """
    MOCK 110V outlet switch actuator
    """

    def __init__(self,actuatorID,address,hub,openTime=None,closeTime=None):
        V110Switch.__init__(self,actuatorID,address,hub,openTime,closeTime)
        self.actuatorType = 'MOCK_V110Switch'
        self.currentState = 0


    def getState(self):
        """
        Function that returns the state of the actuator switch. 1 for open and 0 for closed

        Args :
            - none

        Return :
            - (int) 0 for closed and 1 for open
        """

        return self.currentState


    def setOpen(self):
        """
        Function that sets the actuator switch to open

        Args :
            - none

        Return :
            - none
        """

        self.currentState = 1

        self.updateDBState()




    def setClose(self):
        """
        Function that sets the actuator switch to close

        Args :
            - none

        Return :
            - none
        """

        self.currentState = 0

        self.updateDBState()









