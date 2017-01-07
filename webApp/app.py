"""
@author: Vincent Roy [D]

This module contains the classes and functions for the homeBakedPi web app.

"""


import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../app'))
if not path in sys.path:
    sys.path.insert(1, path)
del path


from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DecimalField
from wtforms.validators import Required, DataRequired
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_file, send_from_directory
from subprocess import call
from hbpApp import *
from flask import jsonify
from datetime import datetime
from datetime import timedelta
from dateTimeConversion import *



# create an app using the Flask frame work
app = Flask(__name__)

# get a twitter bootstrap instance associated to the recently created app
bootstrap = Bootstrap(app)

# configurate the the app (security, username and password)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='my first cat is pompom',
    USERNAME='admin',
    PASSWORD='pompom',
    IMAGES='../imgArch'
))



class LoginForm(Form):
    """
    Class for the login form. This will include the types of fields to be used and the validation process of each field

    Attributes :
        - userID : (string) user id of the current user that is loging in
        - passW : (string) password of the user
        - submit : (button)

    """

    userID = StringField('What is your ID?', validators=[Required()])
    passW = PasswordField('What is your password?', validators=[Required()])
    submit = SubmitField('Submit')



class ThreshForm(Form):
    """
    Class for the threshold form. This will include the types of fields to be used and the validation process of each field

    Attributes :
        - lowThresh : (float) new value for the low threshold of the instrument
        - highThresh : (float) new value for the high threshold of the instrument
        - submit : (button)

    """

    lowThresh = DecimalField('Low thresh', validators=[Required()])
    highThresh = DecimalField('High thresh', validators=[Required()])
    submit = SubmitField('Submit')


class ScheduleForm(Form):
    """
    Class for the actuator schedule form. This will include the types of fields to be used and the validation process of each field

    Attributes :
        - openTime : (float) new value for the open time of the actuator
        - closeTime : (float) new value for the close time of the actuator
        - submit : (button)

    """

    openTime = DecimalField('Open time', validators=[Required()])
    closeTime = DecimalField('Close time', validators=[Required()])
    submit = SubmitField('Submit')



def makeHub():
    """
    This function create a homeBakedPi Hub based on the parameters in the homeBakedPi instance

    Args :
        - none

    Return :
        -  hub : (obj ref) hub object
    """

    theHub = createHub(['../app/parameters.xml',sys.argv[1]])

    return theHub


def getHub():
    """
    Gets the current session hub. If no hub object is available in the session one is created

    Args :
        - none

    Return :
        - (obj ref) hub object
    """

    if not hasattr(g, 'theHub'):
        g.theHub = makeHub()
    return g.theHub



@app.route('/')
def index():
    """
    Function to render the index page of the app

    Args :
        - none

    Return :
        - (page ref) index page
    """

    theHub = getHub()

    listNodes = theHub.getListOfNodes()

    cams = theHub.getListOfNodesWithCamera()

    actuators = theHub.getListActuatorsWithState()

    return render_template('index.html',listNodes=listNodes,cams=cams,actuators=actuators)


@app.route('/intro')
def intro():
    """
    Function to render the intro page of the app. once the user has logged in

    Args :
        - none

    Return :
        - (page ref) intro page
    """

    if not session.get('logged_in'):
        abort(401)

    theHub = getHub()

    listNodes = theHub.getListOfNodes()

    results = theHub.getAllLastValues()

    cams = theHub.getListOfNodesWithCamera()

    actuators = theHub.getListActuatorsWithState()

    return render_template('intro.html',listNodes=listNodes,cams=cams,actuators=actuators,results=results)


@app.route('/envNodesSummary')
def envNodesSummary():
    """
    Function to render the environmental nodes summary page of the app

    Args :
        - none

    Return :
        - (page ref) environmental nodes summary page page
    """

    if not session.get('logged_in'):
        abort(401)

    theHub = getHub()

    listNodes = theHub.getListOfNodes()

    results = theHub.getAllLastValues()

    cams = theHub.getListOfNodesWithCamera()

    actuators = theHub.getListActuatorsWithState()

    return render_template('envNodesSummary.html',results=results,listNodes=listNodes,cams=cams,actuators=actuators)



@app.route('/uploads/<path:filename>')
def download_file(filename):
    """
    Function to down load an image file

    Args :
        - none

    Return :
        -
    """

    return send_from_directory(app.config['IMAGES'], filename, as_attachment=True)



@app.route('/cameraImage/', methods=['GET'])
def cameraImage():
    """
    Function to render the current image of a given node camera

    Args :
        - none

    Return :
        - (page ref) cameraImage page
    """

    if not session.get('logged_in'):
        abort(401)

    selNodeCam = request.args.get('selNodeCam')
    temp = selNodeCam.split(':',1)
    selNode = temp[0]
    selCam = temp[1]

    theHub = getHub()

    listNodes = theHub.getListOfNodes()

    cams = theHub.getListOfNodesWithCamera()

    theNode = theHub.getNode(selNode)
    theCam = theNode.getSensor(selCam)
    theCam.takeReading()

    # get the last image name stored in the db and date
    result =  theCam.getSensorValuesFrmDB(last=1)
    imageFileName = result[0][2]
    imageDateStr = result[0][1]


    #extract the image filename without the path
    start = imageFileName.find('Arch/')+5
    imageFileName = imageFileName[start:]


    return render_template('cameraImage.html',cams=cams,listNodes=listNodes,imageFileName=imageFileName,imageDateStr=imageDateStr,selNode=selNode,selCam=selCam)



