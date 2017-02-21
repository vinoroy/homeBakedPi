"""
@author: Vincent Roy [D]

This module contains the classes and functions for the

"""


import os
import sys



from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_file, send_from_directory
from datetime import datetime
from datetime import timedelta
from dateTimeConversion import *
from eventQueue import *
import time



# create an app using the Flask frame work
app = Flask(__name__)


# configurate the the app (security, username and password)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='my first cat is pompom',
    USERNAME='admin',
    PASSWORD='pompom'
))




def makeQueue():
    """
    This function create a homeBakedPi Hub based on the parameters in the homeBakedPi instance

    Args :
        - none

    Return :
        -  hub : (obj ref) hub object
    """

    theQ = EventQueue()

    return theQ


def getQueue():
    """
    Gets the current session hub. If no hub object is available in the session one is created

    Args :
        - none

    Return :
        - (obj ref) hub object
    """

    if not hasattr(g, 'theQ'):
        g.theQ = makeQueue()
    return g.theQ



@app.route('/')
def index():
    """
    Function to render the index page of the app

    Args :
        - none

    Return :
        - (page ref) index page
    """

    theQ = getQueue()


    return 'Welcome to the event API : possible entries /door /motion /rfid'




@app.route('/insertEvent/<eventStr>')
def insertSensorValue(eventStr):
    """
    Function to insert a value for

    Args :
        - eventStr (string) string the indicate

    Return :
        - (string) insertion confirmation
    """

    #split the insert string into its components to get nodeID, instID and value
    splitEventStr = eventStr.split(';')
    eventType = splitEventStr[0]
    nodeID = splitEventStr[1]
    instID = splitEventStr[2]
    value = float(splitEventStr[3])


    theQ = getQueue()


    if eventType == 'door':

        theQ.addEventToQueue(DoorOpening(theQ,nodeID,instID,value))

        theQ.printEvents()

        theQ.handleEvents()

        return '1'

    elif eventType == 'motion':

        theQ.addEventToQueue(MotionDetection(theQ,nodeID,instID,value))

        theQ.printEvents()

        theQ.handleEvents()

        return '1'

    elif eventType == 'rfid':

        theQ.addEventToQueue(RFIDDetection(theQ,nodeID,instID,value))

        theQ.printEvents()

        theQ.handleEvents()

        return '1'

    else:

        return '0'



@app.route('/door')
def door():


    time.sleep(20)


    return 'door slept for 20 seconds'


@app.route('/rfid')
def rfid():




    return 'vincent has taged in'









if __name__ == '__main__':

    # when on production server
    app.run()

    # when on the dev environment
    #app.run(host='0.0.0.0',port=5000,debug=True)
