from Alerts.AbstractAlert import AbstractAlert
import RPi.GPIO as GPIO


class GPIOOutput(AbstractAlert):
    """
    Dieser Alert schlatet einen digitalen GPIO Port.
    """
    GPIOPin = 0
    OnIfCalled = True

    def __init__(self, alertID, settings):
        self.GPIOPin = self.getSetting('GPIOPin')
        initialState = self.getSetting('initialState')
        self.OnIfCalled = self.getSetting('OnIfCalled')
        GPIO.setmode(GPIO.BCM)
        if initialState == True:
            initialState = GPIO.HIGH
        else:
            initialState = GPIO.LOW
        GPIO.setup(self.GPIOPin, GPIO.OUT)
        GPIO.output(self.GPIOPin, GPIO.LOW)

        super().__init__(alertID, settings)

    def throwAlert(self, port, trigger):
        GPIO.output(self.GPIOPin, GPIO.HIGH)
        if self.OnIfCalled:
            GPIO.output(self.GPIOPin, GPIO.HIGH)
        else:
            GPIO.output(self.GPIOPin, GPIO.LOW)

    def getDescription(self):
        return "Ein Alert der einen digitalen GPIO Port schaltet."