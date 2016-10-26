from bs4 import BeautifulSoup

#this is the class of the Status page
class addPort:
    portService = ""
    def __init__(self, portService):
        self.portService = portService

    def getDisplayString(self):
        template = open("Deamons/Web/addPort/addPort.html", "r")
        template = template.read()

        bs = BeautifulSoup(template, "html.parser")

        return str(bs.prettify())