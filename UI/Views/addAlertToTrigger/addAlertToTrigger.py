from UI.AbstractView import AbstractView
from UI.Models.OptionField import OptionField
import cherrypy


class addAlertToTrigger(AbstractView):
    """View zum hinzufügen von Alerts zu Triggern."""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self, portID, triggerID):
        port = self.PortService.getPortByID(portID)
        trigger = self.TriggerService.getTriggerByID(triggerID)
        return self.jinjaEnv.get_template("selectAlert.html").render(
            trigger=trigger, alerts=sorted(self.AlertService.getAlerts(), key=lambda x: x.getName()), port=port)

    @cherrypy.expose
    def saveRelation(self, triggerID, alertID, portID):
        alert = self.AlertService.getAlertByID(alertID)
        trigger = self.TriggerService.getTriggerByID(triggerID)
        print(trigger)
        trigger.appendAlert(alert)
        raise cherrypy.HTTPRedirect('/conf/portEditOptions/?portID=' + str(portID))