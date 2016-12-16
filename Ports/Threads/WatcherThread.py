import time
from threading import Thread


class WatcherThread(Thread):
    """Der WatcherThread wird immer dann benutzt, wenn der Port selber nicht in der lage ist bei Veränderung zu reagieren."""
    port = None

    def __init__(self, port):
        self.port = port
        super().__init__()

    def run(self):
        lastState = 0
        while True:
            newState = self.port.getPrivateState()
            if lastState != newState:
                self.port.portChanged(newState)
                lastState = newState
            time.sleep(self.port.getMinRefreshTime())
