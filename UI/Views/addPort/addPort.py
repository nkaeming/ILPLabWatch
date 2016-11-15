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
        if URLHelper.getSubmodule(self.rqPath) == "setPortSettings":
            params = URLHelper.getGetInormations(self.rqPath)
            output = self.setPortSettings(params["portType"])
        else:
            output = self.selectPortType()

        return output.getPrettifyedByteObject()

    # the first step for a new port Config. The selection of the Porttype.
    def selectPortType(self):
        bs = template("addPort", "Neuen Port hinzufügen (Porttyp auswählen)")

        #generate the radioSelector Area
        radioSelectorRow = bs.addRow()
        radioSelectorCollumn = bs.getCollumnDiv(12)
        radioSelectorRow.append(radioSelectorCollumn)

        formTag = bs.getForm("/addPort/setPortSettings")
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

        return bs

    # the second step is to configure the Port.
    def setPortSettings(self, portType):
        bs = template("addPort", "Neuen Port hinzufügen (" + portType + ")")
        # alle Portoptionen die möglich sind.
        portOptions = self.portService.getOptionsOfPortType(portType)

        formRow = bs.addRow()
        formCollumn = bs.getCollumnDiv(6)
        formRow.append(formCollumn)

        formTag = bs.getForm("savePort")
        formCollumn.append(formTag)

        freePorts = self.portService.getFreeExternalPorts(portType)

        # adds the Porttype as a hidden input.
        formTag.append(bs.getHiddenInput("portType", portType))

        formTag.append(bs.getSelectInput(name="externalPort", helpText="Wähle den Anschlussport an der Connector Box.", values=dict(zip(freePorts, freePorts)), lable="Anschlussport"))

        # generiere für jede Option ein eigenes Eingabefeld. Reiehnfolge richtet sich nach tab option.
        for option in sorted(portOptions, key=lambda optionName: portOptions[optionName]["tab"]):
            options =  portOptions[option]
            if options["type"] == "text":
                formTag.append(bs.getTextInput(name=option, helpText=options["description"], lable=options["name"], placeholder=options["standard"]))
            elif options["type"] == "boolean":
                formTag.append(bs.getCheckboxInput(name=option, helpText=options["description"], lable=options["name"], value=options["standard"]))
            elif options["type"] == "number":
                formTag.append(bs.getNumberInput(name=option, helpText=options["description"], lable=options["name"], value=options["standard"], minValue=options["min"], maxValue=options["max"], step=options["step"]))

        formTag.append(bs.getButton(type="submit", style="primary", icon="save", lable="Port hinzufügen"))
        return bs

    def getContentType(self):
        return "text/html"

    def getStatus(self):
        return 200