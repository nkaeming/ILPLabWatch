from Models.Observable import Observable
from Models.Trigger import Trigger
from Models.PersistantObject import PersistantObject
import uuid, importlib


class TriggerService(Observable, PersistantObject):
    """Der Trigger service verwaltet alle Trigger."""

    portService = None  # der verbundene Port Service

    trigger = []  # alle Trigger
    alerts = []  # alle Alerts

    def __init__(self, portService):
        self.portService = portService
        self.getConf()

    # gitb den dateinamen der Einstellungsdatei an.
    def getConfigFileName(self):
        return "triggerConf.cfg"

    # trigger werden alle neu erzeugt.
    def setUp(self):
        # erzeuge die Alerts
        for alertID, settings in self.persistantConfig["alerts"].items():
            try:
                alertSettings = self.persistantConfig["alerts"][alertID]
                classPointer = getattr(
                    importlib.import_module("Alerts." + alertSettings["type"] + "." + alertSettings["type"]),
                    alertSettings["type"])
                self.alerts.append(classPointer(alertID, alertSettings))
            except:
                pass

        # erzeuge die Trigger
        for portID, triggers in self.persistantConfig["trigger"].items():
            port = self.portService.getPortByID(portID)
            for triggerID, triggerSettings in triggers.items():
                trigger = Trigger(triggerID, triggerSettings["range"][0], triggerSettings["range"][1], port,
                                  triggerSettings["warnTrigger"])
                # erzeuge die Verknüpfungen
                for alertID in triggerSettings["alerts"]:
                    alert = self.getAlertByID(alertID)
                    trigger.appendAlert(alert)

    # fügt einen neuen Trigger hinzu und gibt ihn als instanz zurück (z.B. um alerts anzufügen.)
    def addTrigger(self, minimal, maximal, port, warnTrigger):
        triggerID = str(uuid.uuid4())
        trigger = Trigger(triggerID, minimal, maximal, port, warnTrigger)
        self.trigger.append(trigger)
        port.addObserver(trigger)
        if not (port.getID() in self.persistantConfig["trigger"]):
            self.persistantConfig["trigger"][port.getID()] = {}

        self.persistantConfig["trigger"][port.getID()][triggerID] = {
            "range": [minimal, maximal],
            "alerts": [],
            "warnTrigger": warnTrigger
        }

        self.writeConf()
        return trigger

    # fügt einen neuen Alert hinzu.
    def addAlert(self, alertType, alertSettings):
        alertName = alertSettings["name"]
        if self.getAlertByName(alertName) == None:
            try:
                alertID = str(uuid.uuid4())
                classPointer = getattr(importlib.import_module("Alerts." + alertType + "." + alertType), alertType)
                alert = classPointer(alertID, alertSettings)
                self.persistantConfig["alerts"][alertID] = alertSettings
                self.writeConf()
                return alert
            except:
                pass
        else:
            return self.getAlertByName(alertName)

    # gibt einen Alert nach seiner ID zurück. Erzeugt das Objekt sofern noch nicht erzeugt.
    def getAlertByID(self, alertID):
        result = filter(lambda alert: alert.getID() == alertID, self.alerts)
        return next(result, None)

    # gibt den Alert nach seinem Namen aus.
    def getAlertByName(self, alertName):
        result = filter(lambda alert: alert.getName() == alertName, self.alerts)
        return next(result, None)

    # fügt eine Verbidnung zwischen einem Trigger und einem Alert hinzu, sofern der Trigger und der Alert im Service registriert sind.
    def addAlertTriggerRelation(self, trigger, alert):
        # TODO: Hier gibt es ein Problem
        if trigger.getPort().getID() in self.persistantConfig["trigger"].keys():
            if trigger.getID() in self.persistantConfig["trigger"].keys():
                if not (alert.getID() in self.persistantConfig["trigger"][trigger.getPort().getName()][trigger.getID()][
                    "alerts"]):
                    self.persistantConfig["trigger"][trigger.getPort().getName()][trigger.getID()]["alerts"].append(
                        alert.getID())
                    trigger.appendAlert(alert)

    # gibt eine Liste mit allen Triggern zu einen Port aus.
    def getTriggerOfPort(self, port):
        return list(filter(lambda trigger: trigger.getPort() == port, self.trigger))
