from UI.AbstractView import AbstractView
import cherrypy, json


class api(AbstractView):
    """Die API Klasse stellt Funktionen zur Verwalltung für Fremdsoftware zur Verfügung."""

    def __init__(self, PortService, TriggerService, AlertService):
        super().__init__(PortService, TriggerService, AlertService)

    """Gibt den aktuellen Status aller Ports zurück."""

    @cherrypy.expose
    def currentStatus(self):
        return json.dumps(self.PortService.getCurrentPortsInformations())
