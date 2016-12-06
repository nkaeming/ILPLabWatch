import Ports.portService as portService
import time

#to Start a loggerDeamon a valid port Service has to be created
def loggerDeamon(portService):
    print("triggering started")

    while True:
        triggers = portService.getTriggerService.getTriggers()
        for trigger in triggers:
            trigger.check()