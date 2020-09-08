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
        icon = QtGui.QIcon.fromTheme("audio-headphones")
        NomadicPI.setWindowIcon(icon)
        self.appContent = QtWidgets.QStackedWidget(NomadicPI)
        self.appContent.setGeometry(QtCore.QRect(0, 0, 800, 490))
        self.appContent.setObjectName("appContent")
        self.home = QtWidgets.QWidget()
        self.home.setObjectName("home")
        self.MusicSkip = QtWidgets.QPushButton(self.home)
        self.MusicSkip.setGeometry(QtCore.QRect(580, 5, 101, 86))
        self.MusicSkip.setText("")
        icon = QtGui.QIcon.fromTheme("media-skip-forward")
        self.MusicSkip.setIcon(icon)
        self.MusicSkip.setIconSize(QtCore.QSize(80, 80))
        self.MusicSkip.setObjectName("MusicSkip")
        self.MusicStop = QtWidgets.QPushButton(self.home)
        self.MusicStop.setGeometry(QtCore.QRect(340, 5, 111, 86))
        self.MusicStop.setText("")
        icon = QtGui.QIcon.fromTheme("media-playback-stop")
        self.MusicStop.setIcon(icon)
        self.MusicStop.setIconSize(QtCore.QSize(80, 80))
        self.MusicStop.setObjectName("MusicStop")
        self.ConsumptionPlayback = QtWidgets.QPushButton(self.home)
        self.ConsumptionPlayback.setGeometry(QtCore.QRect(460, 390, 111, 86))
        self.ConsumptionPlayback.setText("")
        icon = QtGui.QIcon.fromTheme("media-playlist-repeat")
        self.ConsumptionPlayback.setIcon(icon)
        self.ConsumptionPlayback.setIconSize(QtCore.QSize(80, 80))
        self.ConsumptionPlayback.setCheckable(True)
        self.ConsumptionPlayback.setObjectName("ConsumptionPlayback")
        self.UpdateDatabase = QtWidgets.QPushButton(self.home)
        self.UpdateDatabase.setGeometry(QtCore.QRect(340, 390, 111, 86))
        self.UpdateDatabase.setText("")
        icon = QtGui.QIcon.fromTheme("view-refresh")
        self.UpdateDatabase.setIcon(icon)
        self.UpdateDatabase.setIconSize(QtCore.QSize(80, 80))
        self.UpdateDatabase.setCheckable(True)
        self.UpdateDatabase.setObjectName("UpdateDatabase")
        self.MPDAlbumArt = QtWidgets.QLabel(self.home)
        self.MPDAlbumArt.setGeometry(QtCore.QRect(350, 110, 331, 250))
        self.MPDAlbumArt.setToolTip("")
        self.MPDAlbumArt.setText("")
        self.MPDAlbumArt.setAlignment(QtCore.Qt.AlignCenter)
        self.MPDAlbumArt.setObjectName("MPDAlbumArt")
        self.CollectionButton = QtWidgets.QPushButton(self.home)
        self.CollectionButton.setGeometry(QtCore.QRect(690, 100, 101, 86))
        self.CollectionButton.setText("")
        icon = QtGui.QIcon.fromTheme("tools-media-optical-copy")
        self.CollectionButton.setIcon(icon)
        self.CollectionButton.setIconSize(QtCore.QSize(80, 80))
        self.CollectionButton.setObjectName("CollectionButton")
        self.MusicPlay = QtWidgets.QPushButton(self.home)
        self.MusicPlay.setGeometry(QtCore.QRect(460, 5, 111, 86))
        self.MusicPlay.setText("")
        icon = QtGui.QIcon.fromTheme("media-playback-start")
        self.MusicPlay.setIcon(icon)
        self.MusicPlay.setIconSize(QtCore.QSize(80, 80))
        self.MusicPlay.setCheckable(True)
        self.MusicPlay.setObjectName("MusicPlay")
        self.LocationButton = QtWidgets.QPushButton(self.home)
        self.LocationButton.setGeometry(QtCore.QRect(690, 295, 101, 86))
        self.LocationButton.setText("")
        icon = QtGui.QIcon.fromTheme("map-globe")
        self.LocationButton.setIcon(icon)
        self.LocationButton.setIconSize(QtCore.QSize(80, 80))
        self.LocationButton.setObjectName("LocationButton")
        self.NetworkButton = QtWidgets.QPushButton(self.home)
        self.NetworkButton.setGeometry(QtCore.QRect(690, 197, 101, 86))
        self.NetworkButton.setText("")
        icon = QtGui.QIcon.fromTheme("network-cellular-signal-good-symbolic")
        self.NetworkButton.setIcon(icon)
        self.NetworkButton.setIconSize(QtCore.QSize(80, 80))
        self.NetworkButton.setObjectName("NetworkButton")
        self.QuitButton = QtWidgets.QPushButton(self.home)
        self.QuitButton.setGeometry(QtCore.QRect(690, 390, 101, 86))
        self.QuitButton.setText("")
        icon = QtGui.QIcon.fromTheme("exit")
        self.QuitButton.setIcon(icon)
        self.QuitButton.setIconSize(QtCore.QSize(80, 80))
        self.QuitButton.setObjectName("QuitButton")
        self.RandomPlayback = QtWidgets.QPushButton(self.home)
        self.RandomPlayback.setGeometry(QtCore.QRect(580, 390, 101, 86))
        self.RandomPlayback.setText("")
        icon = QtGui.QIcon.fromTheme("media-playlist-shuffle")
        self.RandomPlayback.setIcon(icon)
        self.RandomPlayback.setIconSize(QtCore.QSize(80, 80))
        self.RandomPlayback.setCheckable(True)
        self.RandomPlayback.setObjectName("RandomPlayback")
        self.MPDNextPlaying = QtWidgets.QLabel(self.home)
        self.MPDNextPlaying.setGeometry(QtCore.QRect(10, 200, 321, 71))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.MPDNextPlaying.setFont(font)
        self.MPDNextPlaying.setText("")
        self.MPDNextPlaying.setAlignment(QtCore.Qt.AlignCenter)
        self.MPDNextPlaying.setWordWrap(True)
        self.MPDNextPlaying.setObjectName("MPDNextPlaying")
        self.MPDNowPlaying = QtWidgets.QLabel(self.home)
        self.MPDNowPlaying.setGeometry(QtCore.QRect(10, 120, 321, 71))
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(11)
        self.MPDNowPlaying.setFont(font)
        self.MPDNowPlaying.setText("")
        self.MPDNowPlaying.setAlignment(QtCore.Qt.AlignCenter)
        self.MPDNowPlaying.setWordWrap(True)
        self.MPDNowPlaying.setObjectName("MPDNowPlaying")
        self.CurrentPosition = QtWidgets.QLabel(self.home)
        self.CurrentPosition.setGeometry(QtCore.QRect(10, 400, 319, 29))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.CurrentPosition.setFont(font)
        self.CurrentPosition.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentPosition.setObjectName("CurrentPosition")
        self.CurrentAltitude = QtWidgets.QLabel(self.home)
        self.CurrentAltitude.setGeometry(QtCore.QRect(10, 440, 319, 29))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.CurrentAltitude.setFont(font)
        self.CurrentAltitude.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentAltitude.setObjectName("CurrentAltitude")
        self.CurrentSpeed = QtWidgets.QLabel(self.home)
        self.CurrentSpeed.setGeometry(QtCore.QRect(10, 0, 191, 92))
        font = QtGui.QFont()
        font.setFamily("Open Sans Extrabold")
        font.setPointSize(80)
        font.setBold(True)
        font.setWeight(75)
        self.CurrentSpeed.setFont(font)
        self.CurrentSpeed.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CurrentSpeed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.CurrentSpeed.setObjectName("CurrentSpeed")
        self.MPDPlaylistInfo = QtWidgets.QLabel(self.home)
        self.MPDPlaylistInfo.setGeometry(QtCore.QRect(10, 360, 321, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        self.MPDPlaylistInfo.setFont(font)
        self.MPDPlaylistInfo.setText("")
        self.MPDPlaylistInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.MPDPlaylistInfo.setWordWrap(True)
        self.MPDPlaylistInfo.setObjectName("MPDPlaylistInfo")
        self.SongPlayTime = QtWidgets.QLabel(self.home)
        self.SongPlayTime.setGeometry(QtCore.QRect(340, 366, 341, 20))
        self.SongPlayTime.setText("")
        self.SongPlayTime.setAlignment(QtCore.Qt.AlignCenter)
        self.SongPlayTime.setObjectName("SongPlayTime")
        self.PlaylistDetailsButton = QtWidgets.QPushButton(self.home)
        self.PlaylistDetailsButton.setGeometry(QtCore.QRect(690, 5, 101, 86))
        self.PlaylistDetailsButton.setText("")
        icon = QtGui.QIcon.fromTheme("view-media-playlist")
        self.PlaylistDetailsButton.setIcon(icon)
        self.PlaylistDetailsButton.setIconSize(QtCore.QSize(80, 80))
        self.PlaylistDetailsButton.setCheckable(False)
        self.PlaylistDetailsButton.setObjectName("PlaylistDetailsButton")
        self.SpeedUnit = QtWidgets.QLabel(self.home)
        self.SpeedUnit.setGeometry(QtCore.QRect(210, 0, 120, 92))
        font = QtGui.QFont()
        font.setFamily("Open Sans Extrabold")
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.SpeedUnit.setFont(font)
        self.SpeedUnit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.SpeedUnit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.SpeedUnit.setObjectName("SpeedUnit")
        self.CollectionButton.raise_()
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
        self.SpeedUnit.raise_()
        self.appContent.addWidget(self.home)
        self.current_playlist = QtWidgets.QWidget()
        self.current_playlist.setObjectName("current_playlist")
        self.PlaylistDeleteButton = QtWidgets.QPushButton(self.current_playlist)
        self.PlaylistDeleteButton.setGeometry(QtCore.QRect(690, 198, 101, 86))
        self.PlaylistDeleteButton.setText("")
        icon = QtGui.QIcon.fromTheme("trash-empty")
        self.PlaylistDeleteButton.setIcon(icon)
        self.PlaylistDeleteButton.setIconSize(QtCore.QSize(80, 80))
        self.PlaylistDeleteButton.setObjectName("PlaylistDeleteButton")
        self.PlaylistContents = QtWidgets.QListWidget(self.current_playlist)
        self.PlaylistContents.setGeometry(QtCore.QRect(10, 10, 661, 431))
        self.PlaylistContents.setProperty("showDropIndicator", False)
        self.PlaylistContents.setViewMode(QtWidgets.QListView.ListMode)
        self.PlaylistContents.setBatchSize(2000)
        self.PlaylistContents.setWordWrap(True)
        self.PlaylistContents.setSelectionRectVisible(True)
        self.PlaylistContents.setObjectName("PlaylistContents")
        self.PlaylistCount = QtWidgets.QLabel(self.current_playlist)
        self.PlaylistCount.setGeometry(QtCore.QRect(10, 440, 661, 41))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(16)
        self.PlaylistCount.setFont(font)
        self.PlaylistCount.setAlignment(QtCore.Qt.AlignCenter)
        self.PlaylistCount.setObjectName("PlaylistCount")
        self.PlaylistUpButton = QtWidgets.QPushButton(self.current_playlist)
        self.PlaylistUpButton.setGeometry(QtCore.QRect(690, 5, 101, 86))
        self.PlaylistUpButton.setText("")
        icon = QtGui.QIcon.fromTheme("up")
        self.PlaylistUpButton.setIcon(icon)
        self.PlaylistUpButton.setIconSize(QtCore.QSize(80, 80))
        self.PlaylistUpButton.setObjectName("PlaylistUpButton")
        self.PlaylistDownButton = QtWidgets.QPushButton(self.current_playlist)
        self.PlaylistDownButton.setGeometry(QtCore.QRect(690, 390, 101, 86))
        self.PlaylistDownButton.setText("")
        icon = QtGui.QIcon.fromTheme("down")
        self.PlaylistDownButton.setIcon(icon)
        self.PlaylistDownButton.setIconSize(QtCore.QSize(80, 80))
        self.PlaylistDownButton.setObjectName("PlaylistDownButton")
        self.HomeButton = QtWidgets.QPushButton(self.current_playlist)
        self.HomeButton.setGeometry(QtCore.QRect(690, 102, 101, 86))
        self.HomeButton.setText("")
        icon = QtGui.QIcon.fromTheme("gohome")
        self.HomeButton.setIcon(icon)
        self.HomeButton.setIconSize(QtCore.QSize(80, 80))
        self.HomeButton.setObjectName("HomeButton")
        self.CollectionButton2 = QtWidgets.QPushButton(self.current_playlist)
        self.CollectionButton2.setGeometry(QtCore.QRect(690, 295, 101, 86))
        self.CollectionButton2.setText("")
        icon = QtGui.QIcon.fromTheme("tools-media-optical-copy")
        self.CollectionButton2.setIcon(icon)
        self.CollectionButton2.setIconSize(QtCore.QSize(80, 80))
        self.CollectionButton2.setObjectName("CollectionButton2")
        self.appContent.addWidget(self.current_playlist)
        self.network_status = QtWidgets.QWidget()
        self.network_status.setObjectName("network_status")
        self.appContent.addWidget(self.network_status)
        self.browse_files = QtWidgets.QWidget()
        self.browse_files.setObjectName("browse_files")
        self.appContent.addWidget(self.browse_files)
        self.car_location = QtWidgets.QWidget()
        self.car_location.setObjectName("car_location")
        self.appContent.addWidget(self.car_location)

        self.retranslateUi(NomadicPI)
        self.appContent.setCurrentIndex(1)
        self.PlaylistContents.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(NomadicPI)

    def retranslateUi(self, NomadicPI):
        _translate = QtCore.QCoreApplication.translate
        NomadicPI.setWindowTitle(_translate("NomadicPI", "NomadicPi"))
        self.MusicSkip.setToolTip(_translate("NomadicPI", "Skip Song"))
        self.MusicStop.setToolTip(_translate("NomadicPI", "Stop Music Playback"))
        self.ConsumptionPlayback.setToolTip(_translate("NomadicPI", "Enable / Disable Consumption Playback"))
        self.UpdateDatabase.setToolTip(_translate("NomadicPI", "Update Music Store"))
        self.CollectionButton.setToolTip(_translate("NomadicPI", "Browse Music Collection"))
        self.MusicPlay.setToolTip(_translate("NomadicPI", "Play / Pause Music"))
        self.LocationButton.setToolTip(_translate("NomadicPI", "Location Information"))
        self.NetworkButton.setToolTip(_translate("NomadicPI", "Network Status"))
        self.QuitButton.setToolTip(_translate("NomadicPI", "Exit Application"))
        self.RandomPlayback.setToolTip(_translate("NomadicPI", "Enable / Disable Random Playback"))
        self.CurrentPosition.setText(_translate("NomadicPI", "Current Position: No GPS fix."))
        self.CurrentAltitude.setText(_translate("NomadicPI", "Current Altitude: No GPS fix."))
        self.CurrentSpeed.setText(_translate("NomadicPI", "0"))
        self.PlaylistDetailsButton.setToolTip(_translate("NomadicPI", "Update Music Store"))
        self.SpeedUnit.setText(_translate("NomadicPI", "KM/H"))
        self.PlaylistDeleteButton.setToolTip(_translate("NomadicPI", "Skip Song"))
        self.PlaylistDeleteButton.setStatusTip(_translate("NomadicPI", "Clear Playlist"))
        self.PlaylistContents.setSortingEnabled(False)
        self.PlaylistCount.setText(_translate("NomadicPI", "0 Items"))
        self.PlaylistUpButton.setToolTip(_translate("NomadicPI", "Skip Song"))
        self.PlaylistUpButton.setStatusTip(_translate("NomadicPI", "Scroll Up"))
        self.PlaylistDownButton.setToolTip(_translate("NomadicPI", "Skip Song"))
        self.PlaylistDownButton.setStatusTip(_translate("NomadicPI", "Scroll Down"))
        self.HomeButton.setToolTip(_translate("NomadicPI", "Skip Song"))
        self.HomeButton.setStatusTip(_translate("NomadicPI", "Return Home"))
        self.CollectionButton2.setToolTip(_translate("NomadicPI", "Skip Song"))
        self.CollectionButton2.setStatusTip(_translate("NomadicPI", "Browse Collection"))