# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visual_elements/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
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
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.MusicSkip.setFont(font)
        self.MusicSkip.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/fast-forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MusicSkip.setIcon(icon)
        self.MusicSkip.setIconSize(QtCore.QSize(80, 80))
        self.MusicSkip.setObjectName("MusicSkip")
        self.MusicStop = QtWidgets.QPushButton(self.home)
        self.MusicStop.setGeometry(QtCore.QRect(340, 5, 111, 86))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.MusicStop.setFont(font)
        self.MusicStop.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MusicStop.setIcon(icon1)
        self.MusicStop.setIconSize(QtCore.QSize(80, 80))
        self.MusicStop.setObjectName("MusicStop")
        self.ConsumptionPlayback = QtWidgets.QPushButton(self.home)
        self.ConsumptionPlayback.setGeometry(QtCore.QRect(460, 390, 111, 86))
        self.ConsumptionPlayback.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/repeat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ConsumptionPlayback.setIcon(icon2)
        self.ConsumptionPlayback.setIconSize(QtCore.QSize(80, 80))
        self.ConsumptionPlayback.setCheckable(True)
        self.ConsumptionPlayback.setObjectName("ConsumptionPlayback")
        self.UpdateDatabase = QtWidgets.QPushButton(self.home)
        self.UpdateDatabase.setGeometry(QtCore.QRect(340, 390, 111, 86))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.UpdateDatabase.setFont(font)
        self.UpdateDatabase.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.UpdateDatabase.setIcon(icon3)
        self.UpdateDatabase.setIconSize(QtCore.QSize(80, 80))
        self.UpdateDatabase.setCheckable(True)
        self.UpdateDatabase.setObjectName("UpdateDatabase")
        self.MPDAlbumArt = QtWidgets.QLabel(self.home)
        self.MPDAlbumArt.setGeometry(QtCore.QRect(350, 110, 331, 250))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.MPDAlbumArt.setFont(font)
        self.MPDAlbumArt.setToolTip("")
        self.MPDAlbumArt.setText("")
        self.MPDAlbumArt.setAlignment(QtCore.Qt.AlignCenter)
        self.MPDAlbumArt.setObjectName("MPDAlbumArt")
        self.CollectionButton = QtWidgets.QPushButton(self.home)
        self.CollectionButton.setGeometry(QtCore.QRect(690, 100, 101, 86))
        self.CollectionButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/music_collection.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CollectionButton.setIcon(icon4)
        self.CollectionButton.setIconSize(QtCore.QSize(80, 80))
        self.CollectionButton.setObjectName("CollectionButton")
        self.MusicPlay = QtWidgets.QPushButton(self.home)
        self.MusicPlay.setGeometry(QtCore.QRect(460, 5, 111, 86))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.MusicPlay.setFont(font)
        self.MusicPlay.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/media_play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MusicPlay.setIcon(icon5)
        self.MusicPlay.setIconSize(QtCore.QSize(80, 80))
        self.MusicPlay.setCheckable(True)
        self.MusicPlay.setObjectName("MusicPlay")
        self.LocationButton = QtWidgets.QPushButton(self.home)
        self.LocationButton.setGeometry(QtCore.QRect(690, 295, 101, 86))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.LocationButton.setFont(font)
        self.LocationButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/location.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LocationButton.setIcon(icon6)
        self.LocationButton.setIconSize(QtCore.QSize(80, 80))
        self.LocationButton.setObjectName("LocationButton")
        self.SystemButton = QtWidgets.QPushButton(self.home)
        self.SystemButton.setGeometry(QtCore.QRect(690, 197, 101, 86))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.SystemButton.setFont(font)
        self.SystemButton.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/system-run.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SystemButton.setIcon(icon7)
        self.SystemButton.setIconSize(QtCore.QSize(80, 80))
        self.SystemButton.setObjectName("SystemButton")
        self.QuitButton = QtWidgets.QPushButton(self.home)
        self.QuitButton.setGeometry(QtCore.QRect(690, 390, 101, 86))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.QuitButton.setFont(font)
        self.QuitButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/application-exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.QuitButton.setIcon(icon8)
        self.QuitButton.setIconSize(QtCore.QSize(80, 80))
        self.QuitButton.setObjectName("QuitButton")
        self.RandomPlayback = QtWidgets.QPushButton(self.home)
        self.RandomPlayback.setGeometry(QtCore.QRect(580, 390, 101, 86))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.RandomPlayback.setFont(font)
        self.RandomPlayback.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/shuffle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RandomPlayback.setIcon(icon9)
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
        self.CurrentPosition.setGeometry(QtCore.QRect(10, 390, 319, 35))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.CurrentPosition.setFont(font)
        self.CurrentPosition.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentPosition.setObjectName("CurrentPosition")
        self.CurrentAltitude = QtWidgets.QLabel(self.home)
        self.CurrentAltitude.setGeometry(QtCore.QRect(10, 420, 319, 41))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.CurrentAltitude.setFont(font)
        self.CurrentAltitude.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentAltitude.setObjectName("CurrentAltitude")
        self.CurrentSpeed = QtWidgets.QLabel(self.home)
        self.CurrentSpeed.setGeometry(QtCore.QRect(10, 5, 221, 92))
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
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.SongPlayTime.setFont(font)
        self.SongPlayTime.setText("")
        self.SongPlayTime.setAlignment(QtCore.Qt.AlignCenter)
        self.SongPlayTime.setObjectName("SongPlayTime")
        self.PlaylistDetailsButton = QtWidgets.QPushButton(self.home)
        self.PlaylistDetailsButton.setGeometry(QtCore.QRect(690, 5, 101, 86))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.PlaylistDetailsButton.setFont(font)
        self.PlaylistDetailsButton.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/view_playlist.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlaylistDetailsButton.setIcon(icon10)
        self.PlaylistDetailsButton.setIconSize(QtCore.QSize(80, 80))
        self.PlaylistDetailsButton.setCheckable(False)
        self.PlaylistDetailsButton.setObjectName("PlaylistDetailsButton")
        self.SpeedUnit = QtWidgets.QLabel(self.home)
        self.SpeedUnit.setGeometry(QtCore.QRect(229, 5, 101, 92))
        font = QtGui.QFont()
        font.setFamily("Open Sans Extrabold")
        font.setPointSize(25)
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
        self.SystemButton.raise_()
        self.RandomPlayback.raise_()
        self.ConsumptionPlayback.raise_()
        self.MPDPlaylistInfo.raise_()
        self.SongPlayTime.raise_()
        self.PlaylistDetailsButton.raise_()
        self.SpeedUnit.raise_()
        self.appContent.addWidget(self.home)
        self.current_playlist = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.current_playlist.setFont(font)
        self.current_playlist.setObjectName("current_playlist")
        self.PlaylistItemDeleteButton = QtWidgets.QPushButton(self.current_playlist)
        self.PlaylistItemDeleteButton.setGeometry(QtCore.QRect(690, 165, 101, 71))
        self.PlaylistItemDeleteButton.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/remove_item.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlaylistItemDeleteButton.setIcon(icon11)
        self.PlaylistItemDeleteButton.setIconSize(QtCore.QSize(80, 80))
        self.PlaylistItemDeleteButton.setObjectName("PlaylistItemDeleteButton")
        self.PlaylistContents = QtWidgets.QListWidget(self.current_playlist)
        self.PlaylistContents.setGeometry(QtCore.QRect(10, 10, 660, 430))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlaylistContents.sizePolicy().hasHeightForWidth())
        self.PlaylistContents.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans Semibold")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.PlaylistContents.setFont(font)
        self.PlaylistContents.setProperty("showDropIndicator", False)
        self.PlaylistContents.setViewMode(QtWidgets.QListView.ListMode)
        self.PlaylistContents.setModelColumn(0)
        self.PlaylistContents.setBatchSize(2000)
        self.PlaylistContents.setWordWrap(True)
        self.PlaylistContents.setSelectionRectVisible(True)
        self.PlaylistContents.setObjectName("PlaylistContents")
        self.PlaylistCount = QtWidgets.QLabel(self.current_playlist)
        self.PlaylistCount.setGeometry(QtCore.QRect(10, 440, 660, 40))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(16)
        self.PlaylistCount.setFont(font)
        self.PlaylistCount.setAlignment(QtCore.Qt.AlignCenter)
        self.PlaylistCount.setObjectName("PlaylistCount")
        self.PlaylistUpButton = QtWidgets.QPushButton(self.current_playlist)
        self.PlaylistUpButton.setGeometry(QtCore.QRect(690, 5, 101, 71))
        self.PlaylistUpButton.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlaylistUpButton.setIcon(icon12)
        self.PlaylistUpButton.setIconSize(QtCore.QSize(80, 80))
        self.PlaylistUpButton.setObjectName("PlaylistUpButton")
        self.PlaylistDownButton = QtWidgets.QPushButton(self.current_playlist)
        self.PlaylistDownButton.setGeometry(QtCore.QRect(690, 405, 101, 71))
        self.PlaylistDownButton.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/down.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.PlaylistDownButton.setIcon(icon13)
        self.PlaylistDownButton.setIconSize(QtCore.QSize(80, 80))
        self.PlaylistDownButton.setObjectName("PlaylistDownButton")
        self.HomeButton = QtWidgets.QPushButton(self.current_playlist)
        self.HomeButton.setGeometry(QtCore.QRect(690, 325, 101, 71))
        self.HomeButton.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.HomeButton.setIcon(icon14)
        self.HomeButton.setIconSize(QtCore.QSize(80, 80))
        self.HomeButton.setObjectName("HomeButton")
        self.PlayPlaylistItem = QtWidgets.QPushButton(self.current_playlist)
        self.PlayPlaylistItem.setGeometry(QtCore.QRect(690, 85, 101, 71))
        self.PlayPlaylistItem.setText("")
        self.PlayPlaylistItem.setIcon(icon5)
        self.PlayPlaylistItem.setIconSize(QtCore.QSize(80, 80))
        self.PlayPlaylistItem.setObjectName("PlayPlaylistItem")
        self.DeletePlaylist = QtWidgets.QPushButton(self.current_playlist)
        self.DeletePlaylist.setGeometry(QtCore.QRect(690, 245, 101, 71))
        self.DeletePlaylist.setText("")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.DeletePlaylist.setIcon(icon15)
        self.DeletePlaylist.setIconSize(QtCore.QSize(80, 80))
        self.DeletePlaylist.setObjectName("DeletePlaylist")
        self.appContent.addWidget(self.current_playlist)
        self.system_status = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.system_status.setFont(font)
        self.system_status.setObjectName("system_status")
        self.SystemReturnHome = QtWidgets.QPushButton(self.system_status)
        self.SystemReturnHome.setGeometry(QtCore.QRect(690, 10, 101, 71))
        self.SystemReturnHome.setText("")
        self.SystemReturnHome.setIcon(icon14)
        self.SystemReturnHome.setIconSize(QtCore.QSize(80, 80))
        self.SystemReturnHome.setObjectName("SystemReturnHome")
        self.SystemLoadAvg = QtWidgets.QLabel(self.system_status)
        self.SystemLoadAvg.setGeometry(QtCore.QRect(20, 100, 231, 21))
        self.SystemLoadAvg.setObjectName("SystemLoadAvg")
        self.SystemStatsLabel = QtWidgets.QLabel(self.system_status)
        self.SystemStatsLabel.setGeometry(QtCore.QRect(10, 70, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.SystemStatsLabel.setFont(font)
        self.SystemStatsLabel.setObjectName("SystemStatsLabel")
        self.SystemMemoryAvail = QtWidgets.QLabel(self.system_status)
        self.SystemMemoryAvail.setGeometry(QtCore.QRect(20, 120, 221, 21))
        self.SystemMemoryAvail.setObjectName("SystemMemoryAvail")
        self.MPDStatsLabel = QtWidgets.QLabel(self.system_status)
        self.MPDStatsLabel.setGeometry(QtCore.QRect(10, 0, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.MPDStatsLabel.setFont(font)
        self.MPDStatsLabel.setObjectName("MPDStatsLabel")
        self.NetworkStatsLabel = QtWidgets.QLabel(self.system_status)
        self.NetworkStatsLabel.setGeometry(QtCore.QRect(10, 295, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.NetworkStatsLabel.setFont(font)
        self.NetworkStatsLabel.setObjectName("NetworkStatsLabel")
        self.SystemMemoryUsed = QtWidgets.QLabel(self.system_status)
        self.SystemMemoryUsed.setGeometry(QtCore.QRect(250, 120, 211, 21))
        self.SystemMemoryUsed.setObjectName("SystemMemoryUsed")
        self.SystemMemoryUtilisation = QtWidgets.QLabel(self.system_status)
        self.SystemMemoryUtilisation.setGeometry(QtCore.QRect(460, 120, 211, 21))
        self.SystemMemoryUtilisation.setObjectName("SystemMemoryUtilisation")
        self.SystemCPUUsage = QtWidgets.QLabel(self.system_status)
        self.SystemCPUUsage.setGeometry(QtCore.QRect(250, 100, 211, 21))
        self.SystemCPUUsage.setObjectName("SystemCPUUsage")
        self.SystemCPUFreq = QtWidgets.QLabel(self.system_status)
        self.SystemCPUFreq.setGeometry(QtCore.QRect(460, 100, 211, 21))
        self.SystemCPUFreq.setObjectName("SystemCPUFreq")
        self.DiskStatsLabel = QtWidgets.QLabel(self.system_status)
        self.DiskStatsLabel.setGeometry(QtCore.QRect(10, 142, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans Condensed")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.DiskStatsLabel.setFont(font)
        self.DiskStatsLabel.setObjectName("DiskStatsLabel")
        self.MPDArtists = QtWidgets.QLabel(self.system_status)
        self.MPDArtists.setGeometry(QtCore.QRect(20, 30, 231, 21))
        self.MPDArtists.setObjectName("MPDArtists")
        self.MPDPlaytime = QtWidgets.QLabel(self.system_status)
        self.MPDPlaytime.setGeometry(QtCore.QRect(20, 50, 231, 21))
        self.MPDPlaytime.setObjectName("MPDPlaytime")
        self.MPDAlbums = QtWidgets.QLabel(self.system_status)
        self.MPDAlbums.setGeometry(QtCore.QRect(250, 30, 211, 21))
        self.MPDAlbums.setObjectName("MPDAlbums")
        self.MPDUptime = QtWidgets.QLabel(self.system_status)
        self.MPDUptime.setGeometry(QtCore.QRect(250, 50, 211, 21))
        self.MPDUptime.setObjectName("MPDUptime")
        self.MPDSongs = QtWidgets.QLabel(self.system_status)
        self.MPDSongs.setGeometry(QtCore.QRect(460, 30, 221, 21))
        self.MPDSongs.setObjectName("MPDSongs")
        self.MPDStored = QtWidgets.QLabel(self.system_status)
        self.MPDStored.setGeometry(QtCore.QRect(460, 50, 221, 21))
        self.MPDStored.setObjectName("MPDStored")
        self.SystemFileSystems = QtWidgets.QTableWidget(self.system_status)
        self.SystemFileSystems.setGeometry(QtCore.QRect(10, 175, 662, 121))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SystemFileSystems.sizePolicy().hasHeightForWidth())
        self.SystemFileSystems.setSizePolicy(sizePolicy)
        self.SystemFileSystems.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.SystemFileSystems.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.SystemFileSystems.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.SystemFileSystems.setColumnCount(5)
        self.SystemFileSystems.setObjectName("SystemFileSystems")
        self.SystemFileSystems.setRowCount(0)
        self.SystemFileSystems.horizontalHeader().setDefaultSectionSize(132)
        self.SystemFileSystems.horizontalHeader().setStretchLastSection(False)
        self.SystemFileSystems.verticalHeader().setVisible(False)
        self.SystemNetwork = QtWidgets.QTableWidget(self.system_status)
        self.SystemNetwork.setGeometry(QtCore.QRect(10, 330, 662, 141))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SystemNetwork.sizePolicy().hasHeightForWidth())
        self.SystemNetwork.setSizePolicy(sizePolicy)
        self.SystemNetwork.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.SystemNetwork.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.SystemNetwork.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.SystemNetwork.setColumnCount(4)
        self.SystemNetwork.setObjectName("SystemNetwork")
        self.SystemNetwork.setRowCount(0)
        self.SystemNetwork.horizontalHeader().setDefaultSectionSize(160)
        self.SystemNetwork.horizontalHeader().setStretchLastSection(True)
        self.SystemNetwork.verticalHeader().setVisible(False)
        self.SystemNetwork.verticalHeader().setCascadingSectionResizes(True)
        self.appContent.addWidget(self.system_status)
        self.browse_files = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.browse_files.setFont(font)
        self.browse_files.setObjectName("browse_files")
        self.FileList = QtWidgets.QListWidget(self.browse_files)
        self.FileList.setGeometry(QtCore.QRect(10, 10, 660, 430))
        self.FileList.setIconSize(QtCore.QSize(16, 16))
        self.FileList.setViewMode(QtWidgets.QListView.ListMode)
        self.FileList.setSelectionRectVisible(False)
        self.FileList.setObjectName("FileList")
        self.FileListUp = QtWidgets.QPushButton(self.browse_files)
        self.FileListUp.setGeometry(QtCore.QRect(690, 5, 101, 71))
        self.FileListUp.setText("")
        self.FileListUp.setIcon(icon12)
        self.FileListUp.setIconSize(QtCore.QSize(80, 80))
        self.FileListUp.setObjectName("FileListUp")
        self.FileListDown = QtWidgets.QPushButton(self.browse_files)
        self.FileListDown.setGeometry(QtCore.QRect(690, 405, 101, 71))
        self.FileListDown.setText("")
        self.FileListDown.setIcon(icon13)
        self.FileListDown.setIconSize(QtCore.QSize(80, 80))
        self.FileListDown.setObjectName("FileListDown")
        self.FileReturnHome = QtWidgets.QPushButton(self.browse_files)
        self.FileReturnHome.setGeometry(QtCore.QRect(690, 325, 101, 71))
        self.FileReturnHome.setText("")
        self.FileReturnHome.setIcon(icon14)
        self.FileReturnHome.setIconSize(QtCore.QSize(80, 80))
        self.FileReturnHome.setObjectName("FileReturnHome")
        self.FileAddToPlaylist = QtWidgets.QPushButton(self.browse_files)
        self.FileAddToPlaylist.setGeometry(QtCore.QRect(690, 165, 101, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FileAddToPlaylist.sizePolicy().hasHeightForWidth())
        self.FileAddToPlaylist.setSizePolicy(sizePolicy)
        self.FileAddToPlaylist.setMinimumSize(QtCore.QSize(0, 50))
        self.FileAddToPlaylist.setText("")
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FileAddToPlaylist.setIcon(icon16)
        self.FileAddToPlaylist.setIconSize(QtCore.QSize(80, 80))
        self.FileAddToPlaylist.setObjectName("FileAddToPlaylist")
        self.FileOpenFolder = QtWidgets.QPushButton(self.browse_files)
        self.FileOpenFolder.setGeometry(QtCore.QRect(690, 85, 101, 71))
        self.FileOpenFolder.setText("")
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FileOpenFolder.setIcon(icon17)
        self.FileOpenFolder.setIconSize(QtCore.QSize(80, 80))
        self.FileOpenFolder.setObjectName("FileOpenFolder")
        self.FileParentDirectory = QtWidgets.QPushButton(self.browse_files)
        self.FileParentDirectory.setGeometry(QtCore.QRect(690, 245, 101, 71))
        self.FileParentDirectory.setText("")
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(self.base_path + "visual_elements/icons/parent_folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.FileParentDirectory.setIcon(icon18)
        self.FileParentDirectory.setIconSize(QtCore.QSize(80, 80))
        self.FileParentDirectory.setObjectName("FileParentDirectory")
        self.FileCount = QtWidgets.QLabel(self.browse_files)
        self.FileCount.setGeometry(QtCore.QRect(10, 440, 660, 40))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(16)
        self.FileCount.setFont(font)
        self.FileCount.setAlignment(QtCore.Qt.AlignCenter)
        self.FileCount.setObjectName("FileCount")
        self.appContent.addWidget(self.browse_files)
        self.car_location = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.car_location.setFont(font)
        self.car_location.setObjectName("car_location")
        self.LocationReturnHome = QtWidgets.QPushButton(self.car_location)
        self.LocationReturnHome.setGeometry(QtCore.QRect(690, 10, 101, 71))
        self.LocationReturnHome.setText("")
        self.LocationReturnHome.setIcon(icon14)
        self.LocationReturnHome.setIconSize(QtCore.QSize(80, 80))
        self.LocationReturnHome.setObjectName("LocationReturnHome")
        self.PageHeading = QtWidgets.QLabel(self.car_location)
        self.PageHeading.setGeometry(QtCore.QRect(10, 10, 201, 16))
        self.PageHeading.setObjectName("PageHeading")
        self.GpsSatellites = QtWidgets.QLabel(self.car_location)
        self.GpsSatellites.setGeometry(QtCore.QRect(10, 40, 331, 31))
        self.GpsSatellites.setObjectName("GpsSatellites")
        self.GpsSatellitesUsed = QtWidgets.QLabel(self.car_location)
        self.GpsSatellitesUsed.setGeometry(QtCore.QRect(10, 80, 331, 31))
        self.GpsSatellitesUsed.setObjectName("GpsSatellitesUsed")
        self.GpsFixType = QtWidgets.QLabel(self.car_location)
        self.GpsFixType.setGeometry(QtCore.QRect(10, 120, 331, 31))
        self.GpsFixType.setObjectName("GpsFixType")
        self.CurAltitude = QtWidgets.QLabel(self.car_location)
        self.CurAltitude.setGeometry(QtCore.QRect(10, 160, 331, 31))
        self.CurAltitude.setObjectName("CurAltitude")
        self.CurCoordinates = QtWidgets.QLabel(self.car_location)
        self.CurCoordinates.setGeometry(QtCore.QRect(10, 200, 331, 31))
        self.CurCoordinates.setObjectName("CurCoordinates")
        self.LocationPrecision = QtWidgets.QLabel(self.car_location)
        self.LocationPrecision.setGeometry(QtCore.QRect(10, 240, 331, 31))
        self.LocationPrecision.setObjectName("LocationPrecision")
        self.HorizontalSpeed = QtWidgets.QLabel(self.car_location)
        self.HorizontalSpeed.setGeometry(QtCore.QRect(10, 320, 331, 31))
        self.HorizontalSpeed.setObjectName("HorizontalSpeed")
        self.VerticalSpeed = QtWidgets.QLabel(self.car_location)
        self.VerticalSpeed.setGeometry(QtCore.QRect(10, 360, 331, 31))
        self.VerticalSpeed.setObjectName("VerticalSpeed")
        self.LocalTime = QtWidgets.QLabel(self.car_location)
        self.LocalTime.setGeometry(QtCore.QRect(10, 400, 331, 31))
        self.LocalTime.setObjectName("LocalTime")
        self.GpsHeading = QtWidgets.QLabel(self.car_location)
        self.GpsHeading.setGeometry(QtCore.QRect(10, 280, 331, 31))
        self.GpsHeading.setObjectName("GpsHeading")
        self.appContent.addWidget(self.car_location)

        self.retranslateUi(NomadicPI)
        self.appContent.setCurrentIndex(4)
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
        self.SystemButton.setToolTip(_translate("NomadicPI", "System Status / Settings"))
        self.QuitButton.setToolTip(_translate("NomadicPI", "Exit Application"))
        self.RandomPlayback.setToolTip(_translate("NomadicPI", "Enable / Disable Random Playback"))
        self.CurrentPosition.setText(_translate("NomadicPI", "Current Position: No GPS fix."))
        self.CurrentAltitude.setText(_translate("NomadicPI", "Current Altitude: No GPS fix."))
        self.CurrentSpeed.setText(_translate("NomadicPI", "0"))
        self.PlaylistDetailsButton.setToolTip(_translate("NomadicPI", "View Media Queue"))
        self.SpeedUnit.setText(_translate("NomadicPI", "KM/H"))
        self.PlaylistItemDeleteButton.setToolTip(_translate("NomadicPI", "Delete Song"))
        self.PlaylistItemDeleteButton.setStatusTip(_translate("NomadicPI", "Clear Playlist"))
        self.PlaylistContents.setSortingEnabled(False)
        self.PlaylistCount.setText(_translate("NomadicPI", "0 Items"))
        self.PlaylistUpButton.setToolTip(_translate("NomadicPI", "Scroll Up"))
        self.PlaylistUpButton.setStatusTip(_translate("NomadicPI", "Scroll Up"))
        self.PlaylistDownButton.setToolTip(_translate("NomadicPI", "Scroll Down"))
        self.PlaylistDownButton.setStatusTip(_translate("NomadicPI", "Scroll Down"))
        self.HomeButton.setToolTip(_translate("NomadicPI", "Application Home"))
        self.HomeButton.setStatusTip(_translate("NomadicPI", "Return Home"))
        self.PlayPlaylistItem.setToolTip(_translate("NomadicPI", "Play Song"))
        self.PlayPlaylistItem.setStatusTip(_translate("NomadicPI", "Browse Collection"))
        self.DeletePlaylist.setToolTip(_translate("NomadicPI", "Remove Song"))
        self.DeletePlaylist.setStatusTip(_translate("NomadicPI", "Browse Collection"))
        self.SystemReturnHome.setToolTip(_translate("NomadicPI", "Application Home"))
        self.SystemReturnHome.setStatusTip(_translate("NomadicPI", "Scroll Up"))
        self.SystemLoadAvg.setText(_translate("NomadicPI", "Load Average: "))
        self.SystemStatsLabel.setText(_translate("NomadicPI", "System Info"))
        self.SystemMemoryAvail.setText(_translate("NomadicPI", "Memory Available:"))
        self.MPDStatsLabel.setText(_translate("NomadicPI", "MPD"))
        self.NetworkStatsLabel.setText(_translate("NomadicPI", "Network"))
        self.SystemMemoryUsed.setText(_translate("NomadicPI", "Memory Used:"))
        self.SystemMemoryUtilisation.setText(_translate("NomadicPI", "Utilisation:"))
        self.SystemCPUUsage.setText(_translate("NomadicPI", "CPU Usage:"))
        self.SystemCPUFreq.setText(_translate("NomadicPI", "CPU Frequency:"))
        self.DiskStatsLabel.setText(_translate("NomadicPI", "Disks"))
        self.MPDArtists.setText(_translate("NomadicPI", "Artists:"))
        self.MPDPlaytime.setText(_translate("NomadicPI", "Playtime:"))
        self.MPDAlbums.setText(_translate("NomadicPI", "Albums:"))
        self.MPDUptime.setText(_translate("NomadicPI", "Uptime:"))
        self.MPDSongs.setText(_translate("NomadicPI", "Songs:"))
        self.MPDStored.setText(_translate("NomadicPI", "Stored:"))
        self.FileListUp.setToolTip(_translate("NomadicPI", "Scroll Up"))
        self.FileListDown.setToolTip(_translate("NomadicPI", "Scroll Down"))
        self.FileListDown.setStatusTip(_translate("NomadicPI", "Scroll Up"))
        self.FileReturnHome.setToolTip(_translate("NomadicPI", "Application Home"))
        self.FileReturnHome.setStatusTip(_translate("NomadicPI", "Scroll Up"))
        self.FileAddToPlaylist.setToolTip(_translate("NomadicPI", "Queue File For Playback"))
        self.FileOpenFolder.setToolTip(_translate("NomadicPI", "Open Folder"))
        self.FileParentDirectory.setToolTip(_translate("NomadicPI", "Parent Folder"))
        self.FileCount.setText(_translate("NomadicPI", "0 Items"))
        self.LocationReturnHome.setToolTip(_translate("NomadicPI", "Application Home"))
        self.LocationReturnHome.setStatusTip(_translate("NomadicPI", "Scroll Up"))
        self.PageHeading.setText(_translate("NomadicPI", "Location Information"))
        self.GpsSatellites.setText(_translate("NomadicPI", "Satellites"))
        self.GpsSatellitesUsed.setText(_translate("NomadicPI", "Satellites Used"))
        self.GpsFixType.setText(_translate("NomadicPI", "GPS Fix Type"))
        self.CurAltitude.setText(_translate("NomadicPI", "Altitude"))
        self.CurCoordinates.setText(_translate("NomadicPI", "Coordinates"))
        self.LocationPrecision.setText(_translate("NomadicPI", "LocationPrecision"))
        self.HorizontalSpeed.setText(_translate("NomadicPI", "HorizontalSpeed"))
        self.VerticalSpeed.setText(_translate("NomadicPI", "VerticalSpeed"))
        self.LocalTime.setText(_translate("NomadicPI", "LocalTime"))
        self.GpsHeading.setText(_translate("NomadicPI", "Heading"))
