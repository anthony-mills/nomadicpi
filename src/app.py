import sys
import os.path
import configparser
import logging
import threading
import lib.gps as gps
import lib.mpd as mpd
import lib.user_actions as user_actions

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QMovie

from lib.interface.main_window import Ui_NomadicPI

import sys
logger = logging.getLogger(__name__)

class mainWindow(QtWidgets.QMainWindow):
    
    # Folder for album art
    art_cache = '/tmp'
    
    # Desired date / time format
    dt_format = "%A %d %B %Y %-I:%M %p"
    
    # Track the GPS state with this variable
    gps_info = None

    def __init__(self):
        super(mainWindow, self).__init__()
        
        self.app_config = configparser.ConfigParser()
        self.app_config.read('config.ini')
        self.now_playing = 0;
        
        # Connect to the MPD daemon
        self.connect_mpd()
        
        # Setup the UI
        self.ui = Ui_NomadicPI()
        self.ui.setupUi(self)
        
        # Setup the handlers for user actions
        self.user_actions = user_actions.UserActions(self.ui, self.mpd)
        self.user_actions.ui_button_state()        
        self.update_content()
    
    def connect_mpd(self):
        """
        Connect to the MPD daemon
        """         
        self.mpd = mpd.MpdLib()
        self.art_cache = self.app_config['mpd'].get('AlbumArt', '/tmp/')     
        self.mpd.set_mpd_host(self.app_config['mpd'].get('Host', 'localhost'))
        self.mpd.set_mpd_port(self.app_config['mpd'].get('Port', '6000'))         
        self.mpd.set_art_cache(self.art_cache)   

        self.mpd.connect_mpd()
        self.mpd_status = {}            
    
    def update_content(self):
        """
        Create a timer and periodically update the UI information
        """ 
        self.mpd_status = self.mpd.get_status()    
            
        self.update_mpd()
        
        # Update GPS related information 
        self.update_gps()
        
        threading.Timer(1, self.update_content).start()  
        
    def update_mpd(self):
        """
        Update the interface with any time sensitive MPD info i.e play time etc 
        """                    
        self.user_actions.database_update_status(self.mpd_status)
        
        if self.mpd_status.get('state', '') == 'play':
            if int(self.now_playing)!=int(self.mpd_status['songid']):
                song_data = self.mpd.currently_playing()
                self.now_playing = song_data.get('id', 0)  
                          
                song_info = song_data.get('title', 'Unknown') + '\n ' + song_data.get('artist', 'Unknown');
                self.ui.MPDNowPlaying.setText(song_info)
                
                self.set_album_art(song_data)
            
            m, s = divmod(round(float(self.mpd_status.get('elapsed', 0))), 60) 
            song_elapsed = "%02d:%02d" % (m, s)   
            
            m, s = divmod(round(float(self.mpd_status.get('duration', 0))), 60) 
            song_duration = "%02d:%02d" % (m, s)               
            
            self.ui.SongPlayTime.setText(str(song_elapsed) + ' / ' + str(song_duration))
        
        if self.mpd_status.get('state', '') == 'stop':            
            self.ui.MPDNowPlaying.setText('Playing: N/A')
            self.ui.MPDAlbumArt.clear()
    
    def set_album_art(self, song_data):
        """
        Update the album art displayed in the UI 
        """                  
        search_term = song_data.get('album', '') + ' - ' + song_data.get('artist', '')
        cache_key = (''.join(ch for ch in search_term if ch.isalnum())).lower()
        song_thumb = self.mpd.album_art(search_term, cache_key)

        if type(song_thumb) is str:

            song_img = QPixmap(song_thumb)
            self.ui.MPDAlbumArt.setPixmap(song_img)
        
    def update_gps(self):
        """
        Get the current GPS information and update the UI
        """                
        if gps.gpsd_socket is None:
            try:
                gpsd_host = self.app_config['gpsd'].get('Host', 'localhost')
                gpsd_port = int(self.app_config['gpsd'].get('Port', '2947'))
                
                gps.gps_connect(host=gpsd_host, port=gpsd_port)
            except Exception as e:
                print(str(e))
                print('Unable to connect to GPSD service at: ' + str(gpsd_host) + ':' + str(gpsd_port))
                self.ui.CurrentPosition.setText('Current Position: No GPS Fix')
                self.ui.CurrentAltitude.setText('Altitude: Unknown')
        else:
            self.gps_info = gps.get_current()
            
            if self.gps_info is not None:    
                try:
                    # Get the current GPS speed and convert from m/s to km/h
                    cur_speed = int(3.6 * self.gps_info.speed() )
                    self.ui.CurrentSpeed.setText( str(cur_speed) )            
                    
                except Exception as e:
                    print(e)
                    
                try:            
                    # Get the current Altitude
                    cur_alt = self.gps_info.altitude()
                    self.ui.CurrentAltitude.setText( 'Altitude: ' + str(cur_alt) + 'm' )
                except Exception as e:
                    self.ui.CurrentAltitude.setText( 'Altitude: 3D GPS fix needed.' )
                    print(e)
                           
                try:                             
                    cur_pos = self.gps_info.position()
                    
                    if len(cur_pos) == 2:
                        self.ui.CurrentPosition.setText('Current Position:\n' + str(cur_pos[0]) + ', ' + str(cur_pos[1]))
                except Exception as e:
                    self.ui.CurrentPosition.setText('Current Position: No GPS fix.')

                try:                             
                    cur_time = self.gps_info.get_time(True)
                    self.setWindowTitle(self.app_config['app'].get('AppName', '') + ' - ' + cur_time.strftime(self.dt_format)) 
                except Exception as e:
                    print(e)
                

if __name__ == '__main__':        
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()
    sys.exit(app.exec())
