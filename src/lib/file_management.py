class FileManagement():
    selected_file_item = 0
    path_file_count = 0

    def __init__(self, ui, mpd):
        self.ui = ui
        self.mpd = mpd

        # Register the button actions fot the file management page
        self.ui.FileReturnHome.clicked.connect(self.view_home_widget)
        self.ui.FileListUp.clicked.connect(self.playlist_scroll_up)
        self.ui.FileListDown.clicked.connect(self.playlist_scroll_down)

        self.ui.FileParentDirectory.clicked.connect(self.filesystem_items)
            
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
        if self.selected_file_item > 0:
            self.selected_file_item -= 1
            self.ui.FileList.setCurrentRow(self.selected_file_item)

    def playlist_scroll_down(self):
        """
        Select the playlist item below the current selection
        """
        if int(self.selected_file_item) < int(self.path_file_count):
            self.selected_file_item += 1
            self.ui.FileList.setCurrentRow(self.selected_file_item)

    def filesystem_items(self, path='/'):
        """
        Populate the list widget with the contents of the MPD filesystem
        
        Params
        -------
        string
            File System Path on the MPD filesystem             
        """
        mpd_filelist = self.mpd.ls_mpd_path()
        
        self.path_file_count = len(mpd_filelist) 
        
        self.ui.FileCount.setText('Directory Items: ' + str(self.path_file_count)) 
        
        for dir_item in mpd_filelist:
            if dir_item.get('directory', None) is not None:
                self.ui.FileList.addItem(dir_item['directory'])
                self.ui.FileList.setCurrentRow(self.selected_file_item)
