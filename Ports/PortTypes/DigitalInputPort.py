# IOInputPort is a port that only reads a on/off signal from a port.
import Ports.abstractPort as AbstractPort
import os


class DigitalInputPort(AbstractPort.abstractPort):
    # port description
    description = "Anschluss eines 1/0 Schalters an die Version 1 Box von Tobi."

    # returns the available valueRange of this Port. An IO Port can only be 1 or 0.
    valueRange = [0, 1, 1]

    # a dic to describe all settings of this port (espacially for the UI)
    options = {
        "inverted": {
            "type": "boolean",
            "description": "Wenn aktiv, wird dieser Port invertiert.",
            "standard": 0,
            "name": "Invertieren",
            "tab": 1,
            "final": False
        }
    }

    # creates the port and set it up in the GPIO settings.
    def __init__(self, externalPort, settings):
        super().__init__(externalPort, settings)
        # TODO: in production uncomment the following line
        # os.system("gpio -g mode " + str(self.getInternalPort()) + " out")

    # cheks the actual state of the port and returns 0 for an open switch and 1 for a colsed switch
    def getState(self):
        import random
        value = random.randint(0, 1)
        # TODO: In production uncomment the following line and comment the random line.
        # value = int(os.popen("gpio -g read " + str(self.getInternalPort())).read().lines())

        if self.settings["inverted"] == True:
            if value == 1:
                value = 0
            else:
                value = 1
        return value

    def getValueRange(self):
        return self.valueRange

    def getOptions(self):
        return {**super().superOptions, **self.options}
