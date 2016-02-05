Custom Sensors
==============

.. note::
   Configuring custom sensors is an advanced topic and should only be done if
   you know Python programming and can setup the sensor hardware.

Custom sensors can be added by creating Python modules in the piot/sensor
folder of the PIoT distribution. A subclass of either BaseAnalogSensor or
BaseDigitalSensor will have to be created for each sensor. The subclass will
have to override all properties and methods from the parent class based on the
sensor's requirements. The sump pump sensor can serve as a good example.

If the sump pump monitor functionality is no longer needed, it can be removed
from the sensor folder but should be backed up in case it is needed later.