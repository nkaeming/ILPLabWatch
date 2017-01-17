from jinja2 import Environment, PackageLoader
import pkgutil, importlib, cherrypy, os, json


class UIMain(object):
    PortService = None
    TriggerService = None
    AlertServcie = None

    def __init__(self, PS, TS, AS):
        self.PortService = PS
        self.AlertService = AS
        self.TriggerService = TS

    @cherrypy.expose
    def index(self):
        env = Environment(loader=PackageLoader('UI', 'Templates'))
        template = env.get_template('main.phtml')
        portList = self.PortService.getPorts()
        return template.render(portList=portList)


class UIServer():
    """Die Serverklasse für den Webserver."""

    PortService = None
    TriggerService = None
    AlertService = None

    """DependencyInjection für die Services"""

    def __init__(self, PortService, TriggerService, AlertService):
        self.PortService = PortService
        self.AlertService = AlertService
        self.TriggerService = TriggerService

    """Startet den Server"""

    def start(self):
        # Lädt alle Views in den cherrypy.tree
        for view in pkgutil.iter_modules(['UI/Views']):
            name = view[1]
            classPointer = getattr(importlib.import_module("UI.Views." + name + "." + name), name)
            confPath = "UI/Views/" + name + "/conf.cfg"
            if os.path.isfile(confPath):
                with open(confPath, "r") as configfile:
                    conf = json.load(configfile)
                    cherrypy.tree.mount(classPointer(self.PortService, self.TriggerService, self.AlertService),
                                        "/" + name, conf)
            else:
                cherrypy.tree.mount(classPointer(self.PortService, self.TriggerService, self.AlertService), "/" + name)

        # Globale Konfiguration
        conf = {
            '/': {
                'tools.sessions.on': True,
                'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
            '/static': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'UI/Static'
            },
        }

        # fügt die index Klasse hinzu.
        uiMain = UIMain(self.PortService, self.TriggerService, self.AlertService)
        cherrypy.tree.mount(uiMain, '/', conf)

        # startet die cherrypy engine
        cherrypy.config.update({'server.socket_host': '134.100.109.149'})
        cherrypy.engine.start()
        cherrypy.engine.block()
