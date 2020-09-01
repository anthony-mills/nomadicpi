import sys
from PyQt5 import QtWidgets, QtGui

class UserActions():

    def __init__(self, ui, mpd):
        self.ui = ui
        self.mpd = mpd
        
        # Set the initial button state from the MPD state
        self.ui_button_state()
        
        # Register the button actions
        self.ui.MusicPlay.setCheckable(True)        
        self.ui.MusicPlay.clicked.connect(self.music_play_press)      

        self.ui.RandomPlayback.setCheckable(True)
        self.ui.RandomPlayback.clicked.connect(self.music_random_press)

        self.ui.MusicSkip.clicked.connect(self.music_skip_press)        
        self.ui.MusicStop.clicked.connect(self.music_stop_press)
                
        self.ui.ConsumptionPlayback.clicked.connect(self.music_consume_press)
        self.ui.UpdateDatabase.clicked.connect(self.music_update_press) 
        self.ui.QuitButton.clicked.connect(self.exit_application)  
                
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
                        
        if mpd_status.get('random', 0) == 0:
            self.ui.RandomPlayback.setChecked(False)
        else:
            self.ui.RandomPlayback.setChecked(True)            

        if mpd_status.get('consume', 0) == 0:
            self.ui.ConsumptionPlayback.setText("Enable Consumption Playback")
        else:
            self.ui.ConsumptionPlayback.setText("Disable Consumption Playback")  
        
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
            self.ui.UpdateDatabase.setText("Update Database")
        else:
            self.ui.UpdateDatabase.setText("Database Updating...")   
            
    def exit_application(self):
        """
        Close the MPD connection and close the application
        """                
        self.mpd.close_mpd()
        sys.exit()
