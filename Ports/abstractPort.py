#Abstract port already implements all neccessary funcitons to deal with ports. The real functionality of the ports is implemented in the ports classes which are child classes of the abstract port.
import ConfModule.confAdapter as confAdapter
import LogModule.logWriter as logWriter

class abstractPort():
    #the Port Number on the Connector Box
    externalNumber = 0
    #The internal Rasberry Pi Port.
    internalPort = 0
    #is input Port
    inputPort = False
    #the settings of the Port.
    settings = {}
    #super Options
    superOptions = {
        "name": {
            "type": "text",
            "tab": -4,
            "name": "Portbezeichnung",
            "description": "Der Name des Ports bestehend aus a-z, A-Z und 0-9. Keine Leer- oder Sonderzeichen.",
            "standard": ""
        },
        "logCycle": {
            "type": "number",
            "name" : "Logintervall",
            "description": "Das Loginterval in Sekunden",
            "standard": 5,
            "min": 1,
            "max": 3600,
            "step": 1,
            "tab": -2
        },
        "logging": {
            "type": "boolean",
            "name": "Logging",
            "description": "Wenn diese Einstellung aus ist, so wird der Port nicht geloggt.",
            "standard": 1,
            "tab": -3
        },
        "alertValues": {
            "name": "Schwellwerte",
            "type": "multipleRangeSelect",
            "description": "Alle ausgewählten Wertebereiche lösen Alerts aus. Diese können später zugewiesen werden.",
            "standard": {},
            "tab": -1
        }
    }


    #initialise the Instance and Class Constants
    def __init__(self, externalNumber):
        self.externalNumber = externalNumber
        self.internalPort = confAdapter.getInternalPort(self.getType(), externalNumber)

    def getExternalPort(self):
        return self.externalNumber

    def getInternalPort(self):
        return self.internalPort

    def getName(self):
        return self.settings["name"]

    def getType(self):
        return self.__class__.__name__

    def getLogCycle(self):
        return self.settings["logCycle"]

    #The logging setting is true if the port is monitored by the logging protocols.
    def getLoggingSetting(self):
        return self.settings["logging"]

    #writes the state of the port in the log file.
    def writeLog(self):
        logWriter.writeLog(self)

    #returns true if the port is an input port
    def isInputPort(self):
        return self.inputPort

    #retuns the description of a port. Should be implemented in the child class
    def getDescription(self):
        pass

    #returns the state of a port. has to be implemented in child class
    def getState(self):
        pass

    def getCurrentInformation(self):
        info = {}
        info["port"] = self.externalNumber
        info["name"] = self.getName()
        info["type"] = self.__class__.__name__
        info["logging"] = self.getLoggingSetting()
        info["logCycle"] = self.getLogCycle()
        info["description"] = self.getDescription()
        info["state"] = self.getState()
        return info

    # returns the possible options of the Port.
    def getOptions(self):
        return self.options

    # returns all settings related to the port.
    def getSettings(self):
        return self.settings

    # returns the range of available Values (important for charts and alerts). The return is a list with the format: [lowest,highest,step]
    def getValueRange(self):
        pass