import UI.Helper.URLStripper as URLHelper
from UI.Helper.template import template
from jinja2 import Template

class editConf():
    portService = None
    path = ""

    def __init__(self, rqPath,portService):
        self.portService = portService
        self.path = rqPath

    def getDisplayString(self):
        # wenn es keine tieferen Verweise gibt.
        if URLHelper.getSubmodule(self.path) == "":
            return self.index()

    def index(self):
        template = Template("Hello {{ name }}")
        return bytes(template.render(name="Peter"), "utf-8")

    def getStatus(self):
        return 200

    def getContentType(self):
        return "text/html"