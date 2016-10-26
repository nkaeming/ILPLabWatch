from bs4 import BeautifulSoup
import os
from Ports import PortTypes


#this is the class of the Status page
class addPort:
    portService = ""
    def __init__(self, portService):
        self.portService = portService

    def getDisplayString(self, opt):
        #read all available Port types.
        #TODO: load the place for the prot types from the config
        #TODO: maybe its better to load the ports by the classnames and not by the file names
        availablePortTypes = []
        for item in os.listdir("Ports/portTypes"):
            if item.endswith(".py") and item != "__init__.py":
                availablePortTypes.append(str(item).split(".")[0])



        template = open("Deamons/Web/addPort/addPort.html", "r")
        template = template.read()

        bs = BeautifulSoup(template, "html.parser")

        portSelectTag = bs.find("select", {"id": "portTypeSelect"})

        #adding each available PortType to the selection List.
        for type in availablePortTypes:
            tag = bs.new_tag("option", value=type)
            tag.append(type)
            portSelectTag.append(tag)

        return str(bs.prettify())

    #in this configuration step the port type is selected
    def portSelectStep(self):
        ...