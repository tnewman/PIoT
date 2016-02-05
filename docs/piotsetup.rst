PIoT Setup
==========

Automatic Installation
----------------------

To get started with PIoT, you can install it on the Raspberry Pi with one
command. The command will download and run the automatic installation script.

.. code-block:: bash

    sudo bash -c "bash <(curl -s https://raw.githubusercontent.com/tnewman/PIoT/master/autoinstall.sh)"

Manual Installation
-------------------

.. NOTE::
    The manual steps could be a good learning experience; however, if you
    prefer automation, why not try the script :-)?

Update Raspbian, install PIP (Package Installer for Python) for Python 3 and
install Git.

.. code-block:: bash

    sudo apt-get update
    sudo apt-get -y upgrade
    sudo apt-get -y install git python3-pip

Clone the PIoT GitHub repository into /home/pi/PIoT.

.. code-block:: bash

    git clone https://github.com/tnewman/PIoT /home/pi/PIoT

Navigate into the PIoT directory.

.. code-block:: bash

    cd /home/pi/PIoT

Install PIoT in development mode. Development mode will symlink the PIoT files
instead of copying them, so you can hack on them if you would like.

.. code-block:: bash

    sudo python3 setup.py develop

Install the Gunicorn web application server for the PIoT website that is
hosted on the Raspberry Pi.

.. code-block:: bash

    sudo pip3 install gunicorn

Copy the sample configuration to serve as PIoT's configuration.

.. code-block:: bash

    cp config.cfg.sample config.cfg

Create the tables in the PIoT database.

.. code-block:: bash

    ./initializedatabase.py

Install the SystemD service files.

.. code-block:: bash

    sudo cp piotexportgpio.service /etc/systemd/system/piotexportgpio.service
    sudo cp piotreadsensors.service /etc/systemd/system/piotreadsensors.service
    sudo cp piotweb.service /etc/systemd/system/piotweb.service

Reload SystemD, enable the PIoT services and start them.

.. code-block:: bash

    sudo systemctl enable piotexportgpio.service
    sudo systemctl enable piotreadsensors.service
    sudo systemctl enable piotweb.service

    sudo systemctl restart piotexportgpio.service
    sudo systemctl restart piotreadsensors.service
    sudo systemctl restart piotweb.service

PIoT is now installed, and it will read the distance sensor for the Sump Pump
Monitor. You will not receive SMS notifications until you complete the
configuration steps.
