from PyQt5 import QtGui

class FileManagement():
    selected_file_item = 0
    
    icons = {
        'file' : None,
        'folder' : None
    }
    
    def __init__(self, nomadic):
        self.reset_file_state()
        self.nomadic = nomadic

        # Register the button actions fot the file management page
        self.nomadic.ui.FileReturnHome.clicked.connect(self.nomadic.view_home_widget)
        self.nomadic.ui.FileListUp.clicked.connect(self.playlist_scroll_up)
        self.nomadic.ui.FileListDown.clicked.connect(self.playlist_scroll_down)
    
        self.nomadic.ui.FileOpenFolder.clicked.connect(self.open_folder)
        self.nomadic.ui.FileParentDirectory.clicked.connect(self.open_parent_folder)
        self.nomadic.ui.FileAddToPlaylist.clicked.connect(self.add_item_to_playlist)
        
        self.nomadic.ui.FileList.itemClicked.connect(self.handle_item_click)
        self.nomadic.ui.FileList.itemDoubleClicked.connect(self.handle_item_double_click)
        
        # Set the Icon for files and directorys
        self.icons['file'] = QtGui.QIcon(QtGui.QPixmap("visual_elements/icons/music16x.png"))
        self.icons['folder'] = QtGui.QIcon(QtGui.QPixmap("visual_elements/icons/folder16x.png"))
    
    def reset_file_state(self):
        self.dir_info = {
            'contents' : [],
            'count' : 0,
            'path' : []
        }    
            
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

    def handle_item_click(self):
        """
        Execute method when a select playlist item
        """
        self.selected_file_item = self.nomadic.ui.FileList.currentRow() 
        
    def handle_item_double_click(self):
        """
        Handle doubleclick events on files actions either by opening file or adding file to playlist
        """
        self.handle_item_click()
              
        item_text = self.nomadic.ui.FileList.item(self.selected_file_item).text()

        if "File" in item_text:
            self.add_item_to_playlist()
        else:
            self.open_folder()
            
    def add_item_to_playlist(self):
        """
        Add the selected item to the playlist
        """
        if self.nomadic.ui.FileList.item is not None:    
            item_text = self.nomadic.ui.FileList.item(self.selected_file_item).text()

            if "File" in item_text:
                file_path = item_text.rsplit('File: ', 1)[-1].rstrip('\n')
                self.nomadic.mpd.add_to_playlist(file_path)
            else:
                self.nomadic.mpd.add_to_playlist(item_text)
                
            self.set_item_count()

            if self.nomadic.mpd_status['state'] == 'stop':
                self.nomadic.mpd.play_playback()
            
    def open_parent_folder(self):
        """
        Attempt to open the parent folder of the current directory
        """      
        try:           
            if len(self.dir_info['path']) > 1:
                self.dir_info['path'].pop()
                self.filesystem_items(self.dir_info['path'].pop())
            else:
                self.dir_info['path'] = []
                self.filesystem_items()
                
        except Exception as e:
            print('Unable to open selected folder: ' + str(e))
            
    def open_folder(self):
        """
        Attempt to open the selected folder
        """        
        try:
            file_path = (self.nomadic.ui.FileList.item(self.nomadic.ui.FileList.currentRow())).text()
            self.filesystem_items(file_path)
        except Exception as e:
            print('Unable to open selected folder: ' + str(e))
            
    def set_item_count(self):
        """
        Set the directory item count and the current playlist length
        """                
        try:
            mpd_playlist = self.nomadic.mpd.playlist_contents()
            
            item_text = 'Directory Items: ' + str(self.dir_info['count']) + ' / Playlist Items: ' + str(len(mpd_playlist))
            self.nomadic.ui.FileCount.setText(item_text)     
        except Exception as e:
            print(str(e))
                
    def filesystem_items(self, file_path=None):
        """
        Populate the list widget with the contents of the MPD filesystem
        
        Params
        -------
        string
            File System Path on the MPD filesystem             
        """
        try:
            mpd_filelist = self.nomadic.mpd.ls_mpd_path(file_path)
            
            if file_path is not None:
                path_unique = len(set(self.dir_info['path'])) == len(self.dir_info['path'])
                
                if path_unique:
                    self.dir_info['path'].append(file_path)
                
            item_count = 0
            
            if type(mpd_filelist) is list:
                self.dir_info['count'] = len(mpd_filelist) 
                
                self.set_item_count()
                
                self.nomadic.ui.FileList.clear()
                
                self.dir_info['contents'] = []
                
                for dir_item in mpd_filelist:
                    if dir_item.get('directory', None) is not None:
                        self.nomadic.ui.FileList.addItem(dir_item['directory'])
                        new_item = self.nomadic.ui.FileList.item(item_count)
                                                
                        self.dir_info['contents'].append({
                            'id' : item_count,
                            'value' : dir_item['directory'],
                            'type' : 'directory'
                        })                    
                        
                        if new_item is not None:                 
                            new_item.setIcon(self.icons['folder'])                          
                        
                    if dir_item.get('file', None) is not None:                   
                        file_item = '\nArtist: ' + dir_item.get('artist', '') + '\nSong: ' + dir_item.get('title', '') + '\nFile: ' + dir_item.get('file', '') + '\n'
                        self.nomadic.ui.FileList.addItem(file_item)
                        new_item = self.nomadic.ui.FileList.item(item_count)

                        self.dir_info['contents'].append({
                            'id' : item_count,
                            'value' : dir_item.get('file', ''),
                            'type' : 'directory'
                        })
                        
                        if new_item is not None:                 
                            new_item.setIcon(self.icons['file'])                                              
                        
                    item_count +=1
                    self.nomadic.ui.FileList.setCurrentRow(self.selected_file_item)
        except Exception as e:
            print(str(e))

