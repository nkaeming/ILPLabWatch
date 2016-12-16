import time
from threading import Thread


class LoggingThread(Thread):
    """Dieser Thread wird benutzt um einen Port zu loggen."""
    port = None

    def __init__(self, port):
        self.port = port
        super().__init__()

    def run(self):
        while True:
            self.port.log()
            time.sleep(self.port.getSetting("logCycle"))
