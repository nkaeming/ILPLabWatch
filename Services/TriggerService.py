from Models.Observable import Observable
from Models.Observer import Observer


class TriggerService(Observer, Observable):
    """Der Trigger service verwaltet alle Trigger."""

    portService = None  # der verbundene Port Service

    triggerSettings = {}

    def __init__(self, portService):
        self.portService = portService
        self.setUpTrigger()

    # fügt den Ports als Listener alle Trigger hinzu.
    def updateTrigger(self):
        for portName, trigger in self.triggerSettings.items():
            for alertName, alertSettings in trigger["alerts"].items():
                port = self.portService.getPortByName(portName)
