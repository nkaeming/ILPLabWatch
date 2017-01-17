from UI.AbstractView import AbstractView
import cherrypy
from UI.Models.OptionField import OptionField


class conf(AbstractView):
    """View zum editieren von Porteinstellungen."""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self):
        """Bei nicht erkanntem Index oder Namen wird eine Liste aller Ports ausgegeben."""
        return self.jinjaEnv.get_template("portEditOverview.html").render(
            page="verwalten", portList=self.PortService.getPorts())

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

    def returnConfigPage(self, port):
        """Gibt die Konfigurationsseite zu einem Port aus."""
        if port != None:
            options = port.getOptions()
            portType = port.getType()

            optionFields = []

            # selektiere nur die nicht finalen Optionen
            def isOptionFinal(option):
                """Erwartet ein Tupel mit (Optionname, Optioneinstellungen). Gibt den Wert der final Einstellung zurück oder aber False."""
                try:
                    return option[1]['final']
                except KeyError:
                    return False

            onlyNotFinalOptions = filter(lambda option: isOptionFinal(option) == False, options.items())

            for optionName, optionSettings in options.items():
                # wenn die Einstellung final ist, der Typ des Inputfelds auf einfach Textausgabe setzen.
                if 'final' in optionSettings:
                    if optionSettings['final']:
                        optionSettings['type'] = 'finalDisplayString'

                optionFields.append(OptionField(optionName, optionSettings, port.getSetting(optionName)))
            # hier stehen alle veränderbaren Einstellungen drin.
            optionFields = sorted(optionFields, key=lambda optionField: optionField.getTabIndex())

            # wähle alle Einstellungen die nicht verändert werden können.
            fixFields = []
            for optionName, optionSettings in filter(lambda option: isOptionFinal(option) == True, options.items()):
                fixFields.append({
                    'displayName': optionSettings['name'],
                    'value': port.getSetting(optionName)
                })

            return self.jinjaEnv.get_template("editPortSettings.html").render(options=optionFields, page='verwalten',
                                                                              portType=portType, port=port)
        else:
            raise cherrypy.HTTPRedirect("/conf")
