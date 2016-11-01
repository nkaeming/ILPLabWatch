import UI.Helper.URLStripper as URLHelper
import UI.Helper.layout as layout
#This class makes the main page.
class index():
    portService = None

    def __init__(self, rqPath, portService):
        self.portService = portService

    #returns the DisplayString of the content as byte object
    def getDisplayString(self):
        template = layout.getTemplate()
        return bytes(str(template), "utf-8")

    def getContentType(self):
        return "text/html"

    def getStatus(self):
        return 200