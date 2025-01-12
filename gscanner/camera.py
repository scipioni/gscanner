import cv2 as cv
import logging
import numpy as np

log = logging.getLogger(__name__)


class Camera:
    def __init__(self, config):
        self.grey = False
        self.config = config
        self.cap = None
        self.frame = np.zeros((100,100,3), np.uint8)


    def init(self, w=640, h=480, grey=False):
        if self.config.image:
            self.frame = cv.imread(self.config.image)
            log.info("read %s image", self.config.image)
            return True
        else:
            self.grey = grey
            self.cap = cv.VideoCapture(0)
            if not self.cap.isOpened():
                print("Could not open video device")
                return False
            self.cap.set(cv.CAP_PROP_FRAME_WIDTH, w)
            self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, h)
            return True


    def get(self):
        if not self.cap:
            return self.frame.copy()
        
        _, frame = self.cap.read()
        if self.grey:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)
        else:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.frame = frame
        return frame
