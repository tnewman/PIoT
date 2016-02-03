""" PIoT Notifications
"""

from piot import config
from twilio.rest import TwilioRestClient


class BaseNotification:
    def __init__(self):
        """ Base Notification
        """
        pass

    def send_notification(self, message):
        """ Send a Notification
        :param message: Message to send with the notification.
        :type message: str
        """

        pass


class TwilioSMSNotification(BaseNotification):
    def __init__(self, twilio_client=TwilioRestClient):
        """ Send an SMS Notification via Twilio
            :param twilio_client: Twilio Rest Client Class
            :type twilio_client: TwilioRestClient Class
        """
        self.twilio_client = twilio_client(config.twilio_account,
                                           config.twilio_token,
                                           timeout=1)

    def send_notification(self, message):
        """ Send an SMS notification via Twilio.
        :param message: Message to send with the notification.
        :type message: str
        """

        message = self.twilio_client.messages.create(
            body=message,
            to=config.twilio_sender_number,
            from_=config.twilio_recipient_number
        )
