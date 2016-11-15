import UI.Helper.URLStripper as URLHelper
from UI.Helper.template import template
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
        elif URLHelper.getSubmodule(self.rqPath) == "savePortSettings":
            params = URLHelper.getGetInormations(self.rqPath)
            output = self.savePortSettings(params)
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
        formTag.append(bs.getLinkButton(label="Abbrechen", type="danger", icon="remove", href="/index"))

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
        formCollumn = bs.getCollumnDiv(6,3)
        formRow.append(formCollumn)

        formTag = bs.getForm("savePortSettings")
        formCollumn.append(formTag)

        freePorts = self.portService.getFreeExternalPorts(portType)

        # adds the Porttype as a hidden input.
        formTag.append(bs.getHiddenInput("portType", portType))

        formTag.append(bs.getSelectInput(name="externalPort", helpText="Wähle den Anschlussport an der Connector Box.", values=dict(zip(freePorts, freePorts)), lable="Anschlussport"))

        # generiere für jede Option ein eigenes Eingabefeld. Reihenfolge richtet sich nach tab option.
        for option in sorted(portOptions, key=lambda optionName: portOptions[optionName]["tab"]):
            options =  portOptions[option]
            if options["type"] == "text":
                formTag.append(bs.getTextInput(name=option, helpText=options["description"], label=options["name"], value=options["standard"]))
            elif options["type"] == "boolean":
                formTag.append(bs.getCheckboxInput(name=option, helpText=options["description"], label=options["name"], value=options["standard"]))
            elif options["type"] == "number":
                formTag.append(bs.getNumberInput(name=option, helpText=options["description"], label=options["name"], value=options["standard"], minValue=options["min"], maxValue=options["max"], step=options["step"]))

        formTag.append(bs.getButton(type="submit", style="primary", icon="save", lable="Port hinzufügen"))
        formTag.append(bs.getLinkButton(label="Abbrechen", type="danger", icon="remove", href="/index"))
        return bs

    def savePortSettings(self, params):
        bs = template("addPort", "Neuen Port hinzufügen")

        portOptions = self.portService.getOptionsOfPortType(params["portType"])
        settings = URLHelper.convertGetInformations(self.rqPath, portOptions)
        externalPort = params["externalPort"]

        # fehlerhafte Felder in der form {"name": "Hinweis"}
        wrongFields = {}

        # überprüfen ob alle Eingabe korrekt und mit dem Sytsem vereinbar sind.
        # ist der externe Port noch konfiguartionsfrei.
        if not self.portService.isExternalPortFree(externalPort):
            wrongFields["externalPort"] = "Der ausgewählte Port ist nicht frei."
        # ist der Portname bereits vergeben
        if self.portService.doesPortExistByName(settings["name"]):
            wrongFields["name"] = "Der Portname ist bereits vergeben."
        else:
            # entspricht der Portname den Regeln für Portnamen. [a-z][A-Z][0-9]
            import re
            if re.fullmatch('[A-Za-z0-9]+', settings["name"]) == None:
                wrongFields["name"] = "Der Name entspricht nicht den Bedingungen an Portnamen."
        # prüfe ob das Loggingintervall konform ist
        if not (settings["logCycle"] <= int(portOptions["logCycle"]["max"]) and int(portOptions["logCycle"]["min"]) <= settings["logCycle"]):
            wrongFields["logCycle"] = "Das Loggingintervall ist unzulässig."

        row = bs.addRow()
        collumn = bs.getCollumnDiv(6,3)
        row.append(collumn)

        # wenn alle Eingaben ok sind, neuen Port erstellen.
        if len(wrongFields) == 0:
            try:
                self.portService.addPort(params["portType"], settings, externalPort)
                bodyTag = bs.getParagraph("Der neue Port wurde erstellt.")
                bodyTag.append(bs.getLinkButton(label="Zur Startseite", href="/index", icon="home", type="success"))
                collumn.append(bs.getPanel(
                    body=bodyTag,
                    header="Alles o.k.", type="success"))
            except FileNotFoundError:
                collumn.append(bs.getPanel(
                    body="Es ist ein Fehler beim Erstellen des Ports passiert. Bitte versuche es erneut oder kontaktiere einen Administrator.",
                    header="Fehler", type="danger"))
        else:
            self.wrongInputCorrection(bs, wrongFields, settings, externalPort, params["portType"])

        return bs

    def wrongInputCorrection(self, bs, wrongFields, settings, externalPort, portType):
        # alle Portoptionen die möglich sind.
        portOptions = self.portService.getOptionsOfPortType(portType)

        formRow = bs.addRow()
        formCollumn = bs.getCollumnDiv(6, 3)
        formRow.append(formCollumn)

        formTag = bs.getForm("savePortSettings")
        formCollumn.append(formTag)

        freePorts = self.portService.getFreeExternalPorts(portType)

        # adds the Porttype as a hidden input.
        formTag.append(bs.getHiddenInput("portType", portType))

        formTag.append(bs.getSelectInput(name="externalPort", helpText="Wähle den Anschlussport an der Connector Box.",
                                         values=dict(zip(freePorts, freePorts)), lable="Anschlussport", value=externalPort))

        # generiere für jede Option ein eigenes Eingabefeld. Reihenfolge richtet sich nach tab option.
        for option in sorted(portOptions, key=lambda optionName: portOptions[optionName]["tab"]):
            options = portOptions[option]
            if options["type"] == "text":
                div = bs.getTextInput(name=option, helpText=options["description"], label=options["name"],
                                               value=settings[option])
            elif options["type"] == "boolean":
                div = bs.getCheckboxInput(name=option, helpText=options["description"], label=options["name"],
                                                   value=settings[option])
            elif options["type"] == "number":
                div = bs.getNumberInput(name=option, helpText=options["description"], label=options["name"],
                                                 value=settings[option], minValue=options["min"],
                                                 maxValue=options["max"], step=options["step"])

            # wenn die option als falsches Feld gewählt wurde, werden entsprechende Anzeigen verändert.
            if option in wrongFields.keys():
                div["class"] = div["class"] + " has-error"
                div.append(bs.getAlert(wrongFields[option], "danger"))
            else:
                div["class"] = div["class"] + " has-success"
            formTag.append(div)

        formTag.append(bs.getButton(type="submit", style="primary", icon="save", lable="Port hinzufügen"))
        formTag.append(bs.getLinkButton(label="Abbrechen", type="danger", icon="remove", href="/index"))
        return bs

    def getContentType(self):
        return "text/html"

    def getStatus(self):
        return 200