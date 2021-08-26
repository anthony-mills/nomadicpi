import logging
import sys

import dbus, dbus.mainloop.glib
from gi.repository import GLib

LOGGER = logging.getLogger(__name__)

class Bluetooth():
    dbus_mgr, sys_bus = None, None

    def __init__(self):
        self.sys_bus = dbus.SystemBus()     
        self.dbus_mgr = dbus.Interface(self.sys_bus.get_object('org.bluez', "/"), 'org.freedesktop.DBus.ObjectManager')

    def setup(self):
        pass

    def check_connection(self) -> dict:
        """
        Return the status and device details of any Bluetooth connections

        :return: dict
        """
        bt_device = {
            'name' : None,
            'mac' : None,
            'connection' : False,
            'audio' : False
        }

        dbus_objs = self.dbus_mgr.GetManagedObjects().items()
        for path, ifaces in dbus_objs:
            if 'org.bluez.Device1' in ifaces and 'Connected' in ifaces['org.bluez.Device1']:
                if ifaces['org.bluez.Device1']['Connected'] == 1:
                    bt_device['name'] = str(ifaces['org.bluez.Device1']['Name'])
                    bt_device['mac'] = str(ifaces['org.bluez.Device1']['Address'])
                    bt_device['connection'] = True

            if 'org.bluez.MediaPlayer1' in ifaces:
                bt_device['audio'] = True

        return bt_device

if __name__ == '__main__':
    print("This module cannot be run directly.")
    sys.exit()