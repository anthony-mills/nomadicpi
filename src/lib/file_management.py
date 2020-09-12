from PyQt5 import QtGui

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

        self.ui.FileOpenFolder.clicked.connect(self.open_folder)
            
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

    def open_folder(self):
        """
        Attempt to open the selected folder
        """        
        try:
            file_path = (self.ui.FileList.item(self.ui.FileList.currentRow())).text()
            self.filesystem_items(file_path)
        except Exception as e:
            print('Unable to open selected folder: ' + str(e))
            
                
    def filesystem_items(self, file_path=None):
        """
        Populate the list widget with the contents of the MPD filesystem
        
        Params
        -------
        string
            File System Path on the MPD filesystem             
        """
        mpd_filelist = self.mpd.ls_mpd_path(file_path)
        
        item_count = 0
        
        if type(mpd_filelist) is list:
            self.path_file_count = len(mpd_filelist) 
        
            self.ui.FileCount.setText('Directory Items: ' + str(self.path_file_count)) 
            self.ui.FileList.clear()
            for dir_item in mpd_filelist:
                if dir_item.get('directory', None) is not None:
                    self.ui.FileList.addItem(dir_item['directory'])
                    new_item = self.ui.FileList.item(item_count)
                    new_item.setIcon(QtGui.QIcon.fromTheme("tag-folder"))                    
                    
                if dir_item.get('file', None) is not None:
                    file_item = 'Artist: ' + dir_item.get('artist', '') + '\nSong: ' + dir_item.get('title', '') + '\nFile: ' + dir_item.get('file', '') + '\n'
                    self.ui.FileList.addItem(file_item)
                    new_item = self.ui.FileList.item(item_count)
                    new_item.setIcon(QtGui.QIcon.fromTheme("emblem-music-symbolic"))
                    
                item_count +=1

            self.ui.FileList.setCurrentRow(self.selected_file_item)
