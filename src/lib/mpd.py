import sys
import json
import os.path

import musicbrainzngs
import urllib.request

from mpd import MPDClient
from PIL import Image
from resizeimage import resizeimage

class MpdLib():
    def __init__(self):
        self.mpd_host = '127.0.0.1'
        self.mpd_port = 6600
        self.art_cache = '/tmp/'
        
        musicbrainzngs.set_useragent("NomadicPI", "v0.0.1", "https://github.com/anthony-mills/nomadicpi")    
        
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

    def set_art_cache(self, art_cache):
        """
        Set the cache directory for album art
        """        
        self.art_cache = art_cache
           
        
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
        
        Returns
        -------
        dict
            Dictionary of values concerning the current state of the MPD daemon
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

    def currently_playing(self):
        """
        Return information about the current song playing
        
        Returns
        -------
        dict
            Dictionary of values concerning the current state of the MPD daemon
        """         
        status = self.client.status() 
                
        if status['state'] == 'play':
            return self.client.currentsong()
            
        else:
            return {}
    
    def album_art(self, search_term, cache_key ):
        """
        Change the consume playback state
        
        Parameters
        ----------
        search_term : string
            Search term when looking for album art
        cache_name : string
            Name to store any cache item under 
        """
        
        if os.path.isfile(self.art_cache + str(cache_key)):
            return self.art_cache + str(cache_key)
        else:
            try:
                mb_search = musicbrainzngs.search_release_groups(search_term)

                if type(mb_search['release-group-list'][0]['id']) is str:
                    image_list = musicbrainzngs.get_release_group_image_list(mb_search['release-group-list'][0]['id'])
                    if type(image_list['images'][0]['thumbnails']['small']) is str:        
                        thumb_file = self.art_cache + str(cache_key)
                        urllib.request.urlretrieve(image_list['images'][0]['thumbnails']['small'], thumb_file)
                        
                        fd_img = open(thumb_file, 'rb')
                        img = Image.open(fd_img)
                        img = resizeimage.resize_crop(img, [180, 180])
                        img.save(thumb_file, img.format)
                        fd_img.close()                     
                                                        
                        return thumb_file
            except Exception as e:
                print("Unable to get album art: " + str(e))

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
