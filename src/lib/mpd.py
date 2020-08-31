from mpd import MPDClient

class MpdLib():
    def __init__(self):
        self.mpd_host = '127.0.0.1'
        self.mpd_port = 6600       
        
    def set_mpd_host(self, mpd_host):
        """
        Set the IP or hostname the MPD daemon is running on
        """        
        self.mpd_host = mpd_host
        
    def set_mpd_port(self, mpd_port):
        """
        Set the port the MPD daemon is running on
        """         
        self.mpd_port = mpd_port
        
    def connect_mpd(self):
        """
        Attempt to connect to the MPD daemon
        """         
        self.client = MPDClient()
        self.client.timeout = 10

        try:
            self.client.connect(self.mpd_host, self.mpd_port) 
        except Exception as e:
            print("MPD Error: " + str(e))

    def get_status(self):
        """
        Return the status of the mpd daemon
        """         
        return self.client.status()   
        
    def play_playback(self):
        """
        Change the play state
        """    
        status = self.client.status() 
        
        if status.get('state') == 'play':
            self.client.pause()         
        else:
            self.client.play()          

    def update_library(self):
        """
        Update the MPD library
        """         
        status = self.client.status() 
        
        if status.get('updating_db') is None:
            self.client.update()   
        
    def random_playback(self):
        """
        Change the random playback state
        """         
        status = self.client.status()  
        
        if int(status['random']) == 0:
            self.client.random(1)
        else:
            self.client.random(0)            

    def stop_playback(self):
        """
        Stop MPD playback
        """         
        self.client.stop() 
        
    def next_song(self):
        """
        Skip playback to the next song
        """         
        self.client.next()         
                    
    def consumption_playback(self):
        """
        Change the consume playback state
        """         
        status = self.client.status()  
        
        if int(status['consume']) == 0:
            self.client.consume(1)
        else:
            self.client.consume(0)    
                                            
    def close_mpd(self):
        """
        Close the connection to the MPD daemon
        """         
        self.client.close()
        self.client.disconnect()        
