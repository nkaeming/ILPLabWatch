from UI.AbstractView import AbstractView
import cherrypy


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
            settings = port.getSettings()

            return settings
        else:
            raise cherrypy.HTTPRedirect("/conf")
