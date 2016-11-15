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
            "tab": 1
        },
        "min": {
            "name": "minimaler Wert",
            "type": "number",
            "description": "Der minimale Wert als Integer den der Dummyport ausgeben soll.",
            "standard": 0,
            "tab": 2,
            "min": -2000,
            "max": 2000,
            "step": 1
        },
        "max": {
            "name": "maximaler Wert",
            "type": "number",
            "description": "Der maximale Wert als Integer den der Dummyport ausgeben soll.",
            "standard": 1000,
            "tab": 3,
            "min": -2000,
            "max": 2000,
            "step": 1
        }
    }

    def __init__(self, externalPort, settings):
        super().__init__(externalPort, options, settings)
        random.seed(self.settings["randomSeed"])

    def getState(self):
        settings = self.getSettings()
        return random.randint(settings["min"], settings["max"])

    def getValueRange(self):
        settings = self.getSettings()
        interval = [settings["min"], settings["max"], 1]
        return interval

    def getOptions(self):
        return {**super().superOptions, **self.options}