from PyQt5 import QtGui

class FileManagement():
    selected_file_item = 0

    dir_info = {
        'contents' : None,
        'count' : 0,
        'path' : None,   
        'last_path' : None,
    }
    
    icons = {
        'file' : None,
        'folder' : None
    }
    
    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register the button actions fot the file management page
        self.nomadic.ui.FileReturnHome.clicked.connect(self.nomadic.view_home_widget)
        self.nomadic.ui.FileListUp.clicked.connect(self.playlist_scroll_up)
        self.nomadic.ui.FileListDown.clicked.connect(self.playlist_scroll_down)

        self.nomadic.ui.FileOpenFolder.clicked.connect(self.open_folder)
        
        # Set the Icon for files and directorys
        self.icons['file'] = QtGui.QIcon.fromTheme("emblem-music-symbolic")
        self.icons['folder'] = QtGui.QIcon.fromTheme("tag-folder")
        
    def playlist_scroll_up(self):
        """
        Select the playlist item above the current selection
        """
        if self.selected_file_item > 0:
            self.selected_file_item -= 1
            self.nomadic.ui.FileList.setCurrentRow(self.selected_file_item)

    def playlist_scroll_down(self):
        """
        Select the playlist item below the current selection
        """
        if int(self.selected_file_item) < int(self.dir_info['count']):
            self.selected_file_item += 1
            self.nomadic.ui.FileList.setCurrentRow(self.selected_file_item)

    def open_folder(self):
        """
        Attempt to open the selected folder
        """        
        try:
            file_path = (self.nomadic.ui.FileList.item(self.nomadic.ui.FileList.currentRow())).text()
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
        mpd_filelist = self.nomadic.mpd.ls_mpd_path(file_path)
        
        
        item_count = 0
        
        if type(mpd_filelist) is list:
            self.dir_info['count'] = len(mpd_filelist) 
        
            self.nomadic.ui.FileCount.setText('Directory Items: ' + str(self.dir_info['count'])) 
            self.nomadic.ui.FileList.clear()
            for dir_item in mpd_filelist:
                if dir_item.get('directory', None) is not None:
                    self.nomadic.ui.FileList.addItem(dir_item['directory'])
                    new_item = self.nomadic.ui.FileList.item(item_count)
                    new_item.setIcon(self.icons['folder'])                    
                    
                if dir_item.get('file', None) is not None:
                    file_item = 'Artist: ' + dir_item.get('artist', '') + '\nSong: ' + dir_item.get('title', '') + '\nFile: ' + dir_item.get('file', '') + '\n'
                    self.nomadic.ui.FileList.addItem(file_item)
                    new_item = self.nomadic.ui.FileList.item(item_count)
                    new_item.setIcon(self.icons['file'])
                    
                item_count +=1
                self.nomadic.ui.FileList.setCurrentRow(self.selected_file_item)
