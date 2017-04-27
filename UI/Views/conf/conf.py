from UI.AbstractView import AbstractView
import cherrypy
from UI.Models.OptionField import OptionField
from Ports.AbstractPort import AbstractPort
from Alerts.AbstractAlert import AbstractAlert


class conf(AbstractView):
    """View zum editieren von Porteinstellungen."""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self):
        """Bei nicht erkanntem Index oder Namen wird eine Liste aller Ports ausgegeben."""
        return self.jinjaEnv.get_template("portEditOverview.html").render(
            page="verwalten", portList=self.PortService.getPorts(), alertList=self.AlertService.getAlerts())

    @cherrypy.expose
    def editPort(self, portID=0, portName=""):
        """Konfigurationsseite anhand der PortID oder des Portnamen ausgeben"""
        if portID != 0:
            port = self.PortService.getPortByID(portID)
        elif portName != "":
            port = self.PortService.getPortByName(portName)
        else:
            raise cherrypy.HTTPRedirect("/conf")
        return self.returnConfigPage(port)

    @cherrypy.expose
    def portEditOptions(self, portID=""):
        """Zeigt die Einstellungsmöglichkeiten für diesen Port an."""
        if portID == "":
            raise cherrypy.HTTPRedirect('/conf')
        port = self.PortService.getPortByID(portID)

        if isinstance(port, AbstractPort):
            triggers = self.TriggerService.getTriggerByPort(port)
            return self.jinjaEnv.get_template("portEditOptions.html").render(
                page="verwalten", port=port, triggers=sorted(triggers, key=lambda x: x.getMinimalValue()))
        else:
            raise cherrypy.HTTPRedirect('/conf')

    @cherrypy.expose
    def alertEditOptions(self, alertID=""):
        """Zeigt die Einstellungsmöglichkeiten für diesen Alert an."""
        if alertID == "":
            raise cherrypy.HTTPRedirect('/conf')
        alert = self.AlertService.getAlertByID(alertID)

        if isinstance(alert, AbstractAlert):
            optionFields = []
            options = alert.getOptions()
            for optionName, optionSettings in options.items():
                # wenn die Einstellung final ist, der Typ des Inputfelds auf einfach Textausgabe setzen.
                if 'final' in optionSettings:
                    if optionSettings['final']:
                        optionSettings['type'] = 'finalDisplayString'

                optionFields.append(OptionField(optionName, optionSettings, alert.getSetting(optionName)))

            optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())

            return self.jinjaEnv.get_template("alertEditOptions.html").render(
                page="verwalten", alert=alert, options=optionFields)
        else:
            raise cherrypy.HTTPRedirect('/conf')

    @cherrypy.expose
    def saveAlertOptions(self, **args):
        """Speichert die Änderung an den Einstellungen eines Alerts."""
        alert = self.AlertService.getAlertByID(args['alertID'])
        allOK = True
        optionFields = []
        for optionName, optionSettings in alert.getOptions().items():
            if not 'final' in optionSettings:
                optionSettings['final'] = False

            if optionSettings['final'] == False:
                optionField = OptionField(optionName, optionSettings, args[optionName])
                if not optionField.evaluate():
                    allOK = False
                else:
                    alert.setSetting(optionName, optionField.getValue())
            else:
                optionSettings['type'] = 'finalDsiplayString'
                optionField = OptionField(optionName, optionSettings, alert.getSetting(optionName))

            optionFields.append(optionField)

        # Wenn alle Felder ordentlich ausgefüllt waren, wird er Port gespeichert.
        if allOK:
            return self.jinjaEnv.get_template('alertSettingsSuccessfulChanged.html').render(alert=alert, page="verwalten")
        else:
            # erzeugung der Selectoption für den Port.
            optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())

            return self.jinjaEnv.get_template("alertEditOptions.html").render(options=optionFields, page='verwalten',
                                                                              alertType=alert.getType(), alert=alert)

    def returnConfigPage(self, port):
        """Gibt die Konfigurationsseite zu einem Port aus."""
        if port != None:
            options = port.getOptions()
            portType = port.getType()
            optionFields = []
            optionFields.append(
                OptionField('wiring',
                            {
                                'type': 'finalDisplayString',
                                'description': 'Der Anschluss an dem das zu überwachende Gerät angeschlossen wurde.',
                                'tab': -42,
                                'required': True,
                                'name': 'Anschluss'
                            }, port.getSetting('wiring'))
            )

            for optionName, optionSettings in options.items():
                # wenn die Einstellung final ist, der Typ des Inputfelds auf einfach Textausgabe setzen.
                if 'final' in optionSettings:
                    if optionSettings['final']:
                        optionSettings['type'] = 'finalDisplayString'

                optionFields.append(OptionField(optionName, optionSettings, port.getSetting(optionName)))
            # hier stehen alle veränderbaren Einstellungen drin.
            optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())

            return self.jinjaEnv.get_template("editPortSettings.html").render(options=optionFields, page='verwalten',
                                                                              portType=portType, port=port)
        else:
            raise cherrypy.HTTPRedirect("/conf")

    @cherrypy.expose
    def saveChanges(self, **args):
        port = self.PortService.getPortByID(args['port-id'])
        allOK = True
        optionFields = []
        for optionName, optionSettings in port.getOptions().items():
            if not 'final' in optionSettings:
                optionSettings['final'] = False

            if optionSettings['final'] == False:
                optionField = OptionField(optionName, optionSettings, args[optionName])
                if not optionField.evaluate():
                    allOK = False
                else:
                    port.setSetting(optionName, optionField.getValue())
            else:
                optionSettings['type'] = 'finalDsiplayString'
                optionField = OptionField(optionName, optionSettings, port.getSetting(optionName))

            optionFields.append(optionField)

        # Wenn alle Felder ordentlich ausgefüllt waren, wird er Port gespeichert.
        if allOK:
            return self.jinjaEnv.get_template('portSettingsSuccessfulChanged.html').render(port=port, page="verwalten")
        else:
            # erzeugung der Selectoption für den Port.
            optionFields.append(optionFields.append(
                OptionField('wiring',
                            {
                                'type': 'finalDisplayString',
                                'description': 'Der Anschluss an dem das zu überwachende Gerät angeschlossen wurde.',
                                'tab': -42,
                                'required': True,
                                'name': 'Anschluss'
                            },
                            port.getSetting('wiring'))
            )
            )
            optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())

            return self.jinjaEnv.get_template("editPortSettings.html").render(options=optionFields, page='verwalten',
                                                                              portType=port.getType(), port=port)

    @cherrypy.expose
    def deleteTrigger(self, triggerID):
        """Löscht einen Trigger aus dem System mit Vorwarnung"""
        return self.jinjaEnv.get_template("deleteTrigger.html").render(page='verwalten', triggerID=triggerID)


    @cherrypy.expose
    def deleteTriggerSure(self, triggerID):
        """Löscht einen Trigger aus dem System ohne Vorwarnung"""
        trigger = self.TriggerService.getTriggerByID(triggerID)
        portID = trigger.getPort().getID()
        self.TriggerService.removeTrigger(triggerID)
        raise cherrypy.HTTPRedirect('/conf/portEditOptions/?portID=' + str(portID))