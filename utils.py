from picamera import PiCamera
from picamera.array import PiRGBArray
from threading import Thread
import datetime
import cv2
 
class WebcamVideoStream(object):
    def __init__(self, resolution='800x600'):
        self.camera = PiCamera(resolution=resolution)

        frame = PiRGBArray(self.camera)
        self.camera.capture(frame, format="bgr")
        self.frame = frame.array
 
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self
 
    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return
 
            # otherwise, read the next frame from the stream
            frame = PiRGBArray(self.camera)
            self.camera.capture(frame, format="bgr")
            self.frame = frame.array
 
    def read(self):
        # return the frame most recently read
        return self.frame
 
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


class FPS(object):
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0
 
    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self
 
    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()
 
    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1
 
    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()
 
    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()
