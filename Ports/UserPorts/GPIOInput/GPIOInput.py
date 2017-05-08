import RPIO
from Ports.AbstractPort import AbstractPort


class GPIOInput(AbstractPort):
    lastNumber = 0
    isSelfUpdating = True

    def __init__(self, settings, id):
        super().__init__(settings, id)
        self.__setupConnecttions()
        self.nachInit()

    def __setupConnecttions(self):
        pin = self.getInternalPin()
        RPIO.add_interrupt_callback(pin, self.__callbackFunction)
        RPIO.wait_for_interrupts(threaded=True)

    def __callbackFunction(self, gpioID, value):
        print(value)
        self.portChanged(value)

    def getValueRange(self):
        return (0,1)

    def getDescription(self):
        return "Ein GPIO Input kann nur digitale Signale verarbeiten. Er kann z.B. für einen einfachen Schalter verwendet werden."