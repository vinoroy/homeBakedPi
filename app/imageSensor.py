#!/usr/bin/env python
"""
@author: Vincent Roy []

This module contains all of the image sensor classes

"""


import random
from subprocess import call
from datetime import datetime
from datetime import timedelta
from dateTimeConversion import *
import platform
import random
import sqlite3
import urllib,re
from sensorEvent import *
from sensor import *



class Camera(Sensor):
    """
    Abstract class for the camera family of sensors. Here only some specific
    attributes are specified, no method implementation
    """

    def __init__(self,node,freq,instID):
        Sensor.__init__(self,node,freq,instID)
        self.mesureType = 'Image'
        self.mesureUnit ='jpg'
        self.dbTable = 'CAMREADINGS'


    def takeReading(self):
        """
        Not implemented in the base class but must be in the concrete
        classes
        """

        raise NotImplementedError( "Should have implemented this" )


    def storeReading(self,date,value):
        """
        Stores the reading for the camera class of sensors. Overides the base class store method

        Args :
            - tableName
            - instID
            - date
            - value

        Return :
            - none

        """

        conn = sqlite3.connect(self.node.hub.dbFile)

        conn.execute("INSERT INTO '%s' VALUES ('%s','%s','%f','%s',0)" % (self.dbTable,self.node.nodeID,self.instID,date,value))
        conn.commit()

        conn.close()




# class Pi_Camera(Camera):
#     """
#     Camera connected to a RaspberryPi microcontroller.
#
#     """
#
#
#     def __init__(self,instID,node,freq):
#         Camera.__init__(self,node,freq,instID)
#         self.instType ='RaspiCamera'
#
#
#     def takeReading(self):
#         """
#         Take a reading from the camera sensor that is connected to the Raspberry Pi microcontroller
#
#         Return :
#             - none
#
#         """
#
#         # prepare the command string which includes the name of the file which
#         # is the name of the instID
#         imgFile = self.instID + ".jpg"
#         cptStr = "raspistill -q 60 -o " + imgFile
#
#         # call the take picture command
#         call ([cptStr], shell=True)
#
#         # get current date and convert to date num
#         currDate = datetime.today()
#         numCurrDate = conDateTimeToNum(currDate)
#
#         # store the last result in the database
#         self.storeReading(numCurrDate,imgFile)
#
#          # append date and image file name to the sensor data vector
#         self.data.append([numCurrDate,imgFile])
#
#
# class Pi_WebCamera(Camera):
#     """
#     Camera connected to a RaspberryPi on a web service.
#
#     """
#
#
#     def __init__(self,instID,node,freq):
#         Camera.__init__(self,node,freq,instID)
#         self.instType ='PIWEBCAM'
#
#
#     def takeReading(self):
#         """
#         Take a reading from the camera sensor that is connected to a Raspberry Pi on a web service
#
#         Return :
#             - none
#
#         """
#
#         # compose the url for the image capture function
#         imageCaptureURL = self.node.nodeURL
#         imageCaptureURL = imageCaptureURL + '/getPict'
#
#         # extract the image name from the web page resulting from the image capture
#         imageCapturePage = urllib.urlopen(imageCaptureURL).read()
#         for imgName in re.findall('[A-Za-z1-9]*.jpg', imageCapturePage):
#             print imgName
#
#
#         # compose the url where the image is stored on the web server
#         imageURL = self.node.nodeURL+'/static/' + imgName
#
#
#         # get current date and time string
#         currDate = datetime.today()
#         curDateStr = currDate.strftime('%y-%m-%d-%H-%M')
#
#         # get the node id
#         nodeStr = self.node.nodeID + '_'
#
#
#         # compose the name and path of the image to be saved. The name includes the current date and time
#         filename = '../imgArch/' + nodeStr + curDateStr + '.jpg'
#
#         # extract an save the image from the url
#         urllib.urlretrieve(imageURL, filename)
#
#
#         # get current date and convert to date num
#         currDate = datetime.today()
#         numCurrDate = conDateTimeToNum(currDate)
#
#         # store the last result in the database
#         self.storeReading(numCurrDate,filename)
#
#          # append date and image file name to the sensor data vector
#         self.data.append([numCurrDate,filename])



class MOCK_Camera(Camera):
    """
    Mock camera class used for integration and unit tests when
    sensors are offline
    """

    def __init__(self,instID,node,freq):
        Camera.__init__(self,node,freq,instID)
        self.instType ='Mock_Camera'


    def takeReading(self):
        """
        Take a reading of the mock camera sensor

        Return :
            - none

        """

        imgFile = self.instID + ".jpg"

        currDate = datetime.today()
        numCurrDate = conDateTimeToNum(currDate)

        self.storeReading(numCurrDate,imgFile)

        self.data.append([numCurrDate,imgFile])


