# Raspberry Pi Security System - Simply Secure

This project was developed during the years 2018 and 2019. The code may not be the most elegant, however, this project served as my introduction to programming and microcontrolers - providing me with foundational experience and ultimately leading me to pursue Computer Engineering.

A security system built with Raspberry Pi Model 3B that includes facial recognition, gas detection, laser tripwire, and motion detection with video streaming capabilities. The system sends alerts via Twitter when security events are detected.

## System Components

### 1. Facial Recognition System
- **Description**: Continuously monitors for faces using a camera and OpenCV
- **Features**:
  - Real-time face detection
  - Automatic image capture when faces detected
  - Twitter notifications with captured images
- **Components Required**:
  - Raspberry Pi Camera Module
  - Buzzer (GPIO 17)

### 2. Gas Detection System
- **Description**: Monitors for dangerous gas levels using an MCP3002 ADC and gas sensor
- **Features**:
  - Continuous gas level monitoring
  - Configurable threshold detection
  - Random alert messages on Twitter
  - Audio alarm when gas detected
- **Components Required**:
  - MCP3002 ADC
  - Gas sensor (MQ-2 or similar)
  - Buzzer (GPIO 17)
  - SPI interface connections

### 3. Laser Security System
- **Description**: Creates a laser tripwire using a laser and light sensor
- **Features**:
  - Beam-break detection
  - Instant alerts via Twitter
  - Audio alarm on intrusion
- **Components Required**:
  - Laser module
  - Light Dependent Resistor (LDR) (GPIO 4)
  - Buzzer (GPIO 17)

### 4. Motion Detection System
- **Description**: Video surveillance system with motion detection
- **Features**:
  - Motion-activated recording
  - Live video streaming via web interface
  - Automatic video capture
  - Twitter notifications
- **Components Required**:
  - Raspberry Pi Camera Module
  - PIR Motion Sensor (GPIO 24)
  - LED/Buzzer (GPIO 17)

## Hardware Setup

### Required Components
- Raspberry Pi (3 or newer recommended)
- Raspberry Pi Camera Module
- PIR Motion Sensor
- MQ-2 Gas Sensor
- MCP3002 ADC
- Laser Module
- Light Dependent Resistor (LDR)
- Buzzer
- Jumper Wires
- Breadboard

### Pin Connections

#### Gas Detection System (MCP3002 ADC)
- VDD → 3.3V
- VREF → 3.3V
- CLK → SCLK (GPIO 11)
- DOUT → MISO (GPIO 9)
- DIN → MOSI (GPIO 10)
- CS → CE0 (GPIO 8)
- VSS → GND

#### Laser Security System
- LDR → GPIO 4
- Buzzer → GPIO 17

#### Motion Detection System
- PIR Sensor → GPIO 24
- LED/Buzzer → GPIO 17

## Software Setup

### 1. Basic Raspberry Pi Setup
#### Prerequisites
- Raspberry Pi with Raspberry Pi OS installed
- Internet connection
- Basic knowledge of terminal commands
- Twitter Developer Account
- OpenCV face detection cascade file (`facial_recognition_model.xml`) in the facial_recognition directory

```bash
# Download and install Raspberry Pi OS
# From https://www.raspberrypi.com/software/

# Initial setup after OS installation
sudo raspi-config
# 1. Change default password
# 2. Set up WiFi
# 3. Enable SSH if needed
# 4. Set locale and timezone

# Enable required interfaces
sudo raspi-config
# Navigate to "Interface Options" and enable:
# 1. Camera
# 2. SPI
# 3. I2C

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install git (if not already installed)
sudo apt-get install git -y

# Clone this repository
git clone https://github.com/HarshadChunder/Smart-Security-System
cd Smart-Security-System
```

### 2. Install Required Packages
```bash
# Install system dependencies
sudo apt-get install -y python3-pip python3-opencv
sudo apt-get install -y libatlas-base-dev
sudo apt-get install -y avconv

# Install Python packages
pip3 install -r requirements.txt
```

### 3. Twitter API Setup
1. Create a Twitter Developer account
2. Create a new Twitter Application
3. Generate API keys and tokens
4. Create a `.env` file in the root directory
5. Add keys to `.env` file

### 4. Running the System
```bash
# Start facial recognition
python3 facial_recognition/facial_recognition.py

# Start gas detection
python3 gas_detection/gas_alarm_system.py

# Start laser security
python3 laser_detection/laser_security_system.py

# Start motion detection
python3 motion_detection/motion_detection.py
```

## Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### Adjusting Sensitivity
- Gas Detection: Modify the voltage threshold (default 1200) in `gas_detection/gas_alarm_system.py`
- Laser Security: Adjust the light threshold (default 0.7) in `laser_detection/laser_security_system.py`
- Motion Detection: Adjust PIR sensor sensitivity using its physical potentiometer

### Video Stream Settings
- Default resolution: 720x480
- Default framerate: 30fps
- Stream address: http://172.20.10.4:8000/
- Video save location: /home/pi/Desktop/Video[TIMESTAMP].mp4

### Advanced Configuration
Each subsystem can be fine-tuned by modifying parameters in their respective scripts.

### Common Issues

#### System Performance
- If the system is running slowly, try:
  - Reducing camera resolution
  - Increasing sampling intervals
  - Closing unnecessary applications

#### Hardware Issues
1. Camera not working
   - Check camera connection
   - Ensure camera is enabled in raspi-config
   
2. SPI not working
   - Verify SPI is enabled in raspi-config
   - Check wiring connections

3. Twitter notifications not sending
   - Verify internet connection
   - Check Twitter API credentials
   - Ensure .env file is properly configured

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License - see the [LICENSE](LICENSE.md) file for details.