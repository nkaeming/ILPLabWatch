import random
from Ports.AbstractPort import AbstractPort


class DummyAnalogInputPort(AbstractPort):
    lastNumber = 0

    def __init__(self, settings, id):
        super().__init__(settings, id)
        random.seed(self.getSetting("randomSeed"))
        self.lastNumber = int((self.getSetting("max") - self.getSetting("min")) / 2)
        self.minRefreshTime = 5

    def getPrivateState(self):
        settings = self.getSettings()
        # generate a realistic value, near the old value.
        shortRangeValue = int((settings["max"] - settings["min"]) / 100)
        randomNumber = random.randint(-shortRangeValue, shortRangeValue)
        if randomNumber > settings["max"]:
            randomNumber = settings["max"]
        elif randomNumber < settings["min"]:
            randomNumber = settings["min"]

        self.lastNumber = self.lastNumber + randomNumber
        return self.lastNumber

    def getValueRange(self):
        settings = self.getSettings()
        interval = [settings["min"], settings["max"], 1]
        return interval

    def getDescription(self):
        return "Ein Dummyport, der zufällig generierte Zahlen ausgibt."
