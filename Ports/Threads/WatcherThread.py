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
        self.port.portChanged(self.port.getPrivateState())
        lastState = self.port.getPrivateState()
        while True and self.running == True:
            time.sleep(self.port.getMinRefreshTime())
            newState = None
            while newState == None:
                newState = self.port.getPrivateState()

            if lastState != newState:
                self.port.portChanged(newState)
                lastState = newState

    def stop(self):
        self.running = False
