#The Port Service is a connector between the backend and all services that uses the port.
import importlib, os

import ConfModule.confAdapter as confAdapter
import Ports.abstractPort as abstractPort


class portService():
    portConfig = {}
    ports = {}
    statusLED = {}

    def __init__(self):
        self.portConfig = confAdapter.getPortsConf()
        self.portSetUp()

    #set up all the ports. This function should be called when the configuration changed.
    def portSetUp(self):
        self.ports = {}
        for port in self.portConfig.keys():
            type = self.portConfig[port]["type"]
            class_ = getattr(importlib.import_module("Ports.PortTypes." + type), type)
            portInstance = class_(port, self.portConfig[port])
            self.ports[port] = portInstance

    #returns a port object of the port.
    def getPort(self, externalPortNumber):
        return self.ports[externalPortNumber]

    #rteurns a list of all available PortTypes.
    def getPortTypesAvailable(self):
        availablePortTypes = []
        for item in os.listdir("Ports/portTypes"):
            if item.endswith(".py") and item != "__init__.py":
                availablePortTypes.append(str(item).split(".")[0])
        return availablePortTypes

    #returns a list of all ports that should be logged
    def getLoggedPorts(self):
        loggedPorts = []
        for port in self.getPorts():
            if self.getPort(port).getLoggingSetting() == True:
                loggedPorts.append(self.getPort(port))
        return loggedPorts

    #returns all ports that are in a logCycle that is seconds
    def getPortsLoggedIn(self, seconds):
        loggedPorts = self.getLoggedPorts()
        portsThatAreLogged = []
        for port in loggedPorts:
            if port.getLogCycle() == seconds:
                portsThatAreLogged.append(port)
        return portsThatAreLogged

    #returns all ports
    def getPorts(self):
        return self.ports

    #adds a port to the setUp
    def addPort(self, portType, settings, externalPort):
        if portType in self.getPortTypesAvailable():
            class_ = getattr(importlib.import_module("Ports.PortTypes." + portType), portType)
            settings["type"] = portType
            portInstance = class_(externalPort, settings)
            self.ports[externalPort] = portInstance
            confAdapter.addPort(self.ports[externalPort])
        else:
            raise FileNotFoundError("Dieser Porttyp (" + portType + ") wurde nich gefunden.")

    #delets a port from the setUp
    def deletePort(self, externalPortNumber):
        #TODO: implement
        return 0

    #returns true if a port already exists
    def doesPortExistByName(self, name):
        for port in self.ports.values():
            if port.getName() == name:
                return True
        return False

    #set the status LED's up.
    def setUpLEDs(self):
        pass

    # returns the description of a port Type.
    def getDescriptionOfPortType(self, type):
        class_ = getattr(importlib.import_module("Ports.PortTypes." + type), type)
        return class_.description

    # returns the options of a port type
    def getOptionsOfPortType(self, type):
        klasse = getattr(importlib.import_module("Ports.PortTypes." + type), type)
        options = {**klasse.options, **abstractPort.abstractPort.superOptions}
        return options

    # returns a dic of all available ports with informations
    def getAvailablePortsInformations(self):
        availablePorts = self.getPortTypesAvailable()
        availablePortsInformation = {}
        for port in availablePorts:
            availablePortsInformation[port] = {
                "description": self.getDescriptionOfPortType(port),
                "options": self.getOptionsOfPortType(port),
                #TODO: Diese Funktion hat massive Fehler verursacht. Bitte prüfen.
                "available": self.isPortTypeAvailable(port),
            }
        return availablePortsInformation

    # returns true if a port type is still available. That means a free internal Port in the wiring conf
    def isPortTypeAvailable(self, type):
        # first check if the wiringConf has some configuration for this port type.
        internalPorts = confAdapter.getInternalPorts(type)
        if internalPorts == {}:
            return False
        # check if there are free ports to configure
        for key in internalPorts.keys():
            if key not in self.getPorts().keys():
                return True
        return False

    # returns a list of all free external Ports.
    def getFreeExternalPorts(self, type):
        internalPorts = confAdapter.getInternalPorts(type)
        freePorts = []
        for key in internalPorts.keys():
            if key not in self.getPorts().keys():
               freePorts.append(key)
        return freePorts

    # returns true if an external Port is free
    def isExternalPortFree(self, externalPort):
        return not externalPort in self.portConfig.keys()