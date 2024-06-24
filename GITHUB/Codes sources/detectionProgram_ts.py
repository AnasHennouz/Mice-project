import Jetson.GPIO as GPIO
import cv2
import numpy as np
import time

# GPIO setup
GPIO.setmode(GPIO.BOARD)
pulse_pin = 32
GPIO.setup(pulse_pin, GPIO.OUT)
GPIO.output(pulse_pin, GPIO.LOW)

# GStreamer pipeline with MJPG format at 640x360 resolution
gstreamer_pipeline = (
    'v4l2src device=/dev/video0 ! '
    'image/jpeg, width=640, height=360, framerate=200/1 ! '
    'jpegdec ! videoconvert ! appsink'
)
camera = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)
# Camera setup
#camera = cv2.VideoCapture('/dev/video0')
if not camera.isOpened():
    print("Error: Could not open camera.")
    exit()

count = 0
threshold = 700000
debounce_time = 1 
pulse_duration = 0.1
last_pulse_time = time.monotonic()

try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define HSV range for red color
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])

        # Create mask for red color
        mask = cv2.inRange(hsv_frame, lower_red, upper_red)
        
        # Calculate the sum of mask values
        signal = np.sum(np.sum(mask))
        current_time = time.monotonic()

        # Check if the signal exceeds the threshold
        if signal > threshold and (current_time - last_pulse_time) > debounce_time:
            # Pulse the pin
            GPIO.output(pulse_pin, GPIO.HIGH)
            time.sleep(pulse_duration)
            GPIO.output(pulse_pin, GPIO.LOW)

            # Increment count and print it
            count += 1
            print(count)
            last_pulse_time = current_time

        # Display the frames
        #cv2.imshow('Original Frame', frame)
        #cv2.imshow('Mask', mask)

        # Exit on 'q' key press
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    # Clean up
    camera.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()

