from gscanner.camera import Camera
from gscanner.gui import Gui
from . import utils
import sys
import cv2 as cv


def main():
    from .config import get_config
    config = get_config()

    camera = Camera(config)
    if not camera.init():
        sys.exit(1 )


    def on_idle():
        frame = camera.get()
        frame_debug = frame.copy()
        box = utils.detect_white_paper(frame_debug)
        if box is not None:
            cv.polylines(frame_debug, [box], True, (0,255,0), 2)
            utils.show_box(frame_debug, box)
        gui.show(frame_debug)
        return True

    gui = Gui(on_idle)
    gui.run()


def run():
    main()
