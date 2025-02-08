from time import sleep
import spidev
import tweepy
import random
import datetime
import os
from gpiozero import Buzzer
from dotenv import load_dotenv

# Initialize SPI interface for gas sensor
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 250000

# Load Twitter API credentials
load_dotenv('../.env')

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Initialize Twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
print(api.me().name)

# Initialize buzzer on GPIO pin 17
buzzer = Buzzer(17)

def poll_sensor(channel):
    """Poll MCP3002 ADC
    Args:
        channel (int):  ADC channel 0 or 1
    Returns:
        int: 10 bit value relating voltage 0 to 1023
    """
    assert 0 <= channel <= 1, 'ADC channel must be 0 or 1'

    # Configure the read command
    if channel:
        cbyte = 0b11000000
    else:
        cbyte = 0b10000000

    # sgl/diff = 1; odd/sign = channel; MBSF = 0
    r = spi.xfer2([1,cbyte,0])

    # 10 bit value from returned bytes (bits 13-22):
    # XXXXXXXX, XXXX####, ######XX
    # Convert and return 10 bit value
    return ((r[1] & 31) << 6) + (r[2] >> 2)

try:
    while True:
        # Read gas sensor value
        channel = 0
        channeldata = poll_sensor(channel)
        voltage = round(((channeldata * 3300) / 1024),0)
        
        # Check if gas level exceeds threshold
        if voltage > 1200:
            # Generate random alert message
            A = random.randint(1, 6)
            message = ''
            if A == 1:
                message = 'Gas has been detected!'
            elif A == 2:
                message = 'Combustion'
            elif A == 3:
                message = 'Suspected fire'
            elif A == 4:
                message = 'Combustable gas in the area'
            elif A == 5:
                message = 'Gas has triggered the alarm'
            elif A == 6:
                message = 'Alert! Alert!'
                
            # Add timestamp and post to Twitter
            B = datetime.datetime.now().time()
            C = message + B.strftime('%H/%M/%S')
            api.update_status(C)
            
            # Activate alarm
            buzzer.on()
            print('sent tweet')
            sleep(0.5)

finally:
    # Cleanup on exit
    spi.close()
    
