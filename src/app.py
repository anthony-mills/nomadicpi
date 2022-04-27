import sys

import os.path

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

import lib.nomadic

from ui.interface.main_window import Ui_NomadicPI


class MainWindow(QtWidgets.QMainWindow):
    update_loop = None

    # Time in milliseconds for cadence of update loop
    loop_interval = 1000

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setFixedSize(800, 490)

        # Setup the UI
        self.ui = Ui_NomadicPI()
        self.ui.base_path = os.path.dirname(os.path.abspath(__file__)) + '/'

        self.ui.setupUi(self)
        self.showFullScreen()

        self.nomadic = lib.nomadic.NomadicPi(self.ui)
        app.aboutToQuit.connect(self.exit)

        self.update_loop = QTimer(self)
        self.update_loop.setInterval(self.loop_interval)
        self.update_loop.timeout.connect(self.nomadic.update_content)
        self.update_loop.start()

    def exit(self):
        self.update_loop.stop()
        self.nomadic.exit_application()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())
