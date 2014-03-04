Raspberry Pi Light Tracker
=======================

Possibly the most over engineered solar tracker ever. Python script to read analog photoresistors mounted on a panel and move a stepper motor accordingly. Several commands are implemented and can be entered via a web interface on port 8080.

Dependencies
------------

- [WebIOPi](https://code.google.com/p/webiopi/) - Used to interface via SPI with the MCP3008 adc chip and read the analog photoresistor values.

- [Bottle](http://bottlepy.org/docs/dev/index.html) - Used to host the web interface

- [RPi.GPIO](http://sourceforge.net/p/raspberry-gpio-python/wiki/Home/) - Used to control the GPIO ports for the stepper motor

Hardware Setup
------------

[View details on Upverter](https://upverter.com/kmb32123/fb9a9af913898658/Raspberry-Pi-Light-Tracker/)

###Parts

Amount | Id | Descripition
-------|----|-------------
1 | | Adafruit Pi T-Cobbler Breakout Kit for Raspberry Pi
1 | MCP3008 | 8-Channel 10-Bit ADC With SPI Interface
1 | ULN2803A | 8 Channel high-voltage, high-current Darlington transistor array
1 | | Small Reduction Stepper Motor - 5VDC 512 Step
5 | GL5516 | Light Dependent Photoresistor
5 |  | 3.9 kOhm Resistor
