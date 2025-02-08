from gpiozero import LightSensor, Buzzer
import time
import tweepy
from tweepy import Cursor
import random
import datetime
import os
from dotenv import load_dotenv

# Load Twitter API credentials
load_dotenv('../.env')

# Initialize hardware components
ldr = LightSensor(4)  # Light sensor on GPIO 4
buzzer = Buzzer(17)   # Buzzer on GPIO 17

# Setup Twitter authentication
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
print(api.me().name)

# Main detection loop
while True:
    time.sleep(5)  # Delay between main loop iterations
    
    # Check if laser beam is broken (light level drops)
    if ldr.value < 0.7:
        # Generate random alert message
        A = random.randint(1, 6)
        message = ''
        if A == 1:
            message = 'Intruder Alert!'
        elif A == 2:
            message = 'There could be someone at your house'
        elif A == 3:
            message = 'The beam is broken!!'
        elif A == 4:
            message = 'Suspected Buglary'
        elif A == 5:
            message = 'Your security has been compromised!'
        elif A == 6:
            message = 'Alert! Alert!'
            
        # Add timestamp and post to Twitter
        B = datetime.datetime.now().time()
        C = message + B.strftime('%H/%M/%S')
        api.update_status(C)
        
        # Activate alarm
        buzzer.on()
    else:
        # Reset alarm when beam is restored
        buzzer.off()
             
       
