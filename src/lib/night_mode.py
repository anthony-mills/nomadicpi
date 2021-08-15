import datetime as dt
import logging
import humanize
import psutil

from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

LOGGER = logging.getLogger(__name__)

class NightMode():

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register action to return back to daylight mode
        self.nomadic.ui.NightSwitchMode.clicked.connect(self.nomadic.view_home_widget)

        self.update_view()

    def update_view(self):
        """
        Update the interface while in night mode
        """
        self.update_mpd_info()

    def update_mpd_info(self):
        """
        Update UI with information related to music playback
        """
        if self.nomadic.mpd_status.get('state', '') == 'play':
            if  self.nomadic.now_playing['id'] != self.nomadic.mpd_status['songid']:
                self.nomadic.ui.NightNowPlaying.setText(self.nomadic.mpd.current_song_title(self.nomadic.mpd_status))
                self.nomadic.ui.NightNextPlaying.setText(self.nomadic.mpd.next_song_title(self.nomadic.mpd_status))