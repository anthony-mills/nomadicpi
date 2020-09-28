import humanize 
import psutil
import datetime as dt

from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem

class SystemStatus():

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register the button actions on the network status page
        self.nomadic.ui.SystemReturnHome.clicked.connect(self.nomadic.view_home_widget)
        
        self.show_system_status()
        
    def show_system_status(self):
        self.update_load_avg()
        self.cpu_stats()
        self.disk_info()
        self.update_system_memory()
        self.mpd_daemon()

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
            self.nomadic.ui.SystemFileSystems.setItem(row,0, QTableWidgetItem(filesystem.device))
            self.nomadic.ui.SystemFileSystems.setItem(row,1, QTableWidgetItem(filesystem.mountpoint))
            self.nomadic.ui.SystemFileSystems.setItem(row,2, QTableWidgetItem(filesystem.fstype))
            used = psutil.disk_usage(filesystem.mountpoint)
            self.nomadic.ui.SystemFileSystems.setItem(row,3, QTableWidgetItem(humanize.naturalsize(used.total)))
            self.nomadic.ui.SystemFileSystems.setItem(row,4, QTableWidgetItem(str(used.percent) + '%'))
            row +=1

    def mpd_daemon(self):
        """
        Update the state of the MPD daemon
        """        
        daemon_state = self.nomadic.mpd.mpd_stats()
        
        if type(daemon_state['artists']) is str:
            self.nomadic.ui.MPDArtists.setText('Artists: ' + daemon_state['artists'])
        else:
             self.nomadic.ui.MPDArtists.setText('Artists: Unknown')
        
        if type(daemon_state['albums']) is str:
            self.nomadic.ui.MPDAlbums.setText('Albums: ' + daemon_state['albums'])
        else:
             self.nomadic.ui.MPDAlbums.setText('Albums: Unknown')
             
        if type(daemon_state['songs']) is str:
            self.nomadic.ui.MPDSongs.setText('Songs: ' + daemon_state['songs'])
        else:
             self.nomadic.ui.MPDSongs.setText('Songs: Unknown')

        if type(daemon_state['playtime']) is str:
            mpd_playtime = humanize.naturaldelta(dt.timedelta(seconds=int(daemon_state['playtime'])))
            self.nomadic.ui.MPDPlaytime.setText('Playtime: ' + mpd_playtime[0].upper() + mpd_playtime[1:])
        else:
            self.nomadic.ui.MPDPlaytime.setText('Playtime: Unknown')
        
        if type(daemon_state['uptime']) is str:
            mpd_uptime = humanize.naturaldelta(dt.timedelta(seconds=int(daemon_state['uptime'])))
            self.nomadic.ui.MPDUptime.setText('Uptime: ' + mpd_uptime[0].upper() + mpd_uptime[1:])
        else:
            self.nomadic.ui.MPDUptime.setText('Uptime: Unknown')
             
        if type(daemon_state['db_playtime']) is str:
            mpd_stored = humanize.naturaldelta(dt.timedelta(seconds=int(daemon_state['db_playtime'])))            
            self.nomadic.ui.MPDStored.setText('Stored: ' + mpd_stored[0].upper() + mpd_stored[1:])
        else:
            self.nomadic.ui.MPDStored.setText('Stored: Unknown')                
        
    def cpu_stats(self):
        """
        Update the CPU related statistics
        """        
        cpu_usage = psutil.cpu_percent(interval=1)
        self.nomadic.ui.SystemCPUUsage.setText('CPU Usage: ' + str(cpu_usage) + '%')

        cpu_freq = psutil.cpu_freq()
        self.nomadic.ui.SystemCPUFreq.setText('CPU Frequency: ' + str(round(cpu_freq[0])) + ' Mhz')
                
    def update_load_avg(self):
        """
        Update the system section with the current load average
        """        
        load_avg = psutil.getloadavg()
        self.nomadic.ui.SystemLoadAvg.setText('Load Average: ' + str(load_avg[0]))

    def update_system_memory(self):
        """
        Update the system section with the current memory usage
        """        
        mem_usage = psutil.virtual_memory()
        
        mem_total = 'Total Memory: ' + humanize.naturalsize(mem_usage[0])
        self.nomadic.ui.SystemMemoryAvail.setText(mem_total)
                
        mem_used = 'Memory Used: ' + humanize.naturalsize(mem_usage[3])
        self.nomadic.ui.SystemMemoryUsed.setText(mem_used)
                
        mem_percent = 'Memory Utilisation: ' + str(mem_usage[2]) + '%'
        self.nomadic.ui.SystemMemoryUtilisation.setText(mem_percent)
