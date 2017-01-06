#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module implements all of the abstract and concrete classes for the environmental type sensors.

"""


import random
from subprocess import call
from datetime import datetime
from datetime import timedelta
from dateTimeConversion import *
import platform
import random
import sqlite3
from sensorEvent import *
from sensor import *
    

class TempSensor(Sensor):
    """
    Abstract class for the temperature family of sensors. Here only some specific
    attributes are specified, no method implementation
    """
    
    def __init__(self,node,freq,instID):
        Sensor.__init__(self,node,freq,instID)
        self.mesureType = 'Temperature'
        self.mesureUnit ='deg C'
        self.instType =''
        self.dbTable = 'TEMPREADINGS'
        self.alarmMsg = 'Temperature alarm'
        


class IPTempSensor(TempSensor):
    """
    IP temperature sensor class
    """

    def __init__(self, instID, limits,node,freq):
        TempSensor.__init__(self,node,freq,instID)
        self.instType = 'IPTEMP'
        self.thrsh = limits
        self.urlSensorExtension = 'temp'


    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # send a request to the mock node to get the value of the sensor
        sensorValue = self.sendUrlRequestToNode(self.urlSensorExtension)

        return sensorValue


class MOCK_TempSensor(TempSensor):
    """
    Mock temperture class used for integration and unit tests when
    sensors are offline
    """
    
    def __init__(self, instID, limits,node,freq):
        TempSensor.__init__(self,node,freq,instID)
        self.instType = 'MOCKTEMP'
        self.thrsh = limits
        


    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # generate a rendom int number for the temperature
        idxRnd = random.randint(0, 4)
        mockValues = [-2, -12, 45, 46, 47]
        mockValue = mockValues[idxRnd]

        return mockValue



class LDRSensor(Sensor):
    """
    Abstract class for the LDR (light dependant resistor) family of sensors. Here only some specific
    attributes are specified, no method implementation
    """

    def __init__(self,node,freq,instID):
        Sensor.__init__(self,node,freq,instID)
        self.mesureType = 'Light'
        self.mesureUnit ='luus'
        self.instType =''
        self.dbTable = 'LDRREADINGS'
        self.alarmMsg = 'Lighting level alarm'


class IPLDRSensor(LDRSensor):
    """
    IP LDR (light dependant resistor) sensor
    """

    def __init__(self, instID, limits,node,freq):
        LDRSensor.__init__(self,node,freq,instID)
        self.instType = 'IPLDR'
        self.thrsh = limits
        self.urlSensorExtension = 'ldr'


    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # send a request to the mock node to get the value of the sensor
        sensorValue = self.sendUrlRequestToNode(self.urlSensorExtension)

        return sensorValue



class MOCK_LDRSensor(LDRSensor):
    """
    Mock LDR class used for integration and unit tests when
    sensors are offline
    """

    def __init__(self, instID, limits,node,freq):
        LDRSensor.__init__(self,node,freq,instID)
        self.instType = 'MOCKLDR'
        self.thrsh = limits
        


    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # generate a rendom int number for the light value
        idxRnd = random.randint(0, 4)
        mockValues = [200, 134, 450, 900, 678]
        mockValue = mockValues[idxRnd]

        return mockValue





class HumiditySensor(Sensor):
    """
    Abstract class for the humidity family of sensors. Here only some specific
    attributes are specified, no method implementation
    """

    def __init__(self,node,freq,instID):
        Sensor.__init__(self,node,freq,instID)
        self.mesureType = 'Humidity'
        self.mesureUnit ='% Humidity'
        self.instType =''
        self.dbTable = 'HUMIDITYREADINGS'
        self.alarmMsg = 'Humidity level alarm'
        



class IPHumiditySensor(HumiditySensor):
    """
    IP humidity sensor class
    """

    def __init__(self, instID, limits,node,freq):
        HumiditySensor.__init__(self,node,freq,instID)
        self.instType = 'IPHUMID'
        self.thrsh = limits
        self.urlSensorExtension = 'humid'


    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # send a request to the mock node to get the value of the sensor
        senorValue = self.sendUrlRequestToNode(self.urlSensorExtension)

        return senorValue



class MOCK_HumiditySensor(HumiditySensor):
    """
    Mock humidity class used for integration and unit tests when
    sensors are offline
    """

    def __init__(self, instID, limits,node,freq):
        HumiditySensor.__init__(self,node,freq,instID)
        self.instType = 'MOCKHUMIDITY'
        self.thrsh = limits
        

    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # generate a rendom int number for the humidity values
        idxRnd = random.randint(0, 4)
        mockValues = [34, 67, 45, 90, 88]
        mockValue = mockValues[idxRnd]

        return mockValue



class BarometricPressureSensor(Sensor):
    """
    Abstract class for the barometric pressure family of sensors. Here only some specific
    attributes are specified, no method implementation
    """

    def __init__(self,node,freq,instID):
        Sensor.__init__(self,node,freq,instID)
        self.mesureType = 'Barometric pressure'
        self.mesureUnit ='hPa'
        self.dbTable = 'BAROREADINGS'
        self.alarmMsg = 'Barometric pressure alarm'
        


class IPBaroSensor(BarometricPressureSensor):
    """
    IP barometric pressure sensor class
    """

    def __init__(self, instID, limits,node,freq):
        BarometricPressureSensor.__init__(self,node,freq,instID)
        self.instType = 'IPBARO'
        self.thrsh = limits
        self.urlSensorExtension = 'baro'


    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # send a request to the mock node to get the value of the sensor
        sensorValue = self.sendUrlRequestToNode(self.urlSensorExtension)

        return sensorValue


class MOCK_BarometricPressureSensor(BarometricPressureSensor):
    """
    Mock barometric pressure class used for integration and unit tests when
    sensors are offline
    """

    
    def __init__(self, instID, limits,node,freq):
        BarometricPressureSensor.__init__(self,node,freq,instID)
        self.instType = 'MOCKBARO'
        self.thrsh = limits
        

    def getValueFrmSensor(self):
        """
        Returns the current value from the sensor

        Args :
            - none

        Return :
            - (double) sensor value

        """

        # generate a random int number for the barometric value
        idxRnd = random.randint(0, 4)
        mockValues = [95, 102, 100, 99, 101]
        mockValue = mockValues[idxRnd]

        return mockValue