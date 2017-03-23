from UI.AbstractView import AbstractView
import IOHelper.log as log
import cherrypy


class removePort(AbstractView):
    """View zum erstellen neuer Ports."""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self, portID):
        port = self.PortService.getPortByID(portID)
        return self.jinjaEnv.get_template("removePortSubmit.html").render(
            port=port)

    @cherrypy.expose
    def removePortSure(self, portID):
        port = self.PortService.getPortByID(portID)
        # Zunächst die Logdatein löschen.
        log.deleteLog(port)
        self.PortService.removePort(port)
        raise cherrypy.HTTPRedirect('/')
