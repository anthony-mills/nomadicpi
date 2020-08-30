import sys
import logging
import threading
import lib.gps as gps
import humanize

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
        if gps.gpsd_socket is None:
            try:
                gps.gps_connect(host=gps.gps_host, port=gps.gps_port)
            except: 
                print("Unable to connect to GPSD service at: " + str(gps.gps_host) + ":" + str(gps.gps_port))
        try:
            gps_info = gps.get_current()
            
            cur_speed = gps_info.speed()

            self.ui.CurrentSpeed.setText( str(cur_speed) )
            
            curtime = "Local Time: " + str(gps_info.get_time(local_time=True)) + "\n" \
                        + "UTC: " + str(gps_info.get_time())
            
            self.ui.LocalTime.setText( curtime )
            self.ui.UtcTime.setText( 'UTC: ' + str(gps_info.get_time(local_time=True)) )
                        
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
