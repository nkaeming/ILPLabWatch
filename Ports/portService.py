#The Port Service is a connector between the backend and all services that uses the port.
import importlib

import ConfModule.confAdapter as confAdapter
import Ports.PortTypes.DigitalOutputPort as DigitalOutputPort


class portService():
    portConfig = {}
    ports = {}
    statusLED = {}

    def __init__(self):
        self.portConfig = confAdapter.getPortsConf()
        self.portSetUp()

    #set up all the ports. This function should be called when the configuration changed.
    def portSetUp(self):
        for port in self.portConfig:
            type = self.portConfig[port]["type"]
            class_ = getattr(importlib.import_module("Ports.PortTypes." + type), type)
            portInstance = class_(port, self.portConfig[port])
            self.ports[int(port)] = portInstance

    #returns a port object of the port.
    def getPort(self, externalPortNumber):
        return self.ports[externalPortNumber]

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
    def addPort(self, port):
        #TODO: implement
        return 0

    #delets a port from the setUp
    def deletePort(self, externalPortNumber):
        #TODO: implement
        return 0

    def setUpLEDs(self):
        statusLED = DigitalOutputPort.DigitalOutputPort("statusLED", {})
        warnLED = DigitalOutputPort.DigitalOutputPort("warnLED", {})
