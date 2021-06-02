import logging

import lib.gps as gps

LOGGER = logging.getLogger(__name__)

class LocationStatus():
    gps_status = None

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register the button actions on the location status page
        self.nomadic.ui.LocationReturnHome.clicked.connect(self.nomadic.view_home_widget)

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
                LOGGER.error(str(e))

        self.gps_status = gps.get_current()

        # Load content areas
        self.gps_satellites()
        self.gps_fix_type()
        self.gps_location()

    def gps_location(self):
        """
        Display the current GPS location details
        """
        if hasattr(self.gps_status, 'lat') and hasattr(self.gps_status, 'error') and isinstance(self.gps_status.error, dict) and 'y' in self.gps_status.error:
            self.nomadic.ui.CurLat.setText(f"Latitude: {self.gps_status.lat} ( Accuracy +/- {self.gps_status.error['y']}m )")
        else:
            self.nomadic.ui.CurLat.setText(f"Latitude: Unknown")

        if hasattr(self.gps_status, 'lon') and hasattr(self.gps_status, 'error') and isinstance(self.gps_status.error, dict) and 'x' in self.gps_status.error:
            self.nomadic.ui.CurLong.setText(f"Longitude: {self.gps_status.lon} ( Accuracy +/- {self.gps_status.error['x']}m )")
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
