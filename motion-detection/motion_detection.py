import RPi.GPIO as GPIO
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import tweepy
import datetime
import os
import threading
from dotenv import load_dotenv

# Load Twitter API credentials
load_dotenv('../.env')

# Setup Twitter authentication
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Configure GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)   # Motion sensor input
GPIO.setup(17, GPIO.OUT)  # LED/Buzzer output

# HTML template for web streaming interface
PAGE="""\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="720" height="480"></center>
</body>
</html>
"""

class StreamingOutput(object):
    """Handles camera output for streaming"""
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        """Write new frame to buffer"""
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    """HTTP handler for streaming server"""
    def do_GET(self):
        if self.path == '/':
            # Redirect root to index
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            # Serve HTML page
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            # Stream camera feed
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    """Threaded HTTP server for handling multiple clients"""
    allow_reuse_address = True
    daemon_threads = True

# Initialize camera
camera = picamera.PiCamera(resolution='720x480', framerate=30)

# Prepare Twitter message
message = 'Motion has been detected! Streaming service is now active'
A = datetime.datetime.now().time()
B = message + A.strftime('%H/%M/%S')

# Command to record video stream
terminal_command = 'avconv -f mjpeg -re -t 10 -i http://172.20.10.4:8000/stream.mjpg -an -r 30 -vcodec mpeg4  /home/pi/Desktop/Video'+A.strftime('%H%M%S')+'.mp4'

# Main detection loop
while True:
    if GPIO.input(24):  # Motion detected
        print('Motion has been detected! Streaming service active')
        GPIO.output(17, True)  # Activate alarm
        api.update_status(B)   # Post to Twitter
        
        # Start camera streaming
        output = StreamingOutput()
        camera.start_recording(output, format='mjpeg')
        try:
            # Start web server
            address = ('172.20.10.4', 8000)
            server = StreamingServer(address, StreamingHandler)
            thread_server = threading.Thread(target=server.serve_forever)
            thread_server.start()
            
            # Record video
            os.system(terminal_command)
        finally:
            print('Recording saved')
