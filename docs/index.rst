.. Pi of Things (PIoT) documentation master file, created by
   sphinx-quickstart on Mon Jan 11 21:52:32 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pi of Things (PIoT)'s documentation!
===============================================

What is the Pi of Things (PIoT)?
--------------------------------

The Pi of Things (PIoT) is a learning platform to explore the Internet 
of Things (IoT). The IoT consists of embedded devices that communicate 
with services on the internet, such as smart thermostats. PIoT is an 
open source platform that allows you to interact with sensors, view the 
readings of those sensors over time on a dynamic website that is hosted 
on the Raspberry Pi and receive text message notifications when a sensor 
detects that something has gone wrong. PIoT has a sensor plugin system, 
so you can add plugins for your own sensors in addition to those that 
are provided out of the box.

.. figure:: images/distancesensor.jpg
   :alt: PIoT Distance Sensor
   
   Raspberry Pi with a distance sensor used to develop the PIoT 
   Software.

Bill of Materials
-----------------

Using the Bill of Materials below, you can build your own sump pump 
monitor using the PIoT platform. When aimed at the water in a sump, 
a distance sensor checks to make sure the water level is not too 
high. If the water level is too high, a text message will be sent, 
so you know that something is wrong with your sump pump, saving 
you from a flooded basement.

You will need to acquire the following parts:

+-----------------------------------+----------+
| Part                              | Quantity |
+===================================+==========+
| Raspberry Pi 2 - Model B          | 1        |
+-----------------------------------+----------+
| Wireless N Nano USB Adapter       | 1        |
+---------------------------------------+----------+
| 5VDC 2A Micro USB Adapter             | 1        |
+---------------------------------------+----------+
| Breadboard                            | 1        |
+---------------------------------------+----------+
| Male to Female Jumper Wire            | 9        |
+---------------------------------------+----------+
| 1k Ohm Resistor                       | 3        |
+---------------------------------------+----------+
| SainSmart HC-SR04 Distance Sensor     | 1        |
+---------------------------------------+----------+
| SD Card (16 GB+ Class 10 recommended) | 1        |
+---------------------------------------+----------+

Once you have the above parts, you can follow the installation 
instructions to install the PIoT open source software on your 
Raspberry Pi and configure it to work as a sump pump monitor.

Setup
-----

You will need to install `Rasbian Lite`_ Linux distribution 
onto your Raspberry Pi using the `official instructions`_. 
`Raspbian Lite`_ is recommended because it is lightweight, 
and PIoT was designed to work on it. Other distributions 
are not tested and are not recommended.

.. _official instructions: https://www.raspberrypi.org/documentation/installation/installing-images/
.. _Raspbian Lite: https://www.raspberrypi.org/downloads/raspbian/

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

