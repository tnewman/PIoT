from unittest.mock import MagicMock
from piot import config
from piot.notification import BaseNotification
from piot.notification import TwilioSMSNotification


class TestBaseNotification:
    def test_send_notification(self):
        # This is for coverage - the base class method does nothing
        base = BaseNotification()
        base.send_notification('test message')


class TestTwilioSMSNotification:
    def test_twilio_account_and_token_set(self):
        config.twilio_account = 'account'
        config.twilio_token = 'token'
        twilio = TwilioSMSNotification()

        assert twilio.twilio_client.auth[0] == 'account'
        assert twilio.twilio_client.auth[1] == 'token'

    def test_send_notification(self):
        config.twilio_account = 'account'
        config.twilio_token = 'token'
        config.twilio_sender_number = 'send'
        config.twilio_recipient_number = 'receive'

        twilio = TwilioSMSNotification()

        twilio.twilio_client.messages.create = MagicMock()

        twilio.send_notification('test message')

        twilio.twilio_client.messages.create.assert_called_with(
                body='test message', to='receive', from_='send')
