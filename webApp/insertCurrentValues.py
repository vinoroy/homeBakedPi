#!/usr/bin/env python
"""
@author: Vincent Roy [DTP]

Module with Unit test class for testing the api of the homeBakedPiWebApp

"""


import unittest
import urllib2


response = urllib2.urlopen('http://127.0.0.1:5000/insertSensorValue/KITCHEN;TMP-1;50')
print response.read()

response = urllib2.urlopen('http://127.0.0.1:5000/insertSensorValue/KITCHEN;LDR-1;500')
print response.read()

response = urllib2.urlopen('http://127.0.0.1:5000/insertSensorValue/KITCHEN;HUMID-1;50')
print response.read()

response = urllib2.urlopen('http://127.0.0.1:5000/insertSensorValue/ENTRANCE;SW-1;1')
print response.read()

response = urllib2.urlopen('http://127.0.0.1:5000/insertSensorValue/ENTRANCE;MD-1;1')
print response.read()






