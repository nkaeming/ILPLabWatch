import importlib, uuid, pkgutil
import IOHelper.config as configIO
from Models.Observable import Observable
from Models.Observer import Observer
from Models.PersistantObject import PersistantObject
from Ports.AbstractPort import AbstractPort
from Services.TriggerService import TriggerService


class PortService(Observable, Observer, PersistantObject):
    """Der Portservice ist der zentrale Service für die Ports. Er verwaltet sie, erstellt sie und ist die einzige Scnittstelle zu anderen Programmteilen der in der Lage ist Referenzen auf die Ports zurück zu geben. Im System soll es nur einen Portservice geben."""
    # alle Ports
    ports = []

    TriggerService = None

    def __init__(self):
        self.setUp()

    # setzte den Configfilename für den Service
    def getConfigFileName(self):
        """
        Gibt den Namen der Konfigurationsdatei zurück.
        :return: der Dateiname der Konfigurationsdatei
        :type str
        """
        return "portsConf.cfg"

    def setTriggerService(self, triggerService):
        """
        Legt den TriggerService fest. Es handelt sich um eine DependencyInjection. 
        :param triggerService: Der Triggerservice mit dem der Portservice zusammenarbeiten soll.
        :type triggerService: TriggerService
        """
        self.TriggerService = triggerService

    def setUp(self):
        """
        Erzeugt die Instanzen der Portklassen. Wird immer vom Konstruktor aufgerufen und ist eine private Hilfsfunktion.
        """
        conf = self.getConf()
        for portID, settings in conf.items():
            self.ports.append(self.generatePort(portID, settings))
        self.informObserver()

    def generateAndAddNewPort(self, settings):
        """
        Erzeugt eine neue Portinstanz und füt diese dem Service hinzu.
        :param settings: Die Einstellungen des neuen Ports.
        :type settings: dict
        :return: Die PortID des erstellten Ports
        :type str
        """
        portID = str(uuid.uuid4())
        portInstance = self.generatePort(portID, settings)
        portInstance.addObserver(self)

        self.ports.append(portInstance)
        self.informObserver()

        # die Konfigurationsdatei neu schreiben
        self.writeConf()

        return portID

    def generatePort(self, portID, settings):
        """
        Erzeugt eine Portinstanz und fügt diese nicht dem PortService hinzu. Gibt die Instanz stattdessen zurück. Vergleicbar mit einer Fabrikmethode. 
        :param portID: die ID die der Port erhalten soll.
        :param settings: Die Einstellungen des Ports.
        :return: Die Instanz des Ports.
        :type AbstractPort
        """
        type = settings["type"]
        classPointer = self.getPortClassByType(type)
        port = classPointer(settings, portID)
        return port

    # gibt eine Liste der Ports zurück. Zulässig sind alle abstrakten settings (name, description, logCycle, logging und unit)
    def getPorts(self, setting="name", reverse=False):
        """
        Gibt eine sortierte Liste der Ports zurück.
        :param setting: das Merkmal nach dem sortiert werden soll.
        :type setting: str
        :param reverse: Gibt an ob die Liste in die gegensätzliche Richtung sortiert werden soll.
        :return: eine sortierte Liste von Ports
        :type list
        """
        return sorted(self.ports, key=lambda port: port.getSetting(setting), reverse=reverse)

    def getPortsByType(self, type):
        """
        Gibt die Ports eines bestimmten Typs zurück.
        :param type: der Typ des Ports.
        :type type: str
        :return: eine unsortierte Liste von Ports.
        :type list
        """
        result = filter(lambda port: port.getType() == type, self.getPorts())
        return list(result)

    def getPortByID(self, portID):
        """
        Gibt die Instanz eines Ports nach seiner ID zurück.
        :param portID: die ID des Ports.
        :type portID: str
        :return: eine Portklasse die zu der ID gehört. Existiert der Port nicht im Service, so wird None zurückgegeben.
        :type AbstractPort
        """
        result = filter(lambda port: port.getID() == portID, self.ports)
        return next(result, None)

    def getPortByName(self, portName):
        """
        Gibt die Instanz eines Ports nach seinem Namen zurück.
        :param portName: der Name des Ports
        :type portName: str
        :return: eine Portklasse die zu dem Namen gehört. Existiert der Port nicht im Service, so wird None zurückgegeben.
        :type AbstractPort
        """
        result = filter(lambda port: port.getName() == portName, self.ports)
        return next(result, None)

    def getPortsLogged(self):
        """
        Gibt eine Liste der Ports zurück die geloggt werden.
        :return: Eine unsortierte Liste von Ports.
        :type list
        """
        return list(filter(lambda port: port.isPortLogged() == True, self.ports))

    def getInterruptPorts(self):
        """
        Gibt eine Liste der Ports zurück die nicht mehr ordnungsgemäß ausgeführt werden.
        :return: eine unsortierte Liste von Prots
        :type list
        """
        return list(filter(lambda port: port.isPortOK() == False, self.ports))


    def observableChanged(self, observable):
        """
        Wird ausgerufen wenn eine Observable sich geändert hat. Geerbt von Observer.        
        :param observable: die Observable die sich geändert hat.
        :type observable: Observable
        """
        # wenn sich ein Port verändert hat, dann könnten sich die Einstellungen geändert haben.
        if isinstance(observable, AbstractPort):
            self.writeConf()

    def writeConf(self, conf=None):
        """
        Schreibt die persistente Konfiguration.
        :param conf: ein redundanter Parameter. Aus technsichen Gründen in Python ist darauf nicht zu verzichten.
        :type conf: None
        """
        portList = self.getPorts()
        config = {}
        for port in portList:
            id = port.getID()
            settings = port.getSettings()
            config[id] = settings
        super().writeConf(config)

    def getCurrentPortsInformations(self):
        """
        Gibt alle aktuellen Informationen zu allen Ports als dict zurück. Dies ist z.B. für die Benutzeroberfläche relevant.
        :return: eine Sammlung aller Informationen zu den aktuellen Ports.
        :type dict
        """
        status = {}
        for port in self.getPorts():
            status[port.getID()] = port.getCurrentInformations()
        return status

    def getPortTypes(self):
        """
        Gibt alle verfügbaren PortTypen zurück.
        :return: eine Liste aller Porttypen als Module.
        :type list
        """
        portTypes = []
        for portType in pkgutil.iter_modules(['Ports/UserPorts']):
            portTypes.append(portType[1])
        return portTypes

    def getConfigurablePortTypes(self):
        """
        Gibt alle Porttypen zurück, welche einen freien Anschluss zum Konfigurieren haben.
        :return: Eine Liste der Porttypen
        :type list
        """
        availablePortTypes = []
        for portType in self.getPortTypes():
            if portType in configIO.loadWiring().keys():
                classPointer = self.getPortClassByType(portType)
                availablePorts = len(classPointer.getInputs().keys())
                usedPorts = len(self.getPortsByType(portType))
                if availablePorts > usedPorts:
                    availablePortTypes.append(portType)
        return availablePortTypes

    def getPortClassByType(self, portType):
        """
        Gibt einen Zeiger auf die Klasse zurück die den Port definiert.
        :param portType: Der Typ des Ports.
        :type portType: str
        :return: Ein Class-Objekt auf die Klasse des Ports.
        :type AbstractPort
        """
        return getattr(importlib.import_module("Ports.UserPorts." + portType + "." + portType), portType)

    def getFreeInputsOfPortType(self, portType):
        """
        Gibt die freien Anschlüsse eines Porttypen aus.
        :param portType: Der Typ des Ports.
        :type portType: str
        :return: Ein dict mit allen freien Anschlüssen.
        :type dict
        """
        freeInputs = self.getPortClassByType(portType).getInputs()
        for port in self.getPortsByType(portType):
            freeInputs.pop(port.getPortBoxName())
        return freeInputs

    def doesPortExistByName(self, name):
        """
        Prüft ob der Name eines Ports existiert.
        :param name: Der Name des Ports.
        :type name: str
        :return: true, wenn ein Port mit diesem Namen existiert.
        :type bool
        """
        return len(list(filter(lambda port: port.getName() == name, self.getPorts()))) != 0

    def removePort(self, port):
        """
        Löscht einen Port aus dem Service. Er wird bei erneuten starten auch nicht geladen. Die Überwachung des Ports wird vollständig beendet.
        :param port: Der Port der gelöscht werden soll.
        :type port: AbstractPort
        """
        port.removeAllObservers()
        self.TriggerService.removeTriggersByPort(port)
        port.stopThreads()
        self.ports.remove(port)
        self.writeConf()

    def arePortsOK(self):
        """
        Gibt true zurück, wenn alle Ports keine Fehler haben und auch keine WarnTrigger ausgelöst sind. Methode kann z.B. für die WarnLED benutzt werden. Sie ist ein Indikator für die Systemgesundheit und die Gesundheit der zu überwachenden Peripherie.
        :return: true, wenn alles in Ordnung ist.
        :type bool
        """
        for port in self.getPorts():
            if port.isPortOK():
                triggers = self.TriggerService.getTriggerByPort(port)
                for trigger in triggers:
                    if trigger.isWarnTrigger() and trigger.check():
                        return False
            else:
                return False
        return True

