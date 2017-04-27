import time
from threading import Thread


class LoggingThread(Thread):
    """Dieser Thread wird benutzt um einen Port zu loggen."""
    port = None
    running = False

    def __init__(self, port):
        self.port = port
        super().__init__()

    def run(self):
        self.running = True
        while self.running == True:
            if self.port.isInitialized():
                time.sleep(self.port.getSetting("logCycle"))
                self.port.log()

    def stop(self):
        self.running = False
