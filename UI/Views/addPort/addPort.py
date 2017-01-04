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
        optionFields = []
        for optionName, optionSettings in options.items():
            optionFields.append(OptionField(optionName, optionSettings))

        optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())

        return self.jinjaEnv.get_template("setSettingsOfPort.html").render(wirings=freePortConnections,
                                                                           options=optionFields, page='hinzufuegen',
                                                                           portType=portType)
