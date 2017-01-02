from jinja2 import Environment, FileSystemLoader

class AbstractView():
    """Erstellt einige Grundfunktionen zu einem View. Jeder View muss diese Klasse erweitern"""

    PortService = None
    TriggerService = None
    AlertService = None

    # die Umgebung von jinja
    jinjaEnv = None

    """DependencyInjection für die Services."""

    def __init__(self, PortService, TriggerService, AlertService):
        self.PortService = PortService
        self.AlertService = AlertService
        self.TriggerService = TriggerService

        self.jinjaEnv = Environment(
            loader=FileSystemLoader(["UI/Templates", "UI/Views/" + self.__class__.__name__ + "/templates"]))
