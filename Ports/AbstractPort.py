import IOHelper.config as configIO
import IOHelper.log as logIO
from Models.OptionableObject import OptionableObject
from Ports.Threads.LoggingThread import LoggingThread
from Ports.Threads.WatcherThread import WatcherThread
from Models.Trigger import Trigger


class AbstractPort(OptionableObject):
    """
    Die Klasse AbstractPort muss von jedem Porttyp geerbt werden. Sie ist abstrakt und kann daher nicht alleine erzeugt werden.
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
        Die Methode nachInit muss immer am Ende der initialisierung des Ports vom Kindobjekt aufgerufen werden. Sie startet die Überwachung der Threads und ist daher auf einen vollständig funktionsfähigen Port angewiesen. 
        """
        self.startThreads()
        self.initialized = True

    def startThreads(self):
        """
        Startet die Threads die den Port überwachen. Ist die Variable isSelfUpdating auf True gesetzt, so wird kein WatcherThread gestartet. Ein LogingThread wird gestartet, wenn Logging auf true gesetzt wurde.
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
        Startet die Portthreads zum Logging und der Überwachung neu.
        """
        self.stopThreads()
        self.startThreads()

    def stopThreads(self):
        """
        Stoppt die Portthreads zum Logging und zur Überwachung.
        """
        if isinstance(self.loggingThread, LoggingThread):
            self.loggingThread.stop()
            self.loggingThread = None
        if isinstance(self.watcherThread, WatcherThread):
            self.watcherThread.stop()
            self.watcherThread = None

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
        Schreibt einen Eintrag von dem Port in die Log Datei.
        """
        logIO.writeLog(self)

    def getState(self):
        """
        Gibt den aktuellen Status des Ports zurück. Dies ist der letzte Wert den der Sensor zurückgegeben hat.
        :return: Der aktuellste Messwert des Sensors.
        :type float
        """
        return self.lastValue

    def getValueRange(self):
        """
        Gibt den Wertebereich des Ports zurück. Muss von der Kindklasse implementiert werden!
        :return: Ein Tuple mit den Werten (minimalerWert, maximalerWert, Schrittweite zwisachen den einzelnen Werten)
        :type tuple
        """
        raise NotImplementedError

    def getPrivateState(self):
        """
        Wird vom WatcherThread aufgerufen um den aktuellen Wert des Sensors auszulesen. Insbesonders muss diese Methode implementiert werden, wenn minRefresehTime gesetzt und ungleich -1 ist.
        :return: Den aktuellen Wert des Sensors.
        :type float
        """
        pass

    def portChanged(self, newValue):
        """
        Private Methode die bei einer Änderung des Sensorwertes aufgerufen wird. Sie aktualisiert die Historie des Ports und startet den Triggeraufruf.
        :param newValue: Die
        :return: 
        """
        self.lastValue = newValue
        self.addValueToHistory(newValue)
        # informiert alle trigger.
        self.informObserverOfType(Trigger)

    @classmethod
    def getOptions(cls):
        """
        Statische Methode um die möglichen Optionen eines Ports zurück zu geben. Dies ist für die Oberfläche relevant.
        :return: Ein dict mit allen Optionen des Ports.
        :type dict
        """
        return {**super().getOptions(), **cls.superOptions}

    def getType(self):
        """
        Gibt den Typ des Ports zurück.
        :return: Der Typ des Ports.
        :type str
        """
        return str(self.__class__.__name__)

    @classmethod
    def getInputs(cls):
        """
        Gibt die Anschlussmöglichkeiten des Ports zurück. Sollte überschrieben werden, wenn der Port die Anschlüsse dynamisch nachlädt.
        :return: Anschlussmöglichkeiten des Ports.
        :type dict
        """
        if str(cls.__name__) in configIO.loadWiring().keys():
            return configIO.loadWiring()[str(cls.__name__)]
        return {}

    def getMinRefreshTime(self):
        """
        Gibt die minimale Wartezeit für das Aktualisieren eines Ports zurück. Dies ist für den Watcherthread wichtig. 
        :return: Die inimale Zeit zwischen zwei Anfragen an den Sensor.
        :type float
        """
        return self.minRefreshTime

    def getName(self):
        """
        Gibt den Namen des Ports zurück.
        :return: der Name des Ports 
        :type str
        """
        return self.getSetting("name")

    def getID(self):
        """
        Gibt die eindeutige ID des Ports zurück.
        :return: die ID des Ports.
        :type str
        """
        return self.portID

    def isPortLogged(self):
        """
        Wenn der Port geloggt werden soll, gibt diese Methode true zurück.
        :return: true, wenn der Port geloggt werden soll.
        :type bool
        """
        return self.getSetting("logging")

    def getLogCycle(self):
        """
        Gibt die Sekunden zwischen zwei Logeinträgen zurück.
        :return: die Sekunden zwischen zwei Logzeiten
        :type float
        """
        return self.getSetting("logCycle")

    def __eq__(self, other):
        """
        Prüft ob zwei Ports gleich sind. Zwei Ports sind genau dann gleich, wenn ihre ID übereinstimmt. Diese Methode überschreibt ==
        :param other: Der zu vergleichende Port.
        :type other: AbstractPort
        :return: true, wenn die beiden Ports die gleiche ID haben.
        :type bool
        """
        if self.__class__ == other.__class__:
            return self.getID() == other.getID()
        return False

    def getDescription(self):
        """
        Gibt die Beschreibung eines Porttyps zurück. Diese Methode muss von der indklasse übschrieben werden.
        :return: Die Beschreibung des Ports.
        :type str
        """
        raise NotImplementedError

    def getSettings(self):
        """
        Gibt die aktuellen Einstellungen des Ports zurück. Die Einstellungen sollten mindestens alle möglichen Options enthalten.
        :return: Ein dict mit en Einstellungen.
        :type dict
        """
        return self.settings

    def getUnit(self):
        """
        Gibt die Einheit eines Ports zurück.
        :return: Die Einheit des Ports.
        :type str
        """
        return self.getSetting("unit")

    def getCurrentInformations(self):
        """
        Gibt die aktuellen Informationen zurück. Die aktuellen Informationen enthalten die settings, den aktuellen Status und die Gesundheit des Ports.
        :return: Ein dict mit den aktuellen Informationen des Ports.
        :type dict
        """
        """Gibt alle Informationen alle Informationen zu einem Port zurück."""
        informations = {}
        informations['settings'] = self.getSettings()
        informations['state'] = self.getState()
        informations['portOK'] = self.isPortOK()
        return informations

    def getPortBoxName(self):
        """
        Gibt die externe Bezeichnung des Ports an. Diese steht z.B. an der Anschlussdose des Ports. er wird in der wiring-Konfigurationen des Systems festgelegt. Die Methode kann bei dynamischen Ports ggf. überschrieben werden.
        :return Die externe Bezeichnung des Ports.
        :type str
        """
        return self.getSetting("wiring")

    def getInternalPin(self):
        """
        Gibt die interne räpresentation des Ports zurück. Diese kann z.B. einfach nur ein GPIO Pin sein, oder aber eine Zeichenkette, die den Anschluss an einen AD-Wandler darstellt.
        Die Kindklasse kann diese Methode nutzen um die Ansteuerung des richtigen Senors durchzuführen.
        :return Eine Repräsentation des internen Anschluss des Ports.
        :type str
        """
        return self.internalPin

    def getServiceName(self):
        """
        Der mit dem Port assozierte Service. Dies ist eine Hilfsmethode, nicht überschreiben. Sie kann bei einem Ausbau des System durch weitere Services benutzt werden.
        :return: Der Name der Serviceklasse.
        :type str
        """
        return "PortService"

    def getStateWithUnit(self):
        """
        Gibt den akutellen Wert mit der Einheit aus.
        :return: Der aktuelle Wert mit der Einheit
        :type str
        """
        return str(self.getState()) + str(self.getUnit())

    def addValueToHistory(self, value):
        """
        Fügt der Historie einen Wert hinzu. Die Historie eines Ports dient zur bestimmten Auslösung von Triggern. So wird z.B. ein E-Mail Triger so nicht bei jedem Prüfen eines Wertes aufgerufen sondern nur beim ersten Überschreiten eines Schwellwerts.
        :param value: der Wert der zur Historie hinzugefügt werden soll.
        :type value: float
        """
        if len(self.portHistory) >= 100:
            self.portHistory.pop(0)
        self.portHistory.append(value)

    def getPortHistory(self):
        """
        Gibt die Historie des Ports seit Porgrammstart zurück
        :return: Eine Liste der letzten 100 Messwerte des Ports.
        :type list
        """
        return self.portHistory

    def isInitialized(self):
        """
        Gibt True zurück, wenn der Port fertig initialisiert ist.
        :return: True wenn der Port initialisiert ist.
        :type bool
        """
        return self.initialized
