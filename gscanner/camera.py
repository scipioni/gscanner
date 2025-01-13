import cv2 as cv
import logging
import numpy as np

log = logging.getLogger(__name__)


class Camera:
    def __init__(self, config):
        self.grey = False
        self.config = config
        self.cap = None
        self.frame = np.zeros((100, 100, 3), np.uint8)

    def init(self, grey=False):
        if self.config.image:
            self.frame = cv.imread(self.config.image)
            log.info("read %s image", self.config.image)
            return True   
        elif self.config.gstreamer:
            log.info("open gstreamer camera %s at %dx%d", self.config.camera, self.config.w, self.config.h)
            c = self.config
            self.cap = cv.VideoCapture(f"v4l2src device={c.camera} do-timestamp=true ! image/jpeg, width={c.w}, height={c.h}, framerate=5/1 ! jpegparse ! jpegdec ! videoconvert ! appsink")
            return True
        else:
            self.grey = grey
            self.cap = cv.VideoCapture(self.config.camera)
            if not self.cap.isOpened():
                print("Could not open video device")
                return False
            self.cap.set(cv.CAP_PROP_FPS, 5)
            self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.config.w)
            self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.config.h)
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


# gst-launch-1.0 v4l2src device=/dev/video4 do-timestamp=true ! image/jpeg, width=8000, height=6000, framerate=5/1 ! jpegparse ! jpegdec ! videoconvert ! videoscale ! xvimagesink
