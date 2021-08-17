import datetime as dt
import logging
import humanize
import psutil

from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

LOGGER = logging.getLogger(__name__)

class SystemStatus():

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register the button actions on the network status page
        self.nomadic.ui.SystemReturnHome.clicked.connect(self.nomadic.view_home_widget)
        self.nomadic.ui.UpdateDatabase.clicked.connect(self.music_update_press)

        self.show_system_status()

    def show_system_status(self):
        """
        Aggregate the system metrics
        """
        self.update_load_avg()
        self.cpu_stats()
        self.disk_info()
        self.update_system_memory()
        self.mpd_daemon()
        self.network_info()

        self.database_update_status(self.nomadic.mpd_status)

    def disk_info(self):
        """
        Update the state of the file systems
        """
        system_disks = psutil.disk_partitions()

        row = 0
        self.nomadic.ui.SystemFileSystems.setColumnCount(5)
        self.nomadic.ui.SystemFileSystems.setRowCount(len(system_disks))
        self.nomadic.ui.SystemFileSystems.setHorizontalHeaderLabels(('Device', 'Mount', 'Type', 'Size', 'Usage'))

        for filesystem in system_disks:
            self.nomadic.ui.SystemFileSystems.setItem(row, 0, QTableWidgetItem(filesystem.device))
            self.nomadic.ui.SystemFileSystems.setItem(row, 1, QTableWidgetItem(filesystem.mountpoint))
            self.nomadic.ui.SystemFileSystems.setItem(row, 2, QTableWidgetItem(filesystem.fstype))
            used = psutil.disk_usage(filesystem.mountpoint)
            self.nomadic.ui.SystemFileSystems.setItem(row, 3, QTableWidgetItem(humanize.naturalsize(used.total)))
            self.nomadic.ui.SystemFileSystems.setItem(row, 4, QTableWidgetItem(str(used.percent) + '%'))
            row +=1

    def network_info(self):
        """
        Update the state of the network interfaces
        """
        network_interfaces = psutil.net_if_addrs()
        interface_activity = psutil.net_io_counters(pernic=True)

        row = 0
        self.nomadic.ui.SystemNetwork.setColumnCount(4)
        self.nomadic.ui.SystemNetwork.setRowCount(len(network_interfaces))
        self.nomadic.ui.SystemNetwork.setHorizontalHeaderLabels(('Device', 'IP', 'Sent', 'Received'))

        for interface in network_interfaces:
            if interface != 'lo':

                self.nomadic.ui.SystemNetwork.setItem(row, 0, QTableWidgetItem(interface))

                if network_interfaces[interface][0].address is not None:
                    self.nomadic.ui.SystemNetwork.setItem(row, 1, QTableWidgetItem(network_interfaces[interface][0].address))
                if interface_activity[interface].bytes_sent is not None:
                    self.nomadic.ui.SystemNetwork.setItem(row, 2, QTableWidgetItem(humanize.naturalsize(interface_activity[interface].bytes_sent)))
                if interface_activity[interface].bytes_recv is not None:
                    self.nomadic.ui.SystemNetwork.setItem(row, 3, QTableWidgetItem(humanize.naturalsize(interface_activity[interface].bytes_recv)))
                row +=1

    def mpd_daemon(self):
        """
        Update the state of the MPD daemon
        """
        daemon_state = self.nomadic.mpd.mpd_stats()

        if isinstance(daemon_state['artists'], str):
            self.nomadic.ui.MPDArtists.setText(f"Artists: {daemon_state['artists']}")
        else:
            self.nomadic.ui.MPDArtists.setText("Artists: Unknown")

        if isinstance(daemon_state['albums'], str):
            self.nomadic.ui.MPDAlbums.setText(f"Albums: {daemon_state['albums']}")
        else:
            self.nomadic.ui.MPDAlbums.setText("Albums: Unknown")

        if isinstance(daemon_state['songs'], str):
            self.nomadic.ui.MPDSongs.setText(f"Songs: {daemon_state['songs']}")
        else:
            self.nomadic.ui.MPDSongs.setText("Songs: Unknown")

        if isinstance(daemon_state['playtime'], str):
            playtime = int(daemon_state['playtime'])

            if playtime > 0:
                mpd_playtime = humanize.naturaldelta(dt.timedelta(seconds=int(playtime)))
                playtime = mpd_playtime[0].upper() + mpd_playtime[1:]
            else:
                playtime = "N/A"

            self.nomadic.ui.MPDPlaytime.setText(f"Playtime: {playtime}")
        else:
            self.nomadic.ui.MPDPlaytime.setText("Playtime: Unknown")

        if isinstance(daemon_state['uptime'], str):
            mpd_uptime = humanize.naturaldelta(dt.timedelta(seconds=int(daemon_state['uptime'])))
            self.nomadic.ui.MPDUptime.setText(f"Uptime: {mpd_uptime[0].upper() + mpd_uptime[1:]}")
        else:
            self.nomadic.ui.MPDUptime.setText("Uptime: Unknown")

        if isinstance(daemon_state['db_playtime'], str):
            mpd_stored = humanize.naturaldelta(dt.timedelta(seconds=int(daemon_state['db_playtime'])))
            self.nomadic.ui.MPDStored.setText(f"Stored: {mpd_stored[0].upper() + mpd_stored[1:]}")
        else:
            self.nomadic.ui.MPDStored.setText("Stored: Unknown")

    def cpu_stats(self):
        """
        Update the CPU related statistics
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        self.nomadic.ui.SystemCPUUsage.setText(f"CPU Usage: {cpu_usage}%")

        cpu_freq = psutil.cpu_freq()
        self.nomadic.ui.SystemCPUFreq.setText(f"CPU Frequency: {round(cpu_freq[0])} Mhz")

    def update_load_avg(self):
        """
        Update the system section with the current load average
        """
        load_avg = psutil.getloadavg()
        self.nomadic.ui.SystemLoadAvg.setText(f"Load Average: {load_avg[0]}")

    def update_system_memory(self):
        """
        Update the system section with the current memory usage
        """
        mem_usage = psutil.virtual_memory()

        mem_total = f"Total Memory: {humanize.naturalsize(mem_usage[0])}"
        self.nomadic.ui.SystemMemoryAvail.setText(mem_total)

        mem_used = f"Memory Used: {humanize.naturalsize(mem_usage[3])}"
        self.nomadic.ui.SystemMemoryUsed.setText(mem_used)

        mem_percent = f"Memory Utilisation: {mem_usage[2]}%"
        self.nomadic.ui.SystemMemoryUtilisation.setText(mem_percent)

    def music_update_press(self):
        """
        Trigger manual update of the music library
        """
        LOGGER.debug("Manual update of the MPD library contents triggered.")
        self.nomadic.mpd.update_library()
        self.database_update_status(self.nomadic.mpd_status)

    def database_update_status(self, mpd_status):
        """
        Update the state of database update button

        Parameters
        ----------
        mpd_status : dict
            Dictionary of the MPD daemons current state
        """
        if self.nomadic.mpd_status.get('updating_db') is None:
            self.nomadic.ui.UpdateDatabase.setChecked(False)
        else:
            self.nomadic.ui.UpdateDatabase.setChecked(True)