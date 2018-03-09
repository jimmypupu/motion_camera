from picamera import PiCamera
from picamera.array import PiRGBArray
from collections import deque
from time import sleep
from imutils.video import VideoStream
import imutils
import cv2

#camera = PiCamera()
#print(camera)
#camera.start_preview()
#sleep(10)
#camera.stop_preview()

# define the lower and upper boundaries of the "green"
# ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
#pts = deque(maxlen=args["buffer"])
pts = deque()
counter = 0
(dX, dY) = (0, 0)
direction = ""

#camera = cv2.VideoCapture(0)
camera = PiCamera()

# keep looping
while True:
    # grab the current frame
    #(grabbed, frame) = camera.read()
    frame = PiRGBArray(camera)
    camera.capture(frame, format="bgr")
    frame = frame.array

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    #if args.get("video") and not grabbed: #    break

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img = blurred

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(img, greenLower, greenUpper)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

        # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
					   (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
