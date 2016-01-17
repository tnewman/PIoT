from configparser import ConfigParser
config = ConfigParser()
config.read('config.cfg')

twilio_account = config['Twilio']['account']
twilio_token = config['Twilio']['token']
twilio_sender_number = config['Twilio']['sender_number']
twilio_recipient_number = config['Twilio']['recipient_number']

sql_alchemy_connection_string = 'sqlite:///piot.db'