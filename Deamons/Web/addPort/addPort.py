from bs4 import BeautifulSoup
import os
from Ports import PortTypes


#this is the class of the Status page
class addPort:
    portService = ""
    def __init__(self, portService):
        self.portService = portService

    def getDisplayString(self, opt):
        step = opt[2]

        #load the template file
        template = open("Deamons/Web/addPort/addPort.html", "r")
        template = template.read()
        bs = BeautifulSoup(template, "html.parser")
        headerTag = bs.find("h1", {"id": "header"})

        #decides which step is the actual step
        if step == "portSelect":
            self.portSelectStep(bs)
            headerTag.append("Select PortType")
        elif step == "portNumberSelect":
            self.portNumberSelectStep(bs)
            headerTag.append("Select PortNumber")
        elif step == "portConf":
            self.portConfStep(bs)

        return str(bs.prettify())

    #in this configuration step the port type is selected
    def portSelectStep(self, bs):
        # read all available Port types.
        # TODO: load the place for the prot types from the config
        # TODO: maybe its better to load the ports by the classnames and not by the file names
        availablePortTypes = []
        for item in os.listdir("Ports/portTypes"):
            if item.endswith(".py") and item != "__init__.py":
                availablePortTypes.append(str(item).split(".")[0])

        portSelectTag = bs.find("select", {"id": "portTypeSelect"})

        # adding each available PortType to the selection List.
        for type in availablePortTypes:
            tag = bs.new_tag("option", value=type)
            tag.append(type)
            portSelectTag.append(tag)

    #in this configuration step the port number is selected
    def portNumberSelectStep(self, bs):
        ...

    #in this coniguration step the final configuration of the port is done
    def portConfStep(self, bs):
        ...