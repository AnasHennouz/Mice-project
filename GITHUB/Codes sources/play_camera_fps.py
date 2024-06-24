import numpy as np 
import cv2 
import time 

# creating the videocapture object 
# and reading from the input file 
# Change it to 0 if reading from webcam 
camera_id = "/dev/video0"
# cap = cv2.VideoCapture('vid.mp4') 
cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 10)

# used to record the time when we processed last frame 
prev_frame_time = 0

# used to record the time at which we processed current frame 
new_frame_time = 0

# List to store time differences
time_diffs = []

# Reading the video file until finished 
while(cap.isOpened() and len(time_diffs) < 2000): 

    # Capture frame-by-frame 
    ret, frame = cap.read() 

    # if video finished or no Video Input 
    if not ret: 
        break

    # Our operations on the frame come here 
    gray = frame 

    # time when we finish processing for this frame 
    new_frame_time = time.time() 

    # Calculating the time difference 
    time_diff = new_frame_time - prev_frame_time
    if prev_frame_time != 0:
        time_diffs.append(round(time_diff*1000,2))
    
    prev_frame_time = new_frame_time

    # Calculating the fps 
    fps = 1 / time_diff if time_diff != 0 else 0

    # converting the fps into integer 
    fps = int(fps) 
    print(fps)

    # converting the fps to string so that we can display it on frame 
    fps = str(fps) 

    # font which we will be using to display FPS 
    font = cv2.FONT_HERSHEY_SIMPLEX 

    # putting the FPS count on the frame 
    cv2.putText(gray, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA) 

    # displaying the frame with fps 
    cv2.imshow('frame', gray) 

    # press 'Q' if you want to exit 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# When everything done, release the capture 
cap.release() 
cv2.destroyAllWindows() 

# Save the time differences to a file
with open('time_diffs.txt', 'w') as f:
    for diff in time_diffs:
        f.write(f"{diff:.2f}\n")

