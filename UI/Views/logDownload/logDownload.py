from UI.AbstractView import AbstractView
import cherrypy


class logDownload(AbstractView):
    """View zum herunterladen von logDownloads"""

    def __init__(self, PS, TS, AS):
        super().__init__(PS, TS, AS)

    @cherrypy.expose
    def index(self):
        template = self.jinjaEnv.get_template('downloadDialog.html')
        return template.render(page='logs', ports=self.PortService.getPorts('name'))
