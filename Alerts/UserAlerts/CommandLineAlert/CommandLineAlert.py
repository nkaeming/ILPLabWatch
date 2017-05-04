from Alerts.AbstractAlert import AbstractAlert
from datetime import datetime


class CommandLineAlert(AbstractAlert):
    """Diese Klasse gibt eine Nachricht auf der Konsole aus, sobald der Alert aufgerufen wird."""

    def __init__(self, alertID, settings):
        super().__init__(alertID, settings)

    # erzeugt einen neuen Alert in der Command Line.
    def throwAlert(self, port, trigger):
        """
        Erzeugt eine Nachricht auf der Kommandozeile.
        """
        portName = port.getName()
        portValue = port.getState()
        outputString = "Port Alert " + datetime.strftime('%A %d.%m %H:%M:%S') + "\n Name: " + portName + " \n Wert: " + str(portValue)
        if "message" in self.settings.keys():
            # TODO: Uncomment for Production.
            # pass
            print(outputString + " \n Nachricht: " + str(self.getSetting("message")))
        else:
            # pass
            print(outputString)

    def getDescription(self):
        return "Ein Kommandozeilen Alert, der beim Auslösen eine Meldung in der Konsole ausgibt."
