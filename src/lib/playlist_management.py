class PlaylistManagement():
    selected_playlist_item = 0

    def __init__(self, ui, mpd):
        self.ui = ui
        self.mpd = mpd

        # Register the button actions on the current playlist page
        self.ui.HomeButton.clicked.connect(self.view_home_widget)
        self.ui.PlaylistUpButton.clicked.connect(self.playlist_scroll_up)
        self.ui.PlaylistDownButton.clicked.connect(self.playlist_scroll_down)
        self.ui.PlaylistContents.itemClicked.connect(self.select_playlist_item)
        self.ui.PlaylistContents.itemDoubleClicked.connect(self.play_playlist_item)
        self.ui.PlayPlaylistItem.clicked.connect(self.play_playlist_item)
        self.ui.PlaylistItemDeleteButton.clicked.connect(self.remove_playlist_item)

    def view_home_widget(self):
        """
        Change the visible widget to the application home view
        """
        try:
            self.ui.appContent.setCurrentIndex(0)
        except:
            pass

    def update_playlist_contents(self):
        """
        Update the contents of the playlist window
        """
        mpd_status = self.mpd.get_status()
        playlist_length = mpd_status.get('playlistlength', 0)
        self.ui.PlaylistCount.setText(str(playlist_length) + " Items")
        self.playlist_items()

    def play_playlist_item(self):
        """
        Play a playlist item
        """
        song_id = self.playlist_song_id()

        self.mpd.play_song(song_id)

    def remove_playlist_item(self):
        """
        Remove a song from the playlist
        """
        song_id = self.playlist_song_id(True)

        self.mpd.remove_song(song_id)
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
            song_row = self.ui.PlaylistContents.currentRow()

            if take is None:
                song_value = (self.ui.PlaylistContents.item(song_row)).text()
            else:
                song_value = (self.ui.PlaylistContents.takeItem(song_row)).text()

            song_value = (song_value.split('-', 1))[0][9:]

            return int(song_value)
        except:
            pass

    def select_playlist_item(self):
        """
        Execute method when a select playlist item
        """
        self.selected_playlist_item = self.ui.PlaylistContents.currentRow()


    def playlist_scroll_up(self):
        """
        Select the playlist item above the current selection
        """
        if self.selected_playlist_item > 0:
            self.selected_playlist_item -= 1
            self.ui.PlaylistContents.setCurrentRow(self.selected_playlist_item)

    def playlist_scroll_down(self):
        """
        Select the playlist item below the current selection
        """
        mpd_status = self.mpd.get_status()
        playlist_length = mpd_status.get('playlistlength', 0)

        if int(self.selected_playlist_item) < int(playlist_length):
            self.selected_playlist_item += 1
            self.ui.PlaylistContents.setCurrentRow(self.selected_playlist_item)

    def playlist_items(self):
        """
        Populate the list widget with the contents of the playlist
        """
        mpd_playlist = self.mpd.playlist_contents()

        if len(mpd_playlist) > 0:
            for mpd_item in mpd_playlist:
                song_name = 'Song ID: ' + str(mpd_item.get('id', 0)) + ' - ' + mpd_item.get('title', 'Unknown') + ' - ' + mpd_item.get('artist', 'Unknown')
                self.ui.PlaylistContents.addItem(song_name)
                self.ui.PlaylistContents.setCurrentRow(self.selected_playlist_item)
