import sys
import os.path

import lib.nomadic as nomadic_pi

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui

from ui.interface.main_window import Ui_NomadicPI

class mainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mainWindow, self).__init__()
        
        self.setFixedSize(800, 490) 

        # Setup the UI
        self.ui = Ui_NomadicPI()
        self.ui.base_path = os.path.dirname(os.path.abspath(__file__)) + '/'

        print(self.ui.base_path)
        
        self.ui.setupUi(self)
        self.showFullScreen()
        
        self.nomadic = nomadic_pi.NomadicPi(self.ui)
        #self.showMaximized() 
        app.aboutToQuit.connect(self.nomadic.exit_application)
                
if __name__ == '__main__':        
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()
    sys.exit(app.exec())
