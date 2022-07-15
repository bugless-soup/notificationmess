import asyncio
import logging
import os
import signal
from threading import Thread

import asyncio_glib
import gi

from notificationmess import bar, server, theme

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# CONFIGURATION #
_theme = theme.Theme("theme/config.json")
_bar = bar.NotificationBar(_theme)
_server = server.NotificationServer(_bar, "notificationmess", "bugless-soup", "0.1", "0.1")


#############

def start(debug_notification: bool = False):
    if debug_notification:
        logging.root.level = logging.DEBUG

    async def tasks():
        await asyncio.gather(
            _bar.start(),
            _server.start(),
            unsafe_notify(debug_notification))

    asyncio.set_event_loop_policy(asyncio_glib.GLibEventLoopPolicy())
    _loop = asyncio.get_event_loop()
    _loop.add_signal_handler(signal.SIGTERM, stop)
    _loop.run_until_complete(tasks())


def stop():
    _server.stop()
    _bar.stop()
    Gtk.main_quit()


async def unsafe_notify(debug: bool = False):
    if debug:
        logging.debug("Notification in 3 seconds")
        await asyncio.sleep(3)
        Thread(target=os.system, args=("notify-send 'DEBUG NOTIFICATION'",)).start()
