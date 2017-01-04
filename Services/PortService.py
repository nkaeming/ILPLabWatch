import importlib, uuid, pkgutil
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
        classPointer = self.getPortClassByType(type)
        return classPointer(settings, portID)

    # gibt eine Liste der Ports zurück. Zulässig sind alle abstrakten settings (name, description, logCycle, logging und unit)
    def getPorts(self, setting="name", reverse=False):
        return sorted(self.ports, key=lambda port: port.getSetting(setting), reverse=reverse)

    def getPortsByType(self, type):
        """Gibt alle Ports zurück, welche einen bestimmten Typ haben."""
        result = filter(lambda port: port.getType() == type, self.getPorts())
        return list(result)

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

    # wird aufgerufen, wenn eine Observable sich ändert. Hier z.B. die Ports.
    def observableChanged(self, observable):
        # wenn sich ein Port verändert hat, dann könnten sich die Einstellungen geändert haben.
        if isinstance(observable, AbstractPort):
            self.writeConf()

    # schreibt die persistente Konfiguration. conf ist ein redundanter parameter und sollte nicht übergeben werden.
    def writeConf(self, conf=None):
        portList = self.getPorts()
        config = {}
        for port in portList:
            id = port.getID()
            settings = port.getSettings()
            config[id] = settings
        super().writeConf(config)

    def getCurrentPortsInformations(self):
        """Gibt alle aktuellen Informationen zu allen Ports als dict zurück."""
        status = {}
        for port in self.getPorts():
            status[port.getID()] = port.getCurrentInformations()
        return status

    def getPortTypes(self):
        """Gibt alle Porttypen zurück."""
        portTypes = []
        for portType in pkgutil.iter_modules(['Ports/UserPorts']):
            portTypes.append(portType[1])
        return portTypes

    def getConfigurablePortTypes(self):
        """Gibt alle Porttypen zurück, welche zurzeit freie Anschlüsse zum Konfigurieren haben."""
        availablePortTypes = []
        for portType in self.getPortTypes():
            classPointer = self.getPortClassByType(portType)
            availablePorts = len(classPointer.getInputs().keys())
            usedPorts = len(self.getPortsByType(portType))
            if availablePorts > usedPorts:
                availablePortTypes.append(portType)
        return availablePortTypes

    def getPortClassByType(self, portType):
        """Gibt einen Zeiger auf die Klasse zurück, welche den Prot definiert."""
        return getattr(importlib.import_module("Ports.UserPorts." + portType + "." + portType), portType)

    def getFreeInputsOfPortType(self, portType):
        """Gibt alle freien Anschlüsse eines Ports aus."""
        freeInputs = self.getPortClassByType(portType).getInputs()
        for port in self.getPortsByType(portType):
            freeInputs.pop(port.getPortBoxName())
        return freeInputs

    def doesPortExistByName(self, name):
        """Prüft ob ein Portname bereits existiert."""
        return len(list(filter(lambda port: port.getName() == name, self.getPorts()))) != 0
