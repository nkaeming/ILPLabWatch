from UI.AbstractView import AbstractView
from UI.Models.OptionField import OptionField
import cherrypy


class addPort(AbstractView):
    """View zum erstellen neuer Ports."""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self):
        return self.jinjaEnv.get_template("selectPortType.html").render(
            portTypes=self.PortService.getConfigurablePortTypes(), page="hinzufuegen")

    @cherrypy.expose
    def portSetUP(self, portType):
        options = self.PortService.getPortClassByType(portType).getOptions()
        freePortConnections = self.PortService.getFreeInputsOfPortType(portType)
        freePorts = []
        for item in freePortConnections:
            freePorts.append((item, item))

        internalPortSelector = OptionField('wiring',
                                           {
                                               'type': 'select',
                                               'options': freePorts,
                                               'description': 'Der Anschluss an dem das zu überwachende Gerät angeschlossen wurde.',
                                               'tab': -42,
                                               'required': True,
                                               'name': 'Anschluss'
                                           })

        # ersetlle eine Liste mit dem internalPortSelector
        optionFields = [internalPortSelector]
        for optionName, optionSettings in options.items():
            optionFields.append(OptionField(optionName, optionSettings))

        optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())

        return self.jinjaEnv.get_template("setSettingsOfPort.html").render(wirings=freePortConnections,
                                                                           options=optionFields, page='hinzufuegen',
                                                                           portType=portType)

    @cherrypy.expose
    def savePort(self, **args):
        portType = args['type']
        options = self.PortService.getPortClassByType(portType).getOptions()
        optionFields = []
        allOK = True
        for option, setting in options.items():
            # Prüfen ob der Name bereits existiert.
            if option == 'name':
                suggestedName = args['name']
                if self.PortService.doesPortExistByName(suggestedName):
                    optionField = OptionField(name=option, settings=setting, value=args['name'],
                                              warnText="Der Name existiert bereits.")
                    allOK = False
                else:
                    optionField = OptionField(name=option, settings=setting, value=args[option])
            # prüfen ob der Anschluss noch frei ist.
            elif option == 'wiring':
                if not args['wiring'] in self.PortService.getFreeInputsOfPortType(portType):
                    optionField = OptionField(name=option, settings=setting, value=args['wiring'],
                                              warnText="Dieser Anschluss ist nicht mehr frei.")
                    allOK = False
                else:
                    optionField = OptionField(name=option, settings=setting, value=args[option])
            else:
                optionField = OptionField(name=option, settings=setting, value=args[option])

            if not optionField.evaluate():
                allOK = False
            optionFields.append(optionField)

        # Wenn alle Felder ordentlich ausgefüllt waren, wird er Port gespeichert.
        if allOK:
            portSettings = {'type': portType, 'wiring': args['wiring']}
            for optionField in optionFields:
                portSettings[optionField.getName()] = optionField.getValue()
            print(portSettings)
            portID = self.PortService.generateAndAddNewPort(portSettings)
            return self.jinjaEnv.get_template('savePort.html').render(portSettings=portSettings, portID=portID,
                                                                      page="hinzufuegen")
        else:
            # erzeugung der Selectoption für den Port.
            freePortConnections = self.PortService.getFreeInputsOfPortType(portType)
            freePorts = []
            for item in freePortConnections:
                freePorts.append((item, item))

            internalPortSelector = OptionField('wiring',
                                               {
                                                   'type': 'select',
                                                   'options': freePorts,
                                                   'description': 'Der Anschluss an dem das zu überwachende Gerät angeschlossen wurde.',
                                                   'tab': -42,
                                                   'required': True,
                                                   'name': 'Anschluss'
                                               }, value=args['wiring'])
            optionFields.append(internalPortSelector)
            # -----
            optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())
            freePortConnections = self.PortService.getFreeInputsOfPortType(portType)
            return self.jinjaEnv.get_template("setSettingsOfPort.html").render(wirings=freePortConnections,
                                                                               options=optionFields, page='hinzufuegen',
                                                                               portType=portType)
