import humanize 
import psutil

class SystemStatus():

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register the button actions on the network status page
        self.nomadic.ui.SystemReturnHome.clicked.connect(self.nomadic.view_home_widget)
        
        self.show_system_status()
        
    def show_system_status(self):
        self.update_load_avg()
        self.cpu_stats()
        self.update_system_memory()
        
    def cpu_stats(self):
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
