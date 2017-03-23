from Models.PersistantObject import PersistantObject
from Models.Observer import Observer
from Alerts.AbstractAlert import AbstractAlert
import importlib, uuid, pkgutil


class AlertService(PersistantObject, Observer):
    """Der Alertservcie verwaltet und erzeugt alle Alerts."""

    alerts = []  # eine Liste aller alert Objekte.
    TriggerService = None


    def __init__(self):
        self.setUp()

    def setTriggerService(self, TS):
        """Setzt den Trigger Service"""
        self.TriggerService = TS

    # erzeugt alle alerts für das erste mal. Protected nicht von außen aufrufen.
    def setUp(self):
        conf = self.getConf()
        for id, settings in conf.items():
            alertObject = self.getAlertObject(id, settings)
            alertObject.addObserver(self)
            self.alerts.append(alertObject)

    # erzeugt ein neues alert Objekt. Ähnlich einer Fabrik. Wurde ein Port mit dieser Id bereits erzegt, so wird dieses Objekt zurückgegeben.
    def getAlertObject(self, id, settings):
        alertById = self.getAlertByID(id)
        if alertById == None:
            classPointer = getattr(importlib.import_module("Alerts.UserAlerts." + settings["type"] + "." + settings["type"]),
                                   settings["type"])
            return classPointer(id, settings)
        else:
            return alertById

    # gibt einen Alert nach seiner ID aus.
    def getAlertByID(self, id):
        result = filter(lambda alert: alert.getID() == id, self.alerts)
        return next(result, None)

    # gibt einen Alert nach seiner ID aus.
    def getAlertByName(self, name):
        result = filter(lambda alert: alert.getName() == name, self.alerts)
        return next(result, None)

    # schreibt die Konfiguration des Services neu. conf ist ein redunanter Parameter
    def writeConf(self, conf=None):
        conf = {}
        for alert in self.alerts:
            id = alert.getID()
            settings = alert.getSettings()
            conf[id] = settings
        super().writeConf(conf)

    # gibt den Dateinamen für die conf Datei zurück.
    def getConfigFileName(self):
        return "alertConf.cfg"

    # wird aufggerufen, wenn sich ein Observable geändert hat.
    def observableChanged(self, observable):
        # wenn das zu überwachende Objekt ein alert ist, dann hat sich die Konfiguration geändert.
        if isinstance(observable, AbstractAlert):
            self.writeConf()

    # fügt einen neuen alert hinzu und speicht ihn dauerhaft und gibt das gerade erzegte Alertobjekt zurück.
    def addAlert(self, settings):
        alertID = str(uuid.uuid4())
        alert = self.getAlertObject(alertID, settings)
        self.alerts.append(alert)
        alert.addObserver(self)
        self.writeConf()
        return alert

    def getAlerts(self, setting="name", reverse=False):
        """Gibt alle Alerts zurück."""
        return sorted(self.alerts, key=lambda alert: alert.getSetting(setting), reverse=reverse)

    def getAlertTypes(self):
        """Gibt alle Porttypen zurück die konfigurierbar sind"""
        alertTypes = []
        for alertType in pkgutil.iter_modules(['Alerts/UserAlerts']):
            alertTypes.append(alertType[1])
        return alertTypes

    def getAlertClassByType(self, alertType):
        """Gibt einen Zeiger auf die Klasse zurück, welche den Alert definiert."""
        return getattr(importlib.import_module("Alerts.UserAlerts." + alertType + "." + alertType), alertType)

    def doesAlertExistByName(self, name):
        """Prüft ob ein Portname bereits existiert."""
        return len(list(filter(lambda alert: alert.getName() == name, self.getAlerts()))) != 0

    def generateAndAddNewAlert(self, settings):
        """Erzeugt einen neuen Alert und fügt diesen hinzu."""
        alertID = str(uuid.uuid4())
        alertInstance = self.getAlertObject(alertID, settings)
        alertInstance.addObserver(self)
        self.alerts.append(alertInstance)
        # die Konfigurationsdatei neu schreiben
        self.writeConf()

        return alertID

    def removeAlert(self, alert):
        """Löscht einen Alert"""
        alert.removeAllObservers()
        self.TriggerService.removeTriggersByAlert(alert)
        self.alerts.remove(alert)
        self.writeConf()