""" Application Configuration

    Configuration is read from config.cfg.
"""

from configparser import ConfigParser
config = ConfigParser()
config.read('config.cfg')

twilio_account = config['Twilio']['account']
""" Twilio Account """

twilio_token = config['Twilio']['token']
""" Twilio Token """

twilio_sender_number = config['Twilio']['sender_number']
""" Number Twilio SMS Notifications will be sent from. """

twilio_recipient_number = config['Twilio']['recipient_number']
""" Number Twilio SMS Notifications will be sent to. """

sql_alchemy_connection_string = 'sqlite:///piot.db'
""" SQLite Database File Location. """