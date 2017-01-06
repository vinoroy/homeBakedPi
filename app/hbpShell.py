import cmd, sys
from hbpApp import *
from subprocess import *

class HomeBakedPiShell(cmd.Cmd):

    intro = 'Welcome to the homeBakedPi shell.   Type help or ? to list commands.\n'
    prompt = '(hbp) '


    def do_scan(self, arg):
        'Perform a scan and print the last values of each sensor'

        theHub = createHub(['parameters.xml',sys.argv[1]])

        theHub.lowFreqUpDate()

        theHub.prtHubLastValuesFromDB()


    def do_lstVals(self, arg):
        'Print the last values of each sensor'

        theHub = createHub(['parameters.xml',sys.argv[1]])

        theHub.prtHubLastValuesFromDB()


    def do_hub(self, arg):
        'Print all of the nodes and sensors associated to the hub'

        theHub = createHub(['parameters.xml',sys.argv[1]])

        theHub.prtHubAttributes()

    def do_lstValsMat(self, arg):

        theHub = createHub(['parameters.xml',sys.argv[1]])

        print theHub.getAllLastValues()



if __name__ == '__main__':

    HomeBakedPiShell().cmdloop()

