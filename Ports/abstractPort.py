#Abstract port already implements all neccessary funcitons to deal with ports. The real functionality of the ports is implemented in the ports classes which are child classes of the abstract port.
import ConfModule.confAdapter as confAdapter
import LogModule.logWriter as logWriter

class abstractPort():
    #the Port Number on the Connector Box
    externalNumber = 0
    #The internal Rasberry Pi Port Object
    internalPort = 0
    #the display Name
    name = ""
    #the Logging Cycle in seconds
    logCycle = 0
    #is logging enabled
    logging = True
    #is input Port
    inputPort = False


    #initialise the Instance and Class Constants
    def __init__(self, externalNumber, settings):
        self.externalNumber = externalNumber
        self.internalPort = confAdapter.getInternalPort(self.getType(), externalNumber)
        self.name = settings["name"]
        self.logCycle = settings["logCycle"]
        self.logging = settings["logging"]

    def getExternalPort(self):
        return self.externalNumber

    def getInternalPort(self):
        return self.internalPort

    def getName(self):
        return self.name

    def getType(self):
        return self.__class__.__name__

    def getLogCycle(self):
        return self.logCycle

    #The logging setting is true if the port is monitored by the logging protocols.
    def getLoggingSetting(self):
        return self.logging

    #writes the state of the port in the log file.
    def writeLog(self):
        logWriter.writeLog(self)

    #returns true if the port is an input port
    def isInputPort(self):
        return self.inputPort

    #retuns the description of a port. Should be implemented in the child class
    def getDescription(self):
        ...

    #returns the state of a port. has to be implemented in child class
    def getState(self):
        ...

    def getCurrentInformation(self):
        info = {}
        info["port"] = self.externalNumber
        info["name"] = self.name
        info["type"] = self.__class__.__name__
        info["logging"] = self.logging
        info["logCycle"] = self.logCycle
        info["description"] = self.getDescription()
        info["state"] = self.getState()
        return info