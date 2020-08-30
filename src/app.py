import sys
import logging
import threading
import lib.gps as gps

from PyQt5 import QtWidgets

from lib.interface.main_window import Ui_NomadicPI

import sys
logger = logging.getLogger(__name__)

class mainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mainWindow, self).__init__()

        self.ui = Ui_NomadicPI()
        self.ui.setupUi(self)
        self.ui.QuitButton.clicked.connect(self.exit_application)
        
        self.update_content()
    
    def update_content(self):
        self.update_gps()
        
        threading.Timer(1, self.update_content).start()        
        
    def update_gps(self):
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
                # Get the current GPS speed
                cur_speed = gps_info.speed()
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
        sys.exit()

if __name__ == '__main__':        
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()
    sys.exit(app.exec())
