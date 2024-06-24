import cv2
import time
import Jetson.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BOARD)
pulse_pin = 32
GPIO.setup(pulse_pin, GPIO.IN)

capture_command_pin = 31
GPIO.setup(capture_command_pin, GPIO.OUT)
# GStreamer pipeline with MJPG format at 640x360 resolution
gstreamer_pipeline = (
    'v4l2src device=/dev/video0 ! '
    'image/jpeg, width=1920, height=1080, framerate=60/1 ! '
    'jpegdec ! videoconvert ! appsink'
)
camera = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)
#camera = cv2.VideoCapture('/dev/video0') 
if not camera.isOpened():
    print("Error: Unable to open video source")
    exit()    
count = 0
threshold = 5000
pulse_duration = 0.1

try:
    while True:
        while not GPIO.input(pulse_pin):
            pass
        
        ret, frame = camera.read()
        if not ret:
            print("Error: Unable to read frame")
            break

        # Check if captured image is red
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        signal = np.sum(np.sum(mask))
        current_time = time.monotonic()
        if signal > threshold:
            # Send confirmation signal to Adafruit
            GPIO.output(capture_command_pin, GPIO.HIGH)
            time.sleep(pulse_duration)  # Ensure Adafruit has enough time to detect the signal
            GPIO.output(capture_command_pin, GPIO.LOW)
            count += 1
            print(count)
        cv2.imshow('Original Frame', frame)
        cv2.imshow('Mask', mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Program interrupted by user")
finally:
    camera.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
