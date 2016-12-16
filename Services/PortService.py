import importlib
import uuid
from IOHelper import config
from Models.Observable import Observable
from Models.Observer import Observer


class PortService(Observable, Observer):
    """Der Portservice verwaltet alle Ports."""
    # alle Ports
    ports = []

    # der verbundene TriggerService
    triggerService = None

    def __init__(self):
        self.setUpPorts()

    # setzt den TriggerService
    def setTriggerService(self, triggerService):
        self.triggerService = triggerService
        self.addObserver(triggerService)

    # erzeugt die Instanzen der Portklassen
    def setUpPorts(self):
        portConf = config.loadPorts()
        for portID, settings in portConf.items():
            self.ports.append(self.generatePort(portID, settings))
        self.informObserver()

    # erzeugt einen neuen port und fügt ihn hinzu. Gibt die PortID zurück.
    def generateAndAddNewPort(self, settings):
        portID = str(uuid.uuid4())
        portInstance = self.generatePort(portID, settings)
        self.ports.append(portInstance)
        # ein neuer Port wurde hinzugefügt.
        self.informObserver()
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

    # Geerbt von Observer
    def observableChanged(self, observable):
        # wird aufgerufen, wenn sich am Triggerservice etwas verändert.
        pass
