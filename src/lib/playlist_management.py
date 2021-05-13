import logging

logger = logging.getLogger(__name__)

class PlaylistManagement():
    selected_playlist_item = 0

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register the button actions on the current playlist page
        self.nomadic.ui.HomeButton.clicked.connect(self.nomadic.view_home_widget)
        self.nomadic.ui.PlaylistUpButton.clicked.connect(self.playlist_scroll_up)
        self.nomadic.ui.PlaylistDownButton.clicked.connect(self.playlist_scroll_down)
        self.nomadic.ui.PlaylistContents.itemClicked.connect(self.select_playlist_item)
        self.nomadic.ui.PlaylistContents.itemDoubleClicked.connect(self.play_playlist_item)
        self.nomadic.ui.PlayPlaylistItem.clicked.connect(self.play_playlist_item)
        self.nomadic.ui.PlaylistItemDeleteButton.clicked.connect(self.remove_playlist_item)
        self.nomadic.ui.DeletePlaylist.clicked.connect(self.wipe_playlist)

    def update_playlist_contents(self):
        """
        Update the contents of the playlist window
        """
        self.nomadic.get_mpd_status()
        playlist_length = self.nomadic.mpd_status.get('playlistlength', 0)
        self.nomadic.ui.PlaylistCount.setText(str(playlist_length) + " Items")
        self.playlist_items()

    def play_playlist_item(self):
        """
        Play a playlist item
        """
        song_id = self.playlist_song_id()
        
        logger.debug(f"Requesting MPD playback of playlist item #{song_id}")

        self.nomadic.mpd.play_song(song_id)

    def remove_playlist_item(self):
        """
        Remove a song from the playlist
        """
        song_id = self.playlist_song_id(True)
        logger.debug(f"Requesting MPD removal of playlist item #{song_id}")
        
        self.nomadic.mpd.remove_song(song_id)
        self.update_playlist_contents()

    def wipe_playlist(self):
        """
        Clear the contents of the current playlist
        """
        logger.debug("Clearing the contents of the current playlist.")
        self.nomadic.ui.PlaylistContents.clear()
        self.nomadic.application_home.music_stop_press()
        self.nomadic.mpd.wipe_playlist()
        self.update_playlist_contents()
        
    def playlist_song_id(self, take=None):
        """
        Return the song ID for the currently selected playlist item

        Returns
        -------
        int
            Numeric MPD id of the selected song
        """
        try:
            song_row = self.nomadic.ui.PlaylistContents.currentRow()

            if take is None:
                song_value = (self.nomadic.ui.PlaylistContents.item(song_row)).text()
            else:
                song_value = (self.nomadic.ui.PlaylistContents.takeItem(song_row)).text()

            song_value = (song_value.split('-', 1))[0][9:]

            return int(song_value)
        except:
            pass

    def select_playlist_item(self):
        """
        Execute method when a select playlist item
        """
        self.selected_playlist_item = self.nomadic.ui.PlaylistContents.currentRow()


    def playlist_scroll_up(self):
        """
        Select the playlist item above the current selection
        """
        if self.selected_playlist_item > 0:
            self.selected_playlist_item -= 1
            self.nomadic.ui.PlaylistContents.setCurrentRow(self.selected_playlist_item)

    def playlist_scroll_down(self):
        """
        Select the playlist item below the current selection
        """
        playlist_length = self.nomadic.mpd_status.get('playlistlength', 0)

        if int(self.selected_playlist_item) < int(playlist_length):
            self.selected_playlist_item += 1
            self.nomadic.ui.PlaylistContents.setCurrentRow(self.selected_playlist_item)

    def playlist_items(self):
        """
        Populate the list widget with the contents of the playlist
        """
        self.nomadic.ui.PlaylistContents.clear()
        mpd_playlist = self.nomadic.mpd.playlist_contents()

        if len(mpd_playlist) > 0:
            for mpd_item in mpd_playlist:
                song_name = 'Song ID: ' + str(mpd_item.get('id', 0)) + ' - ' + mpd_item.get('title', 'Unknown') + ' - ' + mpd_item.get('artist', 'Unknown')
                self.nomadic.ui.PlaylistContents.addItem(song_name)
                self.nomadic.ui.PlaylistContents.setCurrentRow(self.selected_playlist_item)
