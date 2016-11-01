import json
#returns the current state of all ports.

class rawCurrentState:
    portService = None
    rqPath = ""

    def __init__(self, rqPath, portService):
        self.portService = portService
        self.rqPath = rqPath

    def getDisplayString(self):
        ports = self.portService.getPorts()
        output = {}
        for key, value in ports.items():
            output[key] = value.getCurrentInformation()

        return bytes(str(json.dumps(output)), "utf-8")

    def getContentType(self):
        #TODO: change this to text/json in production
        return "text/html"

    def getStatus(self):
        return 200