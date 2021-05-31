import logging
import sys
from PyQt5 import QtWidgets, QtGui

logger = logging.getLogger(__name__)

class UserActions():
    selected_playlist_item = 0

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Set the initial button state from the MPD state
        self.ui_button_state()

        # Register the button actions on the home page
        self.nomadic.ui.MusicPlay.clicked.connect(self.music_play_press)
        self.nomadic.ui.RandomPlayback.clicked.connect(self.music_random_press)
        self.nomadic.ui.ConsumptionPlayback.clicked.connect(self.music_consume_press)
        self.nomadic.ui.UpdateDatabase.clicked.connect(self.music_update_press)

        self.nomadic.ui.MusicSkip.clicked.connect(self.music_skip_press)
        self.nomadic.ui.MusicStop.clicked.connect(self.music_stop_press)

        self.nomadic.ui.PlaylistDetailsButton.clicked.connect(self.view_playlist_widget)
        self.nomadic.ui.CollectionButton.clicked.connect(self.view_file_management)
        self.nomadic.ui.SystemButton.clicked.connect(self.view_system_widget)
        self.nomadic.ui.LocationButton.clicked.connect(self.view_location_widget)                
        self.nomadic.ui.QuitButton.clicked.connect(self.nomadic.exit_application)

    def change_page(self, widget_id):
        """
        Change the visible widget in use
        """
        try:
            self.nomadic.ui.appContent.setCurrentIndex(widget_id)
        except:
            pass

    def view_playlist_widget(self):
        """
        Change the visible widget to the current playlist view
        """
        logger.debug("Switching view to the current view.")
        self.change_page(self.nomadic.pages['playlist'])

    def view_system_widget(self):
        """
        Change the visible widget to the system status / settings view
        """
        logger.debug("Switching view to the system status view.")
        self.change_page(self.nomadic.pages['system'])

    def view_location_widget(self):
        """
        Change the visible widget to the location view
        """
        logger.debug("Switching view to the location info view.")
        
        self.nomadic.location_status.activate_page()
        self.change_page(self.nomadic.pages['location'])
                        
    def view_file_management(self):
        """
        Change the visible widget to the filesystem view
        """
        logger.debug("Switching view to the file management view.")
        self.change_page(self.nomadic.pages['files'])     

    def music_play_press(self):
        """
        Start playback of music
        """
        logger.debug("Music play button pressed.")
        self.nomadic.mpd.play_playback()
        self.ui_button_state()

    def music_stop_press(self):
        """
        Stop the playback of music
        """
        logger.debug("Music stop button pressed.")
        self.nomadic.mpd.stop_playback()
        self.nomadic.ui.MusicPlay.setChecked(False)
        self.ui_button_state()
        self.nomadic.ui.SongPlayTime.clear()
        self.nomadic.ui.MPDNextPlaying.clear()
        self.nomadic.ui.MPDNowPlaying.clear()
        self.nomadic.ui.MPDAlbumArt.clear()

    def music_skip_press(self):
        """
        Skip playback to the next song
        """
        if self.nomadic.mpd_status.get('state', '') == 'play':
            logger.debug("Music skip button pressed.")
            self.nomadic.mpd.next_song()
            self.ui_button_state()
            self.nomadic.ui.MPDAlbumArt.clear()

    def music_random_press(self):
        """
        Enable / Disable random playback of music
        """
        logger.debug("Changing the MPD random playback status.")
        self.nomadic.mpd.random_playback()
        self.ui_button_state()

    def music_consume_press(self):
        """
        Enable / Disable consumption playback of music
        """
        logger.debug("Changing the MPD track consumption status.")        
        self.nomadic.mpd.consumption_playback()
        self.ui_button_state()

    def music_update_press(self):
        """
        Trigger manual update of the music library
        """
        logger.debug("Manual update of the MPD library contents triggered.") 
        self.nomadic.mpd.update_library()
        self.ui_button_state()

    def ui_button_state(self):
        """
        Update the state of any UI buttons
        """
        self.nomadic.get_mpd_status()
        
        if self.nomadic.mpd_status.get('state', '') == 'play':
            self.nomadic.ui.MusicPlay.setChecked(True)
            self.nomadic.ui.MusicPlay.setIcon(QtGui.QIcon(self.nomadic.ui.base_path + "visual_elements/icons/media_pause.png"))
        else:
            self.nomadic.ui.MusicPlay.setChecked(False)
            self.nomadic.ui.MusicPlay.setIcon(QtGui.QIcon(self.nomadic.ui.base_path + "visual_elements/icons/media_play.png"))

        if int(self.nomadic.mpd_status.get('random', 0)) == 1:
            self.nomadic.ui.RandomPlayback.setChecked(True)
        else:
            self.nomadic.ui.RandomPlayback.setChecked(False)

        if int(self.nomadic.mpd_status.get('consume', 0)) == 1:
            self.nomadic.ui.ConsumptionPlayback.setChecked(True)
        else:
            self.nomadic.ui.ConsumptionPlayback.setChecked(False)

        self.database_update_status(self.nomadic.mpd_status)

    def update_playlist_count(self):
        """
        Update the playlist count shown on the left column
        """
        playlist_length = self.nomadic.mpd_status.get('playlistlength', None)
        next_song = self.nomadic.mpd_status.get('nextsong', 0)

        if isinstance(playlist_length, str) and int(next_song) > 0:
            try:
                self.nomadic.ui.MPDPlaylistInfo.setText(f"Songs Pending: {playlist_length}")
            except Exception as e:
                logger.error(e)
        else:
            self.nomadic.ui.MPDPlaylistInfo.setText("Songs Pending: 0")

    def database_update_status(self, mpd_status):
        """
        Update the state of database update button

        Parameters
        ----------
        mpd_status : dict
            Dictionary of the MPD daemons current state
        """
        if self.nomadic.mpd_status.get('updating_db') is None:
            self.nomadic.ui.UpdateDatabase.setChecked(False)
        else:
            self.nomadic.ui.UpdateDatabase.setChecked(True)
