import IOHelper.config as configIO
import time
import RPi.GPIO as GPIO
from threading import Thread


class LEDThread(Thread):
    """Dieser Thread wird benutzt um einen Port zu loggen."""
    portService = None
    statusLED = 0
    heartbeatLED = 0

    def __init__(self, PS):
        self.portService = PS
        wiring = configIO.loadWiring()
        self.heartbeatLED = wiring['SystemPorts']['hearbeatLED']
        self.warnLED = wiring['SystemPorts']['warnLED']
        GPIO.setup(self.heartbeatLED, GPIO.OUT)
        GPIO.setup(self.warnLED, GPIO.OUT)
        for i in range(0, 3):
            GPIO.output(self.heartbeatLED, GPIO.HIGH)
            GPIO.output(self.warnLED, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(self.heartbeatLED, GPIO.LOW)
            GPIO.output(self.warnLED, GPIO.LOW)

        super().__init__()

    def run(self):
        self.running = True
        while self.running == True:
            self.checkWarnLED()
            GPIO.output(self.heartbeatLED, GPIO.LOW)
            time.sleep(0.5)
            self.checkWarnLED()
            GPIO.output(self.heartbeatLED, GPIO.HIGH)
            time.sleep(0.5)

    def checkWarnLED(self):
        if self.portService.arePortsOK():
            GPIO.output(self.warnLED, GPIO.LOW)
        else:
            GPIO.output(self.warnLED, GPIO.HIGH)

    def stop(self):
        self.running = False
