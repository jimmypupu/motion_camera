from picamera import PiCamera
import sys
sys.path.insert(0, '../')
#sys.path.insert(0, '/tmp/tensorflow_pkg/')
from picamera.array import PiRGBArray
from collections import deque
from time import sleep
#from imutils.video import VideoStream
#import imutils
import cv2
from utils import WebcamVideoStream, FPS
from servo_control2 import Servo
import YOLO_tiny_tf

#@profile
def main():
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    servo = Servo()

    camera = PiCamera(resolution='400x300')
    sleep(5)
    frame = PiRGBArray(camera)
    camera.capture(frame, format="bgr")
    frame = frame.array
    camera.close()

    yolo = YOLO_tiny_tf.YOLO_TF()

    vs = WebcamVideoStream('448x448').start()

    """prev = ((bbox[0] + bbox[2] / 2), (bbox[1] + bbox[3] / 2))
    servo.servo_control_up_down(20 * (prev[1]-150) / 150)
    servo.servo_control_left_right(-30 * (prev[0]-200) / 200)
    """
    count = 0
    frame_without = 0

    while True:
        frame = vs.read()
        yolo.detect_from_cvmat(frame)
        #frame = imutils.resize(frame, width=400)
        result_box = yolo.result
        #timer = cv2.getTickCount()

        print(count)
        center = [0,0]
        person = 0
        for result in result_box:
            bbox = (result[1], result[2], result[3], result[4])
            print(result[0], bbox)

            #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

            # Display FPS on frame
            #cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

            if result[0] == 'person':
                person += 1
                center[0] += bbox[0]
                center[1] += bbox[1]

        if person == 0:
            frame_without += 1
            if frame_without == 5:
                servo.servo_reset()
                frame_without = 0
        #else:
        if person > 0:
            frame_without = 0
            prev = (center[0]/person, center[1]/person)
            print(prev)
            servo.servo_control_up_down(20 * (prev[1]-224) / 448)
            servo.servo_control_left_right(-30 * (prev[0]-224) / 448)
        count += 1
        # Display result
        #cv2.imshow("Tracking", frame)
        #key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        #if key == ord("q"):
        #    break

if __name__ == "__main__":
    main()
