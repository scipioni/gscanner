import gi
import gscanner
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GdkPixbuf


class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def toggleGreyscale(self, *args):
        print("grey toggle")
        # global camera
        # camera.grey = not camera.grey


class Gui:
    def __init__(self, callback):
        builder = Gtk.Builder()
        builder.add_from_file(
            os.path.join(os.path.dirname(gscanner.__file__), "main.glade")
        )

        self.window = builder.get_object("pyscan")
        self.canvas = builder.get_object("image")
        self.window.show_all()
        builder.connect_signals(Handler())
        GLib.idle_add(callback)
        # Gtk.main()

    def run(self):
        Gtk.main()

    def show(self, frame):
        channels = 1
        h, w = frame.shape[:2]
        if len(frame.shape) > 2:
            channels = frame.shape[2]
        pb = GdkPixbuf.Pixbuf.new_from_data(
            frame.tostring(), GdkPixbuf.Colorspace.RGB, False, 8, w, h, channels * w
        )
        self.canvas.set_from_pixbuf(pb.copy())
