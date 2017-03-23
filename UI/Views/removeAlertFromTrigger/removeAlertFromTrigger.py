from UI.AbstractView import AbstractView
from UI.Models.OptionField import OptionField
import cherrypy


class removeAlertFromTrigger(AbstractView):
    """View zum erstellen neuer Ports."""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self, triggerID, portID):
        trigger = self.TriggerService.getTriggerByID(triggerID)
        port = self.PortService.getPortByID(portID)
        return self.jinjaEnv.get_template("selectAlert.html").render(
            alerts=sorted(trigger.getAlerts(), key=lambda x: x.getName()), port=port, trigger=trigger)

    @cherrypy.expose
    def remove(self, alertID, triggerID, portID):
        alert = self.AlertService.getAlertByID(alertID)
        trigger = self.TriggerService.getTriggerByID(triggerID)
        trigger.removeAlert(alert)
        raise cherrypy.HTTPRedirect('/conf/portEditOptions/?portID=' + portID)