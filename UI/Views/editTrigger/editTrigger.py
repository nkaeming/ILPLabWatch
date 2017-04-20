from UI.AbstractView import AbstractView
import cherrypy, json, datetime
import IOHelper.log as Logreader


class editTrigger (AbstractView):
    """Die API Klasse stellt Funktionen zur Verwalltung für Fremdsoftware zur Verfügung."""

    def __init__(self, PortService, TriggerService, AlertService):
        super().__init__(PortService, TriggerService, AlertService)


    @cherrypy.expose
    def index(self, triggerID):
        trigger = self.TriggerService.getTriggerByID(triggerID)
        port = trigger.getPort()
        return self.jinjaEnv.get_template("editTrigger.html").render(page='verwalten', trigger=trigger, port=port)

    @cherrypy.expose
    def saveTrigger(self, triggerID, lowerBound, upperBound, portID, warntrigger=False):
        trigger = self.TriggerService.getTriggerByID(triggerID)
        if warntrigger in ('on', True, 1, 'True', 'true', '1'):
            warntrigger = True
        else:
            warntrigger = False
        if warntrigger != trigger.isWarnTrigger():
            trigger.setWarntrigger(warntrigger)
        trigger.setInterval((float(lowerBound), float(upperBound)))
        raise cherrypy.HTTPRedirect('/conf/portEditOptions/?portID=' + str(portID))