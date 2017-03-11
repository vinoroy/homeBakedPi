#!/usr/bin/python
"""
@author: Vincent Roy [*]

This module contains the xml reader and parser for the parameters file

"""


from xml.dom.minidom import parse
import xml.dom.minidom
import sys


def paramReader(fileName):
    """
    Xml reader and parser for the parameters file

    Args :
        - fileName : (string) name of the file that is to be read and parsed

    Returns :
        - envDict : (dictionary) dictionay of all the environment parameters

    """

    envDict = dict()

    try :

        # open XML document using minidom parser
        DOMTree = xml.dom.minidom.parse(fileName)
        envList = DOMTree.documentElement

        # get all the environments in the collection (file)
        environments = envList.getElementsByTagName("env")

        for env in environments:

            # create a temporary dict to store the paramters of one environement
            tempParams = dict()

            # get the environment type
            envStr = env.getAttribute("title")

            # get the path of the database file
            dbPath = env.getElementsByTagName('dbPath')[0]
            dbPathStr = dbPath.childNodes[0].data
            tempParams['dbPath'] = dbPathStr


            # get the email
            email = env.getElementsByTagName('email')[0]
            emailStr = email.childNodes[0].data
            tempParams['email'] = emailStr

            # get the email password
            emailPass = env.getElementsByTagName('emailPass')[0]
            emailPassStr = emailPass.childNodes[0].data
            tempParams['emailPass'] = emailPassStr


            # get the smsGateway
            smsGateway = env.getElementsByTagName('smsGateway')[0]
            smsGatewayStr = smsGateway.childNodes[0].data
            tempParams['smsGateway'] = smsGatewayStr


            # get the cellNumber
            cellNumber = env.getElementsByTagName('cellNumber')[0]
            cellNumberStr = cellNumber.childNodes[0].data
            tempParams['cellNumber'] = cellNumberStr


            # get the mock Mode
            mockMode = env.getElementsByTagName('mockMode')[0]
            mockModeStr = mockMode.childNodes[0].data
            tempParams['mockMode'] = int(mockModeStr) # convert to int


            # insert the parameters of the environment into the dictionary of environments
            envDict[envStr] = tempParams

    # if the file does not exist do nothing, or something else
    except:

        pass

    return envDict


if __name__ == "__main__":

    env = paramReader('parameters.xml')

    print env