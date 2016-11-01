import UI.Helper.URLStripper as URLHelper
import UI.Helper.template as layout
#This class makes the main page.
class index():
    portService = None

    def __init__(self, rqPath, portService):
        self.portService = portService

    #returns the DisplayString of the content as byte object
    def getDisplayString(self):
        template = layout.getTemplate()
        layout.setActiveNav(template, "index")
        layout.addUpdateStatusJS(template)
        return bytes(str(template.prettify()), "utf-8")

    def getContentType(self):
        return "text/html"

    def getStatus(self):
        return 200