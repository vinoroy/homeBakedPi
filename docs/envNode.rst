Environmental node
==================

.. toctree::
   :maxdepth: 4


About the environmental node
----------------------------

The environmental sensor node is used to sense the temperature, humidity and luminosity. It is composed of a esp8266
Sparkfun Thing Dev micro controller, DHT22 temperature and humidity sensor and light dependant resistor (LDR) to measure
the luminosity..

The code to control the microcontroller is programmed in Arduino C.

The environmental node acts as an http web server in order to receive sensor data request from the hub. The results of
a data request are relayed back to the hub over the http. A typical http request consist of the ip address of the node
followed by the name of the sensor and the required measurement (ex 192.168.0.1/TMP-1/temp). The following is a list of the
permitted http requests :

1) Temperature measurement request

    xxx.xxx.xxx.xxx/TMP-1/temp

2) Humidity measurement request

    xxx.xxx.xxx.xxx/HUMID-1/humid

3) Luminosity measurement request

    xxx.xxx.xxx.xxx/LDR-1/ldr


Component list
--------------

- Sparkfun ESP8266 Thing Dev - Figure 1
- DHT22 sensor temperature and humidity sensor - Figure 2
- LDR sensor (luminosity)
- 7.5k and 3k resistors for voltage divider
- pref board
- standoffs
- pvc board


Schematic
---------

Figure 3 shows the schematic for the environmental node.


Construction
------------

The environmental node component were mounted on a perf board as shown in figure 4. The perfboard was then mounted to
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

.. figure:: ./images/envNodePhoto.jpg
    :width: 600px
    :align: left
    :height: 500px
    :alt: envNode photo

    Figure 4 - Environmental node mounted on a bread board



