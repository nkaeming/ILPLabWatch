from Alerts.AbstractAlert import AbstractAlert
import RPIO


class GPIOOutput(AbstractAlert):
    """
    Dieser Alert schlatet einen digitalen GPIO Port.
    """
    GPIOPin = 0
    OnIfCalled = True

    def __init__(self, alertID, settings):
        super().__init__(alertID, settings)

        self.GPIOPin = self.getSetting('GPIOPin')
        initialState = self.getSetting('initialState') == "True"
        self.OnIfCalled = self.getSetting('OnIfCalled') == "True"
        RPIO.setmode(RPIO.BCM)

        if initialState == True:
            initialState = RPIO.HIGH
        else:
            initialState = RPIO.LOW

        RPIO.setup(self.GPIOPin, RPIO.OUT)
        RPIO.output(self.GPIOPin, RPIO.LOW)

    def throwAlert(self, port, trigger):
        if self.OnIfCalled:
            RPIO.output(self.GPIOPin, RPIO.HIGH)
        else:
            RPIO.output(self.GPIOPin, RPIO.LOW)

    def getDescription(self):
        return "Ein Alert der einen digitalen GPIO Port schaltet."