import sys
import logging
import threading
import lib.gps as gps
import lib.mpd as mpd

from PyQt5 import QtWidgets

from lib.interface.main_window import Ui_NomadicPI

import sys
logger = logging.getLogger(__name__)

class mainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mainWindow, self).__init__()

        # Connect to the MPD daemon
        self.mpd = mpd.MpdLib()
        self.mpd.connect_mpd()
        
        # Setup the UI
        self.ui = Ui_NomadicPI()
        self.ui.setupUi(self)
        
        self.ui.QuitButton.clicked.connect(self.exit_application)  
        self.ui.MusicPlay.clicked.connect(self.mpd.play_playback)      
        self.ui.RandomPlayback.clicked.connect(self.mpd.random_playback)
        self.ui.ConsumptionPlayback.clicked.connect(self.mpd.consumption_playback)
        self.ui.UpdateDatabase.clicked.connect(self.mpd.update_library)        
                
        self.update_content()
    
    def update_content(self):
        """
        Create a timer and periodically update the UI information
        """              
        self.update_gps()
        self.update_mpd()
        
        threading.Timer(0.3, self.update_content).start()  
        
    def update_mpd(self):
        mpdStatus = self.mpd.get_status()

        if mpdStatus.get('updating_db') is None:
            self.ui.UpdateDatabase.setText( "Update Database" )
        else:
            self.ui.UpdateDatabase.setText( "Database Updating..." )   

        if mpdStatus['state'] == 'play':
            self.ui.MusicPlay.setText( "Pause" )
        else:
            self.ui.MusicPlay.setText( "Play" )     
                        
        if int(mpdStatus['random']) == 0:
            self.ui.RandomPlayback.setText( "Enable Random Playback" )
        else:
            self.ui.RandomPlayback.setText( "Disable Random Playback" )            

        if int(mpdStatus['consume']) == 0:
            self.ui.ConsumptionPlayback.setText( "Enable Consumption Playback" )
        else:
            self.ui.ConsumptionPlayback.setText( "Disable Consumption Playback" )            
        
        
    def update_gps(self):
        """
        Get the current GPS information and update the UI
        """                
        gps_info = None
        
        if gps.gpsd_socket is None:
            try:
                gps.gps_connect(host=gps.gps_host, port=gps.gps_port)
            except: 
                print("Unable to connect to GPSD service at: " + str(gps.gps_host) + ":" + str(gps.gps_port))
        try:
            gps_info = gps.get_current()
        
        except Exception as e:
            print("Error: " + str(e))
        
        if gps_info is not None:    
            try:
                # Get the current GPS speed and convert from m/s to km/h
                cur_speed = int(3.6 * gps_info.speed() )
                self.ui.CurrentSpeed.setText( str(cur_speed) )            
                
                # Get the current Altitude
                cur_alt = gps_info.altitude()
                self.ui.CurrentAltitude.setText( "Altitude: " + str(cur_alt) + "m" )
                
                # Display the time in UTC and the Local timezone
                local_time = gps_info.get_time(local_time=True)
                utc_time = gps_info.get_time()
                cur_time = "Local Time: " + str(local_time) + "\n" + "UTC: " + str(utc_time)
                self.ui.TimeInfo.setText( cur_time )
                            
                cur_pos = gps_info.position()
                
                if len(cur_pos) == 2:
                    self.ui.CurrentPosition.setText("Current Position:\n" + str(cur_pos[0]) + ", " + str(cur_pos[1]))
                        
            except Exception as e:
                print(e)
        
    def exit_application():
        self.mpd.close_mpd()
        sys.exit()

if __name__ == '__main__':        
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()
    sys.exit(app.exec())
