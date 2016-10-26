#IOInputPort is a port that only reads a on/off signal from a port.
import Ports.AbstractPort as AbstractPort
import os


class DigitalInputPort(AbstractPort.abstractPort):
    #IO Ports can be inverted. That means, 1 -> 0 and 0 -> 1
    inverted = False

    #port description
    description = "Anschluss eines 1/0 Schalters."

    #creates the port and set it up in the GPIO settings.
    def __init__(self, externalPort, settings):
        self.inverted = settings["inverted"]
        super().__init__(int(externalPort), settings)
        self.inputPort = True
        #TODO: in production uncomment the following line
        #os.system("gpio -g mode " + str(self.getInternalPort()) + " out")

    def getCurrentInformation(self):
        info = super().getCurrentInformation()
        info["inverted"] = self.inverted
        return info

    #cheks the actual state of the port and returns 0 for an open switch and 1 for a colsed switch
    def getState(self):
        import random
        value = random.randint(0,1)
        #TODO: In production uncomment the following line and comment the random line.
        #value = int(os.popen("gpio -g read " + str(self.getInternalPort())).read().rstrip())

        if self.inverted == True:
            if value == 1:
                value = 0
            else:
                value = 1
        return value

    def getDescription(self):
        return self.description