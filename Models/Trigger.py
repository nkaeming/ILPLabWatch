from Models.Observer import Observer
from Models.Observable import Observable

class Trigger(Observer, Observable):
    """
    
    """

    triggerRange = [0,
                    0]  # die erste zahl gibt den minimalen Wert an, bei der der Trigger auslöst. Die zweite Zahl gibt die höchste Zahel an, bei der der Trigger auslöst.

    port = None  # der Port mit dem der Trigger verknüpft ist.

    alerts = []  # die alerts mit denen der trigger verbunden ist.

    warnTrigger = False  # gibt an ob der Trigger im UI als Warntrigger auftauchen soll.

    triggerID = 0  # eindeutige ID des Trigger

    # min ist die untere Schranke des Triggers und max die obere.
    def __init__(self, triggerID, minimal, maximal, port, warnTrigger):
        self.alerts = []
        self.triggerRange = [minimal, maximal]
        self.port = port
        self.triggerID = triggerID
        self.port.addObserver(self)
        self.warnTrigger = warnTrigger

    # wird ausgelöst, wenn der Port sich verändert.
    def observableChanged(self, observable):
        self.checkAndCall()

    def checkAndCall(self):
        """Falls der Trigger gerade ausglöst ist, werden die Alerts informiert"""
        if self.check():
            self.callAlerts()

    def check(self):
        """Gibt true zurück wenn der Trigger ausgelöst ist."""
        return self.checkValue(self.port.getState())

    def checkValue(self, value):
        """Prüft ob ein bestimmter Wert den Trigger auslösen würde."""
        return self.triggerRange[0] <= value and value <= self.triggerRange[1]

    # ruft alle alerts auf
    def callAlerts(self):
        for alert in self.alerts:
            alert.throwAlert(self.port, self)

    def isFirstCalled(self):
        """Gibt true zurück, wenn der Trigger zum ersten Mal ausgelöst wurde. D.h. wenn der Wert zum ersten Mal in den Bereich reingelaufen ist."""
        portHistory = self.port.getHistory()
        if self.checkValue(portHistory[-1]) == True:
            return False
        return True

    # gibt den minimalen Wert zurück bei dem der Trigger auslöst.
    def getMinimalValue(self):
        return self.triggerRange[0]

    # gibt den maximalen wert zurück bei dem der Trigger auslöst.
    def getMaximalValue(self):
        return self.triggerRange[1]

    # fügt ein neues alert Objekt hinzu.
    def appendAlert(self, alert):
        self.alerts.append(alert)
        self.informTriggerService()

    def informTriggerService(self):
        """Private Methode um den Triggerservice zu informieren"""
        from Services.TriggerService import TriggerService
        self.informObserverOfType(TriggerService)

    # gibt true zurück, wenn der Trigger als Warnung im UI auftauchen soll.
    def isWarnTrigger(self):
        return self.warnTrigger

    # gibt den Port zurück, der den Trigger auslöst
    def getPort(self):
        return self.port

    # gibt die ID des Triggers zurück.
    def getID(self):
        return self.triggerID

    # gibt die Alerts zurück, welche mit diesem Trigger verbunden sind.
    def getAlerts(self):
        return self.alerts

    # entfernt einen alert
    def removeAlert(self, alert):
        if alert in self.alerts:
            self.alerts.remove(alert)
            from Services.TriggerService import TriggerService
            self.informObserverOfType(TriggerService)

    # gibt die Einstellungen des triggers als dict zurück.
    def getSettings(self):
        conf = {}
        conf["portID"] = self.getPort().getID()
        conf["warnTrigger"] = self.isWarnTrigger()
        conf["range"] = self.triggerRange

        alertList = []
        for alert in self.getAlerts():
            alertList.append(alert.getID())
        conf["alerts"] = alertList

        return conf

    def setWarntrigger(self, value):
        """Stellt ein ob der Trigger in Warntrigger ist."""
        self.warnTrigger = value
        self.informTriggerService()

    def setInterval(self, value):
        self.triggerRange = value
        self.informTriggerService()


    # zwei Trigger sind gleich, wenn ihre ID gleich ist.
    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.getID() == other.getID():
                return True
        return False
