from Models.Observer import Observer


# Ein Trigger dient zur Verbindung zwischen den Ports und den Alerts.

class Trigger(Observer):
    """Trigger werden ausgelöst, wenn ein Port kritische Werte erreicht."""

    triggerRange = [0,
                    0]  # die erste zahl gibt den minimalen Wert an, bei der der Trigger auslöst. Die zweite Zahl gibt die höchste Zahel an, bei der der Trigger auslöst.

    port = None  # der Port mit dem der Trigger verknüpft ist.

    alerts = []  # die alerts mit denen der trigger verbunden ist.

    warnTrigger = False  # gibt an ob der Trigger im UI als Warntrigger auftauchen soll.

    triggerID = 0  # eindeutige ID des Trigger

    # min ist die untere Schranke des Triggers und max die obere.
    def __init__(self, triggerID, minimal, maximal, port, warnTrigger):
        self.triggerRange = [minimal, maximal]
        self.port = port
        self.triggerID = triggerID
        self.port.addObserver(self)
        self.warnTrigger = warnTrigger

    # wird ausgelöst, wenn der Port sich verändert.
    def observableChanged(self, observable):
        self.check()

    # Prüft ob der Trigger ausgelöst werden soll
    def check(self):
        if self.triggerRange[0] <= self.port.getState() or self.port.getState() <= self.triggerRange[1]:
            self.callAlerts()

    # ruft alle alerts auf
    def callAlerts(self):
        for alert in self.alerts:
            alert.throwAlert(self.port)

    # ibt den minimalen Wert zurück bei dem der Trigger auslöst.
    def minimalValue(self):
        return self.triggerRange[0]

    # gibt den maximalen wert zurück bei dem der Trigger auslöst.
    def maximalValue(self):
        return self.triggerRange[1]

    # fügt ein neues alert Objekt hinzu.
    def appendAlert(self, alert):
        self.alerts.append(alert)

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
        self.alerts.remove(alert)

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

    # zwei Trigger sind gleich, wenn ihre ID gleich ist.
    def __eq__(self, other):
        if self.__class__ == other.__class__:
            if self.getID() == other.getID():
                return True
            else:
                return False
        else:
            return False
