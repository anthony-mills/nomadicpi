# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visual_elements/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NomadicPI(object):
    def setupUi(self, NomadicPI):
        NomadicPI.setObjectName("NomadicPI")
        NomadicPI.setWindowModality(QtCore.Qt.ApplicationModal)
        NomadicPI.resize(800, 480)
        self.appContent = QtWidgets.QStackedWidget(NomadicPI)
        self.appContent.setGeometry(QtCore.QRect(0, 0, 800, 490))
        self.appContent.setObjectName("appContent")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.MusicSkip = QtWidgets.QPushButton(self.page)
        self.MusicSkip.setGeometry(QtCore.QRect(580, 10, 101, 86))
        self.MusicSkip.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("visual_elements/icons/forward_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MusicSkip.setIcon(icon)
        self.MusicSkip.setIconSize(QtCore.QSize(80, 80))
        self.MusicSkip.setObjectName("MusicSkip")
        self.MusicStop = QtWidgets.QPushButton(self.page)
        self.MusicStop.setGeometry(QtCore.QRect(340, 10, 111, 86))
        self.MusicStop.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("visual_elements/icons/stop_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MusicStop.setIcon(icon1)
        self.MusicStop.setIconSize(QtCore.QSize(80, 80))
        self.MusicStop.setObjectName("MusicStop")
        self.ConsumptionPlayback = QtWidgets.QPushButton(self.page)
        self.ConsumptionPlayback.setGeometry(QtCore.QRect(460, 390, 111, 86))
        self.ConsumptionPlayback.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("visual_elements/icons/consumption_play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ConsumptionPlayback.setIcon(icon2)
        self.ConsumptionPlayback.setIconSize(QtCore.QSize(80, 80))
        self.ConsumptionPlayback.setCheckable(True)
        self.ConsumptionPlayback.setObjectName("ConsumptionPlayback")
        self.UpdateDatabase = QtWidgets.QPushButton(self.page)
        self.UpdateDatabase.setGeometry(QtCore.QRect(340, 390, 111, 86))
        self.UpdateDatabase.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("visual_elements/icons/update_db_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap("visual_elements/icons/not_available_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.UpdateDatabase.setIcon(icon3)
        self.UpdateDatabase.setIconSize(QtCore.QSize(80, 80))
        self.UpdateDatabase.setCheckable(True)
        self.UpdateDatabase.setObjectName("UpdateDatabase")
        self.MPDAlbumArt = QtWidgets.QLabel(self.page)
        self.MPDAlbumArt.setGeometry(QtCore.QRect(350, 110, 331, 250))
        self.MPDAlbumArt.setToolTip("")
        self.MPDAlbumArt.setText("")
        self.MPDAlbumArt.setAlignment(QtCore.Qt.AlignCenter)
        self.MPDAlbumArt.setObjectName("MPDAlbumArt")
        self.FindButton = QtWidgets.QPushButton(self.page)
        self.FindButton.setGeometry(QtCore.QRect(690, 105, 101, 86))
        self.FindButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("visual_elements/icons/find_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FindButton.setIcon(icon4)
        self.FindButton.setIconSize(QtCore.QSize(80, 80))
        self.FindButton.setObjectName("FindButton")
        self.MusicPlay = QtWidgets.QPushButton(self.page)
        self.MusicPlay.setGeometry(QtCore.QRect(460, 10, 111, 86))
        self.MusicPlay.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("visual_elements/icons/play_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap("visual_elements/icons/pause_button.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.MusicPlay.setIcon(icon5)
        self.MusicPlay.setIconSize(QtCore.QSize(80, 80))
        self.MusicPlay.setCheckable(True)
        self.MusicPlay.setObjectName("MusicPlay")
        self.LocationButton = QtWidgets.QPushButton(self.page)
        self.LocationButton.setGeometry(QtCore.QRect(690, 295, 101, 86))
        self.LocationButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("visual_elements/icons/map_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LocationButton.setIcon(icon6)
        self.LocationButton.setIconSize(QtCore.QSize(80, 80))
        self.LocationButton.setObjectName("LocationButton")
        self.NetworkButton = QtWidgets.QPushButton(self.page)
        self.NetworkButton.setGeometry(QtCore.QRect(690, 200, 101, 86))
        self.NetworkButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("visual_elements/icons/wifi_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.NetworkButton.setIcon(icon7)
        self.NetworkButton.setIconSize(QtCore.QSize(80, 80))
        self.NetworkButton.setObjectName("NetworkButton")
        self.QuitButton = QtWidgets.QPushButton(self.page)
        self.QuitButton.setGeometry(QtCore.QRect(690, 390, 101, 86))
        self.QuitButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("visual_elements/icons/quit_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QuitButton.setIcon(icon8)
        self.QuitButton.setIconSize(QtCore.QSize(80, 80))
        self.QuitButton.setObjectName("QuitButton")
        self.RandomPlayback = QtWidgets.QPushButton(self.page)
        self.RandomPlayback.setGeometry(QtCore.QRect(580, 390, 101, 86))
        self.RandomPlayback.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("visual_elements/icons/random_play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RandomPlayback.setIcon(icon9)
        self.RandomPlayback.setIconSize(QtCore.QSize(80, 80))
        self.RandomPlayback.setCheckable(True)
        self.RandomPlayback.setObjectName("RandomPlayback")
        self.MPDNextPlaying = QtWidgets.QLabel(self.page)
        self.MPDNextPlaying.setGeometry(QtCore.QRect(10, 200, 321, 71))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.MPDNextPlaying.setFont(font)
        self.MPDNextPlaying.setText("")
        self.MPDNextPlaying.setAlignment(QtCore.Qt.AlignCenter)
        self.MPDNextPlaying.setWordWrap(True)
        self.MPDNextPlaying.setObjectName("MPDNextPlaying")
        self.MPDNowPlaying = QtWidgets.QLabel(self.page)
        self.MPDNowPlaying.setGeometry(QtCore.QRect(10, 120, 321, 71))
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(11)
        self.MPDNowPlaying.setFont(font)
        self.MPDNowPlaying.setText("")
        self.MPDNowPlaying.setAlignment(QtCore.Qt.AlignCenter)
        self.MPDNowPlaying.setWordWrap(True)
        self.MPDNowPlaying.setObjectName("MPDNowPlaying")
        self.CurrentPosition = QtWidgets.QLabel(self.page)
        self.CurrentPosition.setGeometry(QtCore.QRect(10, 400, 319, 29))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.CurrentPosition.setFont(font)
        self.CurrentPosition.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentPosition.setObjectName("CurrentPosition")
        self.CurrentAltitude = QtWidgets.QLabel(self.page)
        self.CurrentAltitude.setGeometry(QtCore.QRect(10, 440, 319, 29))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.CurrentAltitude.setFont(font)
        self.CurrentAltitude.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentAltitude.setObjectName("CurrentAltitude")
        self.CurrentSpeed = QtWidgets.QLabel(self.page)
        self.CurrentSpeed.setGeometry(QtCore.QRect(10, 0, 191, 92))
        font = QtGui.QFont()
        font.setFamily("Open Sans Extrabold")
        font.setPointSize(50)
        font.setBold(True)
        font.setWeight(75)
        self.CurrentSpeed.setFont(font)
        self.CurrentSpeed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CurrentSpeed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.CurrentSpeed.setObjectName("CurrentSpeed")
        self.MPDPlaylistInfo = QtWidgets.QLabel(self.page)
        self.MPDPlaylistInfo.setGeometry(QtCore.QRect(10, 360, 321, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.MPDPlaylistInfo.setFont(font)
        self.MPDPlaylistInfo.setText("")
        self.MPDPlaylistInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.MPDPlaylistInfo.setWordWrap(True)
        self.MPDPlaylistInfo.setObjectName("MPDPlaylistInfo")
        self.SongPlayTime = QtWidgets.QLabel(self.page)
        self.SongPlayTime.setGeometry(QtCore.QRect(340, 366, 341, 20))
        self.SongPlayTime.setText("")
        self.SongPlayTime.setAlignment(QtCore.Qt.AlignCenter)
        self.SongPlayTime.setObjectName("SongPlayTime")
        self.PlaylistDetailsButton = QtWidgets.QPushButton(self.page)
        self.PlaylistDetailsButton.setGeometry(QtCore.QRect(690, 10, 101, 86))
        self.PlaylistDetailsButton.setText("")
        self.PlaylistDetailsButton.setIcon(icon3)
        self.PlaylistDetailsButton.setIconSize(QtCore.QSize(80, 80))
        self.PlaylistDetailsButton.setCheckable(True)
        self.PlaylistDetailsButton.setObjectName("PlaylistDetailsButton")
        self.CurrentSpeed_2 = QtWidgets.QLabel(self.page)
        self.CurrentSpeed_2.setGeometry(QtCore.QRect(210, 0, 120, 92))
        font = QtGui.QFont()
        font.setFamily("Open Sans Extrabold")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.CurrentSpeed_2.setFont(font)
        self.CurrentSpeed_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CurrentSpeed_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.CurrentSpeed_2.setObjectName("CurrentSpeed_2")
        self.FindButton.raise_()
        self.QuitButton.raise_()
        self.MPDNowPlaying.raise_()
        self.MusicPlay.raise_()
        self.CurrentAltitude.raise_()
        self.MPDNextPlaying.raise_()
        self.CurrentSpeed.raise_()
        self.UpdateDatabase.raise_()
        self.LocationButton.raise_()
        self.MPDAlbumArt.raise_()
        self.CurrentPosition.raise_()
        self.MusicSkip.raise_()
        self.MusicStop.raise_()
        self.NetworkButton.raise_()
        self.RandomPlayback.raise_()
        self.ConsumptionPlayback.raise_()
        self.MPDPlaylistInfo.raise_()
        self.SongPlayTime.raise_()
        self.PlaylistDetailsButton.raise_()
        self.CurrentSpeed_2.raise_()
        self.appContent.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.appContent.addWidget(self.page_2)

        self.retranslateUi(NomadicPI)
        self.appContent.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(NomadicPI)

    def retranslateUi(self, NomadicPI):
        _translate = QtCore.QCoreApplication.translate
        NomadicPI.setWindowTitle(_translate("NomadicPI", "NomadicPi"))
        self.MusicSkip.setToolTip(_translate("NomadicPI", "Skip Song"))
        self.MusicStop.setToolTip(_translate("NomadicPI", "Stop Music Playback"))
        self.ConsumptionPlayback.setToolTip(_translate("NomadicPI", "Enable / Disable Consumption Playback"))
        self.UpdateDatabase.setToolTip(_translate("NomadicPI", "Update Music Store"))
        self.FindButton.setToolTip(_translate("NomadicPI", "Browse Music Collection"))
        self.MusicPlay.setToolTip(_translate("NomadicPI", "Play / Pause Music"))
        self.LocationButton.setToolTip(_translate("NomadicPI", "Location Information"))
        self.NetworkButton.setToolTip(_translate("NomadicPI", "Network Status"))
        self.QuitButton.setToolTip(_translate("NomadicPI", "Exit Application"))
        self.RandomPlayback.setToolTip(_translate("NomadicPI", "Enable / Disable Random Playback"))
        self.CurrentPosition.setText(_translate("NomadicPI", "Current Position: No GPS fix."))
        self.CurrentAltitude.setText(_translate("NomadicPI", "Current Altitude: No GPS fix."))
        self.CurrentSpeed.setText(_translate("NomadicPI", "0"))
        self.PlaylistDetailsButton.setToolTip(_translate("NomadicPI", "Update Music Store"))
        self.CurrentSpeed_2.setText(_translate("NomadicPI", "KM/H"))
