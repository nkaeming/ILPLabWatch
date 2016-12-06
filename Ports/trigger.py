import importlib
# Ein Trigger dient zur Verbindung zwischen den Ports und den Alerts.

class trigger():
    triggerRange = [0,0] # die erste zahl gibt den minimalen Wert an, bei der der Trigger auslöst. Die zweite Zahl gibt die obere Grenze an.

    port = None # der Port mit dem der Trigger verknüpft ist.

    alerts = {} # die alerts mit denen der trigger verbunden ist.

    # min ist die untere Schranke des Triggers und max die obere.
    def __init__(self, min, max, port):
        self.triggerRange = [min, max]
        self.port = port

    # Prüft ob der Trigger ausgelöst werden soll
    def check(self):
        if self.port.getState() <= self.triggerRange[0] or self.port.getState() >= self.triggerRange[1]:
            self.informAlerts()

    # ruft alle alerts auf
    def informAlerts(self):
        for alert, params in self.alerts.items():
            alertClass = getattr(importlib.import_module("Ports.PortAlerts." + alert), alert)
            alertInstance = alertClass()
            alertInstance.throwAlert(self.port, params)

    # fügt dem trigger einen Alert hinzu.
    def addAlert(self, alertType, settings):
        self.alerts[alertType] = settings