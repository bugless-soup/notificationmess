from asyncio import Lock

import gi

from notificationmess.theme import Theme

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk


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


class NotificationBar:
    def __init__(self, theme: Theme):
        super().__init__()
        self.theme = theme
        self.current_id = 0
        self.lock = Lock()
        self.running = False

    async def start(self):
        self.running = True

    def stop(self):
        self.running = False

    async def on_notify(self,
                        app_name: str = None,
                        replaces_id: int = None,
                        app_icon: str = None,
                        summary: str = None,
                        body: str = None,
                        actions: list[str] = None,
                        hints: dict = None,
                        expire_timeout: int = None) -> int:
        self.current_id += 1
        out = replaces_id or self.current_id

        async with self.lock:
            if self.running:
                await self.theme.generate(summary).show(wait_close=True)

        return out
