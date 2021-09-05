import logging
import lib.gps as gps

from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap

LOGGER = logging.getLogger(__name__)

class UserActions():
    selected_playlist_item = 0
    now_playing = {'id' : 0}
    location_text = None
    art_cache_key = ""

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
        self.nomadic.ui.NightMode.setChecked(False)
        self.change_page(self.nomadic.pages['night'])

    def music_play_press(self):
        """
        Start playback of music
        """
        LOGGER.debug("Music play button pressed.")

        if 'connection' in self.nomadic.bt_status and self.nomadic.bt_status['connection']:
            self.nomadic.bluetooth.play_audio()
        else:
            self.nomadic.mpd.play_playback()

        self.nomadic.mpd_status['state'] = 'playing' if self.nomadic.bt_status.get('connection', False) is True else 'play'
        self.ui_button_state()

    def music_stop_press(self):
        """
        Stop the playback of music
        """
        LOGGER.debug("Music stop button pressed.")
        
        if 'connection' in self.nomadic.bt_status and self.nomadic.bt_status['connection']:
            if 'status' in self.nomadic.bt_status and self.nomadic.bt_status['status'] == 'playing':
                self.nomadic.bluetooth.stop_playback()
        else:
            self.nomadic.mpd.stop_playback()

        self.clear_now_playing()
        self.nomadic.ui.MusicPlay.setChecked(False)
        self.ui_button_state()
        self.nomadic.ui.SongPlayTime.clear()
        self.art_cache_key = None
        self.nomadic.ui.MPDAlbumArt.clear()

    def music_skip_press(self):
        """
        Skip playback to the next song
        """
        LOGGER.debug("Music skip button pressed.")
        if 'connection' in self.nomadic.bt_status and self.nomadic.bt_status['connection']:
            self.nomadic.bluetooth.next_playback()
        else:        
            if self.nomadic.mpd_status.get('state', '') == 'play':
                self.nomadic.mpd.next_song()

        self.clear_now_playing()
        self.ui_button_state()
        self.art_cache_key = None
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

        if self.nomadic.mpd_status.get('state', '') == 'play' or self.nomadic.bt_status.get('status', '') == 'playing':
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
        format_time = lambda time: divmod(round(float(time)), 60)

        if 'status' in self.nomadic.bt_status and self.nomadic.bt_status.get('status', '') == 'playing':
            m, s = format_time(self.nomadic.bt_status.get('position', 0) / 1000)
            song_elapsed = "%02d:%02d" % (m, s)

            if self.nomadic.bt_status.get('duration', 0) > 0:
                m, s = format_time(self.nomadic.bt_status.get('duration'))
                song_elapsed = f"{song_elapsed} / {('%02d:%02d' % (m, s))}"

            self.nomadic.ui.SongPlayTime.setText(f"{song_elapsed}")                 
        else:
            if self.nomadic.mpd_status.get('state', '') == 'play':
                m, s = format_time(self.nomadic.mpd_status.get('elapsed', 0))
                song_elapsed = "%02d:%02d" % (m, s)

                m, s = format_time(self.nomadic.mpd_status.get('duration', 0))
                self.nomadic.ui.SongPlayTime.setText(f"{song_elapsed} / {('%02d:%02d' % (m, s))}")  
              
    def update_playlist_count(self):
        """
        Update the playlist count shown on the left column
        """

        if 'connection' in self.nomadic.bt_status and self.nomadic.bt_status['connection']:
            if 'numberoftracks' in self.nomadic.bt_status:
                self.nomadic.ui.MPDPlaylistInfo.setText(f"Playlist Length: {self.nomadic.bt_status['numberoftracks']}")
        else:
            playlist_length = self.nomadic.mpd_status.get('playlistlength', None)

            if isinstance(playlist_length, str):
                try:
                    self.nomadic.ui.MPDPlaylistInfo.setText(f"Playlist Length: {playlist_length}")
                except Exception as e:
                    LOGGER.error(e)
            else:
                self.nomadic.ui.MPDPlaylistInfo.setText("Playlist Length: 0")

    def update_mpd_playing_info(self):
        """
        Update the playing and next playing areas of the home view
        """
        self.update_playlist_count()
        self.ui_button_state()
        self.update_music_playtime()              

        if 'status' in self.nomadic.bt_status and self.nomadic.bt_status.get('status', '') == 'playing':
            artist = self.nomadic.bt_status.get('artist', '')
            now_playing = f"Playing: {artist}\n{self.nomadic.bt_status.get('title', '')}"
            self.nomadic.ui.MPDNowPlaying.setText(now_playing)
            self.nomadic.ui.NightNextPlaying.setText(now_playing)

            if len(artist) > 2:
                self.set_album_art(artist)
        else:
            if self.nomadic.mpd_status.get('state', '') == 'play':
                if self.nomadic.now_playing is None or self.nomadic.now_playing != self.nomadic.mpd_status['songid']:
                    self.nomadic.now_playing = self.nomadic.mpd_status['songid']  

                    self.nomadic.ui.MPDNowPlaying.setText(
                        self.nomadic.mpd.current_song_title(self.nomadic.mpd_status)
                    )

                    self.nomadic.ui.MPDNextPlaying.setText(
                        self.nomadic.mpd.next_song_title(self.nomadic.mpd_status)
                    )

                    self.nomadic.ui.NightNowPlaying.setText(
                        self.nomadic.mpd.current_song_title(self.nomadic.mpd_status)
                    )

                    self.nomadic.ui.NightNextPlaying.setText(self.nomadic.mpd.next_song_title(self.nomadic.mpd_status))
                    self.mpd_album_art()

            if self.nomadic.mpd_status.get('state', '') == 'stop':
                self.music_stop_press()        

    def show_audio_source(self, bluetooth: dict):
        """
        Show the currently connected audio source in the UI

        :param: dict bluetooth 
        """ 
        if 'connection' in bluetooth and bluetooth['connection']:
            srcMsg = f"Source: Bluetooth\nDevice: {bluetooth.get('name', '')}\nAddress: {bluetooth.get('mac', '')}"
            self.nomadic.ui.AudioSrc.setText(srcMsg)
            src_icon = QPixmap(self.nomadic.ui.base_path + "visual_elements/icons/bluetooth_icon.png")
        else:
            self.nomadic.ui.AudioSrc.setText("Source: MPD")
            src_icon = QPixmap(self.nomadic.ui.base_path + "visual_elements/icons/mpd_icon.png")

        self.nomadic.ui.AudioSrcIcon.setPixmap(src_icon)

    def mpd_album_art(self):
        """
        Get the artist of the playing track via MPD and get album art
        """
        song_img, song, search_term = None, self.nomadic.mpd_status.get('song', None), ""

        if isinstance(song, str):
            song_dets = self.nomadic.mpd.playlist_info(self.nomadic.mpd_status.get('song'))

            if 'artist' in song_dets[0] and len(song_dets[0]['artist']) > 2:
                search_term = (f"{song_dets[0]['artist']}")
                LOGGER.info(f"Attempting to get album art for search term: {search_term}.")

        self.set_album_art(search_term)

    def set_album_art(self, search_term: str):
        """
        Attempt to retrieve album art for the UI

        :param: str search_term
        """        
        cache_key = (''.join(ch for ch in search_term if ch.isalnum())).lower()
        if self.art_cache_key != cache_key:
            song_thumb = self.nomadic.mpd.album_art(search_term, cache_key)

            if isinstance(song_thumb, str):
                song_img = QPixmap(song_thumb)
            else:
                song_img = QPixmap(self.nomadic.mpd.default_art()) if song_img is None else QPixmap(self.nomadic.mpd.default_art())

            self.nomadic.ui.MPDAlbumArt.setPixmap(song_img)
            self.art_cache_key = cache_key

    def clear_now_playing(self):
        """
        Clear the areas showing the name of the current and next up track
        """
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
                self.nomadic.ui.CurrentSpeed.setText(f"{gps.ms_kmh_coversion(self.nomadic.gps_info.hspeed)}")

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
