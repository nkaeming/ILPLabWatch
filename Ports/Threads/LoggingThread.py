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
        while True and self.running == True:
            self.port.log()
            time.sleep(self.port.getSetting("logCycle"))

    def stop(self):
        self.running = False
