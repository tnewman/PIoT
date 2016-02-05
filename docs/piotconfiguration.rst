PIoT Configuration
==================

SMS Notifications
-----------------

.. DANGER::
   Twilio has free and paid services. PIoT works with the free services. You
   do not need to pay for an account or provide payment information.

SMS notifications will not work out of the box because they rely on a third
party service called Twilio for delivery. Before you can configure SMS
notifications, register for a `free Twilio account`_.

.. _free Twilio account: https://www.twilio.com/

Twilio will provide you with an account number, token and phone number. Open
config.cfg, go to the Twilio section, add the Twilio account number for
account_number, add the Twilio token for token, add the phone number provided
by Twilio for sender_number and add the phone number that should receive SMS
notifications as recipient number.

.. code-block:: ini

   [Twilio]
   account=fafewJI443fjaiofjioajfoifjewaf
   token=665fefawfe233afaewfaewfwaffewf
   sender_number=+15555555555
   recipient_number=+15555555555

Restart the sensor reading service, and you will receive SMS notifications
if an abnormal sensor value is detected as long as everything is set up
correctly.

.. code-block:: bash

   sudo systemctl restart piotreadsensors.service