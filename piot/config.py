from configparser import ConfigParser
config = ConfigParser()
config.read('config.cfg')

twilio_account = '234323432'#config['Twilio']['account']
twilio_token = '234323432'#config['Twilio']['token']
twilio_sender_number = '234323432'#config['Twilio']['sender_number']
twilio_recipient_number = '234323432'#config['Twilio']['recipient_number']

sql_alchemy_connection_string = 'sqlite:///piot.db'