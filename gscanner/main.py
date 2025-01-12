from gscanner.camera import Camera
from gscanner.gui import Gui
from . import utils
import sys
import imutils


def main():
    from .config import get_config
    config = get_config()

    camera = Camera(config)
    if not camera.init():
        sys.exit(1 )

    def on_idle():
        frame = camera.get()
        
        ratio = frame.shape[0] / config.height
        frame_debug = imutils.resize(frame, height = config.height)

        box = utils.detect_paper_canny(frame_debug)
        if box is not None:
            warped = utils.warp(frame, box, ratio)
            utils.show(warped, title="warped")
        gui.show(frame_debug)
        return True

    gui = Gui(on_idle)
    gui.run()


def run():
    main()
