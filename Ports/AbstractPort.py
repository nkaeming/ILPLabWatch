import IOHelper.config as configIO
import IOHelper.log as logIO
from Models.OptionableObject import OptionableObject
from Ports.Threads.LoggingThread import LoggingThread
from Ports.Threads.WatcherThread import WatcherThread
from Models.Trigger import Trigger


class AbstractPort(OptionableObject):
    """
    Die Klasse AbstractPort muss von jedem Port den ein User implementieren kann geerbt werden.
    """

    # die eindeutige PortID
    portID = None

    # die Einstellungen des Ports
    settings = {}

    # die Optionen die jeder Port hat
    superOptions = {
        "name": {
            "type": "text",
            "tab": -5,
            "name": "Portbezeichnung",
            "description": "Der Name des Ports bestehend aus a-z, A-Z und 0-9. Keine Leer- oder Sonderzeichen.",
            "standard": "",
            "final": True,
            "required": True,
            "regex": "[A-Za-z0-9]+"
        },
        "description": {
            "type": "text",
            "tab": -1,
            "name": "Beschreibung",
            "description": "Eine Beschreibung des Ports.",
            "length": 200
        },
        "logCycle": {
            "type": "number",
            "name": "Logintervall",
            "description": "Das Logintervall in Sekunden.",
            "standard": 5,
            "min": 1,
            "max": 3600,
            "step": 1,
            "tab": -3,
            "final": False,
            "required": True
        },
        "logging": {
            "type": "boolean",
            "name": "Logging",
            "description": "Wenn diese Einstellung aus ist, so wird der Port nicht geloggt.",
            "standard": True,
            "tab": -4,
            "final": False
        },
        "unit": {
            "type": "text",
            "tab": -2,
            "name": "Einheit",
            "description": "Die Einheit die der Port haben soll.",
            "standard": "",
            "final": False,
            "required": False
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

    # der interne Anschluss des Ports.
    internalPin = 0

    # eine Liste mit den letzten 100 Portwerten seit Programmstart
    portHistory = []

    # ist True, wenn der Port final initialisiert ist.
    initialized = False

    def __init__(self, childSettings, id):
        """
        Wird vom Kindobjekt immer aufgerufen. Wird der Konstruktor nicht vom Kindobjekt aufgerufen, wird der Port nicht vollständig richtig gestartet und kann nicht ausgelesen werden.
        :param childSettings: Die Einstellungen der von User implementierten Portklasse.
        :type childSettings: dict
        :param id: die eindeutige ID des Ports
        :type id: str
        """
        self.portID = str(id)
        self.superSettings["type"] = self.getType()
        self.internalPin = self.getInputs()[childSettings["wiring"]]
        super().__init__({**self.superSettings, **childSettings})

    def nachInit(self):
        """
        Wird auf dem Konstruktor der Kindklasse nach der Initialisierung der Sensoren aufgerufen. Die Methode kann unter Umständen überschrieben werden muss dann aber auf jeden Fall aus Der Kindklasse aufgerufen werden.
        """
        self.startThreads()
        self.initialized = True

    def startThreads(self):
        """
        Startet die Threads die den Port überwachen.
        """

        # Ein Port der sich selbst updated registriert selber Veränderungen.
        if self.isSelfUpdating == False:
            self.watcherThread = WatcherThread(self)
            self.watcherThread.start()
        # wenn bei dem Port logging aktiviert ist, so wird hier der entsprecende Deamon gestartet.
        if self.getSetting("logging") == True:
            self.loggingThread = LoggingThread(self)
            self.loggingThread.start()

    def restartThreads(self):
        """
        Startet die Portthreads neu.
        """
        self.stopThreads()
        self.startThreads()

    def stopThreads(self):
        """
        Stoppt die Threads
        """
        if isinstance(self.loggingThread, LoggingThread):
            self.loggingThread.stop()
            self.loggingThread = None
        if isinstance(self.watcherThread, WatcherThread):
            self.watcherThread.stop()
            self.watcherThread = None

    # gibt True zurück, wenn beim Port alles in Ordnung ist.
    def isPortOK(self):
        """
        Prüft ob ein Port funktionsfähig ist.
        :return: True wenn der Port funktionsfähig ist.
        :type bool
        """
        if self.getSetting("logging") == True:
            if self.loggingThread.is_alive() == False:
                return False
        if self.isSelfUpdating == False:
            if self.watcherThread.is_alive() == False:
                return False
        if self.isPortInternalOK() == False:
            return False
        return True

    def isPortInternalOK(self):
        """
        Funktion kann vom Benutzer überschrieben werden, wenn der Sensor es zulässt seine Funktionalität zu überprüfen. Z.B. ob die Verbindung klappt o.Ä.
        :return: True, wenn der Port ordnungsgemäß funktioniert, False sonst.
        :type bool
        """
        return True

    def log(self):
        """
        Schreibt einen Eintrag von dem Port selbst in die Log Datei.
        """
        logIO.writeLog(self)

    def getState(self):
        """
        Gibt den aktuellen Status des Ports zurück. Dies ist der letzte Wert den der Sensor zurückgegeben hat.
        :return: Der aktuellste Messwert des Sensors.
        :type float
        """
        return self.lastValue

    # gibt den möglichen Wertebereich des Ports zurück. [niedrigster, höchster, schrittweite]
    def getValueRange(self):
        """
        Gibt den Wertebereich des Ports zurück.
        :return: Ein Tuple mit den Werten (minimalerWert, maximalerWert, )
        :type tuple
        """
        raise NotImplementedError

    # muss implementiert werden, wenn minRefreshTime gesetzt und ungleich -1 ist.
    def getPrivateState(self):
        pass

    # wird aufgerufen, wenn der Portzustand sich geändert hat.
    def portChanged(self, newValue):
        self.lastValue = newValue
        self.addValueToHistory(newValue)
        # informiert alle trigger.
        self.informObserverOfType(Trigger)

    # gibt die Optionen des Ports zurück. Diese werden dann in der GUI angezeigt. Kann überschrieben werden, sofern nötig.
    @classmethod
    def getOptions(cls):
        return {**super().getOptions(), **cls.superOptions}

    # gibt den Typ des Ports zurück.
    def getType(self):
        return str(self.__class__.__name__)

    @classmethod
    def getInputs(cls):
        """Gibt die Anschlussmöglichkeiten des Ports zurück. Sollte überschrieben werden, wenn der Port die Anschlüsse dynamisch nachlädt."""
        if str(cls.__name__) in configIO.loadWiring().keys():
            return configIO.loadWiring()[str(cls.__name__)]
        return {}

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
            return self.getID() == other.getID()
        return False

    # gibt die Beschreibung des Porttyps zurück.
    def getDescription(self):
        raise NotImplementedError

    # gibt die Einstellungen des Ports zurück.
    def getSettings(self):
        return self.settings

    def getUnit(self):
        """Gibt die Einheit eines Ports zurück."""
        return self.getSetting("unit")

    def getCurrentInformations(self):
        """Gibt alle Informationen alle Informationen zu einem Port zurück."""
        informations = {}
        informations['settings'] = self.getSettings()
        informations['state'] = self.getState()
        informations['portOK'] = self.isPortOK()
        return informations

    def getPortBoxName(self):
        """Gibt die externe Bezeichnung des Ports an. Diese steht z.B. an der Anschlussdose des Ports"""
        return self.getSetting("wiring")

    def getInternalPin(self):
        """Gibt die interne räpresentation des Ports zurück. Diese kann z.B. einfach nur ein GPIO Pin sein, oder aber eine Zeichenkette, die den Anschluss an einen AD-Wandler darstellt."""
        return self.internalPin

    def getServiceName(self):
        return "PortService"

    def getStateWithUnit(self):
        """Gibt den akutellen Wert mit der Einheit aus."""
        return str(self.getState()) + str(self.getUnit())

    def addValueToHistory(self, value):
        """Fügt der Historie einen Wert hinzu"""
        if len(self.portHistory) >= 100:
            self.portHistory.pop(0)
        self.portHistory.append(value)

    def getPortHistory(self):
        """Gibt die Historie des Ports seit Porgrammstart zurück"""
        return self.portHistory

    def isInitialized(self):
        """Gibt True zurück, wenn der Port fertig initialisiert ist."""
        return self.initialized
