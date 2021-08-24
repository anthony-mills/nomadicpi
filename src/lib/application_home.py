import logging
import lib.gps as gps

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

LOGGER = logging.getLogger(__name__)

class UserActions():
    selected_playlist_item = 0
    now_playing = {'id' : 0}
    location_text = None

    def __init__(self, nomadic):
        self.nomadic = nomadic
        self.clear_now_playing()

        # Define font and style for the altitude and heading
        self.location_text = QtGui.QFont()
        self.location_text.setFamily("Open Sans")
        self.location_text.setPointSize(10)

        # Set the initial button state from the MPD state
        self.ui_button_state()

        # Register the button actions on the home page
        self.nomadic.ui.MusicPlay.clicked.connect(self.music_play_press)
        self.nomadic.ui.RandomPlayback.clicked.connect(self.music_random_press)
        self.nomadic.ui.ConsumptionPlayback.clicked.connect(self.music_consume_press)

        self.nomadic.ui.MusicSkip.clicked.connect(self.music_skip_press)
        self.nomadic.ui.MusicStop.clicked.connect(self.music_stop_press)

        self.nomadic.ui.PlaylistDetailsButton.clicked.connect(self.view_playlist_widget)
        self.nomadic.ui.CollectionButton.clicked.connect(self.view_file_management)
        self.nomadic.ui.SystemButton.clicked.connect(self.view_system_widget)
        self.nomadic.ui.LocationButton.clicked.connect(self.view_location_widget)
        self.nomadic.ui.NightMode.clicked.connect(self.view_night_mode)
        self.nomadic.ui.QuitButton.clicked.connect(self.nomadic.exit_application)

    def change_page(self, widget_id):
        """
        Change the visible widget in use
        """
        try:
            self.nomadic.ui.appContent.setCurrentIndex(widget_id)
        except Exception as e:
            LOGGER.error(e)

    def view_playlist_widget(self):
        """
        Change the visible widget to the current playlist view
        """
        LOGGER.debug("Switching view to the current view.")
        self.change_page(self.nomadic.pages['playlist'])

    def view_system_widget(self):
        """
        Change the visible widget to the system status / settings view
        """
        LOGGER.debug("Switching view to the system status view.")
        self.change_page(self.nomadic.pages['system'])

    def view_location_widget(self):
        """
        Change the visible widget to the location view
        """
        LOGGER.debug("Switching view to the location info view.")
        LOGGER.info(self.nomadic.pages['location'])

        self.nomadic.location_status.update_page()
        self.change_page(self.nomadic.pages['location'])

    def view_file_management(self):
        """
        Change the visible widget to the filesystem view
        """
        LOGGER.debug("Switching view to the file management view.")
        self.change_page(self.nomadic.pages['files'])

    def view_night_mode(self):
        """
        Change the interface to "night mode"
        """
        LOGGER.debug("Switching view to night mode.")
        self.change_page(self.nomadic.pages['night'])

    def music_play_press(self):
        """
        Start playback of music
        """
        LOGGER.debug("Music play button pressed.")
        self.nomadic.mpd.play_playback()
        self.ui_button_state()

    def music_stop_press(self):
        """
        Stop the playback of music
        """
        if self.nomadic.mpd_status.get('state', '') != 'stop':
            LOGGER.debug("Music stop button pressed.")
            self.nomadic.clear_now_playing()
            self.nomadic.mpd.stop_playback()
            self.nomadic.ui.MusicPlay.setChecked(False)
            self.ui_button_state()
            self.nomadic.ui.SongPlayTime.clear()
            self.nomadic.ui.MPDAlbumArt.clear()

    def music_skip_press(self):
        """
        Skip playback to the next song
        """
        if self.nomadic.mpd_status.get('state', '') == 'play':
            LOGGER.debug("Music skip button pressed.")
            self.clear_now_playing()
            self.nomadic.mpd.next_song()
            self.ui_button_state()
            self.nomadic.ui.MPDAlbumArt.clear()

    def music_random_press(self):
        """
        Enable / Disable random playback of music
        """
        LOGGER.debug("Changing the MPD random playback status.")
        self.nomadic.mpd.random_playback()
        self.ui_button_state()

    def music_consume_press(self):
        """
        Enable / Disable consumption playback of music
        """
        LOGGER.debug("Changing the MPD track consumption status.")
        self.nomadic.mpd.consumption_playback()
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

    def update_music_playtime(self):
        """
        Update the track playtime
        """        
        if self.nomadic.mpd_status.get('state', '') == 'play':
            m, s = divmod(round(float(self.nomadic.mpd_status.get('elapsed', 0))), 60)
            song_elapsed = "%02d:%02d" % (m, s)

            m, s = divmod(round(float(self.nomadic.mpd_status.get('duration', 0))), 60)
            song_duration = "%02d:%02d" % (m, s)

            self.nomadic.ui.SongPlayTime.setText(f"{song_elapsed} / {song_duration}")  
              
    def update_playlist_count(self):
        """
        Update the playlist count shown on the left column
        """
        playlist_length = self.nomadic.mpd_status.get('playlistlength', None)

        if isinstance(playlist_length, str):
            try:
                self.nomadic.ui.MPDPlaylistInfo.setText(f"Songs Pending: {playlist_length}")
            except Exception as e:
                LOGGER.error(e)
        else:
            self.nomadic.ui.MPDPlaylistInfo.setText("Songs Pending: 0")

    def update_mpd_playing_info(self):
        """
        Update the playing and next playing areas of the home view
        """
        self.update_playlist_count()
        self.ui_button_state()
        self.update_music_playtime()

        if self.nomadic.mpd_status.get('state', '') == 'play':
            if self.nomadic.now_playing is None or self.nomadic.now_playing != self.nomadic.mpd_status['songid']:
                self.nomadic.now_playing = self.nomadic.mpd_status['songid']  

                self.nomadic.ui.MPDNowPlaying.setText(
                    self.nomadic.mpd.current_song_title(self.nomadic.mpd_status)
                )

                self.nomadic.ui.MPDNextPlaying.setText(
                    self.nomadic.mpd.next_song_title(self.nomadic.mpd_status)
                )
                
                self.update_playlist_count()
                self.set_album_art()

                self.nomadic.ui.NightNowPlaying.setText(
                    self.nomadic.mpd.current_song_title(
                        self.nomadic.mpd_status
                    )
                )

                self.nomadic.ui.NightNextPlaying.setText(
                    self.nomadic.mpd.next_song_title(self.nomadic.mpd_status)
                )                    

            if self.nomadic.mpd_status.get('state', '') == 'stop':
                self.music_stop_press()        

    def set_album_art(self):
        """
        Update the album art displayed in the UI
        """
        song = self.nomadic.mpd_status.get('song', None)

        if isinstance(song, str):
            song_dets = self.nomadic.mpd.playlist_info(
                self.nomadic.mpd_status.get('song')
            )

            if isinstance(song_dets[0]['artist'], str) and len(song_dets[0]['artist']) > 2:
                search_term = (f"{song_dets[0]['artist']}")
                LOGGER.info(f"Attempting to get album art for search term: {search_term}.")

                cache_key = (''.join(ch for ch in search_term if ch.isalnum())).lower()
                song_thumb = self.nomadic.mpd.album_art(search_term, cache_key)

                if isinstance(song_thumb, str):

                    song_img = QPixmap(song_thumb)
                    self.nomadic.ui.MPDAlbumArt.setPixmap(song_img)

    def clear_now_playing(self):
        self.nomadic.ui.MPDNextPlaying.clear(), self.nomadic.ui.MPDNowPlaying.clear()
        self.nomadic.ui.NightNowPlaying.clear(), self.nomadic.ui.NightNextPlaying.clear()                        


    def update_gps_info(self):
        """
        Update the state of database update button
        """
        if self.nomadic.gps_info is not None:
            self.nomadic.ui.CurrentPosition.setFont(self.location_text)
            self.nomadic.ui.CurrentAltitude.setFont(self.location_text)

            if hasattr(self.nomadic.gps_info, 'hspeed') and isinstance(self.nomadic.gps_info.hspeed, float):
                self.nomadic.ui.CurrentSpeed.setText(f"{gps.ms_kmh_coversion(self.nomadic.gps_info.hspeed) * self.nomadic.speed_modifier}")

            if hasattr(self.nomadic.gps_info, 'lon') and hasattr(self.nomadic.gps_info, 'lat'):
                self.nomadic.ui.CurrentPosition.setText(f"Coordinates: {round(self.nomadic.gps_info.lat,6)}, {round(self.nomadic.gps_info.lon,6)}")
            else:
                self.nomadic.ui.CurrentPosition.setText("Current Position: No GPS fix.")

            # Get the current Altitude
            if hasattr(self.nomadic.gps_info, 'movement'):
                heading = self.nomadic.gps_info.movement()

                if 'track' in heading and 'altitude' in heading:
                    self.nomadic.ui.CurrentAltitude.setText(f"Altitude: {heading['altitude']}m\nHeading: {round(heading['track'])} degrees {heading['direction']}")

                else:
                    self.nomadic.ui.CurrentAltitude.setText("Altitude: 3D GPS fix needed.")
