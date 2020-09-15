import sys
import os.path
import configparser
import logging
import threading

import lib.gps as gps
import lib.mpd as mpd
import lib.application_home as application_home
import lib.playlist_management as playlist_management
import lib.file_management as file_management

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap, QMovie

logger = logging.getLogger(__name__)

class NomadicPi():
    pages = {
        'home' : 0,
        'playlist' : 1,
        'network' : 2,
        'files' : 3,
        'location' : 4        
    }
    
    # Folder for album art
    art_cache = '/tmp'
    
    # Desired date / time format
    dt_format = "%A %d %B %Y %-I:%M %p"
    
    # Track the GPS state with this variable
    gps_info = None

    def __init__(self, ui):
        self.ui = ui
        self.app_config = configparser.ConfigParser()
        self.app_config.read('config.ini')
        self.now_playing = 0;
        
        # Connect to the MPD daemon
        self.connect_mpd()
        self.get_mpd_status()
        
        # Setup the handlers for user actions on the application home
        self.application_home = application_home.UserActions(self)
        self.application_home.ui_button_state()        

        # Setup the handlers for user actions on the playlist page
        self.current_playlist = playlist_management.PlaylistManagement(self)  
        
        # Setup the handlers for user actions on the file management page
        self.mpd_files = file_management.FileManagement(self)          
        
        self.ui.appContent.setCurrentIndex(self.pages['home'])      
        self.ui.appContent.currentChanged.connect(self.application_page_changed) 
                
        self.update_content()          
        
    def application_page_changed(self):
        """
        Call any methods that need to happen at page change
        """
        try:
            self.current_playlist.update_playlist_contents()
            self.application_home.update_playlist_count()
            self.mpd_files.reset_file_state()
            self.mpd_files.filesystem_items()
        except Exception as e:
            pass                    

    def view_home_widget(self):
        """
        Change the visible widget to the application home view
        """
        try:
            self.ui.appContent.setCurrentIndex(self.pages['home'])
        except Exception as e:
            print(e)

    def get_mpd_status(self):
        """
        Get and store the state of the MPD daemon
        """
        try:
            self.mpd_status = self.mpd.get_status() 
            
            return self.mpd_status
        except Exception as e:
            pass   
                
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
    
    def update_content(self):
        """
        Create a timer and periodically update the UI information
        """ 
        self.get_mpd_status()    
            
        self.update_mpd()
        
        # Update GPS related information 
        self.update_gps()
        
        self.update_loop = threading.Timer(1, self.update_content)
        self.update_loop.start()
        
    def update_mpd(self):
        """
        Update the interface with any time sensitive MPD info i.e play time etc 
        """                    
        self.application_home.database_update_status(self.mpd_status)

        if self.mpd_status.get('state', '') == 'play':
            song_data = self.mpd.currently_playing()
                
            if int(self.now_playing)!=int(self.mpd_status['songid']):
                self.now_playing = song_data.get('id', 0)  
                          
                song_info = 'Playing: ' + song_data.get('artist', 'Unknown') + '\n ' + song_data.get('title', 'Unknown');

                self.ui.MPDNowPlaying.setText(song_info)
                
                self.set_album_art(song_data)
                
                next_song = self.mpd_status.get('nextsong', None)
                if next_song is not None:
                    try:
                        next_up = self.mpd.playlist_info(next_song)
                        
                        if len(next_up) == 1:
                            next_song = next_up[0]
                            song_info = 'Next: ' + next_song.get('artist', 'Unknown') + '\n ' + next_song.get('title', 'Unknown');
                            self.ui.MPDNextPlaying.setText(song_info)                            
                    except:
                        pass
 
                self.application_home.update_playlist_count()
                                       
            if self.ui.MPDAlbumArt.pixmap() is None:
                self.set_album_art(song_data)
                                                       
            m, s = divmod(round(float(self.mpd_status.get('elapsed', 0))), 60) 
            song_elapsed = "%02d:%02d" % (m, s)   
            
            m, s = divmod(round(float(self.mpd_status.get('duration', 0))), 60) 
            song_duration = "%02d:%02d" % (m, s)               
            
            self.ui.SongPlayTime.setText(str(song_elapsed) + ' / ' + str(song_duration))
        
        if self.mpd_status.get('state', '') == 'stop':
            self.now_playing = 0            
    
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
            try:
                self.gps_info = gps.get_current()
            except Exception as e:
                pass            
            
            if self.gps_info is not None:    
                try:
                    # Get the current GPS speed and convert from m/s to km/h
                    cur_speed = int(3.6 * self.gps_info.speed() )
                    self.ui.CurrentSpeed.setText( str(cur_speed) )            
                    
                except Exception as e:
                    print(e)
                    
                try:            
                    # Get the current Altitude
                    
                    heading = self.gps_info.movement()
                    
                    track = round(heading['track'])
                    
                    heading_info = 'Altitude: ' + str(heading['altitude']) + \
                                'm\nHeading: ' + str(track) + \
                                ' degrees ' + heading['direction']
                    
                    self.ui.CurrentAltitude.setText( heading_info )
                except Exception as e:
                    self.ui.CurrentAltitude.setText( 'Altitude: 3D GPS fix needed.' )
                    print(e)
                           
                try:                             
                    cur_pos = self.gps_info.position()
                    
                    if len(cur_pos) == 2:
                        self.ui.CurrentPosition.setText('Current Position:\n' + str(cur_pos[0]) + ', ' + str(cur_pos[1]))
                except Exception as e:
                    self.ui.CurrentPosition.setText('Current Position: No GPS fix.')

                    
    def exit_application(self):
        """
        Close the MPD connection and close the application
        """
        self.update_loop.cancel()
        self.mpd.close_mpd()
        sys.exit(0)                    
