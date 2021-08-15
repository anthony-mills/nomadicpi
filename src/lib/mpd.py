import os.path
import sys
import logging
import musicbrainzngs
import urllib.request

from mpd import MPDClient

LOGGER = logging.getLogger(__name__)

class MpdLib():
    """
    Handle functionality related to MPD communication in the player
    """

    # Default image to display when album art is not found
    not_found = "not_found.png"

    # Default IP of the MPD server
    mpd_host = '127.0.0.1'

    # Default port the MPD service is running on
    mpd_port = 6600

    # Default directory for storing album art
    art_cache = '/tmp/'

    def __init__(self):
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

        try:
            self.client.connect(self.mpd_host, self.mpd_port)
        except Exception as e:
            LOGGER.critical("MPD Error: Cannot connect to the MPD daemon.")
            sys.exit(1)

    def update_status(self):
        """
        Update the status of the mpd daemon

        Returns
        -------
        dict
            Dictionary of values concerning the current state of the MPD daemon
        """
        self.mpd_status = self.client.status()

        return self.mpd_status

    def get_status(self):
        """
        Return the status of the mpd daemon

        Returns
        -------
        dict
            Dictionary of values concerning the current state of the MPD daemon
        """
        return self.mpd_status

    def play_playback(self):
        """
        Change the play state
        """
        status = self.get_status()

        if status.get('state') == 'play':
            self.client.pause()
        else:
            self.client.play()

    def update_library(self):
        """
        Update the MPD library
        """
        status = self.get_status()

        if status.get('updating_db') is None:
            self.client.update()

    def random_playback(self):
        """
        Change the random playback state
        """
        status = self.get_status()

        if int(status['random']) == 0:
            self.client.random(1)
        else:
            self.client.random(0)

    def stop_playback(self):
        """
        Stop MPD playback
        """
        self.client.stop()

    def mpd_stats(self):
        """
        Return stats about the MPD daemon; uptime, size of music db etc
        """
        return self.client.stats()

    def playlist_contents(self):
        """
        Return contents of the current playlist

        :param: int
        :return: array
        """
        return self.client.playlistinfo()

    def playlist_info(self, item_id=None):
        """
        Return stats about the current playlist

        :param: int
        :return: array
        """
        return self.client.playlistinfo(item_id)

    def next_song(self):
        """
        Skip playback to the next song
        """
        self.client.next()

    def play_song(self, song_id):
        """
        Play a song via its MPD id

        :param: int
        """
        self.client.playid(song_id)

    def remove_song(self, song_id):
        """
        Remove a song from the current playlist via its MPD id

        :param: int
        """
        self.client.deleteid(song_id)

    def wipe_playlist(self):
        """
        Wipe the current playlist
        """
        self.client.clear()

    def add_to_playlist(self, path):
        """
        Add file or directory to the current playlist

        Params
        -------
        string
            Directory or File Path to add
        """
        try:
            self.client.add(path)
        except Exception as e:
            LOGGER.error("Unable to add path to MPD: " + str(path) + " - " + str(e))

    def ls_mpd_path(self, file_path=None):
        """
        List the contents of an MPD path

        Params
        -------
        string
            File System Path on the MPD filesystem

        Returns
        -------
        dict
            Dictionary of items / folders located under the requested path
        """
        try:
            if isinstance(file_path, str):
                path_contents = self.client.lsinfo(file_path)
            else:
                path_contents = self.client.lsinfo()
            return path_contents
        except Exception as e:
            LOGGER.error("Unable to read contents of path: " + str(file_path) + " - " + str(e))

    def currently_playing(self):
        """
        Return information about the current song playing

        Returns
        -------
        dict
            Dictionary of values concerning the current state of the MPD daemon
        """
        status = self.get_status()

        if status['state'] == 'play':
            return self.client.currentsong()
        return {}

    def album_art(self, search_term, cache_key):
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
            logging.debug(f"Found album art with cache key: {cache_key}.")

            return self.art_cache + str(cache_key)
        else:
            try:
                mb_search = musicbrainzngs.search_release_groups(search_term)

                logging.debug(f"Trying to query music branz album art with search term: {search_term}.")

                if isinstance(mb_search['release-group-list'][0]['id'], str):
                    image_list = musicbrainzngs.get_release_group_image_list(mb_search['release-group-list'][0]['id'])
                    if isinstance(image_list['images'][0]['thumbnails']['small'], str):
                        thumb_file = self.art_cache + str(cache_key)
                        urllib.request.urlretrieve(image_list['images'][0]['thumbnails']['small'], thumb_file)

                        return thumb_file
            except Exception as e:
                logging.debug("Unable to get album art: " + str(e))

        return self.art_cache + str(self.not_found)

    def current_song_title(self, status):
        """
        Return the current song being played
        """
        cur_song = status.get('song', None)

        if isinstance(status['song'], str):
            song_dets = self.playlist_info(status['song'])

            if len(song_dets) == 1:
                return f"Playing: {song_dets[0].get('artist', 'Unknown')}\n {song_dets[0].get('title', 'Unknown')}"

        return ""

    def next_song_title(self, status):
        """
        Return the next song to be played
        """
        if isinstance(status['nextsong'], str):
            next_up = self.playlist_info(status['nextsong'])

            if len(next_up) == 1:
                return f"Next: {next_up[0].get('artist', 'Unknown')}\n {next_up[0].get('title', 'Unknown')}"

        return ""

    def consumption_playback(self):
        """
        Change the consume playback state
        """
        status = self.get_status()

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