@app.route('/toggleActuator/', methods=['GET'])
def toggleActuator():
    """
    Function to toggle the state of a given actuator

    Args :
        - none

    Return :
        - (page ref) intro.html page
    """

    if not session.get('logged_in'):
        abort(401)

    selActuator = request.args.get('selActuator')
    temp = selActuator.split(':',1)
    selActuator = temp[0]

    theHub = getHub()

    listNodes = theHub.getListOfNodes()

    results = theHub.getAllLastValues()

    cams = theHub.getListOfNodesWithCamera()

    theActuator = theHub.getActuator(selActuator)
    theActuator.toggleSwitch()

    print selActuator
    print 'Current state : '+str(theActuator.getState())

    actuators = theHub.getListActuatorsWithState()

    return render_template('intro.html',listNodes=listNodes,cams=cams,actuators=actuators,results=results)



@app.route('/envNodeDetailed/', methods=['GET'])
def envNodeDetailed():
    """
    Function to render the environmental node detailed page of the app

    Args :
        - none

    Return :
        - (page ref) environmental node detailed page page
    """

    if not session.get('logged_in'):
        abort(401)

    selNode = request.args.get('selNode')
    selSensorNum = int(request.args.get('selSensorNum'))
    selGrafTable = request.args.get('selGrafTable')
    selTimePeriode = request.args.get('selTimePeriode')

    theHub = getHub()

    theNode = theHub.getNode(selNode)

    listNodes = theHub.getListOfNodes()

    cams = theHub.getListOfNodesWithCamera()

    actuators = theHub.getListActuatorsWithState()
    listOfSensors = theNode.getListSensorsID()

    selSensor = theNode.getSensor(listOfSensors[selSensorNum])
    selSensorName = selSensor.instID

    # based on the selected time interval get the measurements fot the instrument
    if selTimePeriode == '1 Day':

        listOfValues = selSensor.getLastDayValuesFrmDB()


    elif selTimePeriode == '1 Week':

        listOfValues = selSensor.getLastWeekValuesFrmDB()

    elif selTimePeriode == '1 Month':

        listOfValues = selSensor.getLastMonthValuesFrmDB()

    return render_template('envNodeDetailed.html',cams=cams,listNodes=listNodes,selNode=selNode, listOfSensors=listOfSensors,selSensorName=selSensorName,selSensorNum=selSensorNum,listOfValues=listOfValues,selGrafTable=selGrafTable,selTimePeriode=selTimePeriode,actuators=actuators)



