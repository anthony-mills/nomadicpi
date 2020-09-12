class FileManagement():
    selected_file_item = 0

    def __init__(self, ui, mpd):
        self.ui = ui
        self.mpd = mpd

        # Register the button actions fot the file management page
        self.ui.FileReturnHome.clicked.connect(self.view_home_widget)
        self.ui.FileListUp.clicked.connect(self.playlist_scroll_up)
        self.ui.FileListDown.clicked.connect(self.playlist_scroll_down)
    
    def view_home_widget(self):
        """
        Change the visible widget to the application home view
        """
        try:
            self.ui.appContent.setCurrentIndex(0)
        except:
            pass

    def playlist_scroll_up(self):
        """
        Select the playlist item above the current selection
        """
        if self.selected_playlist_item > 0:
            self.selected_playlist_item -= 1
            self.ui.FileList.setCurrentRow(self.selected_playlist_item)

    def playlist_scroll_down(self):
        """
        Select the playlist item below the current selection
        """
        mpd_status = self.mpd.get_status()
        playlist_length = mpd_status.get('playlistlength', 0)

        if int(self.selected_playlist_item) < int(playlist_length):
            self.selected_playlist_item += 1
            self.ui.FileList.setCurrentRow(self.selected_playlist_item)

    def filesystem_items(self):
        """
        Populate the list widget with the contents of the MPD filesystem
        """
        pass
