from Alerts.AbstractAlert import AbstractAlert
import time


class CommandLineAlert(AbstractAlert):
    """Diese Klasse gibt eine Nachricht auf der Konsole aus, sobald der Alert aufgerufen wird."""

    def __init__(self, alertID, settings):
        super().__init__(alertID, settings)

    # erzeugt einen neuen Alert in der Command Line.
    def throwAlert(self, port):
        portName = port.getName()
        portValue = port.getState()
        outputString = "Port Alert \n Name: " + portName + " \n Wert: " + str(portValue)
        if "message" in self.settings.keys():
            # TODO: Uncomment for Production.
            pass
            # print(outputString + " \n Nachricht: " + str(self.getSetting("message")))
        else:
            pass
            # print(outputString)

    # gibt die Beschreibung des Alerts aus.
    def getDescription(self):
        return "Ein Kommandozeilen Alert, der beim Auslösen eine Meldung in der Konsole ausgibt."
