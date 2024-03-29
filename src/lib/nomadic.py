import sys
import configparser
import logging
import time
import threading

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot

import lib.application_home as application_home
import lib.bluetooth as bluetooth
import lib.db
import lib.file_management as file_management
import lib.gps as gps
import lib.location_status as location_status
import lib.mpd as mpd
import lib.night_mode as night_mode
import lib.playlist_management as playlist_management
import lib.system_status as system_status

log_format = "%(asctime)s %(levelname)s:%(name)s - %(message)s"

py_ver = float(f"{sys.version_info.major}.{sys.version_info.minor}")

if py_ver < 3.6:
    sys.exit("Need Python version 3.6 or greater.")
elif py_ver >= 3.8:
    logging.basicConfig(filename='/tmp/nomadic.log', level=logging.INFO, filemode='a', force=True, format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
else:
    logging.basicConfig(filename='/tmp/nomadic.log', level=logging.INFO, filemode='a', format=log_format, datefmt="%Y-%m-%d %H:%M:%S")

LOGGER = logging.getLogger(__name__)

logging.info(f"Running under Python version {py_ver}")

class NomadicPi():
    pages = {
        'home' : 0,
        'playlist' : 1,
        'system' : 2,
        'files' : 3,
        'location' : 4,
        'night' : 5
    }

    # Folder for album art
    art_cache = '/tmp'

    # Desired date / time format
    dt_format = "%A %d %B %Y %-I:%M %p"

    # Track the GPS state with this variable
    gps_info, gps_save_interval = None, 60

    base_path, update_loop, bt_status = '', None, {}

    def __init__(self, ui):
        self.ui = ui
        self.app_config = configparser.ConfigParser()

        self.app_config.read(ui.base_path + 'config.ini')
        self.now_playing = None

        # Connect to the SQLite database
        self.db = lib.db.NomadicDb(ui.base_path)

        # Connect to the MPD daemon
        self.connect_mpd()
        self.get_mpd_status()

        # Check the bluetooth status
        self.bluetooth = bluetooth.Bluetooth()

        # Setup the handlers for user actions on the application home
        self.application_home = application_home.UserActions(self)
        self.application_home.ui_button_state()

        # Setup the handlers for user actions on the playlist page
        self.current_playlist = playlist_management.PlaylistManagement(self)

        # Setup the handlers for user actions on the file management page
        self.mpd_files = file_management.FileManagement(self)

        # Setup the handlers for user actions on the system status page
        self.system_status = system_status.SystemStatus(self)

        # Setup the handlers for user actions on the night mode view
        self.night_mode = night_mode.NightMode(self)

        # Setup the handlers for user actions on the location page
        self.location_status = location_status.LocationStatus(self)

        self.ui.appContent.setCurrentIndex(self.pages['home'])
        self.ui.appContent.currentChanged.connect(self.application_page_changed)

        self.update_cycle_count = 0
        self.update_content()

    def application_page_changed(self):
        """
        Call any methods that need to happen at page change
        """
        try:
            self.current_playlist.update_playlist_contents()
            self.application_home.update_playlist_count()
            self.mpd_files.reset_file_state()
            self.mpd_files.filesystem_items()
        except Exception as e:
            LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")

    def view_home_widget(self):
        """
        Change the visible widget to the application home view
        """
        try:
            LOGGER.debug("Switching view to the application home page.")

            self.ui.appContent.setCurrentIndex(self.pages['home'])
        except Exception as e:
            LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")

    def get_mpd_status(self):
        """
        Get and store the state of the MPD daemon
        """
        try:
            self.mpd_status = self.mpd.get_status()

            return self.mpd_status
        except Exception as e:
            LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")

    def connect_mpd(self):
        """
        Connect to the MPD daemon
        """
        self.mpd = mpd.MpdLib()
        self.art_cache = self.ui.base_path + (self.app_config['mpd'].get('AlbumArt', '/tmp/'))
        self.mpd.set_mpd_host(self.app_config['mpd'].get('Host', 'localhost'))
        self.mpd.set_mpd_port(self.app_config['mpd'].get('Port', '6000'))
        self.mpd.set_art_cache(self.art_cache)

        self.mpd.connect_mpd()
        self.mpd_status = self.mpd.update_status()

    def update_content(self):
        """
        Create a timer and periodically update the UI information
        """
        self.update_gps()
        self.update_mpd()

        self.bt_status = self.bluetooth.check_connection()

        # Stop playing music from MPD when a Bluetooth audio player is connected
        if self.mpd_status.get('state', '') == 'play' and self.bt_status.get('audio', False) is True:
            self.mpd.stop_playback()

        # Only update the home page if the widget is visible
        if self.ui.appContent.currentIndex() == self.pages['home']:
            # Update GPS related information
            self.application_home.update_gps_info()

            # Display the currently active audio source
            self.application_home.show_audio_source(self.bt_status)

            # Update MPD now playing information
            self.application_home.update_mpd_playing_info()

        if self.ui.appContent.currentIndex() == self.pages['system']:
            self.system_status.show_system_status()

        if self.ui.appContent.currentIndex() == self.pages['location']:
            self.location_status.update_page()

        if self.ui.appContent.currentIndex() == self.pages['night']:
            self.night_mode.update_view()

    def update_mpd(self):
        """
        Update the interface with any time sensitive MPD info i.e play time etc
        """
        try:
            self.mpd_status = self.mpd.update_status()

            if self.mpd_status.get('state', '') == 'play' and hasattr(self.gps_info, 'time'):
                if self.now_playing is None or self.now_playing != self.mpd_status['songid']:
                    song_dets = self.mpd.playlist_info(self.mpd_status['song']) if len(self.mpd_status.get('song', '')) > 0 else None
                    self.db.save_mpd_song(self.mpd_status.get('songid', ''), song_dets[0].get('title', ''), song_dets[0].get('artist', ''), self.gps_info.time)

        except Exception as e:
            LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")

            # Attempt to reconnect to MPD exception is normally a client timeout
            LOGGER.info("Attempting to reconnect to MPD Daemon..")
            self.connect_mpd()

    def update_gps(self):
        """
        Get the current GPS information and update the UI
        """
        if gps.gpsd_socket is None:
            try:
                gpsd_host = self.app_config['gpsd'].get('Host', 'localhost')
                gpsd_port = int(self.app_config['gpsd'].get('Port', '2947'))

                gps.gps_connect(host=gpsd_host, port=gpsd_port)
                LOGGER.info(f"Established connection to GPSD service.")
            except Exception as e:
                LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")
                LOGGER.warning(f"Unable to connect to GPSD service at: {gpsd_host}:{gpsd_port}")
        else:
            self.gps_info = gps.get_current()

            try:
                if self.update_cycle_count == self.gps_save_interval:
                    self.db.save_location(self.gps_info)
                    self.update_cycle_count = 0
                self.update_cycle_count += 1

            except Exception as e:
                LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")

    def exit_application(self):
        """
        Close the MPD connection and close the application
        """
        self.mpd.close_mpd()
        LOGGER.debug("Exiting application.")
        sys.exit(0)
