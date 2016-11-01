from http.server import BaseHTTPRequestHandler, HTTPServer
from UI.CDN.cdnProvider import cdnProvider
import UI.Helper.URLStripper as URLStripper
import importlib
import json

HOST_NAME = ""
PORT_NUMBER = 8080

#Class Factory for the Request Handler.
def handlerClassFactory(portServiceParam):

    class responseToRequest(BaseHTTPRequestHandler):

        portService = ""

        def __init__(self, *args, **kwargs):
            self.portService = portServiceParam
            super(responseToRequest, self).__init__(*args, **kwargs)

        def do_HEAD(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_GET(self):
            self.do_HEAD()
            rqPath = self.path

            if URLStripper.getModule(rqPath) == "CDN":
                provider = cdnProvider()
                self.wfile.write(provider.getDisplayString(rqPath))
            else:
                module = URLStripper.getModule(rqPath)
                class_ = getattr(importlib.import_module("UI.Views." + module + "." + module), module)
                instance = class_()
                self.wfile.write(instance.getDisplayString(rqPath))


            rqPage = rqPath.split("/")
            if False:
                #returns the states of the ports
                if rqPage[1] == "api":
                    ports = self.portService.getPorts()
                    states = {}
                    for portNumber, port in ports.items():
                        states[portNumber] = port.getCurrentInformation()
                    self.wfile.write(bytes(json.dumps(states), "utf-8"))
                #returns the jquery framework
                elif rqPage[1] == "jquery":
                    file = open("Deamons/Web/jquery.js", "r")
                    self.wfile.write(bytes(file.read(), "utf-8"))
                elif rqPage[1] == "portOverview":
                    portOverviewPage = portOverview(self.portService)
                    self.wfile.write(bytes(portOverviewPage.getDisplayString(), "utf-8"))
                elif rqPage[1] == "addPort":
                    addPortPage = addPort(self.portService, rqPage)
                    self.wfile.write(bytes(addPortPage.getDisplayString(), "utf-8"))
                else:
                    statuspage = StatusPage(self.portService)
                    self.wfile.write(bytes(statuspage.getDisplayString(), "utf-8"))
    return responseToRequest

def startWebDeamon(portService):
    serverClass = HTTPServer
    handlerClass = handlerClassFactory(portService)
    httpd = serverClass((HOST_NAME, PORT_NUMBER), handlerClass)
    print("Webservice started")
    httpd.serve_forever()