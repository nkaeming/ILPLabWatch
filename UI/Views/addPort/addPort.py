import UI.Helper.URLStripper as URLHelper
import UI.Helper.template as layout
import UI.Helper.formGenerator as formGenerator
#This class represents the site for adding new Ports.
class addPort:
    portService = None
    rqPath = ""

    def __init__(self, rqPath, portService):
        self.portService = portService
        self.rqPath = rqPath

    #returns the DisplayString of the content as byte object
    def getDisplayString(self):
        template = layout.getTemplate()
        layout.setActiveNav(template, "addPort")
        layout.setHeading(template, "Port hinzufügen")
        form = formGenerator.getFormTag("GET", "asdasd")
        formGenerator.addRadioSelector(form, "Wähle den Porttyp aus:", "portTypeSelector", {"IOPort": {"optionText": "IOPort zum Anschließen von IO's", "value":"IOPort", "disabled":False}})

        layout.addContentTag(template, form)

        return bytes(str(template.prettify()), "utf-8")

    def getContentType(self):
        return "text/html"

    def getStatus(self):
        return 200