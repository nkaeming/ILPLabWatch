import UI.Helper.URLStripper as URLHelper
from UI.Helper.template import template
from bs4 import BeautifulSoup

class editConf():
    portService = None

    def __init__(self, rqPath,portService):
        self.portService = portService

    def getDisplayString(self):
        bs = template("editConf", "Port Übersicht")
        content = BeautifulSoup(open("UI/Views/editConf/editTemplate.html"), "html.parser")
        bs.appendContent(content)
        return bs.getPrettifyedByteObject()

    def getStatus(self):
        return 200

    def getContentType(self):
        return "text/html"