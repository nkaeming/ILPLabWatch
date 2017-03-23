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
        port = self.PortService.getPortByID(portID)

        return self.jinjaEnv.get_template("addTrigger.html").render(
            page="verwalten", port=port, alerts = self.AlertService.getAlerts("name"))

    @cherrypy.expose
    def saveTrigger(self, portID, lowerBound, upperBound, warntrigger = False):
        """Speichert einen Trigger"""
        if warntrigger in ('on', True, 1, 'True', 'true', '1'):
            warntrigger = True
        else:
            warntrigger = False

        triggerSettings = {
            "portID" : portID,
            "range" : (float(lowerBound), float(upperBound)),
            "warnTrigger": warntrigger,
            "alerts": []
        }

        self.TriggerService.addTigger(triggerSettings)

        raise cherrypy.HTTPRedirect('/conf/portEditOptions/?portID=' + str(portID))