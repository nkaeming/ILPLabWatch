from UI.AbstractView import AbstractView
import cherrypy

class addTrigger(AbstractView):
    """View zum Erstellen neuer Trigger"""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self, portID=""):
        """Startseite des Trigger hinzufüge"""
        if portID == "":
            raise cherrypy.HTTPRedirect('/conf')
        port = self.PS.getPortById(portID)

        return self.jinjaEnv.get_template("addTrigger.html").render(
            page="verwalten", port=port, alerts = self.AlertService.getAlerts("name"))
