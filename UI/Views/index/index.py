import UI.Helper.URLStripper as URLHelper
from UI.Helper.template import template
#This class makes the main page.
class index():
    portService = None

    def __init__(self, rqPath, portService):
        self.portService = portService

    #returns the DisplayString of the content as byte object
    def getDisplayString(self):
        bs = template("index")
        lastRow = bs.addRow()
        container = bs.getCollumnDiv(12)
        header = bs.getHeading(1, "ILP Lab Watch")
        header.append(bs.getIcon("globe"))
        container.append(header)
        lastRow.append(container)

        return bs.getPrettifyedByteObject()

    def getContentType(self):
        return "text/html"

    def getStatus(self):
        return 200