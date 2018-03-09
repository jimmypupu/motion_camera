import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from collections import deque
from time import sleep
from imutils.video import VideoStream
import imutils
import cv2
from utils import WebcamVideoStream, FPS
from servo_control2 import Servo


lowerBound=np.array([10, 200, 100])
upperBound=np.array([22, 255, 255])

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

servo = Servo()
vs = WebcamVideoStream('400x300').start()
count = 0

bbox = [0, 0, 0, 0]

while True:
    img = vs.read()
    #frame = imutils.resize(frame, width=400)
    frame= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    timer = cv2.getTickCount()

    mask = cv2.inRange(frame, lowerBound, upperBound)
    mask = cv2.erode(mask, None, iterations=5)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        cv2.drawContours(frame, cnts, -1, (255,0,0), 3)
        bbox = cv2.boundingRect(cnts[0])
    #else :
    #    # Tracking failure
    #    servo.servo_reset()
    #    cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
 
    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    if count % 5 == 0:
        prev = ((bbox[0] + bbox[2] / 2), (bbox[1] + bbox[3] / 2))
        servo.servo_control_up_down(20 * (prev[1]-150) / 150)
        servo.servo_control_left_right(-30 * (prev[0]-200) / 200)

    count += 1
    cv2.imshow("Tracking", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
