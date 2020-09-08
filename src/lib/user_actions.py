import sys
from PyQt5 import QtWidgets, QtGui

class UserActions():
    selected_playlist_item = 0

    def __init__(self, ui, mpd):
        self.ui = ui
        self.mpd = mpd
        
        # Set the initial button state from the MPD state
        self.ui_button_state()
        
        # Register the button actions on the home page
        self.ui.MusicPlay.clicked.connect(self.music_play_press)      
        self.ui.RandomPlayback.clicked.connect(self.music_random_press)        
        self.ui.ConsumptionPlayback.clicked.connect(self.music_consume_press)     
        self.ui.UpdateDatabase.clicked.connect(self.music_update_press) 
                
        self.ui.MusicSkip.clicked.connect(self.music_skip_press)        
        self.ui.MusicStop.clicked.connect(self.music_stop_press)

        self.ui.PlaylistDetailsButton.clicked.connect(self.view_playlist_widget)        
        self.ui.QuitButton.clicked.connect(self.exit_application)
        
        # Register the button actions on the current playlist page
        self.ui.HomeButton.clicked.connect(self.view_home_widget) 
        self.ui.PlaylistUpButton.clicked.connect(self.playlist_scroll_up) 
        self.ui.PlaylistDownButton.clicked.connect(self.playlist_scroll_down)
                           
    def change_page(self, widget_id):
        """
        Change the visible widget in use
        """
        try:
            self.ui.appContent.setCurrentIndex(widget_id)
        except:
            pass

    def view_home_widget(self):
        """
        Change the visible widget to the application home view
        """
        self.change_page(0)

    def view_playlist_widget(self):
        """
        Change the visible widget to the current playlist view
        """
        self.change_page(1)
        
        mpd_status = self.mpd.get_status()
        playlist_length = mpd_status.get('playlistlength', 0)
        self.ui.PlaylistCount.setText(str(playlist_length) + " Items")
        self.playlist_items()

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
        
    def music_play_press(self):
        """
        Start playback of music
        """                
        self.mpd.play_playback()
        self.ui_button_state()
        
    def music_stop_press(self):
        """
        Stop the playback of music
        """                
        self.mpd.stop_playback()
        self.ui.MusicPlay.setChecked(False)
        self.ui_button_state() 
        self.ui.SongPlayTime.clear()
        self.ui.MPDNextPlaying.clear()
        self.ui.MPDNowPlaying.clear()
        self.ui.MPDAlbumArt.clear()          
        
    def music_skip_press(self):
        """
        Skip playback to the next song
        """     
        mpd_status = self.mpd.get_status()

        if mpd_status['state'] == 'play':
            self.mpd.next_song()
            self.ui_button_state()                 
            self.ui.MPDAlbumArt.clear()
        
    def music_random_press(self):
        """
        Enable / Disable random playback of music
        """                
        self.mpd.random_playback()
        self.ui_button_state()   
        
    def music_consume_press(self):
        """
        Enable / Disable consumption playback of music
        """                
        self.mpd.consumption_playback()
        self.ui_button_state()   
        
    def music_update_press(self):
        """
        Trigger manual update of the music library
        """                
        self.mpd.update_library()
        self.ui_button_state()           
        
    def ui_button_state(self):
        """
        Update the state of any UI buttons
        """    
        mpd_status = self.mpd.get_status()

        if mpd_status.get('state', '') == 'play':
            self.ui.MusicPlay.setChecked(True)
        else:
            self.ui.MusicPlay.setChecked(False)   
                        
        if int(mpd_status.get('random', 0)) == 1:
            self.ui.RandomPlayback.setChecked(True)
        else:
            self.ui.RandomPlayback.setChecked(False)            

        if int(mpd_status.get('consume', 0)) == 1:
            self.ui.ConsumptionPlayback.setChecked(True) 
        else:
            self.ui.ConsumptionPlayback.setChecked(False)           
 
        
        self.database_update_status(mpd_status)
    
    def database_update_status(self, mpd_status):
        """
        Update the state of database update button
        
        Parameters
        ----------
        mpd_status : dict
            Dictionary of the MPD daemons current state   
        """            
        if mpd_status.get('updating_db') is None:
            self.ui.UpdateDatabase.setChecked(False)
        else:
            self.ui.UpdateDatabase.setChecked(True) 
            
    def exit_application(self):
        """
        Close the MPD connection and close the application
        """                
        self.mpd.close_mpd()
        sys.exit(0)
