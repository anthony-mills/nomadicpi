import sys

class UserActions():

    def __init__(self, ui, mpd):
        self.ui = ui
        self.mpd = mpd
        
        # Set the initial button state from the MPD state
        self.ui_button_state()
        
        # Register the button actions
        self.ui.QuitButton.clicked.connect(self.exit_application)  
        self.ui.MusicPlay.clicked.connect(self.music_play_press)      
        self.ui.RandomPlayback.clicked.connect(self.music_random_press)
        self.ui.ConsumptionPlayback.clicked.connect(self.music_consume_press)
        self.ui.UpdateDatabase.clicked.connect(self.music_update_press) 
        
    def music_play_press(self):
        """
        Start playback of music
        """                
        self.mpd.play_playback()
        self.ui_button_state()
        
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

        if mpd_status['state'] == 'play':
            self.ui.MusicPlay.setText("Pause")
        else:
            self.ui.MusicPlay.setText("Play")     
                        
        if int(mpd_status['random']) == 0:
            self.ui.RandomPlayback.setText("Enable Random Playback")
        else:
            self.ui.RandomPlayback.setText("Disable Random Playback")            

        if int(mpd_status['consume']) == 0:
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
