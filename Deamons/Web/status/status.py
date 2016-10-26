from bs4 import BeautifulSoup

#this is the class of the Status page
class Status:
    portService = ""
    def __init__(self, portService):
        self.portService = portService

    def getDisplayString(self):
        template = open("Deamons/Web/status/status.html", "r")
        template = template.read()

        bs = BeautifulSoup(template, "html.parser")
        topColumn = bs.find("tr", {"id":"status-table-top"})
        bottomColumn = bs.find("tr", {"id":"status-table-bottom"})

        portList = self.portService.getPorts()
        for portNumber, port in portList.items():
            portName = port.getName()
            dataTopTag = bs.new_tag("td")
            dataTopTag.append(portName)
            dataBottomTag = bs.new_tag("td", id=portName, **{"class":"input-status yellow"})
            topColumn.append(dataTopTag)
            bottomColumn.append(dataBottomTag)

        return str(bs)