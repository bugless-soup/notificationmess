import asyncio

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import GdkPixbuf, GLib, Gio, Gtk, Gdk, GtkLayerShell


def get_screen_size():
    display = Gdk.Display.get_default()
    mon_geoms = [
        display.get_monitor(i).get_geometry()
        for i in range(display.get_n_monitors())
    ]

    x0 = min(r.x for r in mon_geoms)
    y0 = min(r.y for r in mon_geoms)
    x1 = max(r.x + r.width for r in mon_geoms)
    y1 = max(r.y + r.height for r in mon_geoms)

    return x1 - x0, y1 - y0


screen_geometry = get_screen_size()


def from_bytes(obj: bytes, size: tuple[float, float]):
    glib_bytes = GLib.Bytes.new(obj)
    stream = Gio.MemoryInputStream.new_from_bytes(glib_bytes)
    pixbuf = GdkPixbuf.PixbufAnimation.new_from_stream(stream, None)
    return Widget(Gtk.Image().new_from_animation(pixbuf), size)


class Widget:
    def __init__(self, image: Gtk.Widget, size: tuple[float, float]):
        self.is_shown = False
        self.image = image

        self.fixed = Gtk.Fixed()
        self.fixed.add(self.image)

        self.window = Gtk.Window(decorated=False)
        self.window.set_resizable(False)
        self.window.set_app_paintable(True)
        self.window.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.window.connect('button-press-event', self.close_window)
        self.window.connect("destroy", self.close_window)
        self.window.add(self.fixed)

        GtkLayerShell.init_for_window(self.window)
        GtkLayerShell.auto_exclusive_zone_enable(self.window)
        GtkLayerShell.set_anchor(self.window, GtkLayerShell.Edge.RIGHT, size[0])
        GtkLayerShell.set_anchor(self.window, GtkLayerShell.Edge.BOTTOM, size[1])

    async def show(self, wait_close: bool = False):
        self.is_shown = True
        self.window.show_all()
        if wait_close:
            while self.is_shown:
                await asyncio.sleep(0)
            self.window.close()

    def close_window(self, *args, **kwargs):
        self.is_shown = False
