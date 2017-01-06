#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing

"""

import unittest
from paramReader import *


class TestParamReader(unittest.TestCase):
    """
    Test class for testing the
    """

    def setUp(self):
        """
        Setup the testing
        """

        pass


    def test_paramReader_withThreeEnvs(self):
        """
        Testing the paramReader with know number of environments
        """

        # read the xml file and id that there are four environments
        myEnv = paramReader('parameters.xml')
        self.assertEqual(len(myEnv),4)


    def test_paramReader_noParams(self):
        """
        Testing the paramReader with no params in the file and verify that there are no environment variables
        """

        myEnv = paramReader('parametersNoEnvs.xml')
        self.assertEqual(len(myEnv),0)


    def test_readParams_noFile(self):
        """
        Testing the paramReader with no existing file
        """

        myEnv = paramReader('fileThatDoesNotExist.xml')

        self.assertEqual(len(myEnv),0)


    def test_readParams_notXMLFile(self):
        """
        Testing the paramReader with a file that has no xml
        """

        myEnv = paramReader('parametersNotXML.xml')

        self.assertEqual(len(myEnv),0)


    def test_readParams_verifyContents(self):
        """
        Testing the paramReader and that it returns the correct content of the xml file
        """

        envParams = paramReader('parameters.xml')

        # get the environement params for the given environment type
        params = envParams['dev-m']

        self.assertEqual(params['dbPath'],'bakedPiDB')
        self.assertEqual(params['email'],'vinoroy70@gmail.com')
        self.assertEqual(params['emailPass'],'miller12')
        self.assertEqual(params['mockMode'],1)
