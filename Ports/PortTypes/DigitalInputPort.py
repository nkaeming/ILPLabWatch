#IOInputPort is a port that only reads a on/off signal from a port.
import Ports.abstractPort as AbstractPort
import os


class DigitalInputPort(AbstractPort.abstractPort):
    #port description
    description = "Anschluss eines 1/0 Schalters an die Version 1 Box von Tobi."

    #a dic to describe all settings of this port (espacially for the UI)
    options = {
        "inverted": {
            "type": "boolean",
            "description": "If enabled the Port is inverted.",
            "standard": 0
        }
    }

    #creates the port and set it up in the GPIO settings.
    def __init__(self, externalPort, settings):
        self.settings = settings
        super().__init__(int(externalPort))
        self.inputPort = True
        #TODO: in production uncomment the following line
        #os.system("gpio -g mode " + str(self.getInternalPort()) + " out")

    def getCurrentInformation(self):
        info = super().getCurrentInformation()
        info["inverted"] = self.settings["inverted"]
        return info

    #cheks the actual state of the port and returns 0 for an open switch and 1 for a colsed switch
    def getState(self):
        import random
        value = random.randint(0,1)
        #TODO: In production uncomment the following line and comment the random line.
        #value = int(os.popen("gpio -g read " + str(self.getInternalPort())).read().lines())

        if self.settings["inverted"] == True:
            if value == 1:
                value = 0
            else:
                value = 1
        return value

    def getDescription(self):
        return self.description