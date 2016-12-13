import time
from threading import Thread


class LoggerDeamon(Thread):
    """The Logerdeamon logs all the Ports."""
    portService = None

    def __init__(self, portService):
        self.portService = portService
        super().__init__()

    def run(self):
        second = 0
        maxRes = 60
        print("logging started")

        # create a dictionary to save all possible logTimes. The logTimes will be count up in the dict
        possibleLogTimes = {}
        for i in range(1, maxRes):
            possibleLogTimes[i] = -1

        while True:
            second = second + 1
            thisTimeToLog = []
            for k, v in possibleLogTimes.items():
                possibleLogTimes[k] = v + 1
                # if the second counter of the period is reached the port get logged
                if possibleLogTimes[k] == k:
                    thisTimeToLog.append(k)
                    possibleLogTimes[k] = 0

            for i in thisTimeToLog:
                for port in self.portService.getPortsLoggedIn(i):
                    port.writeLog()
            if second == maxRes:
                second = 0
            time.sleep(1)
