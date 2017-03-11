TO DO
=====


App
---

>1 developpe the event queue task treatment module
        - add live event based tests via web api
        - add alarm on / off state to the hub
        - relagate to a DB the actions associated to an event
        + add temperature threshold event
        + integrate event framework to homeBakedPi
                + modify verify thresholds for envSensor --> adding the createEvent methods in sensors
                + modify verify thresholds for occpSensor
                + add on and off test to verify threshold verification
        + review documention of the event modules
        + problem with paramreader look at unit tests
        + add sms and email actions ---> must add smsGateway and cellNumber to xml params and to hub creation process
        + add tests for actions
        + add tests for event
        + clear log entries in eventQ tests
        + add log entry for event creation
        + add event logging >> building the tests for the log
        + copy the event files to the app folder
        + adding the tests to eventQ
        + change the event type names to captial letters

-2 the scheduling function of the actuators should be put in a separate class to be used by all
-3 change instID for sensorID (this is a deep one it even touches the db)
-4 generalize comm util email agent so that it can connect to any smtp servers


Shell
-----

- command to clear the readings tables (also the log entries)


WebApp
------

- correct the bash script to update homeBakedPi (problem with the copy of the static files)
>1 write a script to insert dummy values into db for dev and testing purposes. Use the testInsert script as an example

-2 add page to view the actuator on off times in table format
-3 the web app displays time in UTC zone, must find a way to convert to EST time unicode(datetime object here)


OccpNode
--------

-1 clean up the door node code
>1 build the perfboard occp node

>2 doc the occp node


EnvNode
-------

-1 clean up the env node code (change the int values for floats)
>1 build the perfboard env node

>2 doc the env node


Notes
-----

* Version 0.3.2 represents a more drastic change in the code with the introduction
  of the hub of nodes, hence to go back to single node code base we must back up
  to version 0.3.1 or 0.2.2

* Version 0.4 represents an architecure change. The homebakedpi web app will not longer be hosted on a remote host.
  The web app in 0.4will be hosted on the hub and will also act as a web app server.

* Version 0.7 present another architecture change. The following is a list of the changes to the architecture and the infrastructure :
        1)  No hardware and software dependencies to the hub (ie serial communication between nodes and the hub, hard software links to actuators).
                Communication between hub and the nodes will be done over wifi using a web api.
                Selected actuators will need to be also activated over wifi via a web api (ie Insteon)

        2)  Prod DB will be copied from the dev DB with no data and a script will be created to reload the prod data. All time stamped data will
            be lost in the process

        3)  The dev and the prod will be setup on identical servers.

        4)  All development will be done directly to the dev server over ssh


Completed
---------

+1 build fault tolerence for node data request over http (ex unplugged node)
+2 draw the schematic of the occp node
+2 draw the schematic of the env node