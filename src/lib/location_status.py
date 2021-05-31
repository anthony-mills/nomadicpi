import lib.gps as gps

import datetime
import logging

logger = logging.getLogger(__name__)

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
                logger.error(str(e))
                
        self.gps_status = gps.get_current()
                
        # Load content areas
        self.gps_satellites()
        self.gps_fix_type() 
        self.gps_location()  

    def gps_location(self):
        """
        Display the current GPS location details
        """        
        if isinstance(self.gps_status.lon, float) and isinstance(self.gps_status.lat, float):
            self.nomadic.ui.CurCoordinates.setText(f"Coordinates: {self.gps_status.lat}, {self.gps_status.lon}") 

        if isinstance(self.gps_status.alt, float):
            altitude = (f"Altitude: {self.gps_status.alt}m")
            
            if 'v' in self.gps_status.error:
                altitude += (f" (Accuracy +/- {self.gps_status.error['y']}m)")
            
            self.nomadic.ui.CurAltitude.setText(altitude) 
        else:
            self.nomadic.ui.CurAltitude.setText(f"Altitude: Unknown")
                         
        if 'x' in self.gps_status.error and 'y' in self.gps_status.error:
            self.nomadic.ui.LocationPrecision.setText(f"Location Accuracy: Latitude {self.gps_status.error['y']}m, Longitude {self.gps_status.error['x']}m")
        else:
            self.nomadic.ui.LocationPrecision.setText(f"Location Accuracy: Unknown")

        heading = self.nomadic.gps_info.movement()       
        if 'track' in heading and 'direction' in heading:
            self.nomadic.ui.GpsHeading.setText(f"Heading: {heading['direction']} ( {round(heading['track'])} degrees )")             
        else:
            self.nomadic.ui.GpsHeading.setText("Heading: Unknown")            

        gps_time = self.nomadic.gps_info.get_time(True);
        if isinstance(self.gps_status.time, str):
            self.nomadic.ui.LocalTime.setText(f"Time: {gps_time}")                
        else:
            self.nomadic.ui.LocalTime.setText("Time: Unknown")   

        if isinstance(self.gps_status.hspeed, float):
            self.nomadic.ui.HorizontalSpeed.setText(f"Speed: {round(self.gps_status.hspeed)} m/s")                
        else:
            self.nomadic.ui.HorizontalSpeed.setText("Speed: Unknown") 

        if isinstance(self.gps_status.climb, int):
            self.nomadic.ui.VerticalSpeed.setText(f"Climb: {self.gps_status.climb} m/s")                
        else:
            self.nomadic.ui.VerticalSpeed.setText("Climb: Unknown") 
                        
    def gps_fix_type(self):
        """
        Display the current GPS fix type
        """        
        if isinstance(self.gps_status.mode, int):
            fix = 'No Fix'            
            
            if (self.gps_status.mode == 2):
                fix = '2D Fix'
            elif (self.gps_status.mode == 3):
                fix = '3D Fix'            

            self.nomadic.ui.GpsFixType.setText(f"Fix Type: {fix}")            
        else:
            self.nomadic.ui.GpsSatellites.setText("Fix Type: No GPS connection.")            

    def gps_satellites(self):
        """
        Add count of currently visible GPS satellites
        """
        if isinstance(self.gps_status.sats, int):
            self.nomadic.ui.GpsSatellites.setText(f"Visible Satellites: {self.gps_status.sats}")
            
        if isinstance(self.gps_status.sats_valid, int):
            self.nomadic.ui.GpsSatellitesUsed.setText(f"Used Satellites: {self.gps_status.sats_valid}")
