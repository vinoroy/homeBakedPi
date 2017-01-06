#!/usr/bin/env python
"""
@author: Vincent Roy [*]

This module contains the classes used by the homeBakedPi system to communicate with the outside
world. It contains the EmailAgent class as well as the FtpAgent

"""

import smtplib
import ftplib
import imaplib




class EmailAgent:
    """
    Used to setup and send emails via gmail smtp server

    Attributes :
        - usrEmail : (string) email address of the user
        - pwd : (string) password for the usr email account

    """

    def __init__(self, usrEmail, pwd):
        self.usrEmail = usrEmail
        self.pwd = pwd
    
    def sendMsg(self,to , subject, msg):
        """
        Send a simple text message to an email via gmail smtp server

        Args :
            - subject : (string) subject of the email
            - msg : (string) text message of the email

        Return :
            - none

        """

        # setup the connection with gmail smtp server
        smtpserver = smtplib.SMTP("smtp.gmail.com",587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(self.usrEmail, self.pwd)
        
        # prepare the email with a subject and a message
        header = 'To:' + to + '\n' + 'From: ' + self.usrEmail + '\n' + 'Subject:' + subject+' \n'
        cmpmsg = header + '\n '+ msg + '\n\n'
        
        # send the mail to the destined user email
        smtpserver.sendmail(self.usrEmail, to, cmpmsg)

        smtpserver.close()
        

class FtpAgent:
    """
    Used to setup an ftp agent that can send and retrieve files from an ftp server

    Attributes :
        - url : (string) url of the FTP server
        - user : (string) usr name of the FTP account
        - passwd : (string) password of the ftp account
    """
    
    def __init__(self, url, usr, passwd):
        self.url = url
        self.usr = usr
        self.passwd = passwd
        

    def getFile(self,targetDir,targetFile,destFile):
        """
        Retrieve a target file from a target directory on the ftp server and save to the
        specified destination file on the local machine

        Args:
            - targetDir : (string) path to the directory of the target file
            - targetFile : (string) name of the target file
            - destFile : (string) name of the destination file

        Return :
             - none

        """

        # open ftp connection
        ftp = ftplib.FTP(self.url,self.usr,self.passwd)

        # get the file
        ftp.cwd(targetDir)
        gFile = open(destFile, "wb")
        ftp.retrbinary('RETR '+targetFile, gFile.write)
        gFile.close()
        ftp.quit()


    def putFile(self,targetDir,targetFile):
        """
        Transfer a target file on local machine to the target directory of the ftp server

        Args :
            - targetDir : (string) path of the directory where the file to transfer resides
            - targetFile : (string) name of the file to be transfered

        Return :
            - none
        """
        
        # open ftp connection
        ftp = ftplib.FTP(self.url,self.usr,self.passwd)

        # open the file to be transfered and transfer
        gFile = open(targetFile, "rb")
        ftp.cwd(targetDir)
        ftp.storbinary('STOR ' + targetFile, gFile)
        gFile.close()
        ftp.quit()


    def prtGettedFile(self, destFile):
        """
        For debugging purposes print out the contents of the retreived file

        Args :
            - destFile : (string) name of the file that was transfered to the local machine

        Return :
            - none

        """


        print "\nReadme File Output:"

        gFile = open(destFile, "r")
        buff = gFile.read()

        print buff

        gFile.close()



def numberOfEmailsInbox(usrEmail, pwd):
    """
    This function counts the number of unread mails in the users inbox. This function is used for unittest validation
    purposes
    """


    # create an IMAP object
    mail = imaplib.IMAP4_SSL('imap.gmail.com',993)

    # login
    mail.login(usrEmail, pwd)

    # get the indox of the account
    mail.select("inbox")

    # get all of the unseen mails
    typ, messageIDs = mail.search(None, "UNSEEN")
    messageIDsString = str( messageIDs[0])
    listOfSplitStrings = messageIDsString.split(" ")

    # return the number of unseen mails
    return len(listOfSplitStrings)
