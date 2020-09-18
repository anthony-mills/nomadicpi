class NetworkStatus():

    def __init__(self, nomadic):
        self.nomadic = nomadic

        # Register the button actions on the network status page
        self.nomadic.ui.NetworkReturnHome.clicked.connect(self.nomadic.view_home_widget)
