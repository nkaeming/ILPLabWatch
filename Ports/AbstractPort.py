import IOHelper.config as configIO
import IOHelper.log as logIO
from Models.Observable import Observable
from Models.OptionalbeObject import OptionalbeObject
from Ports.Threads.LoggingThread import LoggingThread
from Ports.Threads.WatcherThread import WatcherThread
from Models.Trigger import Trigger


class AbstractPort(Observable, OptionalbeObject):
    """Ein abstrakter Port, von dem jeder UserPort erben sollte."""
    # die eindeutige PortID
    portID = None

    # die Einstellungen des Ports
    settings = {}

    # die Optionen die jeder Port hat
    superOptions = {
        "name": {
            "type": "text",
            "tab": -4,
            "name": "Portbezeichnung",
            "description": "Der Name des Ports bestehend aus a-z, A-Z und 0-9. Keine Leer- oder Sonderzeichen.",
            "standard": "",
            "final": True
        },
        "description": {
            "type": "text",
            "tab": 0,
            "name": "Beschreibung",
            "desciption": "Eine Beschribung des Ports.",
            "length": 200
        },
        "logCycle": {
            "type": "number",
            "name": "Logintervall",
            "description": "Das Loginterval in Sekunden",
            "standard": 5,
            "min": 1,
            "max": 3600,
            "step": 1,
            "tab": -2,
            "final": False
        },
        "logging": {
            "type": "boolean",
            "name": "Logging",
            "description": "Wenn diese Einstellung aus ist, so wird der Port nicht geloggt.",
            "standard": 1,
            "tab": -3,
            "final": False
        },
        "unit": {
            "type": "text",
            "tab": -1,
            "name": "Einheit",
            "description": "Die Einheit die der Port haben soll.",
            "standard": "",
            "final": True
        }
    }

    # die Eisntellungen die jeder Port haben muss.
    superSettings = {}

    # der letzte Wert des Ports bei der letzten Überprüfung.
    lastValue = 0

    # der Thread zum loggen
    loggingThread = None

    # der Thread zum überwachen des Ports
    watcherThread = None

    # wenn der Port sich selber updaten kann, wird diese Variable auf True gesetzt.
    isSelfUpdating = False

    # ist isSelfUpdateing False, so wird eine minimale refreshTime benötigt.
    minRefreshTime = 0

    # erwartet vom Kindobjekt
    def __init__(self, childSettings, id):
        self.portID = str(id)
        self.superSettings["type"] = self.getType()
        super().__init__({**self.superSettings, **childSettings})
        self.startThreads()

    # startet die Portthreads
    def startThreads(self):
        if self.getSetting("logging") == True:
            self.loggingThread = LoggingThread(self)
            self.loggingThread.start()
        if self.isSelfUpdating == False:
            self.watcherThread = WatcherThread(self)
            self.watcherThread.start()

    # gibt True zurück, wenn beim Port alles in Ordnung ist.
    def isPortOK(self):
        if self.getSetting("logging") == True:
            if self.loggingThread.is_alive() == False:
                return False
        if self.isSelfUpdating == False:
            if self.watcherThread.is_alive() == False:
                return False
        if self.isPortInternalOK() == False:
            return False
        return True

    # Methode kann überschrieben werden, wenn der Port in sich Strukturen zur Überprüfung beherbergt.
    def isPortInternalOK(self):
        return True

    # schreibt in die Logdatei
    def log(self):
        logIO.writeLog(self)

    # Gibt den aktuellen Status des Ports zurück.
    def getState(self):
        return self.lastValue

    # gibt den möglichen Wertebereich des Ports zurück. [niedrigster, höchster, schrittweite]
    def getValueRange(self):
        raise NotImplementedError

    # muss implementiert werden, wenn minRefreshTime gesetzt und ungleich -1 ist.
    def getPrivateState(self):
        pass

    # wird aufgerufen, wenn der Portzustand sich geändert hat.
    def portChanged(self, newValue):
        self.lastValue = newValue
        # informiert alle trigger.
        self.informObserverOfType(Trigger)

    # gibt die Optionen des Ports zurück. Diese werden dann in der GUI angezeigt. Kann überschrieben werden, sofern nötig.
    def getOptions(self):
        return {**super().getOptions, **self.superOptions}

    # gibt den Typ des Ports zurück.
    def getType(self):
        return str(self.__class__.__name__)

    # gibt alle Anschlussmöglichkeiten für diesen Porttyp zurück.
    def getInputs(self):
        buildInPorts = configIO.loadWiring()[str(self.__class__)]
        ports = buildInPorts
        if hasattr(self, "isDynamicPort"):
            if self.isDynamicPort == True:
                ports = {**buildInPorts, **self.getDynamicInputs()}
        return ports

    # kann bei dynamiscen Ports hinzugefügt werden.
    def getDynamicInputs(self):
        pass

    # gibt die minimale Aktualisierungszeit zurück.
    def getMinRefreshTime(self):
        return self.minRefreshTime

    # gibt den Namen des Ports zurück.
    def getName(self):
        return self.getSetting("name")

    # gibt die PortID zurück
    def getID(self):
        return self.portID

    # gibt True zurück wenn der Port geloggt wird.
    def isPortLogged(self):
        return self.getSetting("logging")

    # gibt die Sekunden zwischen zwei Logzeiten an
    def getLogCycle(self):
        return self.getSetting("logCycle")

    # Zwei Ports sollen genau dann gleich sein, wenn ihre ID übereinstimmt.
    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.getID() == other.getID():
                return True
            else:
                return False
        else:
            return False

    # gibt die Beschreibung des Porttyps zurück.
    def getDescription(self):
        raise NotImplementedError

    # gibt die Einstellungen des Ports zurück.
    def getSettings(self):
        return self.settings
