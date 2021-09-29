import calendar
import logging
import sqlite3
import sys

import dateutil.parser as dp

import lib.gps as gps

LOGGER = logging.getLogger(__name__)

class NomadicDb():
    db_conn = None

    base_path = None

    def __init__(self, base_path):
        """
        :param: str base_path
        """
        self.base_path = base_path

        db_conn = self.open_conn()
        db_conn.close()

    def open_conn(self) -> None:
        """
        Open a connection to the SQLite database and create any missing DB tables

        :param: str base_path

        :return:
        """
        try:
            db_conn = sqlite3.connect(self.base_path + 'nomadicpi.db')
            db_conn.row_factory = sqlite3.Row

            cursor = db_conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS gps_points (date int, latitude real, longitude real, altitude int, speed int)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS mpd_history (date int, song_id int, title string, artist string)''')
            db_conn.commit()
        except Exception as e:
            LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")

        return db_conn

    def delete_table_contents(self, table: str) -> None:
        """
        Delete the contents of a database table

        :param: str table
        """
        db_conn = self.open_conn()
        cursor = db_conn.cursor()
        cursor.execute(f"DELETE FROM {table}")

        LOGGER.info(f"Deleted contents of database tabe: {table}")
        db_conn.commit()
        db_conn.close()

    def save_mpd_song(self, song_id: int, title: str, artist: str, playtime: str):
        """
        Saving a playing MPD track to the database

        :param: int song_id
        :param: str title
        :param: str artist
        :param: str playtime
        """
        db_conn = self.open_conn()
        cursor = db_conn.cursor()

        timestamp = calendar.timegm(dp.parse(playtime).timetuple())
        cursor.execute('''INSERT INTO mpd_history VALUES (?, ?, ?, ?);''', (timestamp, song_id, title, artist))

        LOGGER.info(f"Storing song history: {timestamp},{title},{artist} as {cursor.lastrowid}")
        (db_conn.commit()).close()

    def save_location(self, gps_info: dict) -> None:
        """
        Save the current location details to the database

        :param dict gps_info
        """
        if  hasattr(gps_info, 'mode') and isinstance(gps_info.mode, int) and gps_info.mode >= 2:
            if hasattr(gps_info, 'lat') and hasattr(gps_info, 'lon') and hasattr(gps_info, 'time'):
                db_conn = self.open_conn()
                cursor = db_conn.cursor()

                timestamp = calendar.timegm(dp.parse(gps_info.time).timetuple())

                if hasattr(gps_info, 'hspeed') and isinstance(gps_info.hspeed, float):
                    speed = gps.ms_kmh_coversion(gps_info.hspeed)
                else:
                    speed = 0

                if hasattr(gps_info, 'alt'):
                    alt = round(gps_info.alt)
                else:
                    alt = 0

                cursor.execute('''INSERT INTO gps_points VALUES (?, ?, ?, ?, ?);''', (timestamp, round(gps_info.lat, 6), round(gps_info.lon, 6), alt, speed))

                LOGGER.info(f"Storing GPS point {timestamp},{round(gps_info.lat, 6)},{round(gps_info.lon, 6)} as {cursor.lastrowid}")
                (db_conn.commit()).close()

    def get_gps_points(self) -> dict:
        """
        Get summary points of the GPS log

        :return: dict gps_log
        """
        db_conn = self.open_conn()
        cursor = db_conn.cursor()
        db_sql = cursor.execute("SELECT * FROM gps_points")
        db_rows = [dict(row) for row in db_sql.fetchall()]

        return db_rows

if __name__ == '__main__':
    print("This module cannot be run directly.")
    sys.exit()
