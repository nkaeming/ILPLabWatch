import json
import LogModule.logReader as logReader
import UI.Helper.URLStripper as urlStripper
from datetime import datetime

class rawLogs:
    rqPath = ""
    status = 404
    logData = []

    def __init__(self, rqPath, portService):
        self.rqPath = rqPath
        portName = urlStripper.getSubmodule(rqPath)
        print(portService.doesPortExistByName(portName))
        if portService.doesPortExistByName(portName):
            print("Hello")
            dateRange = urlStripper.getGetInormations(rqPath)
            #TODO: exception handling.
            start = datetime.strptime(dateRange["start"], "%d:%m:%Y:%H:%M:%S")
            end = datetime.strptime(dateRange["end"], "%d:%m:%Y:%H:%M:%S")
            self.logData = logReader.readLog(portName, start, end)
            print(dateRange)
            self.status = 200

    def getDisplayString(self):
        return bytes(str(json.dumps(self.logData)), "utf-8")

    def getStatus(self):
        return self.status

    def getContentType(self):
        # TODO: change this to text/json in production
        return "text/html"