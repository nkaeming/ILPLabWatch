# an alert is called when a port is in the alert area.
class abstractAlert:

    # called by the Deamon when a critical value is reached.
    def throwAlert(self, port):
        pass

    # returns the description of an alert
    def getDescription(self):
        pass