Occupational node
=================

.. toctree::
   :maxdepth: 4


About the occupational node
---------------------------

The occupational sensor node is used to monitor event association to door openings, door lock positions and room motion detection.
It is composed of a esp8266 Sparkfun Thing Dev micro controller, a door magnetic switch, a door lock contact switch and
passive infrared sensor.

The code to control the microcontroller is programmed in Arduino C.

The occupational node is designed to send a message over http to the homeBakedPi web app api in the event that a door is
opened, that the door lock is unlocked or that motion is detected in the room. The logic of the event treatment is left
to the hub.

The occupational node acts as an http web server in order to receive sensor data request from the hub. The results of
a data request are relayed back to the hub over the http. A typical http request consist of the ip address of the node
followed by the name of the sensor and the required measurement (ex 192.168.0.1/MD-1/motion). The following is a list of the
permitted http requests :

1) Motion detection measurement request

    xxx.xxx.xxx.xxx/TMP-1/temp

2) Door opening measurement request

    xxx.xxx.xxx.xxx/SW-1/door

3) Door lock measurement request

    xxx.xxx.xxx.xxx/DL-1/lock


Component list
--------------

- Sparkfun ESP8266 Thing Dev - Figure 1
- magnetic door switch
- PIR motion sensor
- 10k resistors * 2
- terminals
- pref board
- standoffs
- pvc board


Schematic
---------

Figure 3 shows the schematic for the occupational node.


Construction
------------

The occupational node component were mounted on a perf board as shown in figure 4. The perfboard was then mounted to
pvc board with standoffs.


.. figure:: ./images/thingDev.jpeg
    :width: 100px
    :align: left
    :height: 100px
    :alt: Sparkfun Thing Dev

    Figure 1 - Sparkfun Thing dev ESP8266

.. figure:: ./images/dht22.jpeg
    :width: 100px
    :align: left
    :height: 100px
    :alt: DHT22 temperature and humidity sensor

    Figure 2 - DHT22 temperature and humidity sensor

.. figure:: ./images/envNodeSchematic.png
    :width: 600px
    :align: left
    :height: 500px
    :alt: envNode schematic

    Figure 3 - Schematic for the environmental node




