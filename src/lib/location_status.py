class LocationStatus():

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register the button actions on the location status page
        self.nomadic.ui.LocationReturnHome.clicked.connect(self.nomadic.view_home_widget)
