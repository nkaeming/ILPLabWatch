import time
from threading import Thread


class WatcherThread(Thread):
    """Der WatcherThread wird immer dann benutzt, wenn der Port selber nicht in der lage ist bei Veränderung zu reagieren."""
    port = None
    running = False

    def __init__(self, port):
        self.port = port
        super().__init__()

    def run(self):
        self.running = True
        while self.running:
            time.sleep(self.port.getMinRefreshTime())
            lastState = self.port.getState()
            newState = None
            if self.port.isPortOK() == False:
                 self.port.restartThreads()
                 break

            while newState == None:
                newState = self.port.getPrivateState()

            if lastState != newState:
                self.port.portChanged(newState)

    def stop(self):
        self.running = False
