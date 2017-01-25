from Ports.AbstractPort import AbstractPort

class DummyPort2(AbstractPort):
    def __init__(self, childSettings, id):
        super().__init__(childSettings, id)
        # Verbindung initialisieren....
        self.minRefreshTime = 1
        self.nachInit()

    def getPrivateState(self):
        return 5

    def getValueRange(self):
        return [0, 10, 1]

    def getDescription(self):
        return "Dieser ist besonders toll."