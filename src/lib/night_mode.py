import datetime as dt
import logging
import lib.gps as gps

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

LOGGER = logging.getLogger(__name__)

class NightMode():

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register action to return back to daylight mode
        self.nomadic.ui.NightSwitchMode.clicked.connect(self.nomadic.view_home_widget)
        self.nomadic.ui.NightPlayButton.clicked.connect(self.music_play_press)
        self.nomadic.ui.NightTrackSkipButton.clicked.connect(self.music_skip_press)
        self.nomadic.ui.NightStopButton.clicked.connect(self.music_stop_press)

    def update_view(self):
        """
        Update the interface while in night mode
        """
        self.ui_button_state()
        self.update_gps_speed()

        if 'songid' in self.nomadic.mpd_status and self.nomadic.now_playing != self.nomadic.mpd_status['songid']:
            self.update_mpd_info()

    def clear_now_playing(self):
        """
        Clear the contents of the now / next playing areas
        """
        self.nomadic.clear_now_playing()

    def ui_button_state(self):
        """
        Update the state of any UI buttons
        """
        if self.nomadic.mpd_status.get('state', '') == 'play':
            self.nomadic.ui.NightPlayButton.setChecked(True)
            self.nomadic.ui.NightPlayButton.setIcon(QtGui.QIcon(self.nomadic.ui.base_path + "visual_elements/icons/media_pause.png"))
        else:
            self.nomadic.ui.NightPlayButton.setChecked(False)
            self.nomadic.ui.NightPlayButton.setIcon(QtGui.QIcon(self.nomadic.ui.base_path + "visual_elements/icons/media_play.png"))


    def update_mpd_info(self,force_update = 0):
        """
        Update UI with information related to music playback
        """
        LOGGER.info('Updating UI playing state')

        if 'state' in self.nomadic.mpd_status and self.nomadic.mpd_status.get('state', '') == 'play' or force_update == 1:
            self.nomadic.ui.NightNowPlaying.setText(self.nomadic.mpd.current_song_title(self.nomadic.mpd_status))
            self.nomadic.ui.NightNextPlaying.setText(self.nomadic.mpd.next_song_title(self.nomadic.mpd_status))

    def music_play_press(self):
        """
        Start playback of music
        """
        LOGGER.debug("Music play button pressed.")
        self.nomadic.mpd.play_playback()
        self.nomadic.mpd_status['state'] = 'play'
        self.ui_button_state()
        self.update_mpd_info(1)

    def music_skip_press(self):
        """
        Skip playback to the next song
        """
        if 'state' in self.nomadic.mpd_status and self.nomadic.mpd_status.get('state', '') == 'play':
            LOGGER.debug("Music skip button pressed.")
            self.nomadic.mpd.next_song()
            self.ui_button_state()
            self.clear_now_playing()
            self.update_mpd_info(1)

    def music_stop_press(self):
        """
        Stop the playback of music
        """
        if 'state' in self.nomadic.mpd_status and self.nomadic.mpd_status.get('state', '') != 'stop':
            LOGGER.debug("Music stop button pressed.")
            self.clear_now_playing()
            self.nomadic.mpd.stop_playback()
            self.ui_button_state()

    def update_gps_speed(self):
        """
        Update the current GPS speed
        """
        if self.nomadic.gps_info is not None:
            if hasattr(self.nomadic.gps_info, 'hspeed') and isinstance(self.nomadic.gps_info.hspeed, float):
                self.nomadic.ui.NightSpeed.setText(f"{gps.ms_kmh_coversion(self.nomadic.gps_info.hspeed) * self.nomadic.speed_modifier}")            