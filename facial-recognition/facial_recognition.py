import io
import picamera
import cv2
import numpy
import tweepy
import os
import time
from gpiozero import Buzzer
from dotenv import load_dotenv

# Load Twitter API credentials from environment variables
load_dotenv('../.env')

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Initialize Twitter authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Path to save captured images
photo = '/home/pi/Desktop/result.jpg'

# Initialize hardware components
buzzer = Buzzer(17)
camera = picamera.PiCamera() 

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier('facial_recognition_model.xml')

# Main detection loop
while True:
    time.sleep(0.5)  # Brief pause between captures
    
    # Capture image from camera
    stream = io.BytesIO()
    camera.resolution = (1280, 1080)
    camera.capture(stream, format='jpeg')
    
    # Convert image to numpy array for OpenCV processing
    buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)
    image = cv2.imdecode(buff, 1)
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    # Draw rectangles around detected faces
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
    
    print("Found "+str(len(faces))+" face(s)")
    cv2.imwrite('result.jpg',image)
    
    # If faces detected, post to Twitter
    if len(faces) >= 1:
        api.update_with_media(photo)
