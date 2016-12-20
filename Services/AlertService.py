from Models.PersistantObject import PersistantObject
import importlib


class AlertService(PersistantObject):
    """Der Alertservcie verwaltet und erzeugt alle Alerts."""

    alerts = []  # eine Liste aller alert Objekte.

    def __init__(self):
        self.setUp()

    # erzeugt alle alerts für das erste mal. Protected nicht von außen aufrufen.
    def setUp(self):
        conf = self.getConf()
        for id, settings in conf.items():
            self.alerts.append(self.getAlertObject(id, settings))

    # erzeugt ein neues alert Objekt. Ähnlich einer Fabrik. Wurde ein Port mit dieser Id bereits erzegt, so wird dieses Objekt zurückgegeben.
    def getAlertObject(self, id, settings):
        alertById = self.getAlertByID(id)
        if alertById == None:
            classPointer = getattr(importlib.import_module("Alerts." + settings["type"] + "." + settings["type"]),
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

    # gibt den Dateinamen für die conf Datei zurück.
    def getConfigFileName(self):
        return "alertConf.cfg"
