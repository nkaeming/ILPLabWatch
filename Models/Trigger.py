import importlib
from Models.Observer import Observer


# Ein Trigger dient zur Verbindung zwischen den Ports und den Alerts.

class Trigger(Observer):
    """Trigger werden ausgelöst, wenn ein Port kritische Werte erreicht."""

    triggerRange = [0,
                    0]  # die erste zahl gibt den minimalen Wert an, bei der der Trigger auslöst. Die zweite Zahl gibt die höchste Zahel an, bei der der Trigger auslöst.

    port = None  # der Port mit dem der Trigger verknüpft ist.

    alerts = []  # die alerts mit denen der trigger verbunden ist.

    warnTrigger = False  # gibt an ob der Trigger im UI als Warntrigger auftauchen soll.

    # min ist die untere Schranke des Triggers und max die obere.
    def __init__(self, min, max, port):
        self.triggerRange = [min, max]
        self.port = port
        self.port.addObserver(self)

    # wird ausgelöst, wenn der Port sich verändert.
    def observableChanged(self, observable):
        self.check()

    # Prüft ob der Trigger ausgelöst werden soll
    def check(self):
        if self.port.getState() <= self.triggerRange[0] or self.port.getState() >= self.triggerRange[1]:
            self.callAlerts()

    # ruft alle alerts auf
    def callAlerts(self):
        for alert in self.alerts:
            alert.throwAlert(self.port)

    # fügt dem trigger einen Alert hinzu.
    def addAlert(self, alertType, settings):
        alertClass = getattr(importlib.import_module("Alerts." + alertType + "." + alertType), alertType)
        self.alerts.append(alertClass(settings))

    # gibt true zurück, wenn der Trigger als Warnung im UI auftauchen soll.
    def isWarnTrigger(self):
        return self.warnTrigger
