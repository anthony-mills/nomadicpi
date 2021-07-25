import sys
import os.path

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import lib.nomadic

from ui.interface.main_window import Ui_NomadicPI

class mainWindow(QtWidgets.QMainWindow):
    update_loop = None

    def __init__(self):
        super(mainWindow, self).__init__()

        self.setFixedSize(800, 490)

        # Setup the UI
        self.ui = Ui_NomadicPI()
        self.ui.base_path = os.path.dirname(os.path.abspath(__file__)) + '/'

        self.ui.setupUi(self)
        self.showFullScreen()

        self.nomadic = lib.nomadic.NomadicPi(self.ui)
        #self.showMaximized()
        app.aboutToQuit.connect(self.exit)

        self.update_loop = QTimer(self)
        self.update_loop.setInterval(1000)          # Throw event timeout with an interval of 1000 milliseconds
        self.update_loop.timeout.connect(self.nomadic.update_content)
        self.update_loop.start()

    def exit(self):
        self.update_loop.stop()
        self.nomadic.exit_application

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mainWindow()
    application.show()
    sys.exit(app.exec())
