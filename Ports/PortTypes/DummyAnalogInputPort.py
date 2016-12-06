from Ports.abstractPort import abstractPort
import random
# Ein Dummy Port, der random Analog Inputs generiert.


class DummyAnalogInputPort(abstractPort):
    description = "Ein Analoger Dummy Port, der zufällig Integer zwischen den beiden angegebenen Zahlen generiert."

    options = {
        "randomSeed": {
            "name": "Random Seed",
            "type": "text",
            "description": "Ein Seed für den Zufallsgenerator.",
            "standard": "abc",
            "tab": 1,
            "final": True
        },
        "min": {
            "name": "minimaler Wert",
            "type": "number",
            "description": "Der minimale Wert als Integer den der Dummyport ausgeben soll.",
            "standard": 0,
            "tab": 2,
            "min": -2000,
            "max": 2000,
            "step": 1,
            "final": False
        },
        "max": {
            "name": "maximaler Wert",
            "type": "number",
            "description": "Der maximale Wert als Integer den der Dummyport ausgeben soll.",
            "standard": 1000,
            "tab": 3,
            "min": -2000,
            "max": 2000,
            "step": 1,
            "final": False
        }
    }

    lastNumber = 0

    def __init__(self, externalPort, settings):
        super().__init__(externalPort, settings)
        random.seed(self.settings["randomSeed"])
        self.lastNumber = int((settings["max"] - settings["min"]) / 2)

    def getState(self):
        settings = self.getSettings()
        # generate a realistic value, near the old value.
        shortRangeValue = (settings["max"] - settings["min"]) / 100
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

    def getOptions(self):
        return {**super().superOptions, **self.options}