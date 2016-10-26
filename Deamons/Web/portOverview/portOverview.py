from bs4 import BeautifulSoup

#this is the class of the Status page
class portOverview:
    portService = ""
    def __init__(self, portService):
        self.portService = portService

    def getDisplayString(self):
        template = open("Deamons/Web/portOverview/portOverview.html", "r")
        template = template.read()

        bs = BeautifulSoup(template, "html.parser")
        tableBody = bs.find("tbody")

        portList = self.portService.getPorts()
        for portNumber, port in portList.items():
            row = bs.new_tag("tr")
            nameTag = bs.new_tag("td")
            nameTag.append(port.getName())
            row.append(nameTag)

            conNumberTag = bs.new_tag("td")
            conNumberTag.append(str(port.getExternalPort()))
            row.append(conNumberTag)

            typeTag = bs.new_tag("td")
            typeTag.append(port.getType())
            row.append(typeTag)

            logCycleTag = bs.new_tag("td")
            logCycleTag.append(str(port.getLogCycle()))
            row.append(logCycleTag)

            stateTag = bs.new_tag("td", id=port.getName(), **{"class":"input-status yellow"})
            stateTag.append(str(port.getState()))
            row.append(stateTag)

            optionsTag = bs.new_tag("td")
            optionsTagLink = bs.new_tag("a", href="../edit/" + port.getName())
            optionsTagLink.append("Edit")
            optionsTag.append(optionsTagLink)
            row.append(optionsTag)

            tableBody.append(row)

        return str(bs.prettify())