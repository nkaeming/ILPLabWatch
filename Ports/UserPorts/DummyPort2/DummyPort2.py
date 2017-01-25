from Ports.AbstractPort import AbstractPort
import random

class DummyPort2(AbstractPort):
    def __init__(self, childSettings, id):
        super().__init__(childSettings, id)
        # Verbindung initialisieren....
        self.minRefreshTime = 1
        self.nachInit()

    def getPrivateState(self):
        return self.getSetting("returnValue") + random.randint(0,5)

    def getValueRange(self):
        return [0, 10, 1]

    def getDescription(self):
        return "Dieser ist besonders toll."