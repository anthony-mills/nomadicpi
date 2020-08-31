import sys
import logging
import threading
import lib.gps as gps
import lib.mpd as mpd
import lib.user_actions as user_actions

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
        self.mpd_status = {}
        
        # Setup the UI
        self.ui = Ui_NomadicPI()
        self.ui.setupUi(self)
        
        # Setup the handlers for user actions
        self.user_actions = user_actions.UserActions(self.ui, self.mpd)
                
        self.update_content()
        
    def update_content(self):
        """
        Create a timer and periodically update the UI information
        """ 
        self.mpd_status = self.mpd.get_status()    
                     
        self.update_gps()
        self.update_mpd()
        
        threading.Timer(1, self.update_content).start()  
        
    def update_mpd(self):
        """
        Update the interface with any time sensitive MPD info i.e play time etc 
        """                    
        self.user_actions.database_update_status(self.mpd_status)
        
    def update_gps(self):
        """
        Get the current GPS information and update the UI
        """                
        gps_info = None
        
        if gps.gpsd_socket is None:
            try:
                gps.gps_connect(host=gps.gps_host, port=gps.gps_port)
                gps_info = gps.get_current()
            except: 
                print("Unable to connect to GPSD service at: " + str(gps.gps_host) + ":" + str(gps.gps_port))
                self.ui.CurrentPosition.setText("Current Position: No GPS Fix")
                self.ui.CurrentAltitude.setText("Altitude: Unknown")
                self.ui.TimeInfo.setText("Local Time: GPS provided time unavailable")

        
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

if __name__ == '__main__':        
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()
    sys.exit(app.exec())
