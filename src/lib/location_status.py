"""
Handle actions related to the location status page.
"""
import logging
import sys
from datetime import datetime
from os.path import expanduser
import gpxpy
import gpxpy.gpx

import lib.gps as gps

from PyQt5.QtWidgets import QFileDialog

LOGGER = logging.getLogger(__name__)

class LocationStatus():
    gps_status = None

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register the button actions on the location status page
        self.nomadic.ui.LocationReturnHome.clicked.connect(self.nomadic.view_home_widget)
        self.nomadic.ui.ResetTripLogButton.clicked.connect(self.reset_trip_log)
        self.nomadic.ui.ExportGPSLogButton.clicked.connect(self.export_gps_log)

    def update_page(self):
        """
        Update the location details page
        """
        if gps.gpsd_socket is None:
            try:
                gpsd_host = self.nomadic.app_config['gpsd'].get('Host', 'localhost')
                gpsd_port = int(self.nomadic.app_config['gpsd'].get('Port', '2947'))
                gps.gps_connect(host=gpsd_host, port=gpsd_port)

            except Exception as e:
                LOGGER.error(f"Line: {sys.exc_info()[-1].tb_lineno}: {e}")

        self.gps_status = gps.get_current()

        # Load content areas
        self.gps_satellites()
        self.gps_fix_type()
        self.gps_location()
        self.gps_log()

    def reset_trip_log(self):
        """
        Reset the trip log
        """
        self.nomadic.db.delete_table_contents("gps_points")

        self.nomadic.ui.GPSLogPoints.clear()
        self.nomadic.ui.GPSLogDistance.clear()
        self.nomadic.ui.GPSLogMaxAltitude.clear()
        self.nomadic.ui.GPSLogAvgAltitude.clear()
        self.nomadic.ui.GPSLogAvgSpeed.clear()
        self.nomadic.ui.GPSLogDateRange.clear()

    def gps_log(self):
        """
        Display information from the computer GPS log
        """
        db_rows = self.nomadic.db.get_gps_points()

        alt_points, speed_points, distance, cur_lat, cur_lon = [], [], 0, None, None

        for row in db_rows:
            if cur_lat is not None and cur_lon is not None:
                distance += gps.get_distance(cur_lat, cur_lon, row['latitude'], row['longitude'])

            cur_lat, cur_lon = row['latitude'], row['longitude']

            if row.get('altitude', 0) > 0:
                alt_points.append(row['altitude'])
            if row.get('speed', 0) > 0:
                speed_points.append(row['speed'])

        start_date = datetime.fromtimestamp(db_rows[0].get('date')).strftime('%d/%m/%Y %H:%M') if len(alt_points) > 0 else ""
        end_date = datetime.fromtimestamp(db_rows[-1].get('date')).strftime('%d/%m/%Y %H:%M') if len(alt_points) > 0 else ""

        self.nomadic.ui.GPSLogPoints.setText(f"Data Points: {len(alt_points) if len(alt_points) > 0 else 0}")
        self.nomadic.ui.GPSLogDistance.setText(f"Distance: {round(distance, 2) if len(alt_points) > 0 else 0} km")
        self.nomadic.ui.GPSLogMaxAltitude.setText(f"Max Altitude: {max(alt_points) if len(alt_points) > 0 else 0} m")
        self.nomadic.ui.GPSLogAvgAltitude.setText(f"Avg Altitude: {round(sum(alt_points) / len(alt_points)) if len(alt_points) > 0 else 0} m")
        self.nomadic.ui.GPSLogAvgSpeed.setText(f"Avg Speed: {round(sum(speed_points) / len(speed_points)) if sum(speed_points) > 0 else 0} km/h")
        self.nomadic.ui.GPSLogDateRange.setText(f"Period: {start_date} - {end_date}")

    def export_gps_log(self):
        """
        Write the stored GPS points to a GPX file
        """
        gpx = gpxpy.gpx.GPX()

        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        db_rows = self.nomadic.db.get_gps_points()

        for row in db_rows:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(row['latitude'], row['longitude'], elevation=row['altitude'], speed=row['speed']))

        dir_path= QFileDialog.getExistingDirectory(None,"Select folder", expanduser("~"), QFileDialog.ShowDirsOnly)

        try:
            filename = f"{dir_path}/gps_log_export_{(datetime.today().date()).isoformat()}.gpx"

            gpx_file = open(filename, "w+")
            gpx_file.write(gpx.to_xml())
            gpx_file.close()

            LOGGER.info(f"Exported stored GPS data to: {filename}")
        except Exception as e:
                LOGGER.error(f"Error saving GPS export: {e}")

    def gps_location(self):
        """
        Display the current GPS location details
        """
        if hasattr(self.gps_status, 'lat') and hasattr(self.gps_status, 'error') and isinstance(self.gps_status.error, dict) and 'y' in self.gps_status.error:
            self.nomadic.ui.CurLat.setText(f"Latitude: {round(self.gps_status.lat, 6)} ( Accuracy +/- {self.gps_status.error['y']}m )")
        else:
            self.nomadic.ui.CurLat.setText(f"Latitude: Unknown")

        if hasattr(self.gps_status, 'lon') and hasattr(self.gps_status, 'error') and isinstance(self.gps_status.error, dict) and 'x' in self.gps_status.error:
            self.nomadic.ui.CurLong.setText(f"Longitude: {round(self.gps_status.lon, 6)} ( Accuracy +/- {self.gps_status.error['x']}m )")
        else:
            self.nomadic.ui.CurLong.setText(f"Longitude: Unknown")

        if hasattr(self.gps_status, 'alt'):
            altitude = (f"Altitude: {self.gps_status.alt}m")

            if 'v' in self.gps_status.error:
                altitude += (f" ( Accuracy +/- {self.gps_status.error['y']}m )")

            self.nomadic.ui.CurAltitude.setText(altitude)
        else:
            self.nomadic.ui.CurAltitude.setText(f"Altitude: Unknown")

        if hasattr(self.gps_status, 'movement'):
            status = self.gps_status.movement()

            if 'track' in status and 'direction' in status:
                self.nomadic.ui.GpsHeading.setText(f"Heading: {status['direction']} ( {round(status['track'])} degrees )")
            else:
                self.nomadic.ui.GpsHeading.setText("Heading: Unknown")

            if 'local_time' in status:
                self.nomadic.ui.LocalTime.setText(f"Local Time: {status['local_time']}")
            else:
                self.nomadic.ui.LocalTime.setText("Local Time: Unknown")

            if 'utc_time' in status:
                self.nomadic.ui.UtcTime.setText(f"UTC Time: {status['utc_time']}")
            else:
                self.nomadic.ui.UtcTime.setText("UTC Time: Unknown")
        else:
            self.nomadic.ui.GpsHeading.setText("Heading: Unknown")
            self.nomadic.ui.LocalTime.setText("Local Time: Unknown")
            self.nomadic.ui.UtcTime.setText("UTC Time: Unknown")

        if hasattr(self.gps_status, 'hspeed') and isinstance(self.gps_status.hspeed, float):
            self.nomadic.ui.HorizontalSpeed.setText(f"Speed: {gps.ms_kmh_coversion(self.gps_status.hspeed)} km/h ( {round(self.gps_status.hspeed)} m/s )")
        else:
            self.nomadic.ui.HorizontalSpeed.setText("Speed: Unknown")

        if hasattr(self.gps_status, 'climb') and isinstance(self.gps_status.climb, int):
            self.nomadic.ui.VerticalSpeed.setText(f"Climb: {self.gps_status.climb} m/s")
        else:
            self.nomadic.ui.VerticalSpeed.setText("Climb: Unknown")

    def gps_fix_type(self):
        """
        Display the current GPS fix type
        """
        if  hasattr(self.gps_status, 'mode') and isinstance(self.gps_status.mode, int):
            fix = 'No Fix'

            if self.gps_status.mode == 2:
                fix = '2D Fix'
            elif self.gps_status.mode == 3:
                fix = '3D Fix'

            self.nomadic.ui.GpsFixType.setText(f"Fix Type: {fix}")
        else:
            self.nomadic.ui.GpsFixType.setText("Fix Type: No GPS connection.")

    def gps_satellites(self):
        """
        Add count of currently visible GPS satellites
        """
        if hasattr(self.gps_status, 'sats') and hasattr(self.gps_status, 'sats_valid'):
            self.nomadic.ui.GpsSatellites.setText(f"GPS Satellites: {self.gps_status.sats} visible / {self.gps_status.sats_valid} used")
        else:
            self.nomadic.ui.GpsSatellites.setText(f"GPS Satellites: 0 visible / 0 used")
