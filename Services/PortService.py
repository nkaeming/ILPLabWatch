import importlib, uuid
from Models.Observable import Observable
from Models.Observer import Observer
from Models.PersistantObject import PersistantObject
from Ports.AbstractPort import AbstractPort


class PortService(Observable, Observer, PersistantObject):
    """Der Portservice verwaltet alle Ports."""
    # alle Ports
    ports = []

    triggerService = None

    def __init__(self):
        self.setUp()

    # setzte den Configfilename für den Service
    def getConfigFileName(self):
        return "portsConf.cfg"

    # setzt den TriggerService
    def setTriggerService(self, triggerService):
        self.triggerService = triggerService

    # erzeugt die Instanzen der Portklassen
    def setUp(self):
        conf = self.getConf()
        for portID, settings in conf.items():
            self.ports.append(self.generatePort(portID, settings))
        self.informObserver()

    # erzeugt einen neuen port und fügt ihn hinzu. Gibt die PortID zurück.
    def generateAndAddNewPort(self, settings):
        portID = str(uuid.uuid4())
        portInstance = self.generatePort(portID, settings)

        self.ports.append(portInstance)
        self.informObserver()

        # die Konfigurationsdatei neu schreiben
        self.writeConf()

        return portID

    # erzeugt eine Portinstanz, fügt sie allerdings nicht dem Service hinzu sondern gibt sie zurück.
    def generatePort(self, portID, settings):
        type = settings["type"]
        classPointer = getattr(importlib.import_module("Ports.UserPorts." + type + "." + type), type)
        return classPointer(settings, portID)

    # gibt eine Liste der Ports zurück. sortiert nach name oder durch den Parameter ordered = name, namedesc, logging, unit, logcycle oder logcycledesc
    def getPorts(self, ordered="name"):
        # TODO implement
        return self.ports

    # gibt die Portklasse zu einer PortID zurück.
    def getPortByID(self, portID):
        result = filter(lambda port: port.getID() == portID, self.ports)
        return next(result, None)

    # gibt die Portklasse zu einem Portnamen zurück
    def getPortByName(self, portName):
        result = filter(lambda port: port.getName() == portName, self.ports)
        return next(result, None)

    # gibt eine Liste aller Ports zurück die geloggt werden.
    def getPortsLogged(self):
        return list(filter(lambda port: port.isPortLogged() == True, self.ports))

    # gibt eine Liste mit allen Ports aus, die abgestürzt sind oder einen Internen Fehler beim Auslesen haben.
    def getInterruptPorts(self):
        return list(filter(lambda port: port.isPortOK() == False, self.ports))

    # wird aufgerufen, wenn eine Observable sich ändert. Hier z.B. die
    def observableChanged(self, observable):
        if issubclass(observable.__class__, AbstractPort):


    # schreibt die persistente Konfiguration.
    def writeConf(self):
        portList = self.getPorts()
        config = {}
        for port in portList:
            id = port.getID()
            settings = port.getSettings()
            config[id] = settings
        super().writeConf(config)
