from UI.AbstractView import AbstractView
from UI.Models.OptionField import OptionField
import cherrypy


class addAlert(AbstractView):
    """View zum erstellen neuer Ports."""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self):
        return self.jinjaEnv.get_template("selectAlertType.html").render(
            alertTypes=self.AlertService.getAlertTypes(), page="alertHinzufuegen")

    @cherrypy.expose
    def alertSetUP(self, alertType):
        options = self.AlertService.getAlertClassByType(alertType).getOptions()
        optionFields = []
        for optionName, optionSettings in options.items():
            optionFields.append(OptionField(optionName, optionSettings))
        optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())
        return self.jinjaEnv.get_template("setSettingsOfAlert.html").render(options=optionFields, page='alertHinzufuegen',
                                                                           alertType=alertType)

    @cherrypy.expose
    def saveAlert(self, **args):
        alertType = args['type']
        options = self.AlertService.getAlertClassByType(alertType).getOptions()
        optionFields = []
        allOK = True
        for option, setting in options.items():
            if option in args.keys():
                # Prüfen ob der Name bereits existiert.
                if option == 'name':
                    suggestedName = args['name']
                    if self.AlertService.doesAlertExistByName(suggestedName):
                        optionField = OptionField(name=option, settings=setting, value=args['name'],
                                                  warnText="Der Name existiert bereits.", page='alertHinzufuegen')
                        allOK = False
                    else:
                        optionField = OptionField(name=option, settings=setting, value=args[option])
                else:
                    optionField = OptionField(name=option, settings=setting, value=args[option])
            else:
                optionField = OptionField(name=option, settings=setting)

            if not optionField.evaluate():
                allOK = False
            optionFields.append(optionField)

        # Wenn alle Felder ordentlich ausgefüllt waren, wird er Alert gespeichert.
        if allOK:
            alertSettings = {'type': alertType}
            for optionField in optionFields:
                alertSettings[optionField.getName()] = optionField.getValue()

            alertID = self.AlertService.generateAndAddNewAlert(alertSettings)
            return self.jinjaEnv.get_template('saveAlert.html').render(alertSettings=alertSettings, alertID=alertID,
                                                                      page="alertHinzufuegen")
        else:
            optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())
            return self.jinjaEnv.get_template("setSettingsOfAlert.html").render(options=optionFields, page='alertHinzufuegen',
                                                                               alertType=alertType)
