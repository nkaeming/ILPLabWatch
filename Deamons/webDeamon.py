from http.server import BaseHTTPRequestHandler, HTTPServer
from UI.CDN.cdnProvider import cdnProvider
import UI.Helper.URLStripper as URLStripper
from UI.Views.index.index import index as MainPage
import importlib
import json

HOST_NAME = ""
PORT_NUMBER = 8080

#Class Factory for the Request Handler.
def handlerClassFactory(portServiceParam):

    class responseToRequest(BaseHTTPRequestHandler):

        portService = None

        def __init__(self, *args, **kwargs):
            self.portService = portServiceParam
            super(responseToRequest, self).__init__(*args, **kwargs)

        def do_HEAD(self, contentType, responseStatus):
            self.send_response(responseStatus)
            self.send_header("Content-type", contentType)
            self.end_headers()

        def do_GET(self):
            rqPath = self.path

            #if the request is an CDN request it is directed to the CDN Class.
            if URLStripper.getModule(rqPath) == "CDN":
                provider = cdnProvider(rqPath)
                contentType = provider.getContentType()
                status = provider.getStatus()
                self.do_HEAD(contentType, status)
                self.wfile.write(provider.getDisplayString())
            #if no module is given, redirect to index page
            elif URLStripper.getModule(rqPath) == "":
                instance = MainPage(rqPath, portServiceParam)
                contentType = instance.getContentType()
                status = instance.getStatus()
                self.do_HEAD(contentType, status)
                self.wfile.write(instance.getDisplayString())
            #select the module and direct to the module
            else:
                module = URLStripper.getModule(rqPath)
                try:
                    class_ = getattr(importlib.import_module("UI.Views." + module + "." + module), module)
                    instance = class_(rqPath, portServiceParam)
                    contentType = instance.getContentType()
                    status = instance.getStatus()
                    self.do_HEAD(contentType, status)
                    self.wfile.write(instance.getDisplayString())
                except ImportError:
                    self.do_HEAD("text/html", 404)
                    self.wfile.write(bytes("404 Error detected.", "utf-8"))
    return responseToRequest

def startWebDeamon(portService):
    serverClass = HTTPServer
    handlerClass = handlerClassFactory(portService)
    httpd = serverClass((HOST_NAME, PORT_NUMBER), handlerClass)
    print("webservice started")
    httpd.serve_forever()