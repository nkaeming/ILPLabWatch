from Models.PersistantObject import PersistantObject
from Models.Observer import Observer
from Models.Trigger import Trigger
import uuid


class TriggerService(PersistantObject, Observer):
    """Der Triggerservice verwaltet alle Trigger"""

    triggers = []

    portService = None
    alertServcie = None

    def __init__(self, portService, alertService):
        self.portService = portService
        self.alertServcie = alertService
        self.setUp()

    # erzeugt die trigger Liste beim erten Start. Protected nicht von außen aufrufen.
    def setUp(self):
        conf = self.getConf()
        for triggerID, triggerSettings in conf.items():
            trigger = self.getTriggerObject(triggerID, triggerSettings)
            trigger.addObserver(self)
            self.triggers.append(trigger)

    # gibt ein neues Triggerobjekt mit den Settings zurück, sofern der Trigger noch nicht in der Triggerliste existierte, ansonsten wird das bereits existierende Triggerobjekt zurückgegeben.
    def getTriggerObject(self, id, settings):
        triggerByID = self.getTriggerByID(id)
        if triggerByID == None:
            port = self.portService.getPortByID(settings["portID"])
            # sollte es den Port nicht geben wird kein Trigger erzeugt.
            if port == None:
                raise ReferenceError("A Trigger can't exists without a Port.")
            else:
                trigger = Trigger(id, settings["range"][0], settings["range"][1], port, settings["warnTrigger"])
                if "alerts" in settings.keys():
                    for alertID in settings["alerts"]:
                        alert = self.alertServcie.getAlertByID(alertID)
                        trigger.appendAlert(alert)
                return trigger
        else:
            return triggerByID

    # gibt einen Trigger nach seiner ID aus.
    def getTriggerByID(self, id):
        result = filter(lambda trigger: trigger.getID() == id, self.triggers)
        return next(result, None)

    # gibt alle Trigger zu einem Port aus.
    def getTriggerByPort(self, port):
        result = filter(lambda trigger: trigger.getPort() == port, self.triggers)
        return list(result)

    # schreibt die Konfiguration neu.
    def writeConf(self, conf=None):
        conf = {}
        for trigger in self.triggers:
            id = trigger.getID()
            settings = trigger.getSettings()
            conf[id] = settings
        super().writeConf(conf)

    # gib die Konfigurationsdateinamen für den Triggerservice an die Parentclass weiter.
    def getConfigFileName(self):
        return "triggerConf.cfg"

    # wird aufggerufen, wenn sich ein Observable geändert hat.
    def observableChanged(self, observable):
        # wenn das zu überwachende Objekt ein trigger ist, dann hat sich die Konfiguration geändert.
        if isinstance(observable, Trigger):
            self.writeConf()

    # fügt einen neuen Trigger hinzu und speichert ihn persistent.
    def addTigger(self, settings):
        triggerID = str(uuid.uuid4())
        trigger = self.getTriggerObject(triggerID, settings)
        self.triggers.append(trigger)
        self.writeConf()
        return trigger
