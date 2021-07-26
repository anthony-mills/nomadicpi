import sys
import configparser
import logging
import time
import threading

import lib.db
import lib.gps as gps, lib.mpd as mpd
import lib.application_home as application_home
import lib.playlist_management as playlist_management
import lib.location_status as location_status
import lib.system_status as system_status
import lib.file_management as file_management

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap

log_format = "%(asctime)s %(levelname)s:%(name)s - %(message)s"

logging.basicConfig(filename='/tmp/nomadic.log', level=logging.DEBUG, filemode='w', format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
LOGGER = logging.getLogger(__name__)

class NomadicPi():
    pages = {
        'home' : 0,
        'playlist' : 1,
        'system' : 2,
        'files' : 3,
        'location' : 4
    }

    # Folder for album art
    art_cache = '/tmp'

    # Desired date / time format
    dt_format = "%A %d %B %Y %-I:%M %p"

    # Track the GPS state with this variable
    gps_info, gps_save_interval = None, 60
    speed_unit, speed_modifier = 'kmh', 1

    base_path, location_text, update_loop = '', None, None

    def __init__(self, ui):
        self.ui = ui
        self.app_config = configparser.ConfigParser()

        self.app_config.read(ui.base_path + 'config.ini')
        self.now_playing = {'id' : 0};

        # Connect to the SQLite database
        self.db = lib.db.NomadicDb(ui.base_path)

        # Connect to the MPD daemon
        self.connect_mpd()
        self.get_mpd_status()

        # Setup the handlers for user actions on the application home
        self.application_home = application_home.UserActions(self)
        self.application_home.ui_button_state()

        # Setup the handlers for user actions on the playlist page
        self.current_playlist = playlist_management.PlaylistManagement(self)

        # Setup the handlers for user actions on the file management page
        self.mpd_files = file_management.FileManagement(self)

        # Setup the handlers for user actions on the system status page
        self.system_status = system_status.SystemStatus(self)

        # Setup the handlers for user actions on the location page
        self.location_status = location_status.LocationStatus(self)

        self.location_text = QtGui.QFont()
        self.location_text.setFamily("Open Sans")
        self.location_text.setPointSize(10)

        self.ui.appContent.setCurrentIndex(self.pages['home'])
        self.ui.appContent.currentChanged.connect(self.application_page_changed)

        self.speed_units()
        self.update_cycle_count = 0
        self.update_content()

    def speed_units(self):
        """
        Control the unit used for speed of travel km/h of mp/h
        """
        speed_units = self.app_config['app'].get('SpeedUnit', '')

        if speed_units == 'mph':
            self.speed_unit = 'mph'
            self.speed_modifier = 0.62137119
            self.ui.SpeedUnit.setText('MP/H')

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
        (threading.Thread(target=self.update_gps)).start()
        (threading.Thread(target=self.update_mpd)).start()

        # Only update the home page if the widget is visible
        if self.ui.appContent.currentIndex() == self.pages['home']:
            # Update GPS related information
            self.application_home.update_gps_info()

        if self.ui.appContent.currentIndex() == self.pages['system']:
            self.system_status.show_system_status()

        if self.ui.appContent.currentIndex() == self.pages['location']:
            self.location_status.update_page()

    def update_mpd(self):
        """
        Update the interface with any time sensitive MPD info i.e play time etc
        """
        try:
            self.mpd_status = self.mpd.update_status()

            self.application_home.database_update_status(self.mpd_status)

            self.application_home.update_playlist_count()
            self.application_home.ui_button_state()

            if self.mpd_status.get('state', '') == 'play':
                m, s = divmod(round(float(self.mpd_status.get('elapsed', 0))), 60)
                song_elapsed = "%02d:%02d" % (m, s)

                m, s = divmod(round(float(self.mpd_status.get('duration', 0))), 60)
                song_duration = "%02d:%02d" % (m, s)

                self.ui.SongPlayTime.setText(f"{song_elapsed} / {song_duration}")

                if  self.now_playing['id'] != self.mpd_status['songid']:
                    self.now_playing = self.mpd.currently_playing()

                    song_info = f"Playing: {self.now_playing.get('artist', 'Unknown')}\n {self.now_playing.get('title', 'Unknown')}"
                    self.ui.MPDNowPlaying.setText(song_info)

                    next_song = self.mpd_status.get('nextsong', None)

                    if next_song is not None and int(next_song) > 0:
                        try:
                            next_up = self.mpd.playlist_info(next_song)

                            if len(next_up) == 1:
                                next_song = next_up[0]
                                song_info = f"Next: {next_song.get('artist', 'Unknown')}\n {next_song.get('title', 'Unknown')}"
                                self.ui.MPDNextPlaying.setText(song_info)
                        except:
                            pass
                    else:
                        self.ui.MPDNextPlaying.setText("")

                    self.application_home.update_playlist_count()
                    self.set_album_art(self.now_playing)

            if self.mpd_status.get('state', '') == 'stop':
                self.application_home.music_stop_press()
        except Exception as e:
            LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")

            # Attempt to reconnect to MPD exception is normally a client timeout
            LOGGER.info("Attempting to reconnect to MPD Daemon..")
            self.connect_mpd()

    def set_album_art(self, song_data):
        """
        Update the album art displayed in the UI
        """
        search_term = (f"{song_data.get('artist', '')}")
        LOGGER.info(f"Attempting to get album art for search term: {search_term}.")

        cache_key = (''.join(ch for ch in search_term if ch.isalnum())).lower()
        song_thumb = self.mpd.album_art(search_term, cache_key)

        if isinstance(song_thumb, str):

            song_img = QPixmap(song_thumb)
            self.ui.MPDAlbumArt.setPixmap(song_img)

    def update_gps(self):
        """
        Get the current GPS information and update the UI
        """
        if gps.gpsd_socket is None:
            self.ui.CurrentPosition.setFont(self.location_text)
            self.ui.CurrentAltitude.setFont(self.location_text)

            try:
                gpsd_host = self.app_config['gpsd'].get('Host', 'localhost')
                gpsd_port = int(self.app_config['gpsd'].get('Port', '2947'))

                gps.gps_connect(host=gpsd_host, port=gpsd_port)
            except Exception as e:
                LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")
                LOGGER.warning(f"Unable to connect to GPSD service at: {gpsd_host}:{gpsd_port}")
        else:
            try:
                self.gps_info = gps.get_current()

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