import logging
import sys

import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

LOGGER = logging.getLogger(__name__)

class Bluetooth():
    dbus_mgr, sys_bus = None, None

    bt_device = {
        'name' : None,
        'mac' : None,
        'connection' : False,
        'audio' : False,
        'status' : None,
        'artist' : None,
        'track' : None,
    }

    player_iface, transport_iface = None, None

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        
        self.sys_bus = dbus.SystemBus()     
        self.dbus_mgr = dbus.Interface(self.sys_bus.get_object('org.bluez', "/"), 'org.freedesktop.DBus.ObjectManager')
        self.setup_audio() 

    def setup_audio(self):
        dbus_objs = self.dbus_mgr.GetManagedObjects().items()

        for path, ifaces in dbus_objs:
            if 'org.bluez.MediaPlayer1' in ifaces:
                self.player_iface = dbus.Interface(
                        self.sys_bus.get_object('org.bluez', path), 'org.bluez.MediaPlayer1')
            if 'org.bluez.MediaTransport1' in ifaces:
                self.transport_iface = dbus.Interface(
                        self.sys_bus.get_object('org.bluez', path), 'org.freedesktop.DBus.Properties')
        
        if not self.player_iface or not self.transport_iface:
            if not self.player_iface:
                LOGGER.error('Error: Media Player not found.')
            else:
                LOGGER.error('Error: DBus.Properties iface not found.')

        self.sys_bus.add_signal_receiver(
                self.on_property_changed,
                bus_name='org.bluez',
                dbus_interface='org.freedesktop.DBus.Properties')

        #GLib.io_add_watch(sys.stdin, GLib.IO_IN, self.on_playback_control)
        #GLib.MainLoop().run()

        self.bt_device['audio'] = True if self.bt_device is True else False

    def on_property_changed(self, interface, changed, invalidated):
        """
        Update the status of the bt device when a status change is detected
        """
        if interface != 'org.bluez.MediaPlayer1':
            return

        for prop, value in changed.items():
            if prop == 'Status':
                self.bt_device['status'] = str(value)
            if prop == 'Track':
                self.track_details(value)

    def track_details(self, track: dict):
        """
        Insert the track details in the bt_device obj

        :param: dict track
        """
        for key, value in track.items():
            self.bt_device[key.lower()] = int(value) if key == 'Duration' else str(value)

    def check_connection(self) -> dict:
        """
        Return the status and device details of any Bluetooth connections

        :return: dict
        """
        dbus_objs = self.dbus_mgr.GetManagedObjects().items()
        for path, ifaces in dbus_objs:
            if 'org.bluez.Device1' in ifaces and 'Connected' in ifaces['org.bluez.Device1']:
                if ifaces['org.bluez.Device1']['Connected'] == 1:
                    self.bt_device['name'] = str(ifaces['org.bluez.Device1']['Name'])
                    self.bt_device['mac'] = str(ifaces['org.bluez.Device1']['Address'])
                    self.bt_device['connection'] = True

            if 'org.bluez.MediaPlayer1' in ifaces:
                if 'Track' in ifaces['org.bluez.MediaPlayer1']:
                    self.track_details(ifaces['org.bluez.MediaPlayer1']['Track'])
                if 'Status' in ifaces['org.bluez.MediaPlayer1']:
                    self.bt_device['status'] = str(ifaces['org.bluez.MediaPlayer1']['Status'])
                if 'Position' in ifaces['org.bluez.MediaPlayer1']:
                    self.bt_device['position'] = int(ifaces['org.bluez.MediaPlayer1']['Position'])
        print(self.bt_device)
        return self.bt_device

if __name__ == '__main__':
    print("This module cannot be run directly.")
    sys.exit()