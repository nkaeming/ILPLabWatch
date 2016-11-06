import json
import LogModule.logReader as logReader
import UI.Helper.URLStripper as urlStripper
from datetime import datetime, timedelta


class rawLogs:
    rqPath = ""
    status = 404
    logData = []

    def __init__(self, rqPath, portService):
        self.rqPath = rqPath
        portName = urlStripper.getSubmodule(rqPath)
        if portService.doesPortExistByName(portName):
            try:
                dateRange = urlStripper.getGetInormations(rqPath)
                start = datetime.strptime(dateRange["start"], "%d:%m:%Y:%H:%M:%S")
                end = datetime.strptime(dateRange["end"], "%d:%m:%Y:%H:%M:%S")
            except IndexError:
                start = datetime.now() - timedelta(minutes=10)
                end = datetime.now()

            self.logData = logReader.readLog(portName, start, end)
            self.status = 200
            print(self.logData)

    def getDisplayString(self):
        return bytes(str(json.dumps(self.logData)), "utf-8")

    def getStatus(self):
        return self.status

    def getContentType(self):
        # TODO: change this to text/json in production
        return "text/html"