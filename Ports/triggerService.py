import ConfModule.confAdapter as confAdapter
from Ports.trigger import trigger
# der Trigger Service verwaltet alle trigger im System. Da er ähnlich wie der PortService von allen Deamons benutzt wird, wurde sich dafür entschieden den TriggerService über den PortService aufrufbar zu machen.

class triggerService:
    trigger = {}
    portService = None

    def __init__(self, portService):
        self.portService = portService
        self.setUpTriggers()

    def setUpTriggers(self, triggerConf):
        for portName, port in self.portService.getPorts().values():
               triggers = confAdapter.getTriggersOf(portName)
               for id, setUp in triggers.items():
                   trig = self.setUpTrigger(port, setUp["range"][0], setUp["range"][1], setUp["alerts"])
                   self.trigger[portName].append(trig)

    # returns a setted up trigger (like a factory)
    def setUpTrigger(self, port, min, max, alerts):
        trig = trigger(min, max, port)
        for alertName, alertSettings in alerts.items():
            trig.addAlert(alertName, alertSettings)
        return trig

    # returns a list of all riggers for a port.
    def getTriggersForPort(self, portName):
        return self.trigger[portName]

    # adds a trigger.
    def addTrigger(self, min, max, port, alerts):
        confAdapter.addTrigger(port.getName(), alerts, min, max)
        trig = self.setUpTrigger(port, min, max, alerts)
        self.trigger[port.getName()].append(trig)