@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Decorator function for url call to login.html. The login.html page displays a form to enter the username, password
    and a submit button. Once data is submitted a call is made to the current login function and the submitted results
    (ie username and password) are verified to see if acces is granted to the web app.

    Args:
        - passed in via the post method. the parameters are the username and the password

    Return :
        - login.html page

    """

    error = None

    form = LoginForm()

    # check to see if the form has been submitted
    if form.validate_on_submit():
        userID = form.userID.data
        passW = form.passW.data


        if userID != app.config['USERNAME']:
            error = 'Invalid username'

        if passW != app.config['PASSWORD']:
            error = 'Invalid password'

        # if the user and pass are valid then set loggin to true and open the intro page
        else:

            session['logged_in'] = True

            absURL = megaurl_for('intro')
            return redirect(absURL)

    # if the form has not submitted than display the login form
    return render_template('login.html', form=form, error=error)



@app.route('/logout')
def logout():
    """
    Decorator function for url call to logout.html

    Args :
        - none

    Return :
        - logout.html

    """

    session.pop('logged_in', None)

    return render_template('index.html')


@app.route('/setThresholds/', methods=['GET', 'POST'])
def setThresholds():
    """
    Function to display and handle the form for setting the thresholds of a given instrument.

    Args:
        - passed in via the post method. the parameters are the low and high threshold of an instrument

    Return :
        - (page ref) threshold page or intro page if the form has been submitted

    """

    error = None

    thresholds = []

    if not session.get('logged_in'):
        abort(401)

    theHub = getHub()

    listNodes = theHub.getListOfNodes()

    cams = theHub.getListOfNodesWithCamera()

    actuators = theHub.getListActuatorsWithState()

    listNodesInst = theHub.getListNodesInstruments('ENV')

    selNodeInst = request.args.get('selNodeInst')

    if selNodeInst in listNodesInst:

        tmp = selNodeInst.split(':')
        nodeID = tmp[0]
        instID = tmp[1]

        print 'The selected inst : ' + instID

        theInst = theHub.getInstAtNode(nodeID,instID)

        thresholds = theInst.getThresholds()

    form = ThreshForm()

    # if the form values are valid
    if form.validate_on_submit():

        lowThresh = form.lowThresh.data
        highThresh = form.highThresh.data

        selNodeInst = request.args.get('selNodeInst')

        tmp = selNodeInst.split(':')
        nodeID = tmp[0]
        instID = tmp[1]

        theInst = theHub.getInstAtNode(nodeID,instID)

        theInst.setThresholds(lowThresh,highThresh)

        return redirect('/intro')

    # if the form has not submitted than display t
    return render_template('setThresholds.html',listNodes=listNodes,cams=cams,actuators=actuators, form=form, error=error, selNodeInst=selNodeInst,listNodesInst=listNodesInst, thresholds=thresholds)



@app.route('/setSchedules/', methods=['GET', 'POST'])
def setSchedules():
    """
    Function to display and handle the form for setting the schedule times of a given actuator.

    Args:
        - passed in via the post method. the parameters are the open and close time for a given actuator

    Return :
        - (page ref) threshold page or intro page if the form has been submitted

    """

    error = None

    scheduleTimes = []

    if not session.get('logged_in'):
        abort(401)

    theHub = getHub()

    listNodes = theHub.getListOfNodes()

    cams = theHub.getListOfNodesWithCamera()

    actuators = theHub.getListActuatorsWithState()

    listActuators = theHub.getListActuators()

    selActuator = request.args.get('selActuator')

    if selActuator in listActuators:

        print 'The selected actuator : ' + selActuator

        theAct = theHub.getActuator(selActuator)

        scheduleTimes = theAct.getScheduleTimes()

    form = ScheduleForm()

    if form.validate_on_submit():

        openTime = form.openTime.data
        closeTime = form.closeTime.data

        selActuator = request.args.get('selActuator')

        theAct = theHub.getActuator(selActuator)

        theAct.setScheduleTimes(openTime,closeTime)

        return redirect('/intro')

    # if the form has not submitted than display it
    return render_template('setSchedules.html',listNodes=listNodes,cams=cams,actuators=actuators, form=form, error=error, selActuator=selActuator,listActuators=listActuators, scheduleTimes=scheduleTimes)



def megaurl_for(funcName):
    """
    Function to adjust the url of a redirect based on prod or dev server environment

    Args :
        - none

    Return :
        - (string) adjusted url based on environment type
    """

    # get the external URL and the local and compare
    fullUrl = url_for(funcName,_external = True)
    localUrl = url_for(funcName)
    localServerStr = ':5000'

    # see if :5000 is in the external string
    pos = fullUrl.find(localServerStr)

    # identify if we are on the local server or on the production server
    # and adjust the url
    if pos >= 0 : # :5000 is in the string
        return localUrl

    # production server
    else :
        pos = fullUrl.find(localUrl);
        return fullUrl[0:pos] + ':8080' + localUrl


@app.route('/systemOver')
def systemOver():
    """
    Function to render the homeBakedPi system overview web page

    Args :
        - none

    Return :
        - (page ref) homeBakedPi system description web page
    """

    if not session.get('logged_in'):
        abort(401)

    theHub = getHub()

    listNodes = theHub.getListOfNodes()

    cams = theHub.getListOfNodesWithCamera()

    actuators = theHub.getListActuatorsWithState()

    return render_template('systemOver.html',cams=cams,listNodes=listNodes,actuators=actuators)



@app.route('/systemActivation')
def systemActivation():
    """
    Function to render the system activation parameters page where the user can arm and disarm the system. This
    function is UNDER CONSTRUCTION !!!

    Args :
        - none

    Return :
        - (page ref) homeBakedPi system activation page
    """

    if not session.get('logged_in'):
        abort(401)

    theHub = getHub()

    listNodes = theHub.getListOfNodes()

    cams = theHub.getListOfNodesWithCamera()

    actuators = theHub.getListActuatorsWithState()

    return render_template('systemActivation.html',cams=cams,listNodes=listNodes,actuators=actuators)



#**********************************************************************************************************************
#
# API for the homeBakedPi HUB
#
#**********************************************************************************************************************


@app.route('/insertSensorValue/<insertStr>')
def insertSensorValue(insertStr):
    """
    Function to insert a value for an instrument. This is used generally used when an instrument sends data over the network
    as a result of an event.

    Args :
        - insertStr (string) string the indicates the nodeID, the instID and the value

    Return :
        - (string) insertion confirmation
    """

    # split the insert string into its components to get nodeID, instID and value
    splitInsertStr = insertStr.split(';')
    nodeID = splitInsertStr[0]
    instID = splitInsertStr[1]
    value = float(splitInsertStr[2])

    theHub = getHub()

    theInstrument = theHub.getInstAtNode(nodeID,instID)

    if theInstrument != -1 :

        theInstrument.insertEventValue(value)

        return '1'

    else:

        return '0'



if __name__ == '__main__':

    # when on production server
    app.run()

    # when on the dev environment
    #app.run(host='0.0.0.0',port=5000,debug=True)