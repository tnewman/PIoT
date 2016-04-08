Raspberry Pi Setup
==================

Operating System
----------------

Using the SD card purchased as part of the Bill of Materials, you will need
to install `Raspbian Lite`_ Linux distribution onto your Raspberry Pi using
the `official instructions`_. `Raspbian Lite`_ is recommended because it is
lightweight, and PIoT was designed to work on it. Other distributions are not
tested and are not recommended.

.. _official instructions: https://www.raspberrypi.org/documentation/installation/installing-images/
.. _Raspbian Lite: https://www.raspberrypi.org/downloads/raspbian/

Configure Network
-----------------

Insert the WiFi dongle purchased as part of the Bill of Materials, and power
on the Raspberry Pi. You will need your WiFi network's SSID and WPA key.
Generate the configuration for the WPA supplicant with wpa_passphrase SSID
passphrase. Make sure to replace SSID with your WiFi network's SSID and
passphrase with your WiFi network's password.

.. code-block:: bash

    pi@raspberrypi:~ $ wpa_passphrase "SSID" "password"
    network={
        ssid="SSID"
        #psk="password"
        psk=2f6a0beddf2f0588ee426b0c3a0e3d9a523bb07a05cb857f85d826da80fa75c4
    }

.. TIP::
    Make sure your network information is correct, or the Raspberry Pi's
    network will fail to connect when it is rebooted.

Copy the entire output (network section) from the wpa_passphrase command and
append it to the end of /etc/wpa_supplicant/wpa_supplicant.conf.

.. code-block:: bash

    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
            ssid="SSID"
            #psk="password"
            psk=2f6a0beddf2f0588ee426b0c3a0e3d9a523bb07a05cb857f85d826da80fa75c4
    }

Reboot the Raspberry Pi with sudo reboot. The Raspberry Pi should be
connected to your WiFi network when it reboots.

.. TIP::
    The Raspberry Pi's network connections will not initialize if either the
    WiFi or ethernet connection cannot successfully connect. If you want to
    use one network connection, do not use the other. For example, if you want
    to use the WiFi, do not connect the Ethernet connection.

Expand the SD Card
------------------

When the Raspbian image is copied to the SD card, the operating system partition 
will not take up the entire SD card. The SD card should be expanded.

Enter the Raspberry Pi configuration tool.

.. code-block:: bash

    sudo raspi-config --expand-rootfs

Reboot the Raspberry Pi with sudo reboot. The Raspberry Pi's partition should 
now use the entire SD card.