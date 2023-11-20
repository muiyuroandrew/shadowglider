import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import math

class GameWindow(Gtk.Window):
    def __init__(self):
        super(GameWindow, self).__init__(title="Geometric Shape Game")
        self.set_default_size(800, 600)
        self.connect("destroy", Gtk.main_quit)

        self.shape_x = 50
        self.shape_y = 50
        self.velocity = 2

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self.on_draw)
        self.add(self.drawing_area)

        GLib.timeout_add(50, self.update_shape_position)

    def update_shape_position(self):
        self.shape_x += self.velocity
        if self.shape_x > 750 or self.shape_x < 50:
            self.velocity *= -1
        self.drawing_area.queue_draw()
        return True

    def on_draw(self, widget, context):
        context.set_source_rgb(1, 1, 1)
        context.paint()

        context.set_source_rgb(0, 0, 0)
        context.arc(self.shape_x, self.shape_y, 20, 0, 2 * math.pi)
        context.fill()

if __name__ == "__main__":
    win = GameWindow()
    win.show_all()
    Gtk.main()
