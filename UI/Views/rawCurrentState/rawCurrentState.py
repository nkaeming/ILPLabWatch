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
        for key, port in ports.items():
            output[key] = port.getCurrentInformation()
            # TODO: An dieser Stelle wird mit lastCall =0 reingegangen und last Call richtig gesetzt. Wo ist der Fehler???

        return bytes(str(json.dumps(output)), "utf-8")

    def getContentType(self):
        #TODO: change this to text/json in production
        return "text/html"

    def getStatus(self):
        return 200