import Jetson.GPIO as GPIO
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BOARD)
pulse_pin = 33
GPIO.setup(pulse_pin, GPIO.OUT)
camera = cv2.VideoCapture('/dev/video0') 
#camera.set(cv2.CAP_PROP_FPS, 50)
sample_count = 50
count = 0
x = []
while count < sample_count:
    ret, frame = camera.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    signal = np.sum(np.sum(mask))
    x = np.append(x,signal)
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Mask', mask)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
GPIO.cleanup()
plt.plot(x)
plt.show()

