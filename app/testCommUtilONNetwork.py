#!/usr/bin/env python
"""
@author: Vincent Roy [*]

Module with Unit test class for testing the commUtil class on the network (i.e internet)

"""

import unittest
from commUtil import *
import pickle
from datetime import datetime


class TestCommUtilONNetwork(unittest.TestCase):
    """
    Unit test class for testing the commUtil class
    """

    def setUp(self):
        """
        Setup the testing
        """
        pass
    
    def test_sendMsg_EmailAgent(self):
        """
        Testing Email agent sendMsg method by counting the number of emails in inbox then sending an email and counting
        the emails in the inbox after.
        """


        emailsBefore = numberOfEmailsInbox('vinoroy70@gmail.com','miller12')


        myMail = EmailAgent('vinoroy70@gmail.com','miller12')
        currDateTime = datetime.today()
        currDateTimeStr = currDateTime.isoformat().__str__()
        testMsg = 'Testing the email agent : '+currDateTimeStr
        testSubject = 'Email agent unit test'
        myMail.sendMsg('vinoroy70@gmail.com',testSubject,testMsg)


        emailsAfter = numberOfEmailsInbox('vinoroy70@gmail.com','miller12')


        self.assertGreater(emailsAfter,emailsBefore)


    # currently not tested for lack of an ftp server
    
    # def test_putFile_getFile_FtpAgent(self):
    #     """
    #     # Testing ftp agent putFile & getFile methods
    #     """
    #
    #     # create an Ftp agent to the geekgarage ftp server
    #     myFtp = FtpAgent('geekgarage.org','geek0751','MillerBeer12@')
    #     # create a simple list of numbers and dump it into a test file
    #     aList = [1,2,3]
    #     pickle.dump(aList, open( "test123.p", "wb" ))
    #     # send the test file to the server
    #     myFtp.putFile("/xchange",'test123.p')
    #     # get the test file from the server and store in a new file
    #     myFtp.getFile("/xchange",'test123.p',"geted.p")
    #     # load the file and put the contents in a list
    #     comList = pickle.load(open( "geted.p", "rb" ))
    #     # compare the two lists and make sure the contents are the same
    #     self.assertEqual(aList[0],comList[0])
    
 
if __name__ == '__main__':
    unittest.main()