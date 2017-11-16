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
        GPIO.setmode(GPIO.BCM)
        self.portService = PS
        wiring = configIO.loadWiring()
        self.heartbeatLED = int(wiring['SystemPorts']['heartbeatLED'])
        self.warnLED = int(wiring['SystemPorts']['warnLED'])
        GPIO.setup(self.heartbeatLED, GPIO.OUT)
        GPIO.output(self.heartbeatLED, GPIO.LOW)
        GPIO.setup(self.warnLED, GPIO.OUT)
        GPIO.output(self.warnLED, GPIO.LOW)
        super().__init__()

    def run(self):
        self.running = True
        while self.running == True:
            self.checkWarnLED()
            GPIO.output(self.heartbeatLED, GPIO.LOW)
            time.sleep(1.0)
            GPIO.output(self.heartbeatLED, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.heartbeatLED, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(self.heartbeatLED, GPIO.HIGH)
            time.sleep(0.2)

    def checkWarnLED(self):
        if self.portService.arePortsOK():
            GPIO.output(self.warnLED, GPIO.LOW)
        else:
            GPIO.output(self.warnLED, GPIO.HIGH)

    def stop(self):
        self.running = False
