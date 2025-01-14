import sys

import imutils

from .camera import Camera
from .gui import Gui
from . import utils


def main():
    from .config import get_config

    config = get_config()

    gui = Gui()

    camera = Camera(config)
    if not camera.init():
        sys.exit(1)

    def capture():
        frame = camera.get()

        if config.fish:
            frame = utils.unfisheye(frame)

        ratio = frame.shape[0] / config.height
        frame_debug = imutils.resize(frame, height=config.height)
        # utils.show(frame_debug)
        box = utils.detect_paper_canny(frame_debug, debug=config.debug)

        if box is not None:
            warped = utils.warp(frame, box, ratio)
            # utils.show(warped, title="warped")
        gui.show(frame_debug)
        return True

    gui.run(capture)


def run():
    main()
