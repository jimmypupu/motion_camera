from picamera import PiCamera
#import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from collections import deque
from time import sleep
from imutils.video import VideoStream
import imutils
import cv2
from utils import WebcamVideoStream, FPS
from servo_control2 import Servo

#
#   Thanks to
#   https://www.intorobotics.com/how-to-detect-and-track-object-with-opencv/
#   https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/ 
#

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
tracker_type = tracker_types[2]

if int(minor_ver) < 3:
    tracker = cv2.Tracker_create(tracker_type)
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()

#@profile
def main():
    servo = Servo()

    camera = PiCamera(resolution='400x300')
    #bbox = (287, 23, 86, 320)
    sleep(5)
    frame = PiRGBArray(camera)
    camera.capture(frame, format="bgr")
    frame = frame.array
    camera.close()

    bbox = cv2.selectROI('ROI', frame, False, False)
    print("return", bbox)
    cv2.destroyAllWindows()

    ok = tracker.init(frame, bbox)

    vs = WebcamVideoStream('400x300').start()

    prev = ((bbox[0] + bbox[2] / 2), (bbox[1] + bbox[3] / 2))
    servo.servo_control_up_down(20 * (prev[1]-150) / 150)
    servo.servo_control_left_right(-30 * (prev[0]-200) / 200)

    count = 0

    while True:
        frame = vs.read()
        #frame = imutils.resize(frame, width=400)

        timer = cv2.getTickCount()

        ok, bbox = tracker.update(frame)
        bbox = (bbox[0], bbox[1], bbox[2], bbox[3])
        print(ok, bbox)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            servo.servo_reset()
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        #https://github.com/opencv/opencv_contrib/issues/640
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        if count % 5 == 0:
            prev = ((bbox[0] + bbox[2] / 2), (bbox[1] + bbox[3] / 2))
            servo.servo_control_up_down(20 * (prev[1]-150)*0.5 / 150)
            servo.servo_control_left_right(-30 * (prev[0]-200)*0.5 / 200)

        count += 1
        #if count == 100:
        #    return
        cv2.imshow("Tracking", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

if __name__ == "__main__":
    main()
