#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the Sensor class offline (i.e. not connected to a sensor network). More
specifically the unit test are for testing the functions that are common to all sensor classes

"""


import unittest
from envSensor import *
from node import *
from hub import *
import sqlite3
import time
from dateTimeConversion import *
import datetime



#def setScanFreq(self,newFreq):
#def verifyThresholds(self):


class TestSensorOFF(unittest.TestCase):
    """
    Unit test class for testing the Sensor class offline (i.e. not attached to a physical sensing node). More
    specifically the unit test are for testing the functions that are common to all sensor classes. All tests are done
    with a Mock Humidity and Temp sensor
    """

    def setUp(self):
        """
        Setup the testing
        """

        self.myHub = Hub('Main','bakedPiDB')
        self.myNode = Node('KITCHEN',self.myHub,'','','ENV')

        self.testSenHumidity = MOCK_HumiditySensor('MOCK-HUMID-1',[0,101],self.myNode,'LOW')
        self.testSenTemp = MOCK_TempSensor('MOCK-TMP-1',[0,100],self.myNode,'LOW')
        self.testSenBaro = MOCK_TempSensor('MOCK-BARO-1',[0,1200],self.myNode,'LOW')

        self.myHub.setMonitoringParam('ENV',True)


    def tearDown(self):
        """
        Setup the testing
        """

        self.myHub.getLog().clearAllLogEntries()

        self.myHub.setMonitoringParam('ENV',False)


    def test_getLastReading_WOReadings(self):
        """
        Testing the getLastReading method using a mock temperature sensor without having taken a reading. Must return
        nothing.
        """

        newReading = self.testSenTemp.getLastReadingInBuffer()

        self.assertEqual(len(newReading),0)



    def test_getLastReadingStr_WOReadings(self):
        """
        Testing the getLastReadingStr method using a mock temperature sensor without having taken a reading.
        Must return the no data string.
        """

        self.assertEqual(self.testSenTemp.getLastReadingStrInBuffer(),"No data")


    def test_getLastReadingStr_WReadings(self):
        """
        Testing the getLastReadingStr method using a mock temperature sensor. This time with known readings in the sensor bank. Must return
        a string that is not empty.
        """

        self.assertGreater(len(self.testSenTemp.getLastReadingStrInBuffer()),0)


    def test_verifyThresholds_OverLimit(self):
        """
        Testing the verifyThresholds method with the mock temp sensor using a value that is over the upper threshold limit
        """

        testValue = self.testSenHumidity.getHighThreshhold() + 20
        numCurrDate = conDateTimeToNum(datetime.datetime.now())

        eventQLenBefore = self.myHub.getEventQ().getEventQLength()

        self.testSenHumidity.data.append([numCurrDate,testValue])
        self.testSenHumidity.verifyThresholds()

        eventQLenAfter = self.myHub.getEventQ().getEventQLength()

        self.assertGreater(eventQLenAfter,eventQLenBefore)




    def test_verifyThresholds_UnderLimit(self):
        """
        Testing the verifyThresholds method with the mock temp sensor using a value that is under the lower threshold limit
        """

        testValue = self.testSenHumidity.getLowThreshhold() - 20
        numCurrDate = conDateTimeToNum(datetime.datetime.now())

        eventQLenBefore = self.myHub.getEventQ().getEventQLength()

        self.testSenHumidity.data.append([numCurrDate,testValue])
        self.testSenHumidity.verifyThresholds()

        eventQLenAfter = self.myHub.getEventQ().getEventQLength()

        self.assertGreater(eventQLenAfter,eventQLenBefore)


    def test_verifyThresholds_InbetweenLimits(self):
        """
        Testing the verifyThresholds method with the mock temp sensor using a value that is in between the threshold limits
        """

        testValue = (self.testSenHumidity.getLowThreshhold() + self.testSenHumidity.getHighThreshhold())/2
        numCurrDate = conDateTimeToNum(datetime.datetime.now())

        eventQLenBefore = self.myHub.getEventQ().getEventQLength()

        self.testSenHumidity.data.append([numCurrDate,testValue])
        self.testSenHumidity.verifyThresholds()

        eventQLenAfter = self.myHub.getEventQ().getEventQLength()

        self.assertEqual(eventQLenAfter,eventQLenBefore)



    def test_storeReading(self):
        """
        Testing the storeReading method using a mock humidity sensor. The humidityreadings database table must have one
        more row.
        """

        conn = sqlite3.connect(self.myHub.getDBFile())

        cursor = conn.execute("SELECT Count(*) FROM HUMIDITYREADINGS")
        lenBefore = cursor.next()[0]

        self.testSenHumidity.takeReading()
        time.sleep(2) # delay to create a date in the db that is slightly different then the previous (db integrity)

        cursor = conn.execute("SELECT Count(*) FROM HUMIDITYREADINGS")
        lenAfter = cursor.next()[0]

        cursor.close()
        conn.close()

        self.assertGreater(lenAfter,lenBefore)



    def test_clearSensorValuesInDB(self):
        """
        Testing the clearSensorValuesInDB method
        """

        self.testSenHumidity.clearSensorValuesInDB()

        #######
        # Must add test here to verify that the db has been cleared



    def test_getSensorValuesFrmDB_allValues(self):
        """
        Testing the getSensorValuesFrmDB with no parameters. All values for the sensor are to be returned. To perform
        this test we will empty the db values of a given sensor, insert 3 new values and verify that ony three results
        are in the db
        """

        # clear all the values in the table for the sensor
        self.testSenHumidity.clearSensorValuesInDB()

        date1 = conDateTimeToNum(datetime.datetime(2012, 12, 31))
        date2 = conDateTimeToNum(datetime.datetime(2013, 12, 31))
        date3 = conDateTimeToNum(datetime.datetime(2014, 12, 31))

        self.testSenHumidity.storeReading(date1,1)
        self.testSenHumidity.storeReading(date2,2)
        self.testSenHumidity.storeReading(date3,3)

        queryResult = self.testSenHumidity.getSensorValuesFrmDB()

        self.assertEqual(len(queryResult),3)



    def test_getSensorValuesFrmDB_empty(self):
        """
        Testing the getSensorValuesFrmDB with no values in db will return empty array
        """

        self.testSenHumidity.clearSensorValuesInDB()

        queryResult = self.testSenHumidity.getSensorValuesFrmDB()

        self.assertEqual(len(queryResult),0)



    def test_getSensorValuesFrmDB_greaterThenADate(self):
        """
        Testing the getSensorValuesFrmDB with only a start date . All values for the sensor that are greater then are
        to be returned. To perform this test we will empty the db, insert given values and qery the insrtument to return the
        db for values greater then and we expect the result to return exactly three values since only three are greater than the
        given start date
        """

        self.testSenHumidity.clearSensorValuesInDB()


        # create the datenumbers for the start and dates to store in the db
        startDate = conDateTimeToNum(datetime.datetime(2014, 4, 1))
        date1 = conDateTimeToNum(datetime.datetime(2012, 12, 31))
        date2 = conDateTimeToNum(datetime.datetime(2013, 12, 31))
        date3 = conDateTimeToNum(datetime.datetime(2014, 12, 31))
        date4 = conDateTimeToNum(datetime.datetime(2015, 12, 31))
        date5 = conDateTimeToNum(datetime.datetime(2016, 12, 31))

        self.testSenHumidity.storeReading(date1,1)
        self.testSenHumidity.storeReading(date2,2)
        self.testSenHumidity.storeReading(date3,3)
        self.testSenHumidity.storeReading(date4,4)
        self.testSenHumidity.storeReading(date5,5)

        queryResult = self.testSenHumidity.getSensorValuesFrmDB(startDate)

        self.assertEqual(len(queryResult),3)



    def test_getSensorValuesFrmDB_between(self):
        """
        Testing the getSensorValuesFrmDB with between two dates . All values for the sensor that are between the two
        dates are to be returned. To perform this test we will empty the db, add known values and query the instrument
        for an expected return nmber of values
        """

        self.testSenHumidity.clearSensorValuesInDB()

        startDate = conDateTimeToNum(datetime.datetime(2014, 4, 1))
        endDate = conDateTimeToNum(datetime.datetime(2016, 4, 1))
        date1 = conDateTimeToNum(datetime.datetime(2012, 12, 31))
        date2 = conDateTimeToNum(datetime.datetime(2013, 12, 31))
        date3 = conDateTimeToNum(datetime.datetime(2014, 12, 31))
        date4 = conDateTimeToNum(datetime.datetime(2015, 12, 31))
        date5 = conDateTimeToNum(datetime.datetime(2016, 12, 31))

        self.testSenHumidity.storeReading(date1,1)
        self.testSenHumidity.storeReading(date2,2)
        self.testSenHumidity.storeReading(date3,3)
        self.testSenHumidity.storeReading(date4,4)
        self.testSenHumidity.storeReading(date5,5)

        queryResult = self.testSenHumidity.getSensorValuesFrmDB(startDate,endDate)

        self.assertEqual(len(queryResult),2)



    def test_getSensorValuesFrmDB_last(self):
        """
        Testing the getSensorValuesFrmDB to get only the last value. To perform this test we will empty the db, insert
        known values and query the instrument for a expected result.
        """

        self.testSenHumidity.clearSensorValuesInDB()

        date1 = conDateTimeToNum(datetime.datetime(2012, 12, 31))
        date2 = conDateTimeToNum(datetime.datetime(2013, 12, 31))
        date3 = conDateTimeToNum(datetime.datetime(2014, 12, 31))
        date4 = conDateTimeToNum(datetime.datetime(2015, 12, 31))
        date5 = conDateTimeToNum(datetime.datetime(2016, 12, 31))

        self.testSenHumidity.storeReading(date1,1)
        self.testSenHumidity.storeReading(date2,2)
        self.testSenHumidity.storeReading(date3,3)
        self.testSenHumidity.storeReading(date4,4)
        self.testSenHumidity.storeReading(date5,5)

        queryResult = self.testSenHumidity.getSensorValuesFrmDB(last=1)

        self.assertEqual(len(queryResult),1)

        self.assertEqual(queryResult[0][0],date5)


    def test_getLastWeekValuesFrmDB(self):
        """
        Testing the getLastWeekValuesFrmDB. To perform this test we will empty the db, insert known values and query
        the instrument for the expected result.
        """

        self.testSenHumidity.clearSensorValuesInDB()

        cur = conDateTimeToNum(datetime.datetime.now())
        date1 = cur - .5
        date2 = cur - 1
        date3 = cur - 2
        date4 = cur - 5
        date5 = cur - 8

        self.testSenHumidity.storeReading(date1,1)
        self.testSenHumidity.storeReading(date2,2)
        self.testSenHumidity.storeReading(date3,3)
        self.testSenHumidity.storeReading(date4,4)
        self.testSenHumidity.storeReading(date5,5)

        queryResult = self.testSenHumidity.getLastWeekValuesFrmDB()

        self.assertEqual(len(queryResult),4)



    def test_getLastDayValuesFrmDB(self):
        """
        Testing the getLastDayValuesFrmDB to perform this test we will empty the db, insert known values and query for
        the expected result
        """

        self.testSenHumidity.clearSensorValuesInDB()

        cur = conDateTimeToNum(datetime.datetime.now())
        date1 = cur - .5
        date2 = cur - 1
        date3 = cur - 2
        date4 = cur - 5
        date5 = cur - 8

        self.testSenHumidity.storeReading(date1,1)
        self.testSenHumidity.storeReading(date2,2)
        self.testSenHumidity.storeReading(date3,3)
        self.testSenHumidity.storeReading(date4,4)
        self.testSenHumidity.storeReading(date5,5)

        queryResult = self.testSenHumidity.getLastDayValuesFrmDB()

        self.assertEqual(len(queryResult),2)



    def test_getLastMonthValuesFrmDB(self):
        """
        Testing the getLastMonthValuesFrmDB. To perform this test we will empty the db, insert known values and query for
        the expected result
        """

        self.testSenHumidity.clearSensorValuesInDB()

        cur = conDateTimeToNum(datetime.datetime.now())
        date1 = cur - .5
        date2 = cur - 20
        date3 = cur - 22
        date4 = cur - 40
        date5 = cur - 50

        self.testSenHumidity.storeReading(date1,1)
        self.testSenHumidity.storeReading(date2,2)
        self.testSenHumidity.storeReading(date3,3)
        self.testSenHumidity.storeReading(date4,4)
        self.testSenHumidity.storeReading(date5,5)

        queryResult = self.testSenHumidity.getLastMonthValuesFrmDB()

        self.assertEqual(len(queryResult),3)



    def test_getHub(self):
        """
        Testing the getHub will return the valid value of the hub that is associated to the Node that is associated to
        the sensor
        """

        self.myNode.addSensor(self.testSenHumidity)
        self.myHub.addNode(self.myNode)

        self.assertEqual(self.testSenHumidity.getHub(),self.myHub)



    def test_getInstID(self):
        """
        Testing that the getInstID will return the valid value of the sensor ID
        """

        self.assertEqual(self.testSenHumidity.getInstID(),'MOCK-HUMID-1')


    def test_getNode(self):
        """
        Testing that the getNode will return the valid value of the node associated to the sensor
        """

        self.assertEqual(self.testSenHumidity.getNode(),self.myNode)




    def test_getHighThreshhold(self):
        """
        Testing that the getHighThreshhold will return the valid value of the threshold
        """

        self.assertEqual(self.testSenHumidity.getHighThreshhold(),101)



    def test_getLowThreshhold(self):
        """
        Testing that the getLowThreshhold will return the valid value of the threshold
        """

        self.assertEqual(self.testSenHumidity.getLowThreshhold(),0)


    def test_setThresholds(self):
        """
        Testing that the setThresholds will update the object values and also update the database
        """

        self.testSenBaro.setThresholds(23,45)




if __name__ == '__main__':
    unittest.main()

