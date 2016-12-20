from Models.PersistantObject import PersistantObject
from Models.Trigger import Trigger


class TriggerService(PersistantObject):
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
                trigger = Trigger(id, settings["range"][0], settings["range"][0], port, settings["warnTrigger"])
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

    # gib die Konfigurationsdateinamen für den Triggerservice an die Parentclass weiter.
    def getConfigFileName(self):
        return "triggerConf.cfg"
