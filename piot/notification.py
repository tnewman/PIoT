from piot import config
from twilio.rest import TwilioRestClient


class BaseNotification:
    def send_notification(self, message):
        pass


class TwilioSMSNotification(BaseNotification):
    def __init__(self, twilio_client=TwilioRestClient):
        self.twilio_client = twilio_client(config.twilio_account,
                                           config.twilio_token,
                                           timeout=1)

    def send_notification(self, message):
        message = self.twilio_client.messages.create(
            body=message,
            to=config.twilio_sender_number,
            from_=config.twilio_recipient_number
        )
