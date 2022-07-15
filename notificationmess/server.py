from typing import Optional

from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method

from notificationmess.bar import NotificationBar


class NotificationServer(ServiceInterface):
    bus: Optional[MessageBus]

    def __init__(self, bar: NotificationBar,
                 name: str = None, vendor: str = None, version: str = None, spec_version: str = None):
        super().__init__('org.freedesktop.Notifications')
        self.bar = bar
        self.server_name = name or ""
        self.server_vendor = vendor or ""
        self.server_version = version or ""
        self.server_spec_version = spec_version or ""
        self.bus = None

    async def start(self):
        if self.bus is None:
            self.bus = await MessageBus().connect()
            self.bus.export('/org/freedesktop/Notifications', self)
            await self.bus.request_name('org.freedesktop.Notifications')
            await self.bus.wait_for_disconnect()

    def stop(self):
        if self.bus is not None and self.bus.connected:
            self.bus.disconnect()
            self.bus = None

    @method()
    def GetServerInformation(self) -> 'ssss':
        return [self.server_name, self.server_vendor, self.server_version, self.server_spec_version]

    @method()
    async def Notify(self,
                     app_name: 's',
                     replaces_id: 'u',
                     app_icon: 's',
                     summary: 's',
                     body: 's',
                     actions: 'as',
                     hints: 'a{sv}',
                     expire_timeout: 'i') -> 'u':
        return await self.bar.on_notify(app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout)
