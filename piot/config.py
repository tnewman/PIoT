""" Application Configuration

    Configuration is read from config.cfg.
"""

from configparser import ConfigParser
config = ConfigParser()
config.read('config.cfg')

def get_with_default(section, name, default):
    """ Gets a config value or a default if it does not exist.
    :param section: Section
    :type section: str
    :param name: Name
    :type name: str
    :param default: Default if it does not exist in the config.
    :type default: str
    :return: Value from config or default.
    :rtype: str
    """

    if config.has_option(section, name):
        return config.get(section, name)
    else:
        return default

twilio_account = get_with_default('Twilio', 'account', '')
""" Twilio Account """

twilio_token = get_with_default('Twilio', 'token', '')
""" Twilio Token """

twilio_sender_number = get_with_default('Twilio', 'sender_number', '')
""" Number Twilio SMS Notifications will be sent from. """

twilio_recipient_number = get_with_default('Twilio', 'recipient_number', '')
""" Number Twilio SMS Notifications will be sent to. """

sql_alchemy_connection_string = 'sqlite:///piot.db'
""" SQLite Database File Location. """