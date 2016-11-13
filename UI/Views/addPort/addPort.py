import UI.Helper.URLStripper as URLHelper
from UI.Helper.template import template
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
        bs = template("addPort", "Neuen Port hinzufügen")

        #generate the radioSelector Area
        radioSelectorRow = bs.addRow()
        radioSelectorCollumn = bs.getCollumnDiv(12)
        radioSelectorRow.append(radioSelectorCollumn)

        formTag = bs.getForm("/addPort/2")
        radioSelectorCollumn.append(formTag)

        availablePorts = self.portService.getAvailablePortsInformations()
        displayItems = {}
        for key, value in availablePorts.items():
            displayItems[key] = {
                "value": key,
                "lable": key,
                "disabled": not value["available"],
                "description": value["description"]
            }

        radioSelector = bs.getMultipleRadioSelect(displayItems, "portType")
        formTag.append(bs.getHeading(2, "Bitte Porttyp wählen"))
        formTag.append(radioSelector)
        formTag.append(bs.getButton(lable="Weiter", style="success"))

        #generate the infoArea
        infoRow = bs.addRow()
        infoCollumn = bs.getCollumnDiv(12)
        infoRow.append(infoCollumn)

        infoPanel = bs.getPanel("Das System überprüft alle Ports auf ihre Anschlussverfügbarkeit. Ist ein Porttyp nicht mehr anwählbar, so wurden bereits alle Anschlüsse dieses Typs belegt oder die Connector Box verfügt über keine dieser Anschlüsse. Um bereits belegte Anschlüsse frei zu geben, müssen die entsprechenden Ports in der Übersicht gelöscht werden oder die wiringConf auf die Connector Box angepassst werden.", header="Manche Optionen sind nicht wählbar. Warum?")
        infoCollumn.append(infoPanel)

        return bs.getPrettifyedByteObject()

    def getContentType(self):
        return "text/html"

    def getStatus(self):
        return 200