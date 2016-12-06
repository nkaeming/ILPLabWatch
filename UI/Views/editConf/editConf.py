import UI.Helper.URLStripper as URLHelper

from jinja2 import Environment
from jinja2 import FileSystemLoader


class editConf():
    portService = None
    path = ""
    env = None

    def __init__(self, rqPath, portService):
        self.portService = portService
        self.path = rqPath
        self.env = Environment()
        self.env.loader = FileSystemLoader(".")

    def getDisplayString(self):
        # wenn es keine tieferen Verweise gibt.
        if URLHelper.getSubmodule(self.path) == "":
            return self.index()
        elif URLHelper.getSubmodule(self.path) != "":
            return self.editPort(URLHelper.getSubmodule(self.path))

    def editPort(self, portID):
        template = self.env.get_template("UI/Views/editConf/layouts/editPortConf.html")
        settings = self.portService.getPort(portID).getCurrentInformation()
        return bytes(template.render(activeSite="editConf", portSettings=settings), "utf-8")

    def index(self):
        template = self.env.get_template("UI/Views/editConf/layouts/editTemplate.html")
        portsList = self.portService.getPorts()
        portsInformation = {}
        for port in portsList.values():
            portsInformation[port.getName()] = port.getCurrentInformation()

        return bytes(template.render(ports=portsInformation, activeSite="editConf"), "utf-8")

    def getStatus(self):
        return 200

    def getContentType(self):
        return "text/html"
