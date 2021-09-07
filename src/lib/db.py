import calendar
import logging
import sqlite3

from datetime import datetime
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

    def open_conn(self):
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
            db_conn.commit()
        except Error as e:
            LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")

        return db_conn

    def save_location(self, gps_info: dict):
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

                cursor.execute('''INSERT INTO gps_points VALUES (?, ?, ?, ?, ?);''', (timestamp,round(gps_info.lat, 6), round(gps_info.lon, 6), alt, speed))

                LOGGER.info(f"Storing GPS point {timestamp},{round(gps_info.lat, 6)},{round(gps_info.lon, 6)} as {cursor.lastrowid}")
                db_conn.commit()
                db_conn.close()

    def delete_table_contents(self, table:str):
        db_conn = self.open_conn()
        cursor = db_conn.cursor()
        cursor.execute(f"DELETE FROM {table}")

        LOGGER.info(f"Deleted contents of database tabe: {table}")
        db_conn.commit()
        db_conn.close()        

    def get_gps_log_summary(self) -> dict:
        """
        Get summary points of the GPS log

        :return: dict gps_log
        """
        db_conn = self.open_conn()
        cursor = db_conn.cursor()        
        db_sql = cursor.execute("SELECT * FROM gps_points")
        db_rows = [dict(row) for row in db_sql.fetchall()]
        alt_points, speed_points, distance, cur_lat, cur_lon = [], [], 0, None, None

        for row in db_rows:
            if cur_lat is not None and cur_lon is not None:
                distance += gps.get_distance(cur_lat, cur_lon, row['latitude'], row['longitude'])

            cur_lat, cur_lon = row['latitude'], row['longitude']

            if row.get('altitude', 0) > 0:
                alt_points.append(row['altitude'])
            if row.get('speed', 0) > 0:
                speed_points.append(row['speed'])

        gps_log = {
            'data_points' : len(alt_points) if len(alt_points) > 0 else 0,
            'max_alt' : max(alt_points) if len(alt_points) > 0 else 0 ,
            'avg_alt' : round(sum(alt_points) / len(alt_points)) if len(alt_points) > 0 else 0,
            'avg_speed' : round(sum(speed_points) / len(speed_points) if sum(speed_points) > 0 else 0),
            'distance' : round(distance, 2) if len(alt_points) > 0 else 0,
            'start_date' : datetime.fromtimestamp(db_rows[0].get('date')).strftime('%d/%m/%Y %H:%M') if len(alt_points) > 0 else "",
            'end_date' : datetime.fromtimestamp(db_rows[-1].get('date')).strftime('%d/%m/%Y %H:%M') if len(alt_points) > 0 else ""       
        }

        return gps_log
