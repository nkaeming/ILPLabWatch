from UI.AbstractView import AbstractView
from UI.Models.OptionField import OptionField
import cherrypy


class removeAlert(AbstractView):
    """View zum erstellen neuer Ports."""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self, alertID):
        alert = self.AlertService.getAlertByID(alertID)
        return self.jinjaEnv.get_template("removeAlertSubmit.html").render(
            alert=alert)

    @cherrypy.expose
    def removeAlertSure(self, alertID):
        alert = self.AlertService.getAlertByID(alertID)
        self.AlertService.removeAlert(alert)
        raise cherrypy.HTTPRedirect('/')