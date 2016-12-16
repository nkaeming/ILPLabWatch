from Alerts.AbstractAlert import AbstractAlert


class CommandLineAlert(AbstractAlert):
    """Diese Klasse gibt eine Nachricht auf der Konsole aus, sobald der Alert aufgerufen wird."""

    def __init__(self, settings):
        super().__init__(settings)

    # erzeugt einen neuen Alert in der Command Line.
    def throwAlert(self, port):
        portName = port.getName()
        portValue = port.getState()
        outputString = "Port Alert \n Name: " + portName + " \n Wert: " + str(portValue)
        if "userMessage" in self.settings.keys():
            print(outputString + " \n Nachricht: " + str(self.getSetting["message"]))
        else:
            print(outputString)
