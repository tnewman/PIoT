#!/usr/bin/env python3
import os
import sys
os.chdir('..')
sys.path.append('.')
from piot.notification import TwilioSMSNotification
from twilio import TwilioRestException 

print('==================')
print('Twilio Test Script')
print('==================')

while True:
    twilio_notification=TwilioSMSNotification()
    
    try:
        twilio_notification.send_notification('Test Notification from PIoT')
    except TwilioRestException:
        print('Twilio Exception - Check Connectivity and Settings')
        print('Test Failed')
        exit(1)
    
    print('SMS Send')
    
    print('Did you receieve an SMS [Yes/No]')
    result=input()
    
    if result.lower()=='yes':
        print('Test Passed')
        exit(0)
    elif result.lower()=='no':
        print('Test Failed')
        exit(1)
