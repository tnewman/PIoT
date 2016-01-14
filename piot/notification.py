from piot import config
from twilio.rest import TwilioRestClient


class BaseNotification:
    def send_notification(message):
        pass


class TwilioSMSNotification(BaseNotification):
    def send_notification(self, message):
        client=TwilioRestClient(config.twilio_account, 
                                config.twilio_token)
        
        message=client.messages.create(
            body=message,
            to=config.twilio_sender_number,
            from_=config.twilio_recipient_number
        )
